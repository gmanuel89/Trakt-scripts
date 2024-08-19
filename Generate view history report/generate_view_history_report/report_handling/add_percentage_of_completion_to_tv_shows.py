#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import traceback

## Import functions
from trakt.get_title_seasons import get_title_seasons

## Add the percentage of completion to TV shows (in the extracted report)
def add_percentage_of_completion_to_tv_shows(viewed_items_report: list[dict], user_watch_history: list[dict], client_id: str) -> list[dict]:
    # For each viewed item
    for vwd in viewed_items_report:
        # Initialise
        vwd['watchedEpisodes'] = None
        vwd['percentageOfCompletion'] = None
        #vwd['isMiniseries'] = None
        try:
            # Proceed only if it is a TV show
            if vwd.get('type') == 'episode' or vwd.get('type') == 'show':
                # Build a sub-history only for the selected show
                history_for_selected_show = []
                for hst in user_watch_history:
                    if vwd.get('type') == hst.get('type'):
                        if vwd.get('traktId') == hst.get('show').get('ids').get('trakt'):
                            history_for_selected_show.append(hst)
                # Determine the episodes watched (discard duplicates from the history)
                episodes_watched = []
                for epsd in history_for_selected_show:
                    episode_details = {
                        'season': epsd.get('episode').get('season'),
                        'episode': epsd.get('episode').get('number')
                    }
                    if episode_details not in episodes_watched:
                        episodes_watched.append(episode_details)
                # Count the watched episoded
                number_of_watched_episodes = len(episodes_watched)
                # Get the TV shows summary
                tv_show_summary_info = get_title_seasons(vwd.get('traktId'), client_id, True)
                # Determine if a title is a miniseries
                #vwd['isMiniseries'] = determine_if_miniseries(tv_show_summary_info)
                # Get the total number of episodes from the summary
                total_number_of_episodes = 0
                for seasn in tv_show_summary_info:
                    # Discard the specials
                    if seasn.get('number') != 0:
                        total_number_of_episodes = total_number_of_episodes + len(seasn.get('episodes'))
                # Get the percentage
                vwd['watchedEpisodes'] = str(number_of_watched_episodes) + '  of  ' + str(total_number_of_episodes)
                vwd['percentageOfCompletion'] = round(number_of_watched_episodes / total_number_of_episodes * 100, 1)
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report
