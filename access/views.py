from pathlib import Path
import json
import time
import base64
import os
import logging
import requests
import traceback
from datetime import datetime

from django.http import JsonResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import RequestException
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import CustomUser, Agency, PreRecordedUser, PreRecordedAgency
from .serializers import CustomUserSerializer, AgencySerializer, PreRecordedAgencySerializer
from .fetchcitizendetails import get_citizen_details, map_citizen_details_to_model

from .constants import USER_DATA_FILE_PATH, AGENCY_DATA_FILE_PATH, GLOBAL_FILE_PATH

from django.db import transaction
from django.http import QueryDict
from . import models

logger = logging.getLogger(__name__)


def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


def read_global():
    with open(GLOBAL_FILE_PATH, 'r') as file:
        return json.load(file)


def write_global(data):
    with open(GLOBAL_FILE_PATH, 'w') as file:
        json.dump(data, file)


def get_authorization_code():
    auth_key = 'ScC63jo40LjxifHweyLUR6IVto0a'
    auth_secret = 'jk6jLebfES42oYmf8YuFNuMFpTUa'
    auth_code = f"{auth_key}:{auth_secret}"
    return base64.b64encode(auth_code.encode()).decode()


def global_session():
    data = read_global()
    if data['accessToken'] != "" and data['expiryTime'] > time.time():
        return True
    return False


def generate_token():
    request_url = 'oauth2/token'
    if not global_session():
        headers = {'Authorization': 'Basic ' + get_authorization_code()}
        form_params = {'grant_type': 'client_credentials'}

        response = requests.post(
            'https://stg-sso.dit.gov.bt/' + request_url,
            headers=headers,
            data=form_params,
            verify=False,
            timeout=30
        )

        if response.status_code == 200:
            json_object = response.json()
            expiry_time = int(time.time()) + json_object['expires_in']

            global_settings = read_global()
            global_settings['accessToken'] = json_object['access_token']
            global_settings['expiryTime'] = expiry_time

            write_global(global_settings)

            return global_settings['accessToken']
        else:
            return "Something went wrong. Please try again!"
    else:
        return read_global()['accessToken']


@csrf_exempt
def fetch_citizen_details(request, cid):
    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        api_url = settings.CREDENTIALS['API_URL']
        response = requests.get(
            f'{api_url}{cid}', headers=headers, verify=False)

        if response.status_code == 200:
            citizen_detail = response.json().get('citizenDetailsResponse', {}
                                                 ).get('citizenDetail', [None])[0]

            # Map user data before storing in the JSON file
            mapped_user_data = map_user_data(citizen_detail)

            print(f"User Data from Step 2: {citizen_detail}")

            # Store user data in the JSON file
            write_json(USER_DATA_FILE_PATH, mapped_user_data)

            return JsonResponse(citizen_detail, safe=False)
        else:
            print(
                f"Response error. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching citizen details'}, status=response.status_code)

    except RequestException as e:
        print(f"Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def map_user_data(citizen_detail):
    # Map the relevant data from citizen_detail to user model fields
    mapped_data = {
        'identity_number': citizen_detail.get('cid', ''),
        'first_name': citizen_detail.get('firstName', ''),
        'middle_name': citizen_detail.get('middleName', '') or '',
        'last_name': citizen_detail.get('lastName', ''),
        'date_of_birth': formatDOB(citizen_detail.get('dob', '')),
        'gender': mapGender(citizen_detail.get('gender', '')),
        'mob_number': citizen_detail.get('mobileNumber', ''),
        'perm_add_village': citizen_detail.get('villageName', ''),
        'perm_add_gewog': citizen_detail.get('gewogName', ''),
        'perm_add_dzongkhag': citizen_detail.get('dzongkhagName', ''),
        'nationality': mapNationality(citizen_detail.get('country', '')),
        'username': '',  # Include an empty username
        'password': '',  # Include an empty password
        'email': '',  # Include an empty email
    }
    return mapped_data


def formatDOB(dob):
    date_object = datetime.strptime(dob, '%d/%m/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    return formatted_date


def mapGender(gender):
    return 'Female' if gender == 'F' else 'Male'


def mapNationality(country):
    if not country or country.strip() == '':
        return 'Bhutanese'
    return country


def map_rcsc_data_to_agency_model(rcsc_data):
    # Map the relevant data from rcsc_data to Agency model fields
    mapped_data = {
        'agency_code': rcsc_data.get('agencyID', ''),
        'user_role_agency': rcsc_data.get('positionTitle', ''),
        'agency_name': rcsc_data.get('agencyName', ''),
        'user_code': rcsc_data.get('employeeNumber', ''),
        'user': '',
    }
    return mapped_data

# views.py - Step 3 (fetch_rcsc_details function)


@csrf_exempt
def fetch_rcsc_details(request, cid, reg_email):
    print(
        f"Received request for RCSC details of CID: {cid} with reg_email: {reg_email}")

    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        rcsc_api_url = settings.CREDENTIALS['RCSC_API']
        print(f"Making request to RCSC API: {rcsc_api_url}{cid}")
        print(f"Request headers: {headers}")

        # Step 1: Read user_data.json
        user_data = read_json(USER_DATA_FILE_PATH)

        # Step 2: Update email field in user data
        user_data.update({'email': reg_email})  # Update the email field

        # Debugging print statement
        print(f"Updated user_data: {user_data}")

        # Step 3: Save updated user data back to user_data.json
        write_json(USER_DATA_FILE_PATH, user_data)

        # Debugging print statement
        print("User data written to file.")

        # Step 4: Proceed with RCSC API request
        response = requests.get(
            f'{rcsc_api_url}{cid}', headers=headers, verify=False)

        if response.status_code == 200:
            rcsc_details = response.json().get(
                'employeedetails', {}).get('employeedetail', [])[0]
            print(f"RCSC Details Response Data: {rcsc_details}")

            # Map the RCSC data to Agency model
            mapped_data = map_rcsc_data_to_agency_model(rcsc_details)

            # Store agency data in the session
            request.session['agency_data'] = mapped_data

            # store agency data to the JSON file
            write_json(AGENCY_DATA_FILE_PATH, mapped_data)

            # Proceed to Step 4 or any other step as needed
            return JsonResponse(mapped_data, safe=False)
        else:
            print(
                f"Response error from RCSC API. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching RCSC details'}, status=response.status_code)

    except RequestException as e:
        print(f"RCSC API Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


# views.py - Step 4
# Step 1: Register user
@api_view(['POST'])
@csrf_exempt
def register_user(request):
    try:
        print("Received request to register user.")

        # Get username, password, and email from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Received username: {username}, password: {password}")

        # If you need additional data from the session, retrieve it here
        user_data = read_json(USER_DATA_FILE_PATH)
        user_data.update({'username': username})
        write_json(USER_DATA_FILE_PATH, user_data)

        # Create a dictionary with only the necessary data for user creation
        user_creation_data = {
            'username': user_data.get('username', ''),
            'password': password,
            'email': user_data.get('email', ''),
            'identity_number': user_data.get('identity_number', ''),
            'nationality': user_data.get('nationality', ''),
            'first_name': user_data.get('first_name', ''),
            'middle_name': user_data.get('middle_name', ''),
            'last_name': user_data.get('last_name', ''),
            'date_of_birth': user_data.get('date_of_birth', ''),
            'gender': user_data.get('gender', ''),
            'mob_number': user_data.get('mob_number', ''),
            'perm_add_village': user_data.get('perm_add_village', ''),
            'perm_add_gewog': user_data.get('perm_add_gewog', ''),
            'perm_add_dzongkhag': user_data.get('perm_add_dzongkhag', ''),
        }

        # Use Django's transaction.atomic for atomic operations
        with transaction.atomic():
            # Create instances of the models and validate them
            user_serializer = CustomUserSerializer(data=user_creation_data)
            if not user_serializer.is_valid():
                print(f"User serializer errors: {user_serializer.errors}")

            # Save the user instance
            user_instance = user_serializer.save()

            # Update agency_data inside the same transaction block
            agency_data = read_json(AGENCY_DATA_FILE_PATH)
            agency_data.update({'user': str(user_instance.id)})
            write_json(AGENCY_DATA_FILE_PATH, agency_data)

            print(
                f"Session data after user registration: {request.session.items()}")

            # Return the user ID in the response
            response_data = {'userId': user_instance.id}
            return Response(response_data, status=201)

    except Exception as e:
        # Log the exception details
        print(f"Error registering user: {str(e)}")
        response_data = {'error': 'Error registering user'}
        print(f"Response data: {response_data}")
        return Response(response_data, status=500)


# Step 2: Register agency
@api_view(['POST'])
@csrf_exempt
def register_agency(request):
    try:
        # Get the agency data directly from the frontend
        agency_data = read_json(AGENCY_DATA_FILE_PATH)
        logger.debug(f"Received agency data: {agency_data}")

        # Ensure 'user' is a dictionary before accessing 'userId'
        user_data = agency_data.get('user', '')
        logger.debug(f"User data from agency_data: {user_data}")

        user_id = user_data
        logger.debug(f"User ID extracted: {user_id}")

        if not user_id:
            logger.error("User ID in the file is missing")
            return Response({'error': 'User ID in the file is missing'}, status=400)

        # Use Django's transaction.atomic for atomic operations
        with transaction.atomic():
            # Create and validate the agency serializer
            agency_serializer = AgencySerializer(
                data=agency_data, context={'user_data': user_data})
            agency_serializer.is_valid(raise_exception=True)

            # Save the agency instance
            agency_instance = agency_serializer.save()

            # Clear session data after successful registration
            if 'user_data' in request.session:
                request.session.pop('user_data')

            if 'agency_data' in request.session:
                request.session.pop('agency_data')

            response_data = {'success': 'Agency registered successfully'}
            logger.debug(f"Response data: {response_data}")
            return Response(response_data, status=201)

    except Exception as e:
        # Log the exception details
        logger.exception(f"Error registering agency: {str(e)}")
        response_data = {'error': 'Error registering agency'}
        logger.debug(f"Response data: {response_data}")
        return Response(response_data, status=500)


class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        agency_data = request.data.get('agency', {})

        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        agency_serializer = AgencySerializer(data=agency_data)
        if agency_serializer.is_valid():
            agency_serializer.save(user=user)
        else:
            user.delete()
            return Response(agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(user_serializer.data)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserUpdate(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        user_serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)

        agency_data = request.data.get('agency', {})
        if instance.agency:
            agency_serializer = AgencySerializer(
                instance.agency, data=agency_data, partial=partial)
            if agency_serializer.is_valid():
                agency_serializer.save()
            else:
                return Response(agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.data)


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                agency = user.agency
                if agency:
                    agency_data = {
                        'user_role_agency': agency.user_role_agency,
                    }
                else:
                    agency_data = None

                return Response({"token": token.key, "user_role_agency": agency_data.get('user_role_agency', None)}, status=status.HTTP_200_OK)
            else:
                logger.warning('Authentication failed for username: %s', username)
                return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error('Exception during login: %s', str(e))
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@csrf_exempt
def get_user_details(request):
    try:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)

        user_data = {
            'identity_number': user.identity_number,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'email': user.email,
            'mob_number': user.mob_number,
            'perm_add_village': user.perm_add_village,
            'perm_add_gewog': user.perm_add_gewog,
            'perm_add_dzongkhag': user.perm_add_dzongkhag,
            'nationality': user.nationality,
            'date_joined': user.date_joined,
        }

        agency = user.agency
        if agency:
            agency_data = {
                'user_code': agency.user_code,
                'ps_add_village': agency.ps_add_village,
                'ps_add_gewog': agency.ps_add_gewog,
                'ps_add_dzongkhag': agency.ps_add_dzongkhag,
                'father_name': agency.father_name,
                'mother_name': agency.mother_name,
                'parent_occupation': agency.parent_occupation,
                'guardian_name': agency.guardian_name,
                'guardian_occupation': agency.guardian_occupation,
                'parent_status': agency.parent_status,
                'current_living_with': agency.current_living_with,
                'agency_code': agency.agency_code,
                'user_role_agency': agency.user_role_agency,
                'agency_name': agency.agency_name,
                'user_class': agency.user_class,
                'user_sub_class': agency.user_sub_class,
                'academy_code': agency.academy_code,
                'status': agency.status,
            }
        else:
            agency_data = None

        return Response({"user": user_data, "agency": agency_data}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error('Exception while fetching user details: %s', str(e))
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            password_reset_url = request.build_absolute_uri(
                reverse('password-reset', args=[token])
            )
            send_mail(
                'Password Reset Request',
                f'Please click on the link to reset your password: {password_reset_url}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetView(APIView):
    def post(self, request, token, *args, **kwargs):
        password = request.data.get('password')
        user = User.objects.filter(
            username=request.data.get('username')).first()

        if user and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid token or username."}, status=status.HTTP_400_BAD_REQUEST)


# @APIView(['POST'])
@csrf_exempt
def verify_pre_recorded_user(request):
    cid = request.GET.get('cid')

    try:
        user = PreRecordedUser.objects.get(identity_number=cid)
        agency = PreRecordedAgency.objects.filter(
            prerecorded_user=user).first()

        user_data = {
            'identity_number': user.identity_number,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'email': user.email,
            'mob_number': user.mob_number,
            'perm_add_village': user.perm_add_village,
            'perm_add_gewog': user.perm_add_gewog,
            'perm_add_dzongkhag': user.perm_add_dzongkhag,
            'nationality': user.nationality,
            'date_joined': user.date_joined,
            # Add other fields from PreRecordedUser model as needed

            'agency_data': {
                'user_code': agency.user_code,
                'ps_add_village': agency.ps_add_village,
                'ps_add_gewog': agency.ps_add_gewog,
                'ps_add_dzongkhag': agency.ps_add_dzongkhag,
                'father_name': agency.father_name,
                'mother_name': agency.mother_name,
                'parent_occupation': agency.parent_occupation,
                'guardian_name': agency.guardian_name,
                'guardian_occupation': agency.guardian_occupation,
                'parent_status': agency.parent_status,
                'current_living_with': agency.current_living_with,
                'agency_code': agency.agency_code,
                'user_role_agency': agency.user_role_agency,
                'agency_name': agency.agency_name,
                'user_class': agency.user_class,
                'user_sub_class': agency.user_sub_class,
                'academy_code': agency.academy_code,
                'status': agency.status,
                # Add other fields from PreRecordedAgency model as needed
            }
        }

        return JsonResponse({
            'success': True,
            'message': 'Pre-recorded user found.',
            'user_data': user_data
        })
    except PreRecordedUser.DoesNotExist:
        logger.error(f'Pre-recorded user not found for CID: {cid}')
        return JsonResponse({'success': False, 'message': 'Pre-recorded user not found.'}, status=404)
    except Exception as e:
        logger.exception(f'Error in verify_pre_recorded_user: {str(e)}')
        return JsonResponse({'success': False, 'message': 'Internal Server Error'}, status=500)


# Step 1: Register pre-recorded user
@api_view(['POST'])
@csrf_exempt
def register_pre_recorded_user(request):
    try:
        print("Received request to register pre-recorded user.")

        # Get user data from the request data
        user_data = request.data
        print(f"Received user data: {user_data}")

        # If password is not provided in the data, set it to an empty string
        password = user_data.get('password', '')

        # Set default values for required fields if not provided
        for field in ['identity_number', 'nationality', 'first_name', 'last_name', 'date_of_birth', 'gender',
                      'mob_number', 'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag']:
            user_data.setdefault(field, '')

        # Set the password back to the original value
        user_data['password'] = password

        # Create a dictionary with only the necessary data for user creation
        user_creation_data = {
            'username': user_data.get('username', ''),
            'password': user_data.get('password', ''),
            'email': user_data.get('email', ''),
            'identity_number': user_data.get('identity_number', ''),
            'nationality': user_data.get('nationality', ''),
            'first_name': user_data.get('first_name', ''),
            'middle_name': user_data.get('middle_name', ''),
            'last_name': user_data.get('last_name', ''),
            'date_of_birth': user_data.get('date_of_birth', ''),
            'gender': user_data.get('gender', ''),
            'mob_number': user_data.get('mob_number', ''),
            'perm_add_village': user_data.get('perm_add_village', ''),
            'perm_add_gewog': user_data.get('perm_add_gewog', ''),
            'perm_add_dzongkhag': user_data.get('perm_add_dzongkhag', ''),
        }

        # Use Django's transaction.atomic for atomic operations
        with transaction.atomic():
            # Create instances of the models and validate them
            user_serializer = CustomUserSerializer(data=user_creation_data)
            if not user_serializer.is_valid():
                print(f"User serializer errors: {user_serializer.errors}")
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the user instance
            user_instance = user_serializer.save()

            print(f"Session data after pre-recorded user registration: {request.session.items()}")

            # Return the user ID in the response
            response_data = {'userId': user_instance.id}
            return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Log the exception details
        print(f"Error registering pre-recorded user: {str(e)}")
        response_data = {'error': 'Error registering pre-recorded user'}
        print(f"Response data: {response_data}")
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Step 2: Register pre-recorded agency
@api_view(['POST'])
@csrf_exempt
@permission_classes([])
def register_pre_recorded_agency(request):
    try:
        logger.info("Received request to register pre-recorded agency.")

        # Get the agency data from the request
        agency_data = request.data.get('agency_data', {})
        logger.debug(f"Received agency data: {agency_data}")

        # Print the full request body for debugging
        logger.debug(f"Full request body: {request.data}")

        # Ensure 'user' data is present in the agency data
        user_data = agency_data.get('user', None)
        logger.debug(f"User data in agency_data: {user_data}")
        if not user_data:
            logger.error("User data is missing in the agency data")
            return Response({'error': 'User data is missing in the agency data'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert user ID to integer
        user_id = int(user_data)

        # Pass user ID as context to serializer
        serializer_context = {'user_id': user_id}

        # Set default values for required fields if not provided
        for field in ['user_code', 'ps_add_village', 'ps_add_gewog', 'ps_add_dzongkhag', 'father_name',
                      'mother_name', 'parent_occupation', 'guardian_name', 'guardian_occupation', 'parent_status',
                      'current_living_with', 'agency_code', 'user_role_agency', 'agency_name', 'user_class',
                      'user_sub_class', 'academy_code']:
            agency_data.setdefault(field, '')

        # Use Django's transaction.atomic for atomic operations
        with transaction.atomic():
            # Create and validate the agency serializer
            agency_serializer = PreRecordedAgencySerializer(data=agency_data, context=serializer_context)
            agency_serializer.is_valid(raise_exception=True)

            # Save the agency instance
            agency_instance = agency_serializer.save()

            logger.info(
                f"Pre-recorded agency registered successfully with ID: {agency_instance.id}")

            response_data = {
                'success': 'Pre-recorded agency registered successfully'}
            return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Log the exception details
        logger.exception(f"Error registering pre-recorded agency: {str(e)}")
        response_data = {'error': 'Error registering pre-recorded agency'}
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@csrf_exempt
def user_logout(request):
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('sessionid')  # Clear session cookie
    return response