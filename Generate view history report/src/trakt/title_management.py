## Import libraries
import requests
import traceback
from session_manager.APIClient import APIClient

## Get title aliases
def get_title_aliases(api_client: APIClient, title_trakt_id: str, title_type: str) -> dict:
    """Get title aliases"""
    # Initialise output
    title_alias_info = {}
    # Get info from Trakt
    try:
        if title_type == 'show' or title_type == 'episode':
            title_type_string = 'shows'
        else:
            title_type_string = 'movies'
        title_alias_info_from_trakt = api_client.get(f'{title_type_string}/{title_trakt_id}/aliases')
        title_alias_info = title_alias_info_from_trakt.json()
    except:
        traceback.print_exc()
    # Return
    return title_alias_info

## Get title information
def get_title_information(api_client: APIClient, title_trakt_id: str, full_info=True) -> dict:
    """Get title information"""
    # Initialise output
    title_information = {}
    # Get info from Trakt
    try:
        if full_info:
            full_info_api_url_suffix = '?extended=full'
        else:
            full_info_api_url_suffix = ''
        title_info_from_trakt = api_client.get(f'shows/{title_trakt_id}{full_info_api_url_suffix}')
        title_information = title_info_from_trakt.json()
    except:
        print('Error in decoding response: title not found!')
        traceback.print_exc()
    # Return
    return title_information

## Get title seasons
def get_title_seasons(api_client: APIClient, title_trakt_id: str, include_episodes=True) -> list[dict]:
    """Get title seasons"""
    # Initialise output
    title_seasons = []
    # Define if to include episodes in the response
    if include_episodes:
        api_url_string = '?extended=episodes'
    else:
        api_url_string = ''
    # Get info from Trakt
    try:
        title_info_from_trakt = api_client.get(f'/shows/{title_trakt_id}/seasons{api_url_string}')
        title_seasons = title_info_from_trakt.json()
    except:
        traceback.print_exc()
    # Return
    return title_seasons
