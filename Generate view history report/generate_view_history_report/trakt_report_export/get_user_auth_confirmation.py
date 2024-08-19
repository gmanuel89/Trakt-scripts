#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback
import time
import json

## Authentication to Trakt (step 2): confirm user authentication
def get_user_auth_confirmation(device_code: str, client_id: str, client_secret: str, seconds_to_wait_between_calls=10) -> dict:
    # Initialise response
    trakt_access_token = None
    try:
        # Keep waiting for user response
        print('Waiting for user authorization confirmation...')
        while True:
            # Build the URL for API call
            trakt_api_url = 'https://api.trakt.tv'
            auth_get_token_url = trakt_api_url + '/oauth/device/token'
            # Payload for POST call
            payload_for_post_call = {
                'code': device_code,
                'client_id': client_id,
                'client_secret' : client_secret
            }
            # Perform the call for authentication
            trakt_authentication_response = requests.post(auth_get_token_url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload_for_post_call))
            # Handle cases based on the response
            if trakt_authentication_response.ok:
                trakt_access_token = trakt_authentication_response.json().get('access_token')
                print('Access granted!\nToken: %s' %trakt_access_token)
                print('The token is valid for 3 months, write it down and use it for future authentication')
                print('by placing it in the "accessToken" field in the parameters.json file')
                break
            else:
                if trakt_authentication_response.status_code == 400:
                    print('Authorization still pending... Waiting for %s seconds...' %seconds_to_wait_between_calls)
                    time.sleep(seconds_to_wait_between_calls)
                    continue
                elif trakt_authentication_response.status_code == 404:
                    print('Invalid device code! Repeat the whole authentication process!')
                    break
                elif trakt_authentication_response.status_code == 409:
                    print('The device code has been already approved')
                    break
                elif trakt_authentication_response.status_code == 410:
                    print('Device code expired! Repeat the whole authentication process!')
                    break
                elif trakt_authentication_response.status_code == 418:
                    print('Device code refused! Repeat the whole authentication process!')
                    break
                elif trakt_authentication_response.status_code == 429:
                    print('Too many API calls... Waiting for %s seconds...' %seconds_to_wait_between_calls * 2)
                    time.sleep(seconds_to_wait_between_calls * 2)      
    except:
        traceback.print_exc()
    # Return
    return trakt_access_token
