#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import requests
import traceback

## Get the history of the user (Access Token required only if the user is private)
def get_watchlist_for_user(user_id: str, client_id: str, access_token: str, content_type='episodes', sort_by='title', sort_how='asc') -> list[dict]:
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
        headers_for_api_call = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': str(client_id),
            'Authorization': 'Bearer ' + str(access_token)
        }
        # Pass sort by (it works only if content type is provided)
        if content_type is not None and (content_type == 'movies' or content_type == 'episodes' or content_type == 'seasons' or content_type == 'shows'):
            if sort_by is not None:
                headers_for_api_call['X-Sort-By'] = sort_by
            if sort_how is not None:
                headers_for_api_call['X-Sort-How'] = sort_how
        # Fetch watchlist (in pages) from Trakt
        pageNumber = 1
        pageLimit = 1000
        while True:
            trakt_api_url = 'https://api.trakt.tv/users/' + str(user_id) + '/watchlist' + content_type_api_string + sorting_api_string + '?page=' + str(pageNumber) + '&limit=' + str(pageLimit)
            watchlist_response = requests.get(trakt_api_url, headers = headers_for_api_call)
            if watchlist_response.ok:
                user_watchlist.extend(watchlist_response.json())
                if int(watchlist_response.headers.get('X-Pagination-Page-Count')) != pageNumber:
                    pageNumber = pageNumber + 1
                else:
                    break
            else:
                break
    except:
        traceback.print_exc()
    # Return
    return user_watchlist
