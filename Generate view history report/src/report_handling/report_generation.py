## Import libraries
from constants.constants import *
import traceback
from trakt.title_management import *
from report_handling.csv_handling import *

## Add the aliases to shows (use language codes) (in the extracted report)
def add_aliases_to_titles(viewed_items_report: list[dict], show_aliases: dict, languages=['it']) -> list[dict]:
    """Add the aliases to shows (use language codes) (in the extracted report)"""
    # For each viewed item
    for vwd in viewed_items_report:
        try:
            # Get all the aliases for the title
            title_aliases = show_aliases.get(vwd.get('traktId'))
            # Get aliases for each language
            for lang in languages:
                alias_dictionary_key = 'alias (%s)' %(str(lang).lower())
                vwd[alias_dictionary_key] = None
                for als in title_aliases:
                    if str(lang).lower() == str(als.get('country')).lower():
                        vwd[alias_dictionary_key] = als.get('title')
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report

## Add the original title to titles (in the extracted report)
def add_original_titles_to_titles(viewed_items_report: list[dict], show_title_information: dict, show_aliases: dict) -> list[dict]:
    """Add the original title to titles (in the extracted report)"""
    # For each viewed item
    for vwd in viewed_items_report:
        # Initialise
        vwd['originalTitle'] = vwd.get('title')
        try:
            # Retrieve information for the show
            title_information = show_title_information.get(vwd.get('traktId'), None)
            # Determine the origin country of the title
            origin_country = title_information.get('country', None)
            # Fetch the corresponding alias
            for als in show_aliases.get(vwd.get('traktId')):
                if str(als.get('country')) == str(origin_country):
                    # Store it in the output
                    vwd['originalTitle'] = als.get('title')
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report

## Add the percentage of completion to TV shows (in the extracted report)
def add_percentage_of_completion_to_tv_shows(viewed_items_report: list[dict], user_watch_history: list[dict], client_id: str) -> list[dict]:
    """Add the percentage of completion to TV shows (in the extracted report)"""
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

## Add the progress to TV shows (in the extracted report)
def add_progress_to_tv_shows(viewed_items_report: list[dict], user_watch_history: list[dict]) -> list[dict]:
    """Add the progress to TV shows (in the extracted report)"""
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

## Add the flag of "is the series over" to TV shows (in the extracted report)
def add_series_is_over_flag_to_tv_shows(viewed_items_report: list[dict], show_title_information: dict) -> list[dict]:
    """Add the flag of "is the series over" to TV shows (in the extracted report)"""
    # For each viewed item
    for vwd in viewed_items_report:
        # Initialise
        vwd['showStatus'] = None
        try:
            # Proceed only if it is a TV show
            if vwd.get('type') == 'episode' or vwd.get('type') == 'show':
                # Retrieve information for the show
                title_information = show_title_information.get(vwd.get('traktId'))
                # Determine if the series is over
                series_status = title_information.get('status', None)
                # Store it in the output
                vwd['showStatus'] = series_status
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report

## Determine if it is a miniseries based on summary info
def determine_if_miniseries(tv_show_summary_info: list[dict]) -> bool:
    """Determine if it is a miniseries based on summary info"""
    # Initialise
    is_miniseries = False
    # Get the seasons
    tv_seasons = []
    for seasn in tv_show_summary_info:
        tv_seasons.append(int(seasn.get('number')))
    # Convert it to a set and sort it
    tv_seasons_unique = set(tv_seasons)
    tv_seasons_unique = sorted(tv_seasons_unique)
    # Determine if it is a miniseries
    if len(tv_seasons_unique) == 1 and tv_seasons_unique[0] == 0:
        is_miniseries = True
    # Return
    return is_miniseries

## Fix the layout of the output report
def fix_report_layout(report_content: list[dict]) -> list[dict]:
    """Fix the layout of the output report"""
    # Rename and order headers
    csv_header_renamed_and_ordered = {
        'title': OUTPUT_REPORT_COLUMN_TITLE + ' (international english)',
        'originalTitle': OUTPUT_REPORT_COLUMN_TITLE + ' (original)',
        'year': OUTPUT_REPORT_COLUMN_YEAR,
        'type': OUTPUT_REPORT_COLUMN_TYPE,
        'traktId': OUTPUT_REPORT_COLUMN_TRAKT_ID,
        'imdbId': OUTPUT_REPORT_COLUMN_IMDB_ID,
        'latestWatchedEpisode': OUTPUT_REPORT_COLUMN_LAST_WATCHED_EPISODE,
        'watchedEpisodes': OUTPUT_REPORT_COLUMN_WATCHED_EPISODES,
        'percentageOfCompletion': OUTPUT_REPORT_COLUMN_PERCENTAGE_OF_COMPLETION,
        'showStatus': OUTPUT_REPORT_COLUMN_STATUS,
        'listedAt': OUTPUT_REPORT_COLUMN_LISTED_AT,
        'season': OUTPUT_REPORT_COLUMN_SEASON,
        'episodeNumber': OUTPUT_REPORT_COLUMN_EPISODE_NUMBER,
        'episodeTitle': OUTPUT_REPORT_COLUMN_EPISODE_TITLE,
        'episodeWatchedAt': OUTPUT_REPORT_COLUMN_WATCHED_AT,
        'movieWatchedAt': OUTPUT_REPORT_COLUMN_WATCHED_AT
    }
    # Dynamic alias
    for hd in report_content[0].keys():
        if 'alias' in str(hd).lower():
            csv_header_renamed_and_ordered[hd] = OUTPUT_REPORT_COLUMN_TITLE + str(hd).split('alias')[1]
    # Remap headers
    report_content = rename_csv_headers(report_content, csv_header_renamed_and_ordered)
    # Return
    return report_content
    