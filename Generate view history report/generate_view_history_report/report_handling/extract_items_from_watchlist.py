#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Extract viewed items from watchlist (in a more organised form)
def extract_items_from_watchlist(user_watchlist: list[dict]) -> list[dict]:
    # Initialise output
    watchlist_items = []
    # For each item in the history
    for wtch in user_watchlist:
        title_type = wtch.get('type')
        if title_type == 'show' or title_type == 'episode':
            title_name = wtch.get('show').get('title')
            title_year = wtch.get('show').get('year')
            title_trakt_id = wtch.get('show').get('ids').get('trakt')
            title_imdb_id = wtch.get('show').get('ids').get('imdb')
            title_listed_at = wtch.get('listed_at')
        elif title_type == 'movie':
            title_name = wtch.get('movie').get('title')
            title_year = wtch.get('movie').get('year')
            title_trakt_id = wtch.get('movie').get('ids').get('trakt')
            title_imdb_id = wtch.get('movie').get('ids').get('imdb')
            title_listed_at = wtch.get('listed_at')
        # Build the summarized info for title
        title_info = {
            'title': title_name,
            'year': title_year,
            'type': title_type,
            'listedAt': title_listed_at,
            'traktId': title_trakt_id,
            'imdbId': title_imdb_id
        }
        # Check against the curated list that is being created
        if len(watchlist_items) == 0:
            watchlist_items.append(title_info)
        else:
            if title_info in watchlist_items:
                continue
            else:
                watchlist_items.append(title_info)
    # Return
    return watchlist_items
