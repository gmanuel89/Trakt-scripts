#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback

## Get title information
def get_title_information(title_trakt_id: str, client_id: str, full_info=True) -> dict:
    # Initialise output
    title_information = {}
    # Headers
    headers_api_call = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id
    }
    # Get info from Trakt
    try:
        if full_info:
            full_info_api_url_suffix = '?extended=full'
        else:
            full_info_api_url_suffix = ''
        title_info_from_trakt = requests.get('https://api.trakt.tv/shows/' + str(title_trakt_id) + full_info_api_url_suffix, headers=headers_api_call)
        title_information = title_info_from_trakt.json()
    except:
        traceback.print_exc()
    # Return
    return title_information
