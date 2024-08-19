#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback
import json

## Authentication to Trakt (step 1): generate device code
def generate_trakt_device_code(client_id: str) -> dict:
    # Initialise response
    trakt_device_code_info = None
    try:
        # Build the URL for API call
        trakt_api_url = 'https://api.trakt.tv'
        auth_get_token_url = trakt_api_url + '/oauth/device/code'
        # Perform the call for authentication
        trakt_authentication_response = requests.post(auth_get_token_url, headers={'Content-Type': 'application/json'}, data=json.dumps({'client_id': str(client_id)}))
        # Get the content
        trakt_device_code_info = trakt_authentication_response.json()
        device_code = trakt_device_code_info.get('device_code')
        print('Device code: %s' %device_code)
        verification_url = trakt_device_code_info.get('verification_url')
        verification_code = trakt_device_code_info.get('user_code')
        # Display message to the user
        print('Go to the webpage %s and enter the verification code: %s'  %(verification_url, verification_code) )
    except:
        traceback.print_exc()
    # Return
    return trakt_device_code_info
