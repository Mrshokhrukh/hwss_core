import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from access.models import CustomUser


def get_data_from_cid_number(cid_number):
    from access.views import generate_token

    token = "Bearer " + generate_token()
    headers = {"Authorization": token}
    api_url = settings.CREDENTIALS["API_URL"]
    response = requests.get(f"{api_url}{cid_number}", headers=headers)
    if response.status_code != status.HTTP_200_OK:
        return Response(
            {"error": "CID (Identity Number) is not valid."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    data = response.json()
    return data["citizenDetailsResponse"]


def process_cid_data_for_user_creation_using_gyalsung(cid_number, agency):
    cid_api_data = get_data_from_cid_number(cid_number)
    return {
        "first_name": cid_api_data.get("firstName"),
        "middle_name": cid_api_data.get("middleName"),
        "last_name": cid_api_data.get("lastName"),
        "date_of_birth": cid_api_data.get("dob"),
        "gender": cid_api_data.get("gender"),
        "mob_number": cid_api_data.get("mobileNumber"),
        "perm_add_village": cid_api_data.get("villageName"),  # permanent address
        "perm_add_gewog": cid_api_data.get("gewogName"),
        "perm_add_dzongkhag": cid_api_data.get("dzongkhagName"),
        "nationality": cid_api_data.get("nationality"),
        "father_name": cid_api_data.get("fatherName"),
        "mother_name": cid_api_data.get("motherName"),
        "ps_add_village": cid_api_data.get("villageName"),  # present address
        "ps_add_gewog": cid_api_data.get("gewogName"),
        "ps_add_dzongkhag": cid_api_data.get("dzongkhagName"),
        "role": "general_public",
        "active_agency": agency,
        "registration_method": "gyalsung_registration",
        "is_gyalsung": True,
        "gyalsung_status": "registered",
    }


def create_user_and_agency_from_raw_data_for_gyalsung(user_data):
    user = CustomUser.objects.create_user(
        username=user_data.get("username"),
        email=user_data.get("email"),
        identity_number=user_data.get("identity_number"),
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
        password=user_data.get("password"),
        role=user_data.get("role"),
        active_agency=user_data.get("active_agency"),
        registration_method=user_data.get("registration_method"),
        is_gyalsung=user_data.get("is_gyalsung"),
        gyalsung_status=user_data.get("gyalsung_status"),
    )
    return user.id
