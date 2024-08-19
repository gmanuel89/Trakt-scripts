#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback

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
