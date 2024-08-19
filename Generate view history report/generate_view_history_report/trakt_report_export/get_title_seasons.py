#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback

## Get title seasons
def get_title_seasons(title_trakt_id: str, client_id: str, include_episodes=True) -> list[dict]:
    # Initialise output
    title_information = {}
    # Headers
    headers_api_call = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id
    }
    # Define if to include episodes in the response
    if include_episodes:
        api_url_string = '?extended=episodes'
    else:
        api_url_string = ''
    # Get info from Trakt
    try:
        title_info_from_trakt = requests.get('https://api.trakt.tv/shows/' + str(title_trakt_id) + '/seasons' + api_url_string, headers=headers_api_call)
        title_information = title_info_from_trakt.json()
    except:
        traceback.print_exc()
    # Return
    return title_information
