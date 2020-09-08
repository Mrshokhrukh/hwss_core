# -----------------------------------------------//
# -------- IMPORTS PART OF THE VIEWS -----------//
# ----------------------------------------------//

import base64
import json
import logging
import random
import string
import time
import traceback
from datetime import date, datetime

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import RequestException
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from access.constants import GLOBAL_FILE_PATH
from access.models import Agency, CustomUser, PreRecordedUser, UserAgency
from access.serializers import (
    AgencySerializer,
    CustomUserSerializer,
    UserAgencySerializer,
)
from access.utils import (
    create_user_and_agency_from_raw_data_for_gyalsung,
    process_cid_data_for_user_creation_using_gyalsung,
    convert_date_format,
    process_cid_gyalsung_user_data,
    merged_gyalsung_api_and_cid_api_data_for_user_creation,
)
from gyalsung.models import (
    GyalsungAssessment,
    GyalsungEventSubstanceRiskMeasurement,
    GyalsungUserScreeningHistory,
)
from screening.models import (
    CaseBasedSubmission,
    CaseScreening,
    EventBasedSubmission,
    EventScreening,
)

logger = logging.getLogger(__name__)


# -----------------------------------------------//
# ------ AUTH TOKEN PART OF THE VIEWS ----------//
# ----------------------------------------------//


@api_view(["GET"])
@permission_classes([AllowAny])
@csrf_exempt
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({"csrf_token": csrf_token})


@permission_classes([AllowAny])
def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


@permission_classes([AllowAny])
def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file)


@permission_classes([AllowAny])
def read_global():
    with open(GLOBAL_FILE_PATH, "r") as file:
        return json.load(file)


@permission_classes([AllowAny])
def write_global(data):
    with open(GLOBAL_FILE_PATH, "w") as file:
        json.dump(data, file)


@permission_classes([AllowAny])
def get_authorization_code():
    auth_key = settings.CREDENTIALS["API_KEY"]
    auth_secret = settings.CREDENTIALS["API_SECRET"]
    auth_code = f"{auth_key}:{auth_secret}"
    return base64.b64encode(auth_code.encode()).decode()


@permission_classes([AllowAny])
def get_gyalsung_authorization_code():
    auth_key = settings.CREDENTIALS["GYALSUNG_API_KEY"]
    auth_secret = settings.CREDENTIALS["GYALSUNG_API_SECRET"]
    auth_code = f"{auth_key}:{auth_secret}"
    return base64.b64encode(auth_code.encode()).decode()


@permission_classes([AllowAny])
def global_session():
    data = read_global()
    if data["accessToken"] != "" and data["expiryTime"] > time.time():
        return True
    return False


@permission_classes([AllowAny])
def generate_token():
    token_url = settings.CREDENTIALS["TOKEN_URL"]
    if not global_session():
        headers = {"Authorization": "Basic " + get_authorization_code()}
        form_params = {"grant_type": "client_credentials"}

        response = requests.post(
            token_url, headers=headers, data=form_params, timeout=30
        )

        if response.status_code == 200:
            json_object = response.json()
            expiry_time = int(time.time()) + json_object["expires_in"]

            global_settings = read_global()
            global_settings["accessToken"] = json_object["access_token"]
            global_settings["expiryTime"] = expiry_time

            write_global(global_settings)

            return global_settings["accessToken"]
        else:
            return "Something went wrong. Please try again!"
    else:
        return read_global()["accessToken"]


@permission_classes([AllowAny])
def generate_gyalsung_token():
    token_url = settings.CREDENTIALS["GYALSUNG_API_TOKEN_URL"]
    headers = {"Content-Type": "application/json"}
    data = {
        "client_id": settings.CREDENTIALS["GYALSUNG_API_KEY"],
        "client_secret": settings.CREDENTIALS["GYALSUNG_API_SECRET"],
    }
    response = requests.post(
        token_url,
        headers=headers,
        json=data,
    )
    if response.status_code == 200:
        json_object = response.json()
        return json_object["access_token"]
    else:
        return "Something went wrong. Please try again!"


# -----------------------------------------------//
# ------ API FETCHING PART OF THE VIEWS --------//
# ----------------------------------------------//


@permission_classes([AllowAny])
def fetch_citizen_details(request, cid):
    try:
        token = "Bearer " + generate_token()
        headers = {"Authorization": token}
        api_url = settings.CREDENTIALS["API_URL"]
        response = requests.get(f"{api_url}{cid}", headers=headers)

        if response.status_code == 200:
            citizen_detail = (
                response.json()
                .get("citizenDetailsResponse", {})
                .get("citizenDetail", [None])[0]
            )

            mapped_user_data = map_user_data(citizen_detail)

            request.session["user_data"] = mapped_user_data

            return JsonResponse(citizen_detail, safe=False)
        else:
            return JsonResponse(
                {"error": "Error fetching citizen details"}, status=response.status_code
            )

    except RequestException as e:
        print(f"Request Exception: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def fetch_rcsc_details(request, cid, reg_email):

    try:
        token = "Bearer " + generate_token()
        headers = {"Authorization": token}
        rcsc_api_url = settings.CREDENTIALS["RCSC_API"]

        # Step 2: Proceed with RCSC API request
        response = requests.get(f"{rcsc_api_url}{cid}", headers=headers)

        if response.status_code == 200:
            rcsc_details = (
                response.json().get("employeedetails", {}).get("employeedetail", [])[0]
            )

            # Map the RCSC data to Agency and UserAgency models
            agency_data, user_agency_data = map_rcsc_data_to_agency_model(rcsc_details)

            # Proceed to Step 4 or any other step as needed
            return JsonResponse(
                {"agency_data": agency_data, "user_agency_data": user_agency_data},
                safe=False,
            )
        else:
            return JsonResponse(
                {"error": "Error fetching RCSC details"}, status=response.status_code
            )

    except RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def get_emis_student_details(request, student_code, dob, reg_email):

    try:
        token = "Bearer " + generate_token()
        headers = {"Authorization": token}
        emis_student_api_url = settings.CREDENTIALS["EMIS_STUDENT_API"]
        request_url = f"{emis_student_api_url}{student_code}/{dob}"

        print(f"Making request to EMIS Student API: {request_url}")

        # Step 2: Proceed with EMIS API request
        response = requests.get(request_url, headers=headers)

        if response.status_code == 200:
            emis_details = response.json()
            print(f"EMIS Details Response Data: {emis_details}")

            # Map the EMIS data to Agency and UserAgency models
            agency_data, user_agency_data = map_emis_data_to_agency_models(emis_details)

            # Proceed with saving the data or any other operations as needed
            return JsonResponse(
                {"agency_data": agency_data, "user_agency_data": user_agency_data},
                safe=False,
            )
        else:
            print(
                f"Response error from EMIS API. Status code: {response.status_code}, Response body: {response.text}"
            )
            return JsonResponse(
                {"error": "Error fetching EMIS student details"},
                status=response.status_code,
            )

    except RequestException as e:
        print(f"EMIS API Request Exception: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@permission_classes([AllowAny])
def get_emis_staff_details(request, emp_id, reg_email):
    print(
        f"Received request for EMIS details of Employee ID: {emp_id} with reg_email: {reg_email}"
    )

    try:
        token = "Bearer " + generate_token()
        headers = {"Authorization": token}
        emis_staff_api_url = settings.CREDENTIALS["EMIS_STAFF_API"]
        request_url = f"{emis_staff_api_url}{emp_id}"

        # Proceed with EMIS API request
        response = requests.get(request_url, headers=headers)

        if response.status_code == 200:
            emis_details = response.json()

            # Map the EMIS data to Agency and UserAgency models
            agency_data, user_agency_data = map_emis_staff_data_to_agency_models(
                emis_details
            )

            # Proceed with saving the data or any other operations as needed
            return JsonResponse(
                {"agency_data": agency_data, "user_agency_data": user_agency_data},
                safe=False,
            )
        else:
            return JsonResponse(
                {"error": "Error fetching EMIS staff details"},
                status=response.status_code,
            )

    except RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


# -----------------------------------------------//
# ----- MAPPER HELPERS PART OF THE VIEWS -------//
# ----------------------------------------------//


@permission_classes([AllowAny])
def map_user_data(citizen_detail):
    mapped_data = {
        "identity_number": citizen_detail.get("cid", ""),
        "first_name": citizen_detail.get("firstName", ""),
        "middle_name": citizen_detail.get("middleName", "") or "",
        "last_name": citizen_detail.get("lastName", ""),
        "date_of_birth": formatDOB(citizen_detail.get("dob", "")),
        "gender": mapGender(citizen_detail.get("gender", "")),
        "mob_number": citizen_detail.get("mobileNumber", ""),
        "perm_add_village": citizen_detail.get("villageName", ""),
        "perm_add_gewog": citizen_detail.get("gewogName", ""),
        "perm_add_dzongkhag": citizen_detail.get("dzongkhagName", ""),
        "nationality": mapNationality(citizen_detail.get("country", "")),
        "father_name": citizen_detail.get("fatherName", ""),
        "mother_name": citizen_detail.get("motherName", ""),
        "ps_add_village": citizen_detail.get("villageName", ""),
        "ps_add_gewog": citizen_detail.get("gewogName", ""),
        "ps_add_dzongkhag": citizen_detail.get("dzongkhagName", ""),
        "user_role_agency": "",
        "user_class": "",
        "user_sub_class": "",
        "academy_code": "",
        "username": "",
        "password": "",
        "email": "",
    }
    return mapped_data


@permission_classes([AllowAny])
def formatDOB(dob):
    date_object = datetime.strptime(dob, "%d/%m/%Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return formatted_date


@permission_classes([AllowAny])
def mapGender(gender):
    return "Female" if gender == "F" else "Male"


@permission_classes([AllowAny])
def mapNationality(country):
    if not country or country.strip() == "":
        return "Bhutanese"
    return country


@permission_classes([AllowAny])
def map_rcsc_data_to_agency_model(rcsc_data):
    agency_data = {
        "agency_code": rcsc_data.get("agencyID", ""),
        "agency_name": rcsc_data.get("agencyName", ""),
        "agency_parent": rcsc_data.get("parentAgency", ""),
    }

    if "clinical counselor" in rcsc_data.get("positionTitle", "").lower():
        user_role = CustomUser.ROLE_CLINICAL_COUNSELOR
    elif "ict officer" in rcsc_data.get("positionTitle", "").lower():
        user_role = CustomUser.ROLE_ADMIN
    elif (
        "counselor" in rcsc_data.get("positionTitle", "").lower()
        and "clinical" not in rcsc_data.get("positionTitle", "").lower()
    ):
        user_role = CustomUser.ROLE_SCHOOL_COUNSELOR
    elif "student" in rcsc_data.get("positionTitle", "").lower():
        user_role = CustomUser.ROLE_STUDENT
    else:
        user_role = CustomUser.ROLE_PUBLIC

    user_agency_data = {
        "user_role_agency": rcsc_data.get("positionTitle", ""),
        "user_code": rcsc_data.get("employeeNumber", ""),
        "parent_occupation": rcsc_data.get("parentOccupation", ""),
        "guardian_name": rcsc_data.get("guardianName", ""),
        "guardian_occupation": rcsc_data.get("guardianOccupation", ""),
        "parent_status": rcsc_data.get("parentStatus", ""),
        "current_living_with": rcsc_data.get("livingWith", ""),
        "user_role_agency": user_role,
        "user_class": rcsc_data.get("class", ""),
        "user_sub_class": rcsc_data.get("subclass", ""),
    }

    return agency_data, user_agency_data


@permission_classes([AllowAny])
def map_emis_data_to_agency_models(emis_data):
    def roman_to_int(s):
        roman_numerals = {
            "I": 1,
            "II": 2,
            "III": 3,
            "IV": 4,
            "V": 5,
            "VI": 6,
            "VII": 7,
            "VIII": 8,
            "IX": 9,
            "X": 10,
            "XI": 11,
            "XII": 12,
        }
        return roman_numerals.get(s, 0)

    student_detail = (
        emis_data.get("studentDetails", {}).get("studenDetail", [])[0]
        if emis_data.get("studentDetails", {}).get("studenDetail")
        else {}
    )
    if student_detail:
        current_living_with = (
            "Guardian" if student_detail.get("guardian") else "Parents"
        )
        father_name = student_detail.get("father", "")
        mother_name = student_detail.get("mother", "")
        if father_name:
            if "late" in father_name.lower() or "lt" in father_name.lower():
                current_living_with = "Mother"
        elif mother_name:
            if "late" in mother_name.lower() or "lt" in mother_name.lower():
                current_living_with = "Father"
        agency_data = {
            "agency_code": student_detail.get("AgencyCode", ""),
            "agency_name": student_detail.get("school", ""),
            "present_dzongkhag": student_detail.get("present_dzongkhag", ""),
            "present_gewog": student_detail.get("present_gewog", ""),
            "present_village": student_detail.get("present_village", ""),
        }
        user_class = student_detail.get("class", "")
        user_class_int = (
            roman_to_int(user_class.upper()) if user_class != "PP" else user_class
        )
        user_agency_data = {
            "user_code": student_detail.get("student_code", ""),
            "parent_occupation": f"{student_detail.get('father_occupation', '')}/{student_detail.get('mother_occupation', '')}",
            "guardian_name": student_detail.get("guardian", "Not Provided"),
            "guardian_occupation": student_detail.get(
                "guardian_occupation", "Not Provided"
            ),
            "current_living_with": current_living_with,
            "user_role_agency": "student",
            "user_class": user_class_int,
            "user_stream": student_detail.get("stream", ""),
            "user_sub_class": student_detail.get("section", ""),
            "parent_status": student_detail.get("MaritialStatus", ""),
        }
    else:
        agency_data = {}
        user_agency_data = {}

    return agency_data, user_agency_data


@permission_classes([AllowAny])
def map_emis_staff_data_to_agency_models(emis_data):
    staff_detail = (
        emis_data.get("staffDetails", {}).get("staffDetail", [])[0]
        if emis_data.get("staffDetails", {}).get("staffDetail")
        else {}
    )

    agency_data = {
        "agency_code": staff_detail.get("AgencyCode", ""),
        "agency_name": staff_detail.get("working_address", ""),
        "present_dzongkhag": staff_detail.get("present_dzongkhag", ""),
        "present_gewog": staff_detail.get("present_gewog", ""),
        "present_village": staff_detail.get("present_village", ""),
    }

    user_agency_data = {
        "user_code": staff_detail.get("emp_id", ""),
        "parent_occupation": "",
        "guardian_name": "",
        "guardian_occupation": "",
        "parent_status": "",
        "current_living_with": "",
        "user_role_agency": "school_counselor",
        "user_class": "",
        "user_sub_class": "",
    }

    return agency_data, user_agency_data


# -----------------------------------------------//
# ------ AUTH FUNCTIONS PART OF THE VIEWS ------//
# ----------------------------------------------//


class CustomTokenAuthentication(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        # Extract the token from the request
        auth_token = request.META.get("HTTP_AUTHORIZATION")

        # Check if token exists
        if not auth_token:
            raise AuthenticationFailed("Invalid token header. No credentials provided.")

        # Split the token type and key
        try:
            token_type, token_key = auth_token.split(" ")
        except ValueError:
            raise AuthenticationFailed("Invalid token header format.")

        # Check if token type is valid
        if token_type.lower() != "token":
            raise AuthenticationFailed(
                'Invalid token type. Only "Token" authentication is supported.'
            )

        # Retrieve token from the database
        try:
            token = Token.objects.select_related("user").get(key=token_key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        # Token is valid, return a minimal response indicating its validity
        return Response({"valid": True}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    user_data = request.data.get("userData", {})
    agency_data = request.data.get("agencyData", {})
    user_agency_data = request.data.get("userAgencyData", {})

    email = user_data.get("email")
    username = user_data.get("username")
    password = user_data.get("password")
    identity_number = user_data.get("identity_number")

    if not email:
        return Response(
            {"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    if not username:
        return Response(
            {"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    if not password:
        return Response(
            {"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    if not user_agency_data.get("user_code") or not user_agency_data.get(
        "user_role_agency"
    ):
        return Response(
            {"error": "User code and role within agency are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST
            )
        if (
            identity_number
            and CustomUser.objects.filter(
                identity_number=identity_number, is_old_case_user=False
            ).exists()
        ):
            return Response(
                {
                    "error": "User with this Identity Number already exists. Please login or use forgot password."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            agency_code = agency_data.get("agency_code")
            agency, _ = Agency.objects.get_or_create(
                agency_code=agency_code, defaults=agency_data
            )

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                identity_number=identity_number,
                first_name=user_data.get("first_name"),
                middle_name=user_data.get("middle_name"),
                last_name=user_data.get("last_name"),
                date_of_birth=user_data.get("date_of_birth"),
                gender=user_data.get("gender"),
                mob_number=user_data.get("mob_number"),
                perm_add_village=user_data.get("perm_add_village"),
                perm_add_gewog=user_data.get("perm_add_gewog"),
                perm_add_dzongkhag=user_data.get("perm_add_dzongkhag"),
                nationality=user_data.get("nationality"),
                father_name=user_data.get("father_name"),
                mother_name=user_data.get("mother_name"),
                ps_add_village=user_data.get("ps_add_village"),
                ps_add_gewog=user_data.get("ps_add_gewog"),
                ps_add_dzongkhag=user_data.get("ps_add_dzongkhag"),
                role=user_data.get("role"),
                active_agency=agency,
                registration_method="cluster_registration",
            )

            user_agency = UserAgency.objects.create(
                user=user,
                agency=agency,
                user_code=user_agency_data.get("user_code"),
                parent_occupation=user_agency_data.get("parent_occupation"),
                guardian_name=user_agency_data.get("guardian_name"),
                guardian_occupation=user_agency_data.get("guardian_occupation"),
                parent_status=user_agency_data.get("parent_status"),
                current_living_with=user_agency_data.get("current_living_with"),
                user_role_agency=user_agency_data.get("user_role_agency"),
                user_class=user_agency_data.get("user_class"),
                user_stream=user_agency_data.get("user_stream"),
                user_sub_class=user_agency_data.get("user_sub_class"),
            )

            response_data = {
                "userId": user.id,
                "message": "User registered successfully.",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

    except IntegrityError as ie:
        if "username" in str(ie):
            return Response(
                {"error": "Username conflict occurred."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "email" in str(ie):
            return Response(
                {"error": "Email conflict occurred."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "identity_number" in str(ie):
            return Response(
                {"error": "Identity number conflict occurred."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"error": f"Database error during registration: {str(ie)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred during registration."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def registerCounselorCaseUser(request):
    user_data = request.data.get("userData", {})
    agency_data = request.data.get("agencyData", {})
    user_agency_data = request.data.get("userAgencyData", {})

    cid = user_data.get("CID")
    if not cid:
        return Response(
            {"error": "CID (Identity Number) is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        existing_user = CustomUser.objects.filter(identity_number=cid).first()

        if existing_user and existing_user.registration_method != "case_registration":
            error_message = (
                f"User with CID {cid} already exists but was registered via "
                f"'{existing_user.registration_method}' method. "
                f"Cannot proceed with counselor case registration."
            )
            return Response(
                {
                    "error": error_message,
                    "registration_method": existing_user.registration_method,
                },
                status=status.HTTP_409_CONFLICT,
            )

        with transaction.atomic():
            agency_code = agency_data.get("agency_code")
            if not agency_code:
                return Response(
                    {"error": "Agency code is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            agency, agency_created = Agency.objects.update_or_create(
                agency_code=agency_code,
                defaults={
                    k: v
                    for k, v in agency_data.items()
                    if v is not None and k != "agency_code"
                },
            )

            full_name = user_data.get("clientFullName", "").strip()
            first_name, middle_names, last_name = "", "", ""
            if full_name:
                name_parts = full_name.strip().split()
                name_parts = [part for part in name_parts if part]
                if len(name_parts) == 1:
                    first_name, middle_names, last_name = (
                        name_parts[0],
                        "",
                        name_parts[0][0] if name_parts[0] else "",
                    )
                elif len(name_parts) == 2:
                    first_name, last_name, middle_names = (
                        name_parts[0],
                        name_parts[1],
                        "",
                    )
                else:
                    first_name, last_name, middle_names = (
                        name_parts[0],
                        name_parts[-1],
                        " ".join(name_parts[1:-1]),
                    )

            user_to_process = None
            is_new_user = False

            if existing_user:
                user_to_process = existing_user

                new_username = user_data.get("username")
                new_email = user_data.get("email")
                if (
                    new_username
                    and new_username != existing_user.username
                    and CustomUser.objects.filter(username=new_username)
                    .exclude(pk=existing_user.pk)
                    .exists()
                ):
                    return Response(
                        {"error": f"Username '{new_username}' is already taken."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if (
                    new_email
                    and new_email != existing_user.email
                    and CustomUser.objects.filter(email=new_email)
                    .exclude(pk=existing_user.pk)
                    .exists()
                ):
                    return Response(
                        {"error": f"Email '{new_email}' is already taken."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                update_fields = []

                def update_if_changed(field_name, new_value):
                    if (
                        new_value is not None
                        and getattr(existing_user, field_name) != new_value
                    ):
                        setattr(existing_user, field_name, new_value)
                        update_fields.append(field_name)

                update_if_changed("username", user_data.get("username"))
                update_if_changed("email", user_data.get("email"))
                update_if_changed("first_name", first_name)
                update_if_changed("middle_name", middle_names)
                update_if_changed("last_name", last_name)
                update_if_changed("date_of_birth", user_data.get("DOB"))
                update_if_changed("gender", user_data.get("gender"))
                update_if_changed("mob_number", user_data.get("phoneNumber"))
                update_if_changed("perm_add_village", user_data.get("currentAddress"))
                update_if_changed("perm_add_gewog", user_data.get("gewog"))
                update_if_changed("perm_add_dzongkhag", user_data.get("dzongkhag"))
                update_if_changed("ps_add_village", user_data.get("currentAddress"))
                update_if_changed("ps_add_gewog", user_data.get("gewog"))
                update_if_changed("ps_add_dzongkhag", user_data.get("dzongkhag"))
                update_if_changed("active_agency", agency)

                if update_fields:
                    existing_user.save(update_fields=update_fields)

            else:
                is_new_user = True

                new_username = user_data.get("username")
                new_email = user_data.get("email")
                if (
                    new_username
                    and CustomUser.objects.filter(username=new_username).exists()
                ):
                    return Response(
                        {"error": f"Username '{new_username}' already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if new_email and CustomUser.objects.filter(email=new_email).exists():
                    return Response(
                        {"error": f"Email '{new_email}' already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user = CustomUser.objects.create_user(
                    username=new_username,
                    email=new_email,
                    identity_number=cid,
                    first_name=first_name,
                    middle_name=middle_names,
                    last_name=last_name,
                    date_of_birth=user_data.get("DOB"),
                    gender=user_data.get("gender"),
                    mob_number=user_data.get("phoneNumber"),
                    perm_add_village=user_data.get("currentAddress"),
                    perm_add_gewog=user_data.get("gewog"),
                    perm_add_dzongkhag=user_data.get("dzongkhag"),
                    nationality="Bhutanese",
                    ps_add_village=user_data.get("currentAddress"),
                    ps_add_gewog=user_data.get("gewog"),
                    ps_add_dzongkhag=user_data.get("dzongkhag"),
                    role="general_public",
                    active_agency=agency,
                    registration_method="case_registration",
                )
                user_to_process = user

            ua_defaults = {
                "user_code": user_agency_data.get("user_code"),
                "parent_occupation": user_agency_data.get("parent_occupation"),
                "guardian_name": user_agency_data.get("guardian_name"),
                "guardian_occupation": user_agency_data.get("guardian_occupation"),
                "parent_status": user_agency_data.get("parent_status"),
                "current_living_with": user_agency_data.get("current_living_with"),
                "user_role_agency": user_agency_data.get("user_role_agency"),
                "user_class": user_agency_data.get("user_class"),
                "user_stream": user_agency_data.get("user_stream"),
                "user_sub_class": user_agency_data.get("user_sub_class"),
            }
            ua_defaults = {k: v for k, v in ua_defaults.items() if v is not None}

            user_agency, ua_created = UserAgency.objects.update_or_create(
                user=user_to_process, agency=agency, defaults=ua_defaults
            )

            cs_defaults = {
                "case_name": user_data.get("caseName"),
                "purpose": user_data.get("purpose"),
                "dzongkhag": user_data.get("dzongkhag"),
                "counselor": user_data.get("counselorName"),
                "date": date.today(),
            }
            cs_defaults = {k: v for k, v in cs_defaults.items() if v is not None}

            case_screening, cs_created = CaseScreening.objects.update_or_create(
                user=user_to_process, defaults=cs_defaults
            )

            status_code = status.HTTP_201_CREATED if is_new_user else status.HTTP_200_OK
            message = (
                "Counselor case user registered successfully."
                if is_new_user
                else "Counselor case user updated successfully."
            )
            response_data = {"userId": user_to_process.id, "message": message}
            return Response(response_data, status=status_code)

    except IntegrityError as ie:
        if "username" in str(ie).lower():
            return Response(
                {
                    "error": "Username conflict occurred. The provided username might already be in use."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "email" in str(ie).lower():
            return Response(
                {
                    "error": "Email conflict occurred. The provided email might already be in use."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "unique_identity_number" in str(ie).lower():
            return Response(
                {
                    "error": "CID conflict occurred. This should have been caught earlier unless constraint violation happened unexpectedly."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"error": "Database error: An integrity constraint was violated."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred during registration."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def registerCounselorEventUser(request):
    user_data = request.data.get("userData", {})
    agency_data = request.data.get("agencyData", {})
    user_agency_data = request.data.get("userAgencyData", {})

    cid = user_data.get("CID")
    if not cid:
        return Response(
            {"error": "CID (Identity Number) is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # if not user_agency_data.get('user_code') or not user_agency_data.get('user_role_agency'):
    #     return Response({'error': 'User code and role within agency are required.'}, status=status.HTTP_400_BAD_REQUEST)

    counselor_name = user_data.get("counselorName")
    if not counselor_name:
        return Response(
            {"error": "Counselor name is required to find the event."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        event_screening = EventScreening.objects.filter(
            counselor=counselor_name, approval_status="approved"
        ).first()

        if not event_screening:
            return Response(
                {
                    "error": f"Approved event screening for counselor '{counselor_name}' not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        existing_user = CustomUser.objects.filter(identity_number=cid).first()

        if existing_user and existing_user.registration_method != "event_registration":
            error_message = (
                f"User with CID {cid} already exists but was registered via "
                f"'{existing_user.registration_method}' method. "
                f"Cannot proceed with counselor event registration."
            )
            return Response(
                {
                    "error": error_message,
                    "registration_method": existing_user.registration_method,
                },
                status=status.HTTP_409_CONFLICT,
            )

        with transaction.atomic():
            agency_code = agency_data.get("agency_code")
            if not agency_code:
                return Response(
                    {"error": "Agency code is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            agency, agency_created = Agency.objects.update_or_create(
                agency_code=agency_code,
                defaults={
                    k: v
                    for k, v in agency_data.items()
                    if v is not None and k != "agency_code"
                },
            )

            full_name = user_data.get("clientFullName", "").strip()
            first_name, middle_names, last_name = "", "", ""
            if full_name:
                name_parts = full_name.strip().split()
                name_parts = [part for part in name_parts if part]
                if len(name_parts) == 1:
                    first_name, middle_names, last_name = (
                        name_parts[0],
                        "",
                        name_parts[0][0] if name_parts[0] else "",
                    )
                elif len(name_parts) == 2:
                    first_name, last_name, middle_names = (
                        name_parts[0],
                        name_parts[1],
                        "",
                    )
                else:
                    first_name, last_name, middle_names = (
                        name_parts[0],
                        name_parts[-1],
                        " ".join(name_parts[1:-1]),
                    )

            user_to_process = None
            is_new_user = False

            if existing_user:
                user_to_process = existing_user

                new_username = user_data.get("username")
                new_email = user_data.get("email")
                if (
                    new_username
                    and new_username != existing_user.username
                    and CustomUser.objects.filter(username=new_username)
                    .exclude(pk=existing_user.pk)
                    .exists()
                ):
                    return Response(
                        {"error": f"Username '{new_username}' is already taken."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if (
                    new_email
                    and new_email != existing_user.email
                    and CustomUser.objects.filter(email=new_email)
                    .exclude(pk=existing_user.pk)
                    .exists()
                ):
                    return Response(
                        {"error": f"Email '{new_email}' is already taken."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                update_fields = []

                def update_if_changed(field_name, new_value):
                    if (
                        field_name == "active_agency"
                        and new_value is not None
                        and getattr(existing_user, field_name) != new_value
                    ):
                        setattr(existing_user, field_name, new_value)
                        update_fields.append(field_name)
                    elif (
                        new_value is not None
                        and getattr(existing_user, field_name) != new_value
                    ):
                        setattr(existing_user, field_name, new_value)
                        update_fields.append(field_name)

                update_if_changed("username", user_data.get("username"))
                update_if_changed("email", user_data.get("email"))
                update_if_changed("first_name", first_name)
                update_if_changed("middle_name", middle_names)
                update_if_changed("last_name", last_name)
                update_if_changed("date_of_birth", user_data.get("DOB"))
                update_if_changed("gender", user_data.get("gender"))
                update_if_changed("mob_number", user_data.get("phoneNumber"))
                update_if_changed("perm_add_village", user_data.get("currentAddress"))
                update_if_changed("perm_add_gewog", user_data.get("gewog"))
                update_if_changed("perm_add_dzongkhag", user_data.get("dzongkhag"))
                update_if_changed("ps_add_village", user_data.get("currentAddress"))
                update_if_changed("ps_add_gewog", user_data.get("gewog"))
                update_if_changed("ps_add_dzongkhag", user_data.get("dzongkhag"))
                update_if_changed("active_agency", agency)

                if update_fields:
                    existing_user.save(update_fields=update_fields)

            else:
                is_new_user = True

                new_username = user_data.get("username")
                new_email = user_data.get("email")
                if (
                    new_username
                    and CustomUser.objects.filter(username=new_username).exists()
                ):
                    return Response(
                        {"error": f"Username '{new_username}' already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if new_email and CustomUser.objects.filter(email=new_email).exists():
                    return Response(
                        {"error": f"Email '{new_email}' already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user = CustomUser.objects.create_user(
                    username=new_username,
                    email=new_email,
                    identity_number=cid,
                    first_name=first_name,
                    middle_name=middle_names,
                    last_name=last_name,
                    date_of_birth=user_data.get("DOB"),
                    gender=user_data.get("gender"),
                    mob_number=user_data.get("phoneNumber"),
                    perm_add_village=user_data.get("currentAddress"),
                    perm_add_gewog=user_data.get("gewog"),
                    perm_add_dzongkhag=user_data.get("dzongkhag"),
                    nationality="Bhutanese",
                    ps_add_village=user_data.get("currentAddress"),
                    ps_add_gewog=user_data.get("gewog"),
                    ps_add_dzongkhag=user_data.get("dzongkhag"),
                    role="general_public",
                    active_agency=agency,
                    registration_method="event_registration",
                )
                user_to_process = user

            ua_defaults = {
                "user_code": user_agency_data.get("user_code"),
                "user_role_agency": user_agency_data.get("user_role_agency"),
            }
            ua_defaults = {k: v for k, v in ua_defaults.items() if v is not None}

            user_agency, ua_created = UserAgency.objects.update_or_create(
                user=user_to_process, agency=agency, defaults=ua_defaults
            )

            event_screening.users.add(user_to_process)

            status_code = status.HTTP_201_CREATED if is_new_user else status.HTTP_200_OK
            message = (
                "Counselor event user registered successfully."
                if is_new_user
                else "Counselor event user updated successfully."
            )
            response_data = {"userId": user_to_process.id, "message": message}
            return Response(response_data, status=status_code)

    except IntegrityError as ie:
        if "username" in str(ie).lower():
            return Response(
                {
                    "error": "Username conflict occurred. The provided username might already be in use."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "email" in str(ie).lower():
            return Response(
                {
                    "error": "Email conflict occurred. The provided email might already be in use."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "unique_identity_number" in str(ie).lower():
            return Response(
                {
                    "error": "CID conflict occurred. This should have been caught earlier."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"error": "Database error: An integrity constraint was violated."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred during registration."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def get_gyalsung_user_data_using_cid(request):
    identity_number = request.data.get("cid")
    if not identity_number:
        return Response(
            {"error": "CID (Identity Number) is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    cid_api_data, status_code = process_cid_gyalsung_user_data(identity_number)
    return Response(cid_api_data, status=status_code)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_gyalsung_user_using_cid(request):
    from gyalsung.serializers import GyalsungCounselorUserSerializer

    identity_number = request.data.get("cid")
    if not identity_number:
        return Response(
            {"error": "CID (Identity Number) is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    existing_user = CustomUser.objects.filter(identity_number=identity_number).first()
    newely_created_user = False
    if not existing_user:
        current_useragency = UserAgency.objects.filter(user=request.user)
        if current_useragency:
            user_data = process_cid_data_for_user_creation_using_gyalsung(
                identity_number, current_useragency.agency
            )
        else:
            user_data = process_cid_data_for_user_creation_using_gyalsung(
                identity_number, None
            )

        email = f"{user_data['first_name']}{user_data.get('last_name', '_')}@gmail.com"
        password = f"{user_data['first_name']}@2025#"

        user_data["username"] = identity_number
        user_data["email"] = email
        user_data["password"] = password
        user_data["identity_number"] = identity_number

        final_gyalsung_user_data = (
            merged_gyalsung_api_and_cid_api_data_for_user_creation(
                request.data, user_data
            )
        )
        user_id = create_user_and_agency_from_raw_data_for_gyalsung(
            final_gyalsung_user_data
        )
        newely_created_user = True
        existing_user = CustomUser.objects.get(id=user_id)

    gyalsung_user_screen_history = GyalsungUserScreeningHistory.objects.create(
        user=existing_user
    )

    # now populate details to the new gyalsung db
    if not newely_created_user:
        # update new gyalsung field data only
        existing_user.is_gyalsung = True
        existing_user.gyalsung_status = "registered"
        existing_user.guard_mob_number = request.data.get("guard_contact_number")
        existing_user.hospital_name = request.data.get("hospital_name")
        existing_user.hospital_dzongkhag = request.data.get("hospital_dzongkhag")
        existing_user.appointment_date = convert_date_format(
            request.data.get("appointment_date")
        )
        existing_user.academy_name = request.data.get("academy")
        existing_user.personal_number = request.data.get("personal_number")
        existing_user.save()

        event_submission_qs = EventBasedSubmission.objects.filter(
            user_id=existing_user.id
        )
        gyalsung_user_screen_history.event_submission.add(*event_submission_qs)
        case_submission_qs = CaseBasedSubmission.objects.filter(
            user_id=existing_user.id
        )
        gyalsung_user_screen_history.event_submission.add(*case_submission_qs)

    response_data = {
        "user_id": existing_user.id,
        "user_data": GyalsungCounselorUserSerializer(existing_user).data,
        "message": "User registered successfully.",
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        user_data = request.data.get("user", {})
        agency_data = request.data.get("agency", {})

        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        agency_serializer = AgencySerializer(data=agency_data)
        if agency_serializer.is_valid():
            agency_serializer.save(user=user)
        else:
            user.delete()
            return Response(
                agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        headers = self.get_success_headers(user_serializer.data)
        return Response(
            user_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserUpdate(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        user_serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        user_serializer.is_valid(raise_exception=True)
        self.perform_update(user_serializer)

        agency_data = request.data.get("agency", {})
        if instance.agency:
            agency_serializer = AgencySerializer(
                instance.agency, data=agency_data, partial=partial
            )
            if agency_serializer.is_valid():
                agency_serializer.save()
            else:
                return Response(
                    agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(user_serializer.data)


class UserList(ListAPIView):
    permission_classes = [permissions.AllowAny]
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
            "user_details": user_serializer.data,
            "agency_details": agency_serializer.data,
            "user_agency_details": user_agency_serializer.data,
        }

        return Response(response_data)


class UpdateGyalsungDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Log authentication status
        if request.user.is_authenticated:
            logger.info(f"User {request.user} is authenticated")
        else:
            logger.info("User is not authenticated")

        identity_number = request.data.get("identity_number", None)
        academy_code = request.data.get("academy_code", None)

        if not identity_number or not academy_code:
            logger.error("Identity number and academy code are required")
            return Response(
                {"error": "Identity number and academy code are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(identity_number=identity_number)
        except CustomUser.DoesNotExist:
            logger.error("User not found")
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if retrieved user is of role student or public
        if user.role not in [CustomUser.ROLE_STUDENT, CustomUser.ROLE_PUBLIC]:
            logger.error("Retrieved user is not a student or public user")
            return Response(
                {"error": "Retrieved user is not a student or public user"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Update is_gyalsung field
        is_gyalsung = request.data.get("is_gyalsung", None)
        if is_gyalsung is not None:
            user.is_gyalsung = is_gyalsung

        # Update academy_code field
        user.academy_code = academy_code

        # Update active_agency field
        try:
            active_agency = Agency.objects.get(agency_code=academy_code)
            user.active_agency = active_agency
        except Agency.DoesNotExist:
            logger.error("Agency not found")
            return Response(
                {"error": "Agency not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.save()

        logger.info("User details updated successfully")
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)

                user_role = user.role

                user_id = user.id

                return Response(
                    {"token": token.key, "user_role": user_role, "user_id": user_id},
                    status=status.HTTP_200_OK,
                )
            else:
                if CustomUser.objects.filter(username=username).exists():
                    logger.warning(
                        "Authentication failed for username: %s - Wrong password",
                        username,
                    )
                    return Response(
                        {"error": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            logger.error("Exception during login: %s", str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Agency):
            return {
                "id": obj.id,
                "agency_code": obj.agency_code,
                "agency_name": obj.agency_name,
            }
        return super().default(obj)


class GetUserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            logger.info("User details request received")

            user = request.user

            user_data = {
                "id": user.id,
                "username": user.username,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
                "identity_number": user.identity_number,
                "nationality": user.nationality,
                "first_name": user.first_name,
                "middle_name": user.middle_name or "",
                "last_name": user.last_name,
                "date_of_birth": (
                    user.date_of_birth.isoformat() if user.date_of_birth else None
                ),
                "gender": user.gender,
                "email": user.email,
                "mob_number": user.mob_number,
                "father_name": user.father_name,
                "mother_name": user.mother_name,
                "perm_add_village": user.perm_add_village,
                "perm_add_gewog": user.perm_add_gewog,
                "perm_add_dzongkhag": user.perm_add_dzongkhag,
                "ps_add_village": user.ps_add_village,
                "ps_add_gewog": user.ps_add_gewog,
                "ps_add_dzongkhag": user.ps_add_dzongkhag,
                "profile_picture": (
                    user.profile_picture.url if user.profile_picture else None
                ),
                "is_gyalsung": user.is_gyalsung,
                "academy_code": user.academy_code,
                "date_joined": (
                    user.date_joined.isoformat() if user.date_joined else None
                ),
                "role": user.role,
                "access_level": user.access_level,
            }

            agency_data = {}
            if user.active_agency:
                agency_data = {
                    "id": user.active_agency.id,
                    "agency_code": user.active_agency.agency_code,
                    "agency_name": user.active_agency.agency_name,
                    "agency_parent": user.active_agency.agency_parent,
                    "present_dzongkhag": user.active_agency.present_dzongkhag,
                    "present_gewog": user.active_agency.present_gewog,
                    "present_village": user.active_agency.present_village,
                }

            user_agency_data = {}
            user_agency = UserAgency.objects.filter(user=user).first()
            if user_agency:
                user_agency_data = (
                    {
                        "user_code": user_agency.user_code,
                        "parent_occupation": user_agency.parent_occupation,
                        "guardian_name": user_agency.guardian_name,
                        "guardian_occupation": user_agency.guardian_occupation,
                        "parent_status": user_agency.parent_status,
                        "current_living_with": user_agency.current_living_with,
                        "user_role_agency": user_agency.user_role_agency,
                        "user_class": user_agency.user_class,
                        "user_stream": user_agency.user_stream,
                        "user_sub_class": user_agency.user_sub_class,
                    },
                )

            response_data = {
                "user": user_data,
                "agency": agency_data,
                "userAgency": user_agency_data,
            }

            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return JsonResponse(
                {"error": "An error occurred while fetching user details."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            new_password = self.generate_random_password()
            user.set_password(new_password)
            user.save()

            # Create EmailMessage instance instead of using send_mail
            email_message = EmailMessage(
                subject="[PEMA System] Your New One-Time Password",
                body=(
                    f"Dear User,\n\n"
                    f"A request to reset your password has been completed. Please use the following one-time password to access your account:\n"
                    f"Password: {new_password}\n\n"
                    f"For security reasons, we highly recommend you to login with this new password and change your password from settings/profile page immediately.\n\n"
                    f"Warm regards,\n\n"
                    f"The PEMA System\n"
                    f"PEMA Secretariat, Thimphu\n"
                    f"Email: support@thepemasystem.gov.bt\n"
                    f"Phone: +975-2-332862\n"
                ),
                from_email="PEMA System <noreply@thepemasystem.gov.bt>",
                to=[email],
            )

            # Set additional headers if needed
            email_message.extra_headers = {
                "From": "PEMA System <noreply@thepemasystem.gov.bt>",
                "Reply-To": "support@thepemasystem.gov.bt",
            }

            email_message.send(fail_silently=False)

            return Response(
                {
                    "message": "A new temporary password has been sent to your provided email address. Please check your inbox or junk mail to login to your account with the new teamporary password."
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token, *args, **kwargs):
        password = request.data.get("password")
        User = get_user_model()
        try:
            user_email = request.data.get("email")
            user = User.objects.get(email=user_email)

            if user and default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response(
                    {"message": "Password has been reset successfully."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid token or email."}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email."}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def verify_pre_recorded_user(request):
    cid = request.GET.get("cid")

    try:
        logger.info(f"Attempting to verify pre-recorded user with CID: {cid}")

        user = PreRecordedUser.objects.get(identity_number=cid)

        logger.info(f"Pre-recorded user found for CID: {cid}")

        if user.is_registered:
            logger.info("Pre-recorded user is already registered.")
            return JsonResponse(
                {
                    "success": False,
                    "message": "Pre-recorded user is already registered.",
                },
                status=400,
            )

        user_data = {
            "id": user.id,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "identity_number": user.identity_number,
            "nationality": user.nationality,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "date_of_birth": user.date_of_birth,
            "gender": user.gender,
            "email": user.email,
            "mob_number": user.mob_number,
            "father_name": user.father_name,
            "mother_name": user.mother_name,
            "perm_add_village": user.perm_add_village,
            "perm_add_gewog": user.perm_add_gewog,
            "perm_add_dzongkhag": user.perm_add_dzongkhag,
            "profile_picture": (
                user.profile_picture.url if user.profile_picture else None
            ),
            "active_agency": None,  # No active agency for pre-recorded user
            "is_gyalsung": user.is_gyalsung,
            "academy_code": user.academy_code,
            "date_joined": user.date_joined,
            "role": user.role,
            "access_level": user.access_level,
        }

        agency_data = {"agency_name": user.agency_name, "agency_code": user.agency_code}

        user_agency_data = {
            "user_code": user.user_code,
            "parent_occupation": user.parent_occupation,
            "guardian_name": user.guardian_name,
            "guardian_occupation": user.guardian_occupation,
            "parent_status": user.parent_status,
            "current_living_with": user.current_living_with,
            "user_role_agency": user.user_role_agency,
            "user_class": user.user_class,
            "user_sub_class": user.user_sub_class,
        }

        logger.info("Returning pre-recorded user data")
        return Response(
            {
                "success": True,
                "message": "User verification successful.",
                "user": user_data,
                "agency": agency_data,
                "userAgency": user_agency_data,
            },
            status=status.HTTP_200_OK,
        )

    except PreRecordedUser.DoesNotExist:
        logger.error(f"Pre-recorded user not found for CID: {cid}")
        return JsonResponse(
            {"success": False, "message": "Pre-recorded user not found."}, status=404
        )
    except Exception as e:
        logger.exception(f"Error in verify_pre_recorded_user: {str(e)}")
        traceback.print_exc()
        return JsonResponse(
            {"success": False, "message": "Internal Server Error"}, status=500
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def register_pre_recorded_user(request):
    try:
        user_data = request.data.get("userData", {})
        agency_data = request.data.get("agencyData", {})
        user_agency_data = request.data.get("userAgencyData", {})

        with transaction.atomic():
            # Check if the agency exists, if not, create it
            agency_code = agency_data.get("agency_code")
            agency, created = Agency.objects.get_or_create(
                agency_code=agency_code,
                defaults={"agency_name": agency_data.get("agency_name")},
            )

            # Create the user
            user = CustomUser.objects.create_user(
                username=user_data.get("username"),
                email=user_data.get("email"),
                identity_number=user_data.get("identity_number"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                date_of_birth=user_data.get("date_of_birth"),
                gender=user_data.get("gender"),
                mob_number=user_data.get("mob_number"),
                perm_add_village=user_data.get("perm_add_village"),
                perm_add_gewog=user_data.get("perm_add_gewog"),
                perm_add_dzongkhag=user_data.get("perm_add_dzongkhag"),
                password=user_data.get("password"),
                role=user_data.get("role"),
                active_agency=agency,  # <-- This is the line you need to add
            )

            # Create or update UserAgency link
            # You are already correctly setting the user and agency here
            UserAgency.objects.create(
                user=user,
                agency=agency,
                user_code=user_agency_data.get("user_code"),
                parent_occupation=user_agency_data.get("parent_occupation"),
                guardian_name=user_agency_data.get("guardian_name"),
                guardian_occupation=user_agency_data.get("guardian_occupation"),
                parent_status=user_agency_data.get("parent_status"),
                current_living_with=user_agency_data.get("current_living_with"),
                user_role_agency=user_agency_data.get("user_role_agency"),
                user_class=user_agency_data.get("user_class"),
                user_sub_class=user_agency_data.get("user_sub_class"),
            )

            # Update the PreRecordedUser model
            pre_recorded_user_identity_number = user_data.get("identity_number")
            PreRecordedUser.objects.filter(
                identity_number=pre_recorded_user_identity_number
            ).update(is_registered=True)

            response_data = {
                "userId": user.id,
                "message": "Pre-recorded user registered successfully.",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        traceback.print_exc()
        response_data = {"error": "Error registering user"}
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def user_logout(request):
    response = JsonResponse({"message": "Logout successful"})
    response.delete_cookie("sessionid")
    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    try:
        user = request.user

        user_data = request.data.get("user", {})
        user_agency_data = request.data.get("userAgency", {})

        user_fields = [
            "first_name",
            "last_name",
            "email",
            "mob_number",
            "father_name",
            "mother_name",
            "perm_add_village",
            "perm_add_gewog",
            "perm_add_dzongkhag",
        ]

        for field in user_fields:
            new_value = user_data.get(field)
            if new_value is not None:
                setattr(user, field, new_value)

        user.save()

        user_agency = getattr(user, "agency_details", None)
        if user_agency:
            user_agency_fields = [
                "parent_occupation",
                "parent_status",
                "guardian_name",
                "guardian_occupation",
                "current_living_with",
            ]
            for field in user_agency_fields:
                new_value = user_agency_data.get(field)
                if new_value is not None:
                    setattr(user_agency, field, new_value)

            user_agency.save()

        return Response(
            {"message": "User details updated successfully"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"message": "Failed to update user details. Please try again."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@csrf_exempt
def change_password(request):
    User = get_user_model()

    # Retrieve user ID from authentication token
    user_id = request.user.id

    # Retrieve current password, new password, and confirm new password from request data
    current_password = request.data.get("current_password")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    # Check if new password matches the confirmation
    if new_password != confirm_password:
        return Response(
            {"error": "New password and confirm password do not match."}, status=400
        )

    # Retrieve the user object
    user = User.objects.get(pk=user_id)

    # Check if the current password provided matches the user's current password
    if not user.check_password(current_password):
        return Response({"error": "Current password is incorrect."}, status=400)

    # Set the user's new password
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password changed successfully."}, status=200)


@csrf_exempt
def get_referral_counselors(request):
    if request.method == "GET":
        # Get the role and active agency name from the request parameters
        role = request.GET.get("role")
        active_agency_name = request.GET.get("active_agency")

        # Query users based on the role only
        users = CustomUser.objects.filter(role=role)

        # Create a list of users with their full name and active agency if available
        users_list = []
        for user in users:
            # Check if the middle name is None and replace it with an empty string
            middle_name = user.middle_name if user.middle_name else ""

            if user.active_agency:
                users_list.append(
                    {
                        "id": user.id,
                        "full_name": f"{user.first_name} {middle_name} {user.last_name}",
                        "active_agency": user.active_agency.agency_name,
                    }
                )
            else:
                users_list.append(
                    {
                        "id": user.id,
                        "full_name": f"{user.first_name} {middle_name} {user.last_name}",
                        "active_agency": "",
                    }
                )

        # Return the list of users as JSON response
        return JsonResponse({"data": users_list})

    else:
        return JsonResponse({"error": "Only GET requests are allowed"})


class LoginGyalsung(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            app_key_encoded = request.data.get("app_key")
            app_secret_encoded = request.data.get("app_secret")

            # Decoding base64 encoded app_key and app_secret
            app_key_decoded = base64.b64decode(app_key_encoded).decode("utf-8")
            app_secret_decoded = base64.b64decode(app_secret_encoded).decode("utf-8")

            logger.info("Login request received - Username: %s", app_key_decoded)

            # Check if the decoded app_key and app_secret match the predefined values
            if (
                app_key_decoded == "TheGyalsung"
                and app_secret_decoded == "Gyalsung4Hwss@2024"
            ):
                # Assuming CustomUser is your custom user model
                user = authenticate(
                    username=app_key_decoded, password=app_secret_decoded
                )

                if user is not None:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"token": token.key}, status=status.HTTP_200_OK)
                else:
                    logger.warning(
                        "Authentication failed for username: %s", app_key_decoded
                    )
                    return Response(
                        {"error": "Invalid credentials"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                logger.warning("Invalid app_key or app_secret provided")
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error("Exception during login: %s", str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def check_email_cid(request):
    email = request.data.get("email")
    cid = request.data.get("cid")

    # Validate input
    if not email or not cid:
        return JsonResponse({"error": "Email and CID are required."}, status=400)

    # Check if email or CID exists
    user_exists = CustomUser.objects.filter(
        Q(email=email) | Q(identity_number=cid)
    ).exists()

    if user_exists:
        return JsonResponse(
            {"exists": True, "message": "Email or CID already exists."}, status=200
        )
    else:
        return JsonResponse(
            {"exists": False, "message": "Email and CID are available."}, status=200
        )
