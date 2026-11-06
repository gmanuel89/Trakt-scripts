## Import libraries
import traceback
import json
import time
import hashlib
import base64
import os
import logging
from session_manager.APIClient import APIClient

## Initialise logger
app_logger = logging.getLogger(__name__)

## Authentication to Trakt
def authenticate_to_trakt(api_client: APIClient, client_id: str, redirect_uri=None) -> dict | None:
    """Authentication to Trakt using Authorization Code flow with PKCE."""
    # Initialise response
    headers_for_api_calls = None
    # Fix default redirect URI
    if redirect_uri is None:
        redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    try:
        # --- PKCE: Generate verifier and challenge ---
        code_verifier, code_challenge = generate_pkce_pair()
        # Guidance to user
        app_logger.info('Authenticating to Trakt...')
        app_logger.info('Open the link in a browser and paste the PIN')
        auth_url = (
            f'https://trakt.tv/oauth/authorize'
            f'?response_type=code'
            f'&client_id={client_id}'
            f'&redirect_uri={redirect_uri}'
            f'&code_challenge={code_challenge}'
            f'&code_challenge_method=S256'
        )
        app_logger.info(auth_url)
        # Input the PIN
        auth_pin = str(input('PIN: '))
        # Authenticate to Trakt
        request_headers = {
        'Accept': 'application/json',
        'User-Agent': 'Betaseries to Trakt',
        'Connection': 'Keep-Alive',
        }
        auth_payload_data = {
            'code': auth_pin,
            'client_id': client_id,
            'code_verifier': code_verifier,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        # Perform the call for authentication
        trakt_authentication_response = api_client.post('/oauth/token', additional_headers=request_headers, data=auth_payload_data)
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
        app_logger.debug(traceback.format_exc())
    # Return
    return headers_for_api_calls

## Check the validity of the access token (by performing a random API call and seeing the response)
def check_trakt_access_token_validity(api_client: APIClient, trakt_username: str) -> bool:
    """Check the validity of the access token (by performing a random API call and seeing the response)"""
    # Initialise
    token_is_valid = False
    # Verify token validity
    try:
        trakt_api_endpoint = f'users/{trakt_username}/favorites/movies/rank'
        trakt_response = api_client.get(trakt_api_endpoint)
        if trakt_response.ok:
            token_is_valid = True
    except:
        app_logger.debug(traceback.format_exc())
    return token_is_valid

##
def generate_pkce_pair() -> tuple[str, str]:
    """Generate a PKCE code_verifier and code_challenge pair."""
    # code_verifier: 43-128 chars, URL-safe random string
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b'=').decode('utf-8')
    # code_challenge: SHA-256 hash of verifier, base64url-encoded
    digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

## Authentication to Trakt (step 1): generate device code
def generate_trakt_device_code(api_client: APIClient, client_id: str) -> dict | None:
    """Authentication to Trakt (step 1): generate device code"""
    # Initialise response
    trakt_device_code_info = None
    try:
        # Strip headers
        api_client.session.headers = {'Content-Type': 'application/json'}
        # Perform the call for authentication
        trakt_authentication_response = api_client.post('/oauth/device/code', json={'client_id': str(client_id)})
        # Get the content
        trakt_device_code_info = trakt_authentication_response.json()
        device_code = trakt_device_code_info.get('device_code')
        app_logger.info('Device code: %s' %device_code)
        verification_url = trakt_device_code_info.get('verification_url')
        verification_code = trakt_device_code_info.get('user_code')
        # Display message to the user
        app_logger.info(f'Go to the webpage {verification_url} and enter the verification code: {verification_code}')
    except:
        app_logger.debug(traceback.format_exc())
    # Return
    return trakt_device_code_info

## Authentication to Trakt (step 2): confirm user authentication
def get_user_auth_confirmation(api_client: APIClient, device_code: str, client_id: str, seconds_to_wait_between_calls=10) -> dict | None:
    """Authentication to Trakt (step 2): confirm user authentication"""
    # Initialise response
    trakt_access_token = None
    try:
        # Strip headers
        api_client.session.headers = {'Content-Type': 'application/json'}
        # Keep waiting for user response
        app_logger.info('Waiting for user authorization confirmation...')
        while True:
            # Payload for POST call
            payload_for_post_call = {
                'code': device_code,
                'client_id': client_id
            }
            # Perform the call for authentication
            trakt_authentication_response = api_client.post('/oauth/device/token', data=json.dumps(payload_for_post_call))
            # Handle cases based on the response
            if trakt_authentication_response.ok:
                trakt_access_token = trakt_authentication_response.json().get('access_token')
                app_logger.info(f'Access granted!\nToken: {trakt_access_token}')
                app_logger.info('The token is valid for 24 hours, write it down and use it for future authentication')
                app_logger.info('by placing it in the "accessToken" field in the parameters.json file')
                break
            else:
                if trakt_authentication_response.status_code == 400:
                    app_logger.warning(f'Authorization still pending... Waiting for {seconds_to_wait_between_calls} seconds...')
                    time.sleep(seconds_to_wait_between_calls)
                    continue
                elif trakt_authentication_response.status_code == 404:
                    app_logger.error('Invalid device code! Repeat the whole authentication process!')
                    break
                elif trakt_authentication_response.status_code == 409:
                    app_logger.warning('The device code has been already approved')
                    break
                elif trakt_authentication_response.status_code == 410:
                    app_logger.error('Device code expired! Repeat the whole authentication process!')
                    break
                elif trakt_authentication_response.status_code == 418:
                    app_logger.error('Device code refused! Repeat the whole authentication process!')
                    break
                elif trakt_authentication_response.status_code == 429:
                    app_logger.warning(f'Too many API calls... Waiting for {seconds_to_wait_between_calls * 2} seconds...')
                    time.sleep(seconds_to_wait_between_calls * 2)      
    except:
        app_logger.debug(traceback.format_exc())
    # Return
    return trakt_access_token
