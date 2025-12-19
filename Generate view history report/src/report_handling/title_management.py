## Import libraries
from langcodes import *

## Extract viewed items from watchlist (in a more organised form)
def extract_items_from_watchlist(user_watchlist: list[dict]) -> list[dict]:
    """Extract viewed items from watchlist (in a more organised form)"""
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

## Extract viewed items from history (in a more organised form)
def extract_viewed_items_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
    """Extract viewed items from history (in a more organised form)"""
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

## Extract viewed movies from history (in a more organised form)
def extract_viewed_movies_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
    """Extract viewed movies from history (in a more organised form)"""
    # Initialise output
    viewed_items = []
    # For each item in the history
    for hst in user_watch_history:
        title_type = hst.get('type')
        if title_type == 'movie':
            title_name = hst.get('movie').get('title')
            title_year = hst.get('movie').get('year')
            movie_watched_at = hst.get('watched_at')
            if isinstance(movie_watched_at, list):
                movie_watched_at = ', '.join(movie_watched_at)
            # Build the summarized info for title
            title_info = {
                'title': title_name,
                'year': title_year,
                'movieWatchedAt': movie_watched_at
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

## Extract viewed show episodes from history (in a more organised form)
def extract_viewed_show_episodes_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
    """Extract viewed show episodes from history (in a more organised form)"""
    # Initialise output
    viewed_items = []
    # For each item in the history
    for hst in user_watch_history:
        title_type = hst.get('type')
        if title_type == 'show' or title_type == 'episode':
            title_name = hst.get('show').get('title')
            title_year = hst.get('show').get('year')
            episode_season = hst.get('episode').get('season')
            episode_number = hst.get('episode').get('number')
            episode_title = hst.get('episode').get('title')
            episode_watched_at = hst.get('watched_at')
            if isinstance(episode_watched_at, list):
                episode_watched_at = ', '.join(episode_watched_at)
            # Build the summarized info for title
            title_info = {
                'title': title_name,
                'year': title_year,
                'season': episode_season,
                'episodeNumber': episode_number,
                'episodeTitle': episode_title,
                'episodeWatchedAt': episode_watched_at
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

## Fix the input language code
def fix_input_language_codes(language_codes: str | list[str]) -> list[str]:
    """Fix the input language code"""
    # If not provided...
    if language_codes is None or language_codes == '' or len(language_codes) == 0:
        return ['it']
    # Fix input type
    if isinstance(language_codes, str): title_languages = [title_languages]
    # Initialise output
    fixed_language_codes = []
    # For each line
    for lc in language_codes:
        # Get the mapping for the language
        if Language.get(lc).is_valid():
            fixed_language_codes.append(lc)
    # Return
    return fixed_language_codes

## Removed duplicate items from history
def remove_duplicate_entries_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
    """Removed duplicate items from history"""
    # Initialise output
    watch_history_deduplicated = []
    # Index of all watch entries
    watch_history_index = []
    # For each item in the history
    for hst in user_watch_history:
        hst_item = hst.copy()
        # Clear the watch history
        hst_item.pop('watched_at')
        # Check against the curated list that is being created
        if len(watch_history_index) == 0:
            watch_history_index.append(hst_item)
        else:
            if hst_item in watch_history_index:
                continue
            else:
                watch_history_index.append(hst_item)
    # Run trhough the index and retrieve all the watched_at entries
    for hst_idx in watch_history_index:
        item_watched_at = []
        for hst in user_watch_history:
            if hst_idx.get('type') == 'show' or hst_idx.get('type') == 'episode':
                if hst.get('type') == 'show' or hst.get('type') == 'episode':
                    if hst_idx.get('show').get('ids').get('trakt') == hst.get('show').get('ids').get('trakt'):
                        if hst_idx.get('episode').get('season') == hst.get('episode').get('season') and hst_idx.get('episode').get('number') == hst.get('episode').get('number'):
                            item_watched_at.append(hst.get('watched_at'))
            elif hst_idx.get('type') == 'movie':
                if hst.get('type') == 'movie':
                    if hst_idx.get('movie').get('ids').get('trakt') == hst.get('movie').get('ids').get('trakt'):
                        item_watched_at.append(hst.get('watched_at'))
        if len(item_watched_at) == 1: item_watched_at = item_watched_at[0]
        hst_idx['watched_at'] = item_watched_at
        watch_history_deduplicated.append(hst_idx)
    # Return
    return watch_history_deduplicated
