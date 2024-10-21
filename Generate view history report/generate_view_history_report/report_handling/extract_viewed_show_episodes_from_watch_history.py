#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-10-21
#####

## Extract viewed show episodes from history (in a more organised form)
def extract_viewed_show_episodes_from_watch_history(user_watch_history: list[dict]) -> list[dict]:
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
