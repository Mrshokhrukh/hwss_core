# -----------------------------------------------//
# -------- IMPORTS PART OF THE VIEWS -----------//
# ----------------------------------------------//

from rest_framework import serializers
from .models import CustomUser, Agency, UserAgency
from django.contrib.auth.hashers import make_password
from pathlib import Path
import json
import time
import base64
import os
import logging
import requests
import traceback
from django.utils import timezone
from django.db.models import F
from datetime import datetime
import token

from django.http import JsonResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import RequestException
from django.conf import settings


from django.middleware.csrf import get_token
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate
from .models import CustomUser, Agency, PreRecordedUser, UserAgency
from .serializers import CustomUserSerializer, AgencySerializer, PreRecordedUserSerializer, UserAgencySerializer
from .fetchcitizendetails import get_citizen_details, map_citizen_details_to_model
from django.contrib.auth.tokens import default_token_generator

from .constants import USER_DATA_FILE_PATH, AGENCY_DATA_FILE_PATH, GLOBAL_FILE_PATH

from django.db import transaction
from django.http import QueryDict
from . import models

logger = logging.getLogger(__name__)


# -----------------------------------------------//
# ------ AUTH TOKEN PART OF THE VIEWS ----------//
# ----------------------------------------------//

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    API endpoint to retrieve CSRF token.
    """
    csrf_token = get_token(request)
    return Response({'csrf_token': csrf_token})


@permission_classes([AllowAny])
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


@permission_classes([AllowAny])
def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


@permission_classes([AllowAny])
def read_global():
    with open(GLOBAL_FILE_PATH, 'r') as file:
        return json.load(file)


@permission_classes([AllowAny])
def write_global(data):
    with open(GLOBAL_FILE_PATH, 'w') as file:
        json.dump(data, file)


@permission_classes([AllowAny])
def get_authorization_code():
    auth_key = 'ScC63jo40LjxifHweyLUR6IVto0a'
    auth_secret = 'jk6jLebfES42oYmf8YuFNuMFpTUa'
    auth_code = f"{auth_key}:{auth_secret}"
    return base64.b64encode(auth_code.encode()).decode()


@permission_classes([AllowAny])
def global_session():
    data = read_global()
    if data['accessToken'] != "" and data['expiryTime'] > time.time():
        return True
    return False


@permission_classes([AllowAny])
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


# -----------------------------------------------//
# ------ API FETCHING PART OF THE VIEWS --------//
# ----------------------------------------------//

@permission_classes([AllowAny])
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

            mapped_user_data = map_user_data(citizen_detail)

            print(f"User Data from Step 2: {citizen_detail}")

            request.session['user_data'] = mapped_user_data

            print(f"User Data from Step 1: {mapped_user_data}")

            return JsonResponse(citizen_detail, safe=False)
        else:
            print(
                f"Response error. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching citizen details'}, status=response.status_code)

    except RequestException as e:
        print(f"Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def fetch_rcsc_details(request, cid, reg_email):
    print(
        f"Received request for RCSC details of CID: {cid} with reg_email: {reg_email}")

    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        rcsc_api_url = settings.CREDENTIALS['RCSC_API']
        print(f"Making request to RCSC API: {rcsc_api_url}{cid}")

        # Step 2: Proceed with RCSC API request
        response = requests.get(
            f'{rcsc_api_url}{cid}', headers=headers, verify=False)

        if response.status_code == 200:
            rcsc_details = response.json().get(
                'employeedetails', {}).get('employeedetail', [])[0]
            print(f"RCSC Details Response Data: {rcsc_details}")

            # Map the RCSC data to Agency and UserAgency models
            agency_data, user_agency_data = map_rcsc_data_to_agency_model(
                rcsc_details)

            # Proceed to Step 4 or any other step as needed
            return JsonResponse({'agency_data': agency_data, 'user_agency_data': user_agency_data}, safe=False)
        else:
            print(
                f"Response error from RCSC API. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching RCSC details'}, status=response.status_code)

    except RequestException as e:
        print(f"RCSC API Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def get_emis_student_details(request, student_code, dob, reg_email):
    print(
        f"Received request for EMIS details of Student Code: {student_code}, DoB: {dob}, with reg_email: {reg_email}")

    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        emis_student_api_url = settings.CREDENTIALS['EMIS_STUDENT_API']
        request_url = f'{emis_student_api_url}{student_code}/{dob}'

        print(f"Making request to EMIS Student API: {request_url}")

        # Step 2: Proceed with EMIS API request
        response = requests.get(request_url, headers=headers, verify=False)

        if response.status_code == 200:
            emis_details = response.json()
            print(f"EMIS Details Response Data: {emis_details}")

            # Map the EMIS data to Agency and UserAgency models
            agency_data, user_agency_data = map_emis_data_to_agency_models(
                emis_details)

            # Proceed with saving the data or any other operations as needed
            return JsonResponse({'agency_data': agency_data, 'user_agency_data': user_agency_data}, safe=False)
        else:
            print(
                f"Response error from EMIS API. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching EMIS student details'}, status=response.status_code)

    except RequestException as e:
        print(f"EMIS API Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def get_emis_staff_details(request, emp_id, reg_email):
    print(
        f"Received request for EMIS details of Employee ID: {emp_id} with reg_email: {reg_email}")

    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        emis_staff_api_url = settings.CREDENTIALS['EMIS_STAFF_API']
        request_url = f'{emis_staff_api_url}{emp_id}'

        print(f"Making request to EMIS Staff API: {request_url}")

        # Proceed with EMIS API request
        response = requests.get(request_url, headers=headers, verify=False)

        if response.status_code == 200:
            emis_details = response.json()
            print(f"EMIS Staff Details Response Data: {emis_details}")

            # Map the EMIS data to Agency and UserAgency models
            agency_data, user_agency_data = map_emis_staff_data_to_agency_models(
                emis_details)

            # Proceed with saving the data or any other operations as needed
            return JsonResponse({'agency_data': agency_data, 'user_agency_data': user_agency_data}, safe=False)
        else:
            print(
                f"Response error from EMIS API. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching EMIS staff details'}, status=response.status_code)

    except RequestException as e:
        print(f"EMIS API Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


# -----------------------------------------------//
# ----- MAPPER HELPERS PART OF THE VIEWS -------//
# ----------------------------------------------//

@permission_classes([AllowAny])
def map_user_data(citizen_detail):
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
        'father_name': citizen_detail.get('fatherName', ''),
        'mother_name': citizen_detail.get('motherName', ''),
        'ps_add_village': citizen_detail.get('villageName', ''),
        'ps_add_gewog': citizen_detail.get('gewogName', ''),
        'ps_add_dzongkhag': citizen_detail.get('dzongkhagName', ''),
        'user_role_agency': '',
        'user_class': '',
        'user_sub_class': '',
        'academy_code': '',
        'username': '',
        'password': '',
        'email': '',
    }
    return mapped_data


@permission_classes([AllowAny])
def formatDOB(dob):
    date_object = datetime.strptime(dob, '%d/%m/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    return formatted_date


@permission_classes([AllowAny])
def mapGender(gender):
    return 'Female' if gender == 'F' else 'Male'


@permission_classes([AllowAny])
def mapNationality(country):
    if not country or country.strip() == '':
        return 'Bhutanese'
    return country


@permission_classes([AllowAny])
def map_rcsc_data_to_agency_model(rcsc_data):
    agency_data = {
        'agency_code': rcsc_data.get('agencyID', ''),
        'agency_name': rcsc_data.get('agencyName', ''),
    }

    if 'clinical counselor' in rcsc_data.get('positionTitle', '').lower():
        user_role = CustomUser.ROLE_CLINICAL_COUNSELOR
    elif 'it officer' in rcsc_data.get('positionTitle', '').lower():
        user_role = CustomUser.ROLE_ADMIN
    elif 'school_counselor' in rcsc_data.get('positionTitle', '').lower():
        user_role = CustomUser.ROLE_SCHOOL_COUNSELOR
    elif 'student' in rcsc_data.get('positionTitle', '').lower():
        user_role = CustomUser.ROLE_STUDENT
    else:
        user_role = CustomUser.ROLE_STUDENT

    user_agency_data = {
        'user_role_agency': rcsc_data.get('positionTitle', ''),
        'user_code': rcsc_data.get('employeeNumber', ''),
        'ps_add_village': rcsc_data.get('village', ''),
        'ps_add_gewog': rcsc_data.get('gewog', ''),
        'ps_add_dzongkhag': rcsc_data.get('dzongkhag', ''),
        'parent_occupation': rcsc_data.get('parentOccupation', ''),
        'guardian_name': rcsc_data.get('guardianName', ''),
        'guardian_occupation': rcsc_data.get('guardianOccupation', ''),
        'parent_status': rcsc_data.get('parentStatus', ''),
        'current_living_with': rcsc_data.get('livingWith', ''),
        'user_role_agency': user_role,
        'user_class': rcsc_data.get('class', ''),
        'user_sub_class': rcsc_data.get('subclass', ''),
    }

    return agency_data, user_agency_data


@permission_classes([AllowAny])
def map_emis_data_to_agency_models(emis_data):
    student_detail = emis_data.get('studentDetails', {}).get('studentDetail', [])[
        0] if emis_data.get('studentDetails', {}).get('studentDetail') else {}

    if student_detail.get('guardian'):
        current_living_with = 'Guardian'
    else:
        father_name = student_detail.get('father', '')
        mother_name = student_detail.get('mother', '')
        if 'late' in father_name.lower() or 'lt' in father_name.lower():
            current_living_with = 'Mother'
        elif 'late' in mother_name.lower() or 'lt' in mother_name.lower():
            current_living_with = 'Father'
        else:
            current_living_with = 'Parents'

    agency_data = {
        'agency_code': student_detail.get('AgencyCode', ''),
        'agency_name': student_detail.get('school', ''),
    }

    user_agency_data = {
        'user_code': student_detail.get('student_code', ''),
        'ps_add_village': student_detail.get('present_village', ''),
        'ps_add_gewog': student_detail.get('present_geog', ''),
        'ps_add_dzongkhag': student_detail.get('present_dzongkhag', ''),
        'parent_occupation': f"{student_detail.get('father_occupation', '')}/{student_detail.get('mother_occupation', '')}",
        'guardian_name': student_detail.get('guardian', ''),
        'guardian_occupation': student_detail.get('guardian_occupation', ''),
        'parent_status': '',
        'current_living_with': current_living_with,
        'user_role_agency': 'student',
        'user_class': student_detail.get('class', ''),
        'user_sub_class': student_detail.get('stream', '')
    }

    # Return the mapped data
    return agency_data, user_agency_data


@permission_classes([AllowAny])
def map_emis_staff_data_to_agency_models(emis_data):
    staff_detail = emis_data.get('staffDetails', {}).get('staffDetail', [])[
        0] if emis_data.get('staffDetails', {}).get('staffDetail') else {}

    agency_data = {
        'agency_code': staff_detail.get('AgencyCode', ''),
        'agency_name': staff_detail.get('working_address', ''),
    }

    user_agency_data = {
        'user_code': staff_detail.get('emp_id', ''),
        'ps_add_village': staff_detail.get('present_village', ''),
        'ps_add_gewog': staff_detail.get('present_gewog', ''),
        'ps_add_dzongkhag': staff_detail.get('present_dzongkhag', ''),
        'parent_occupation': '',
        'guardian_name': '',
        'guardian_occupation': '',
        'parent_status': '',
        'current_living_with': '',
        'user_role_agency': 'school_counselor',
        'user_class': '',
        'user_sub_class': '',
    }

    return agency_data, user_agency_data


# -----------------------------------------------//
# ------ AUTH FUNCTIONS PART OF THE VIEWS ------//
# ----------------------------------------------//

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        print("Received request to register user.")

        # Extract data from request
        user_data = request.data.get('userData', {})
        agency_data = request.data.get('agencyData', {})
        user_agency_data = request.data.get('userAgencyData', {})

        print(f'User Data Received are:', user_data)
        print(f'Agency Data Received are:', agency_data)
        print(f'User Agency Data Received are:', user_agency_data)

        # Begin a transaction to ensure atomicity
        with transaction.atomic():
            # Check if the agency exists, if not, create it
            agency_code = agency_data.get('agency_code')
            agency, created = Agency.objects.get_or_create(agency_code=agency_code, defaults=agency_data)

            # Create the user
            user = CustomUser.objects.create_user(
                username=user_data.get('username'),
                email=user_data.get('email'),
                identity_number=user_data.get('identity_number'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                date_of_birth=user_data.get('date_of_birth'),
                gender=user_data.get('gender'),
                mob_number=user_data.get('mob_number'),
                perm_add_village=user_data.get('perm_add_village'),
                perm_add_gewog=user_data.get('perm_add_gewog'),
                perm_add_dzongkhag=user_data.get('perm_add_dzongkhag'),
                password=user_data.get('password'),
                role=user_data.get('role')
            )

            # Create the UserAgency link
            user_agency_data['user'] = user
            user_agency_data['agency'] = agency
            UserAgency.objects.create(**user_agency_data)

            response_data = {'userId': user.id, 'message': 'User registered successfully.'}
            return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Error registering user: {str(e)}")
        traceback.print_exc()
        error_message = str(e)
        response_data = {'error': error_message}
        print(f"Response data: {response_data}")

        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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


class UserList(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        user_serializer = self.get_serializer(queryset, many=True)

        agencies = Agency.objects.all()
        agency_serializer = AgencySerializer(agencies, many=True)

        user_agencies = UserAgency.objects.all()
        user_agency_serializer = UserAgencySerializer(user_agencies, many=True)

        response_data = {
            'user_details': user_serializer.data,
            'agency_details': agency_serializer.data,
            'user_agency_details': user_agency_serializer.data,
        }

        return Response(response_data)


class UpdateGyalsungDetails(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user != request.user:
            return Response({"error": "You do not have permission to perform this action"}, status=403)

        data = request.data
        if 'is_gyalsung' in data:
            user.is_gyalsung = data['is_gyalsung']
        if 'academy_code' in data:
            user.academy_code = data['academy_code']

        user.save()

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            logger.info('Login request received - Username: %s', username)

            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)

                user_role = user.role

                user_id = user.id

                logger.info(
                    'Login response sent - Token: %s, User Role: %s', token.key, user_role)

                print('returning token is:', token.key)
                return Response({"token": token.key, "user_role": user_role, "user_id": user_id}, status=status.HTTP_200_OK)
            else:
                logger.warning(
                    'Authentication failed for username: %s', username)
                return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error('Exception during login: %s', str(e))
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Agency):
            return {
                'id': obj.id,
                'agency_code': obj.agency_code,
                'agency_name': obj.agency_name,
            }
        return super().default(obj)


class GetUserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            logger.info('User details request received')

            user = request.user

            user_data = {
                'id': user.id,
                'username': user.username,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'identity_number': user.identity_number,
                'nationality': user.nationality,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
                'email': user.email,
                'mob_number': user.mob_number,
                'father_name': user.father_name,
                'mother_name': user.mother_name,
                'perm_add_village': user.perm_add_village,
                'perm_add_gewog': user.perm_add_gewog,
                'perm_add_dzongkhag': user.perm_add_dzongkhag,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
                'active_agency': None,
                'is_gyalsung': user.is_gyalsung,
                'academy_code': user.academy_code,
                'date_joined': user.date_joined,
                'role': user.role,
                'access_level': user.access_level,
            }

            agency_data = {}
            if user.active_agency:
                agency_data = {
                    'id': user.active_agency.id,
                    'agency_code': user.active_agency.agency_code,
                    'agency_name': user.active_agency.agency_name,
                }

            user_agency_data = {}
            try:
                user_agency = UserAgency.objects.get(user=user)
                user_agency_data = {
                    'user_code': user_agency.user_code,
                    'ps_add_village': user_agency.ps_add_village,
                    'ps_add_gewog': user_agency.ps_add_gewog,
                    'ps_add_dzongkhag': user_agency.ps_add_dzongkhag,
                    'parent_occupation': user_agency.parent_occupation,
                    'guardian_name': user_agency.guardian_name,
                    'guardian_occupation': user_agency.guardian_occupation,
                    'parent_status': user_agency.parent_status,
                    'current_living_with': user_agency.current_living_with,
                    'user_role_agency': user_agency.user_role_agency,
                    'user_class': user_agency.user_class,
                    'user_sub_class': user_agency.user_sub_class,
                }
            except UserAgency.DoesNotExist:
                pass

            return JsonResponse({"user": user_data, "agency": agency_data, "userAgency": user_agency_data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return JsonResponse({"error": "An error occurred while fetching user details."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class AgencySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Agency
#         fields = '__all__'

#     def create(self, validated_data):
#         # Create the agency instance
#         agency_instance = Agency.objects.create(**validated_data)
#         return agency_instance

#     def update(self, instance, validated_data):
#         for field, value in validated_data.items():
#             setattr(instance, field, value)
#         instance.save()
#         return instance


# class UserAgencySerializer(serializers.ModelSerializer):
#     agency_details = AgencySerializer(read_only=True)

#     class Meta:
#         model = UserAgency
#         fields = '__all__'

#     def create(self, validated_data):
#         user_agency_instance = UserAgency.objects.create(**validated_data)

#         user_instance = validated_data.get('user')
#         agency_instance = validated_data.get('agency_details')
#         if user_instance and agency_instance:
#             user_instance.active_agency = agency_instance
#             user_instance.save()

#         return user_agency_instance

#     def update(self, instance, validated_data):
#         for field, value in validated_data.items():
#             setattr(instance, field, value)
#         instance.save()

#         user_instance = instance.user
#         agency_instance = instance.agency_details
#         if user_instance and agency_instance:
#             user_instance.active_agency = agency_instance
#             user_instance.save()

#         return instance


# class CustomUserSerializer(serializers.ModelSerializer):
#     active_agency = AgencySerializer(read_only=True)
#     agency_details = serializers.PrimaryKeyRelatedField(
#         queryset=UserAgency.objects.all(), allow_null=True)

#     class Meta:
#         model = CustomUser
#         fields = [
#             'id', 'username', 'is_staff', 'is_active', 'is_gyalsung', 'identity_number',
#             'nationality', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
#             'gender', 'email', 'mob_number', 'father_name', 'mother_name',
#             'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag',
#             'profile_picture', 'academy_code', 'date_joined',
#             'password',  'role', 'active_agency', 'agency_details'
#         ]
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         agency_details = validated_data.pop('agency_details', None)
#         instance = super().create(validated_data)
#         if password:
#             instance.set_password(password)
#             instance.save()

#         if agency_details:
#             UserAgency.objects.create(user=instance, **agency_details)

#         return instance


# class PreRecordedUserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = [
#             'id', 'username', 'is_staff', 'is_active', 'is_gyalsung', 'identity_number',
#             'nationality', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
#             'gender', 'email', 'mob_number', 'father_name', 'mother_name',
#             'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag',
#             'profile_picture', 'active_agency', 'academy_code', 'date_joined',
#             'password',  'role'
#         ]

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = super().create(validated_data)
#         if password:
#             instance.set_password(password)
#             instance.save()
#         return instance
    
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            # Adjust the URL to point to your frontend's password reset page
            password_reset_url = f"{settings.FRONTEND_URL}/password-reset/{token}/"
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
    permission_classes = [AllowAny]

    def post(self, request, token, *args, **kwargs):
        password = request.data.get('password')
        User = get_user_model()
        try:
            # This assumes the email is sent as part of the request
            user_email = request.data.get('email')
            user = User.objects.get(email=user_email)

            if user and default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid token or email."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def verify_pre_recorded_user(request):
    cid = request.GET.get('cid')

    try:
        logger.info(f'Attempting to verify pre-recorded user with CID: {cid}')

        user = PreRecordedUser.objects.get(identity_number=cid)

        logger.info(f'Pre-recorded user found for CID: {cid}')

        if user.is_registered:
            logger.info('Pre-recorded user is already registered.')
            return JsonResponse({'success': False, 'message': 'Pre-recorded user is already registered.'}, status=400)

        user_data = {
            'id': user.id,
            'username': user.username,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'identity_number': user.identity_number,
            'nationality': user.nationality,
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'email': user.email,
            'mob_number': user.mob_number,
            'father_name': user.father_name,
            'mother_name': user.mother_name,
            'perm_add_village': user.perm_add_village,
            'perm_add_gewog': user.perm_add_gewog,
            'perm_add_dzongkhag': user.perm_add_dzongkhag,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'active_agency': None,  # No active agency for pre-recorded user
            'is_gyalsung': user.is_gyalsung,
            'academy_code': user.academy_code,
            'date_joined': user.date_joined,
            'role': user.role,
            'access_level': user.access_level,
        }

        agency_data = {
            'agency_name': user.agency_name,
            'agency_code': user.agency_code
        }

        user_agency_data = {
            'user_code': user.user_code,
            'ps_add_village': user.ps_add_village,
            'ps_add_gewog': user.ps_add_gewog,
            'ps_add_dzongkhag': user.ps_add_dzongkhag,
            'parent_occupation': user.parent_occupation,
            'guardian_name': user.guardian_name,
            'guardian_occupation': user.guardian_occupation,
            'parent_status': user.parent_status,
            'current_living_with': user.current_living_with,
            'user_role_agency': user.user_role_agency,
            'user_class': user.user_class,
            'user_sub_class': user.user_sub_class,
        }

        logger.info('Returning pre-recorded user data')
        return Response({
            "success": True,
            "message": "User verification successful.",
            "user": user_data,
            "agency": agency_data,
            "userAgency": user_agency_data,
        }, status=status.HTTP_200_OK)

    except PreRecordedUser.DoesNotExist:
        logger.error(f'Pre-recorded user not found for CID: {cid}')
        return JsonResponse({'success': False, 'message': 'Pre-recorded user not found.'}, status=404)
    except Exception as e:
        logger.exception(f'Error in verify_pre_recorded_user: {str(e)}')
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': 'Internal Server Error'}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_pre_recorded_user(request):
    try:
        print("Received request to register user.")

        user_data = request.data.get('userData', {})
        agency_data = request.data.get('agencyData', {})
        user_agency_data = request.data.get('userAgencyData', {})

        print(f'User Data Received are:', user_data)
        print(f'Agency Data Received are:', agency_data)
        print(f'User Agency Data Received are:', user_agency_data)

        with transaction.atomic():
            # Check if the agency exists, if not, create it
            agency_code = agency_data.get('agency_code')
            agency, created = Agency.objects.get_or_create(agency_code=agency_code, defaults=agency_data)

            # Create the user
            user = CustomUser.objects.create_user(
                username=user_data.get('username'),
                email=user_data.get('email'),
                identity_number=user_data.get('identity_number'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                date_of_birth=user_data.get('date_of_birth'),
                gender=user_data.get('gender'),
                mob_number=user_data.get('mob_number'),
                perm_add_village=user_data.get('perm_add_village'),
                perm_add_gewog=user_data.get('perm_add_gewog'),
                perm_add_dzongkhag=user_data.get('perm_add_dzongkhag'),
                password=user_data.get('password'),
                role=user_data.get('role')
            )

            # Create or update UserAgency link
            user_agency_data['user'] = user
            user_agency_data['agency'] = agency
            UserAgency.objects.create(**user_agency_data)

            # Update the PreRecordedUser model
            pre_recorded_user_identity_number = user_data.get('identity_number')
            PreRecordedUser.objects.filter(
                identity_number=pre_recorded_user_identity_number).update(is_registered=True)

            response_data = {'userId': user.id, 'message': 'Pre-recorded user registered successfully.'}
            return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Error registering user: {str(e)}")
        traceback.print_exc()
        response_data = {'error': 'Error registering user'}
        print(f"Response data: {response_data}")
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def user_logout(request):
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('sessionid')
    return response



