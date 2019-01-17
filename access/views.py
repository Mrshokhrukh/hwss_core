from rest_framework import generics
from .models import CustomUser, Agency
from .serializers import CustomUserSerializer, AgencySerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from .fetchcitizendetails import get_citizen_details, map_citizen_details_to_model
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import logging
import json
import time
import base64
import os
from django.http import JsonResponse
from django.conf import settings
import requests
from requests.exceptions import RequestException
from django.views.decorators.csrf import csrf_exempt



GLOBAL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'global.json')

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


logger = logging.getLogger(__name__)

@csrf_exempt
def fetch_citizen_details(request, cid):
    print(f"Received request for CID: {cid}")
    print(f"Request Headers: {request.headers}")

    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        api_url = settings.CREDENTIALS['API_URL']

        print(f"Making request to: {api_url}{cid}")
        print(f"Request headers: {headers}")

        response = requests.get(
            f'{api_url}{cid}', headers=headers, verify=False)

        # Log response details
        if response.status_code == 200:
            citizen_detail = response.json().get('citizenDetailsResponse', {}
                                                 ).get('citizenDetail', [None])[0]
            print(f"Response Data: {citizen_detail}")
            return JsonResponse(citizen_detail, safe=False)
        else:
            print(
                f"Response error. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching citizen details'}, status=response.status_code)

    except RequestException as e:
        print(f"Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def register_api_user(request):
    """
    Register a user with the provided data.
    Modify this function based on your actual model fields.
    """
    try:
        user_data = request.POST  # Assuming the frontend sends user data in the request body

        # Create a new user
        user = get_user_model().objects.create_user(
            username=user_data['username'],
            identity_number=user_data['identity_number'],
            nationality=user_data['nationality'],
            first_name=user_data['first_name'],
            middle_name=user_data['middle_name'],
            last_name=user_data['last_name'],
            date_of_birth=user_data['date_of_birth'],
            gender=user_data['gender'],
            email=user_data['email'],
            mob_number=user_data['mob_number'],
            perm_add_village=user_data['perm_add_village'],
            perm_add_gewog=user_data['perm_add_gewog'],
            perm_add_dzongkhag=user_data['perm_add_dzongkhag'],
        )

        # Log the user creation details
        print(f"User created successfully: {user}")

        return JsonResponse({'success': 'User registered successfully'}, status=201)
    except Exception as e:
        print(f"Error registering user: {str(e)}")
        return JsonResponse({'error': 'Error registering user'}, status=500)

# def fetch_rcsc_details(request, cid):
#     print(f"Received request for RCSC details of CID: {cid}")

#     try:
#         token = 'Bearer ' + generate_token()
#         headers = {'Authorization': token}
#         rcsc_api_url = settings.CREDENTIALS['RCSC_API']
#         print(f"Making request to RCSC API: {rcsc_api_url}{cid}")
#         print(f"Request headers: {headers}")

#         response = requests.get(f'{rcsc_api_url}{cid}', headers=headers, verify=False)

#         if response.status_code == 200:
#             rcsc_details = response.json()
#             print(f"RCSC Details Response Data: {rcsc_details}")
#             return JsonResponse(rcsc_details, safe=False)
#         else:
#             print(f"Response error from RCSC API. Status code: {response.status_code}, Response body: {response.text}")
#             return JsonResponse({'error': 'Error fetching RCSC details'}, status=response.status_code)

#     except RequestException as e:
#         print(f"RCSC API Request Exception: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)



def map_rcsc_data_to_agency_model(rcsc_data):
    # Map the relevant data from rcsc_data to Agency model fields
    mapped_data = {
        'agency_code': rcsc_data.get('agencyID', ''),
        'user_role_agency': rcsc_data.get('positionTitle', ''),
        'agency_name': rcsc_data.get('agencyName', ''),
        'user_code': rcsc_data.get('employeeNumber', ''),
        # Map other fields as needed
    }
    return mapped_data

def fetch_rcsc_details(request, cid):
    print(f"Received request for RCSC details of CID: {cid}")

    try:
        token = 'Bearer ' + generate_token()
        headers = {'Authorization': token}
        rcsc_api_url = settings.CREDENTIALS['RCSC_API']
        print(f"Making request to RCSC API: {rcsc_api_url}{cid}")
        print(f"Request headers: {headers}")

        response = requests.get(f'{rcsc_api_url}{cid}', headers=headers, verify=False)

        if response.status_code == 200:
            rcsc_details = response.json().get('employeedetails', {}).get('employeedetail', [])[0]
            print(f"RCSC Details Response Data: {rcsc_details}")

            # Map the RCSC data to Agency model
            mapped_data = map_rcsc_data_to_agency_model(rcsc_details)

            # Get the user ID associated with the request
            user_id = request.user.id  # Assuming the user is authenticated

            # Create or update the Agency model instance
            agency, created = Agency.objects.update_or_create(user_id=user_id, defaults=mapped_data)

            # Return the mapped data to Vue.js
            return JsonResponse(mapped_data, safe=False)

        else:
            print(f"Response error from RCSC API. Status code: {response.status_code}, Response body: {response.text}")
            return JsonResponse({'error': 'Error fetching RCSC details'}, status=response.status_code)

    except RequestException as e:
        print(f"RCSC API Request Exception: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


# class UserCreate(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

#     def create(self, request, *args, **kwargs):
#         user_serializer = self.get_serializer(data=request.data)
#         user_serializer.is_valid(raise_exception=True)
#         user = user_serializer.save()

#         agency_data = request.data.get('agency', {})
#         agency_serializer = AgencySerializer(data=agency_data)
#         if agency_serializer.is_valid():
#             agency_serializer.save(user=user)
#         else:
#             user.delete()
#             return Response(agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         headers = self.get_success_headers(user_serializer.data)
#         return Response(user_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        agency_data = request.data.get('agency', {})

        # Validate user data
        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Validate agency data
        agency_serializer = AgencySerializer(data=agency_data)
        if agency_serializer.is_valid():
            agency_serializer.save(user=user)  # Associate agency with user
        else:
            user.delete()  # Rollback user creation if agency validation fails
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

    user = get_object_or_404(PreRecordedUser, identity_number=cid, date_of_birth=dob)
    return Response({
        'success': True,
        'message': 'Pre-recorded user found.',
        'user_data': {
            'identity_number': user.identity_number,
            'first_name': user.first_name,
            # Add other fields as needed
        }
    })