# fetchcitizendetails.py
import base64
import json
import logging
import time
from pathlib import Path

import requests
from django.conf import settings

# Configure logging at the beginning of the file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GLOBAL_JSON_PATH = Path(settings.BASE_DIR) / "hwss_core/global.json"


def save_token_to_global_json(access_token, expiry_time):
    with open(GLOBAL_JSON_PATH, "w") as file:
        json.dump({"accessToken": access_token, "expiryTime": expiry_time}, file)


def read_token_from_global_json():
    with open(GLOBAL_JSON_PATH, "r") as file:
        data = json.load(file)
        return data


def get_oauth_token():
    global_data = read_token_from_global_json()
    current_time = int(time.time())

    if global_data.get("expiryTime", 0) <= current_time:
        key_secret = (
            f"{settings.DCRC_CONSUMER_KEY}:{settings.DCRC_CONSUMER_SECRET}".encode(
                "utf-8"
            )
        )
        encoded_key_secret = base64.b64encode(key_secret).decode("utf-8")

        response = requests.post(
            settings.DCRC_TOKEN_URL,
            headers={"Authorization": f"Basic {encoded_key_secret}"},
            data={"grant_type": "client_credentials"},
            verify=False,
        )
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        token_data = response.json()
        save_token_to_global_json(
            token_data["access_token"], current_time + token_data["expires_in"]
        )
        return token_data["access_token"]
    else:
        return global_data["accessToken"]


def get_citizen_details(cid_number):
    token = get_oauth_token()
    request_url = f"{settings.DCRC_API_BASE_URL}/citizendetails/{cid_number}"
    headers = {"Authorization": f"Bearer {token}"}

    logger.info(f"Making request to DCRC API: {request_url}")

    try:
        response = requests.get(request_url, headers=headers, verify=False)
        response.raise_for_status()  # This will raise an error for HTTP error responses
        logger.info("DCRC API response received successfully.")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"An error occurred while fetching details from DCRC API: {e}")
        (
            logger.error(f"Response status code: {e.response.status_code}")
            if e.response
            else None
        )
        logger.error(f"Response content: {e.response.content}") if e.response else None
        raise  # Re-raise the exception to be handled by the caller


def map_citizen_details_to_model(data):
    return {
        "identity_number": data.get("cid", ""),
        "nationality": "Bhutanese" if data.get("cid") else "",
        "first_name": data.get("firstName", ""),
        "middle_name": data.get("middleName", ""),
        "last_name": data.get("lastName", ""),
        "date_of_birth": data.get("dob", ""),
        "gender": data.get("gender", "O"),
        "mob_number": data.get("mobileNumber", ""),
        "perm_add_village": data.get("villageName", ""),
        "perm_add_gewog": data.get("gewogName", ""),
        "perm_add_dzongkhag": data.get("dzongkhagName", ""),
    }
