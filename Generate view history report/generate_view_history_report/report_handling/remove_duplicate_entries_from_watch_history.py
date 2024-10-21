#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-21
#####

## Removed duplicate items from history
def remove_duplicate_entries_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
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
