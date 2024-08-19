#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback
import json

## Check in to a Trakt title
def checkin_to_trakt(show_title: str, show_year: int, show_trakt_id: str, season_number: int, episode_number: int, watched_at: str, client_id: str, access_token: str) -> requests.Response | None:
    # Initialise output
    check_in_response = None
    # Headers
    headers_for_api_call = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': client_id,
        'Authorization': 'Bearer ' + access_token
    }
    # Payload
    payload_for_post_request = {
        'show': {
          'title': show_title,
          'year': show_year,
          'ids': {
            'trakt': show_trakt_id
          }
        },
        'sharing': {
          'twitter': False,
          'mastodon': False,
          'tumblr': False
        }
    }
    # Season and episode
    if season_number is not None and season_number != 0:
        if 'episode' not in payload_for_post_request: payload_for_post_request['episode'] = {}
        payload_for_post_request['episode']['season'] = season_number
    if episode_number is not None and episode_number != 0:
        if 'episode' not in payload_for_post_request: payload_for_post_request['episode'] = {}
        payload_for_post_request['episode']['number'] = episode_number
    # Watched at
    if watched_at is not None and watched_at != '':
        payload_for_post_request['watched_at'] = watched_at
    # API call
    try:
        check_in_response = requests.post('https://api.trakt.tv/checkin', headers=headers_for_api_call, data=json.dumps(payload_for_post_request))
        print('Payload:\n%s' %payload_for_post_request)
    except:
        traceback.print_exc()
    # Return
    return check_in_response
