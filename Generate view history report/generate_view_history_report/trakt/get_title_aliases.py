#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback

## Get title aliases
def get_title_aliases(title_trakt_id: str, title_type: str, client_id: str) -> dict:
    # Initialise output
    title_alias_info = {}
    # Headers
    headers_api_call = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id
    }
    # Get info from Trakt
    try:
        if title_type == 'show' or title_type == 'episode':
            title_type_string = 'shows'
        else:
            title_type_string = 'movies'
        title_alias_info_from_trakt = requests.get('https://api.trakt.tv/' + title_type_string + '/' + str(title_trakt_id) + '/aliases', headers=headers_api_call)
        title_alias_info = title_alias_info_from_trakt.json()
    except:
        traceback.print_exc()
    # Return
    return title_alias_info
