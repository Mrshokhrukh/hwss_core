import json
from django.conf import settings
from pathlib import Path

# This utility will handle reading and writing the OAuth tokens

GLOBAL_JSON_PATH = Path(settings.BASE_DIR) / 'global.json'

def save_token_to_global_json(access_token, expiry_time):
    with open(GLOBAL_JSON_PATH, 'w') as file:
        json.dump({'accessToken': access_token, 'expiryTime': expiry_time}, file)

def read_token_from_global_json():
    with open(GLOBAL_JSON_PATH, 'r') as file:
        data = json.load(file)
        return data
