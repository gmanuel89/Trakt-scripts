#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback

## Authentication to Trakt
def authenticate_to_trakt(client_id: str, client_secret: str, redirect_uri=None) -> dict:
    # Initialise response
    headers_for_api_calls = None
    # Fix default redirect URI
    if redirect_uri is None: redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    try:
        # Guidance to user
        print('Authenticating to Trakt...')
        print('Open the link in a browser and paste the PIN')
        print('https://trakt.tv/oauth/authorize?response_type=code&client_id=%s&redirect_uri=urn:ietf:wg:oauth:2.0:oob' %client_id)
        print('')
        # Input the PIN
        auth_pin = str(input('PIN: '))
        # Authenticate to Trakt
        trakt_api_url = 'https://api.trakt.tv'
        auth_get_token_url = '%s/oauth/token' % trakt_api_url
        request_headers = {
        'Accept': 'application/json',
        'User-Agent': 'Betaseries to Trakt',
        'Connection': 'Keep-Alive',
        }
        auth_payload_data = {
            'code': auth_pin,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        # Perform the call for authentication
        trakt_authentication_response = requests.post(auth_get_token_url, headers=request_headers, data=auth_payload_data)
        # Get the content
        trakt_authentication_response_content = trakt_authentication_response.json()
        # Return the headers to be used for future authentication
        auth_headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id,
        'Authorization': 'Bearer ' + trakt_authentication_response_content.get('access_token')
        }
        # Build the final headers
        headers_for_api_calls = auth_headers | request_headers
    except:
        traceback.print_exc()
    # Return
    return headers_for_api_calls