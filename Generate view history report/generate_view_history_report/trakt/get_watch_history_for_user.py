#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback

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
