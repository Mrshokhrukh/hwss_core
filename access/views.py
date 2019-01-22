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

from .models import CustomUser, Agency
from .serializers import CustomUserSerializer, AgencySerializer
from .fetchcitizendetails import get_citizen_details, map_citizen_details_to_model

from .constants import USER_DATA_FILE_PATH, AGENCY_DATA_FILE_PATH, GLOBAL_FILE_PATH

from django.db import transaction

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
    }
    return mapped_data

# views.py - Step 3 (fetch_rcsc_details function)


def fetch_rcsc_details(request, cid):
    print(f"Received request for RCSC details of CID: {cid}")

    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        rcsc_api_url = settings.CREDENTIALS['RCSC_API']
        print(f"Making request to RCSC API: {rcsc_api_url}{cid}")
        # print(f"Request headers: {headers}")

        response = requests.get(
            f'{rcsc_api_url}{cid}', headers=headers, verify=False)

        if response.status_code == 200:
            rcsc_details = response.json().get(
                'employeedetails', {}).get('employeedetail', [])[0]
            print(f"RCSC Details Response Data: {rcsc_details}")

            # Map the RCSC data to Agency model
            mapped_data = map_rcsc_data_to_agency_model(rcsc_details)

            # Convert 'user_code' to integer
            mapped_data['user_code'] = int(mapped_data['user_code'])

            # Store agency data in the session
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

        # Get username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # If you need additional data from the session, retrieve it here
        user_data = read_json(USER_DATA_FILE_PATH)

        print(f"Received data - Username: {username}, Password: {password}")
        print(f"User Data: {user_data}")

        # Create a dictionary with the necessary data for the serializers
        user_data.update({'username': username, 'password': password})

        # Use Django's transaction.atomic for atomic operations
        with transaction.atomic():
            # Create instances of the models and validate them
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)

            # Save the user instance
            user_instance = user_serializer.save()

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
        print("Received request to register agency.")

        # Get the user ID and agency data from the request data
        user_id = int(request.data.get('userId'))  # Convert user_id to an integer
        agency_data = request.data.get('agencyData')

        print(f"User ID from frontend: {user_id}")
        print(f"Agency Data from frontend: {agency_data}")

        # Ensure 'user' key is not present in agency_data
        agency_data.pop('user', None)

        print("Removed 'user' key from agency data:", agency_data)

        # Get the user instance using the user ID
        user_instance = CustomUser.objects.get(id=user_id)

        # Set the user field in the AgencySerializer
        agency_serializer = AgencySerializer(data=agency_data, context={'user': user_instance})
        if agency_serializer.is_valid():
            agency_instance = agency_serializer.save()  # No need to set user_id explicitly

            print(f"Agency instance created: {agency_instance}")

            response_data = {'success': 'Agency registered successfully'}
            return Response(response_data, status=201)
        else:
            print("Validation errors in agency data:")
            print(agency_serializer.errors)
            response_data = {'error': 'Validation error in agency data'}
            return Response(response_data, status=400)

    except Exception as e:
        # Log the exception details
        print(f"Error registering agency: {str(e)}")
        traceback.print_exc()  # Add this line to print detailed traceback
        response_data = {'error': 'Error registering agency'}
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
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


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
def verify_pre_recorded_user(request):
    cid = request.data.get('cid')
    dob = request.data.get('dob')

    user = get_object_or_404(
        PreRecordedUser, identity_number=cid, date_of_birth=dob)
    return Response({
        'success': True,
        'message': 'Pre-recorded user found.',
        'user_data': {
            'identity_number': user.identity_number,
            'first_name': user.first_name,
            # Add other fields as needed
        }
    })
