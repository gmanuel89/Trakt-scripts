## Import libraries
import requests
import traceback
import json
from session_manager.APIClient import APIClient

## Get the history of the user (Access Token required only if the user is private)
def get_watch_history_for_user(api_client: APIClient, user_id: str, content_type='episodes', time_interval=None) -> list[dict]:
    """Get the history of the user (Access Token required only if the user is private)"""
    # Initialise output
    user_watch_history = []
    # Fix types
    if content_type is None or (content_type != 'movies' and content_type != 'episodes' and content_type != 'seasons' and content_type != 'shows'):
        content_type_api_string = ''
    else:
        content_type_api_string = '/' + str(content_type) + '/'
    # Fix time interval
    if time_interval is not None:
        time_interval_api_string = f'&start_at={time_interval[0]}&end_at={time_interval[1]}'
    else:
        time_interval_api_string = ''
    # Fetch history (in pages) from Trakt
    try:
        page_number = 1
        pageLimit = 1000
        while True:
            trakt_api_url = f'users/{user_id}/history{content_type_api_string}?page={page_number}&limit={pageLimit}{time_interval_api_string}'
            history_response = api_client.get(trakt_api_url)
            if history_response.ok:
                user_watch_history.extend(history_response.json())
                if int(history_response.headers.get('X-Pagination-Page-Count')) != page_number:
                    page_number = page_number + 1
                else:
                    break
            else:
                break
    except:
        traceback.print_exc()
    # Return
    return user_watch_history

## Get the history of the user (Access Token required only if the user is private)
def get_watchlist_for_user(api_client: APIClient, user_id: str, content_type='episodes', sort_by='title', sort_how='asc') -> list[dict]:
    """Get the history of the user (Access Token required only if the user is private)"""
    # Initialise output
    user_watchlist = []
    # Fix types
    if content_type is None or (content_type != 'movies' and content_type != 'episodes' and content_type != 'seasons' and content_type != 'shows'):
        content_type_api_string = ''
        sorting_api_string = ''
    else:
        content_type_api_string = '/' + str(content_type)
        # Fix sort by and sort how (it works only if content type is provided)
        if sort_by is not None or sort_how is not None:
            sorting_api_string = '/sort/'
        else:
            sorting_api_string = ''
    try:
        # Pass sort by (it works only if content type is provided)
        if content_type is not None and (content_type == 'movies' or content_type == 'episodes' or content_type == 'seasons' or content_type == 'shows'):
            if sort_by is not None:
                api_client.session.headers.update({'X-Sort-By' : sort_by})
            if sort_how is not None:
                api_client.session.headers.update({'X-Sort-How' : sort_how})
        # Fetch watchlist (in pages) from Trakt
        page_number = 1
        page_limit = 1000
        while True:
            trakt_api_url = f'users/{user_id}/watchlist{content_type_api_string}{sorting_api_string}?page={page_number}&limit={page_limit}'
            watchlist_response = api_client.get(trakt_api_url)
            if watchlist_response.ok:
                user_watchlist.extend(watchlist_response.json())
                if int(watchlist_response.headers.get('X-Pagination-Page-Count')) != 0 and int(watchlist_response.headers.get('X-Pagination-Page-Count')) != page_number:
                    page_number = page_number + 1
                else:
                    break
            else:
                break
    except:
        traceback.print_exc()
    # Return
    return user_watchlist

## Check in to a Trakt title
def checkin_to_trakt(api_client: APIClient, show_title: str, show_year: int, show_trakt_id: str, season_number: int, episode_number: int, watched_at: str) -> requests.Response | None:
    """Check in to a Trakt title"""
    # Initialise output
    check_in_response = None
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
        check_in_response = api_client.post('checkin', data=json.dumps(payload_for_post_request))
        print('Payload:\n%s' %payload_for_post_request)
    except:
        traceback.print_exc()
    # Return
    return check_in_response
