#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Extract viewed items from history (in a more organised form)
def extract_viewed_items_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
    # Initialise output
    viewed_items = []
    # For each item in the history
    for hst in user_watch_history:
        title_type = hst.get('type')
        if title_type == 'show' or title_type == 'episode':
            title_name = hst.get('show').get('title')
            title_year = hst.get('show').get('year')
            title_trakt_id = hst.get('show').get('ids').get('trakt')
            title_imdb_id = hst.get('show').get('ids').get('imdb')
        elif title_type == 'movie':
            title_name = hst.get('movie').get('title')
            title_year = hst.get('movie').get('year')
            title_trakt_id = hst.get('movie').get('ids').get('trakt')
            title_imdb_id = hst.get('movie').get('ids').get('imdb')
        # Build the summarized info for title
        title_info = {
            'title': title_name,
            'year': title_year,
            'type': title_type,
            'traktId': title_trakt_id,
            'imdbId': title_imdb_id
        }
        # Check against the curated list that is being created
        if len(viewed_items) == 0:
            viewed_items.append(title_info)
        else:
            if title_info in viewed_items:
                continue
            else:
                viewed_items.append(title_info)
    # Return
    return viewed_items
