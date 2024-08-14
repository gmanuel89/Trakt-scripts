## Import libraries
import json
import requests
import traceback
import time
import csv

# Read configuration file
configuration_file_path = 'parameters.json'
configuration = json.loads(open(configuration_file_path).read())
client_id = configuration.get('trakt').get('clientId')
client_secret = configuration.get('trakt').get('clientSecret')
access_token = configuration.get('trakt').get('accessToken')
trakt_username = configuration.get('trakt').get('username')
report_csv_file_name = configuration.get('data').get('outputCsvReportFileName')


######### FUNCTIONS
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

## Check the validity of the access token (by performing a random API call and seeing the response)
def check_trakt_access_token_validity(access_token: str, client_id: str, trakt_username: str) -> bool:
    # Initialise
    token_is_valid = False
    # Verify token validity
    try:
        headers_for_api_call = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': str(client_id),
            'Authorization': 'Bearer ' + str(access_token)
        }
        trakt_api_url = 'https://api.trakt.tv/users/' + trakt_username + '/favorites/movies/rank'
        trakt_response = requests.get(trakt_api_url, headers=headers_for_api_call)
        if trakt_response.ok:
            token_is_valid = True
    except:
        traceback.print_exc()
    return token_is_valid

## Get the history of the user (Access Token required only if the user is private)
def get_watch_history_for_user(user_id: str, client_id: str, access_token: str, content_type='episodes', time_interval=None) -> list[dict]:
    # Initialise output
    user_watch_history = []
    # Fix types
    if content_type is None or (content_type != 'movies' and content_type != 'episodes' and content_type != 'seasons' and content_type != 'shows'):
        content_type_api_string = ''
    else:
        content_type_api_string = '/' + str(content_type) + '/'
    # Fix time interval
    if time_interval is not None:
        time_interval_api_string = '&start_at=%s&end_at=%s' %(time_interval[0], time_interval[1])
    else:
        time_interval_api_string = ''
    # Fetch history (in pages) from Trakt
    try:
        headers_for_api_call = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': str(client_id),
            'Authorization': 'Bearer ' + str(access_token)
        }
        pageNumber = 1
        pageLimit = 1000
        while True:
            trakt_api_url = 'https://api.trakt.tv/users/' + str(user_id) + '/history' + content_type_api_string + '?page=' + str(pageNumber) + '&limit=' + str(pageLimit) + time_interval_api_string
            history_response = requests.get(trakt_api_url, headers = headers_for_api_call)
            if history_response.ok:
                user_watch_history.extend(history_response.json())
                if int(history_response.headers.get('X-Pagination-Page-Count')) != pageNumber:
                    pageNumber = pageNumber + 1
                else:
                    break
            else:
                break
    except:
        traceback.print_exc()
    # Return
    return user_watch_history

## Extracted viewed items from history
def extract_viewed_items_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
    # Initialise output
    viewed_items = []
    # For each item in the history
    for hst in user_watch_history:
        title_type = hst.get('type')
        if title_type == 'show' or title_type == 'episode':
            title_name = hst.get('show').get('title')
            title_year = hst.get('show').get('year')
            title_trakt_id = hst.get('show').get('ids').get('trakt')
            title_imdb_id = hst.get('show').get('ids').get('imdb')
        elif title_type == 'movie':
            title_name = hst.get('movie').get('title')
            title_year = hst.get('movie').get('year')
            title_trakt_id = hst.get('movie').get('ids').get('trakt')
            title_imdb_id = hst.get('movie').get('ids').get('imdb')
        # Build the summarized info for title
        title_info = {
            'title': title_name,
            'year': title_year,
            'type': title_type,
            'traktId': title_trakt_id,
            'imdbId': title_imdb_id
        }
        # Check against the curated list that is being created
        if len(viewed_items) == 0:
            viewed_items.append(title_info)
        else:
            if title_info in viewed_items:
                continue
            else:
                viewed_items.append(title_info)
    # Return
    return viewed_items

##### SCRIPT EXECUTION
# Test if the provided token is valid
access_token_validity = check_trakt_access_token_validity(access_token, client_id, trakt_username)
if access_token_validity:
    print('The provided access token is valid!')
else:
    print('The provided access token is not valid, generating a new one...')
    # Generate a new Access Token
    trakt_device_code = generate_trakt_device_code(client_id)
    if trakt_device_code is not None:
        trakt_device_code_confirmation = get_user_auth_confirmation(trakt_device_code.get('device_code'), client_id, client_secret)
# Get user's history
user_watch_history = get_watch_history_for_user(trakt_username, client_id, access_token, None, None)
# Extract the viewed items from the history
viewed_items = extract_viewed_items_from_watch_history(user_watch_history)
# Print report
with open (report_csv_file_name, 'w+', encoding='UTF8', newline='') as output_file:
    csv_writer = csv.DictWriter(output_file, fieldnames=viewed_items[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(viewed_items)
