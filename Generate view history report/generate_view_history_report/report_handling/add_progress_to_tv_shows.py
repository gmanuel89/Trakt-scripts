#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import traceback

## Add the progress to TV shows (in the extracted report)
def add_progress_to_tv_shows(viewed_items_report: list[dict], user_watch_history: list[dict]) -> list[dict]:
    # For each viewed item
    for vwd in viewed_items_report:
        # Initialise
        vwd['latestWatchedEpisode'] = None
        try:
            # Proceed only if it is a TV show
            if vwd.get('type') == 'episode' or vwd.get('type') == 'show':
                # Build a sub-history only for the selected show
                history_for_selected_show = []
                for hst in user_watch_history:
                    if vwd.get('type') == hst.get('type'):
                        if vwd.get('traktId') == hst.get('show').get('ids').get('trakt'):
                            history_for_selected_show.append(hst)
                # Determine the last episode watched
                latestSeason = 0
                latestEpisode = 0
                for epsd in history_for_selected_show:
                    if epsd.get('episode').get('season') > latestSeason and epsd.get('episode').get('number') > latestEpisode:
                        vwd['latestWatchedEpisode'] = str(epsd.get('episode').get('season')) + 'x' + str(epsd.get('episode').get('number'))
                        latestSeason = epsd.get('episode').get('season')
                        latestEpisode = epsd.get('episode').get('number')
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report
