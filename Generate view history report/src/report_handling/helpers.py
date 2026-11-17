## Import libraries
import logging
from report_handling.csv_handling import *
from report_handling.title_management import *
from report_handling.report_generation import *

## Initialise logger
app_logger = logging.getLogger(__name__)

## Generate viewed items report
def generate_viewed_items_report(user_watch_history: list[dict], remove_duplicate_entries_from_watch_list_report=True) -> tuple[list[dict], list[dict]]:
    """Generate viewed items report"""
    if len(user_watch_history) > 0:
        # Extract user's tv show espisode and movie history
        if remove_duplicate_entries_from_watch_list_report:
            app_logger.info('Merging duplicates from user watch history...')
            user_watch_history_deduplicated = remove_duplicate_entries_from_watch_history(user_watch_history)
        else:
            user_watch_history_deduplicated = user_watch_history
        app_logger.info('Getting watched episodes and movies from user watch history...')
        viewed_show_episodes_report = extract_viewed_show_episodes_from_watch_history(user_watch_history_deduplicated)
        viewed_movies_report = extract_viewed_movies_from_watch_history(user_watch_history_deduplicated)
        # return
        return viewed_show_episodes_report, viewed_movies_report
    else:
        return [], []

## Generate watch history report
def generate_watch_history_report(user_watch_history: list[dict], title_languages: list[str], client_id: str, trakt_api_client: APIClient) -> list[dict]:
    """Generate watch history report"""
    # Initialise output
    viewed_items_report = []
    if len(user_watch_history) > 0:
        # Extract the viewed items from the history
        app_logger.info('Extracting the viewed items from the watch history...')
        viewed_items_report = extract_viewed_items_from_watch_history(user_watch_history)
        # Get show's detailed information
        app_logger.info('Getting detailed information for titles...')
        show_title_information = {}
        for shw in viewed_items_report:
            show_title_information[shw.get('traktId')] = get_title_information(trakt_api_client, shw.get('traktId'), shw.get('type'), True)
        # Add aliases to titles
        app_logger.info('Getting aliases...')
        show_aliases = {}
        for shw in viewed_items_report:
            show_aliases[shw.get('traktId')] = get_title_aliases(trakt_api_client, shw.get('traktId'), shw.get('type'))
        viewed_items_report = add_aliases_to_titles(viewed_items_report, show_aliases, title_languages)
        # Add the progress to TV shows
        app_logger.info('Getting watch progress for shows...')
        viewed_items_report = add_progress_to_tv_shows(viewed_items_report, user_watch_history)
        # Add percentage of completion to shows
        app_logger.info('Getting percentage of completion for shows...')
        viewed_items_report = add_percentage_of_completion_to_tv_shows(trakt_api_client, viewed_items_report, user_watch_history, client_id)
        # Add if series is over
        app_logger.info('Getting status for shows...')
        viewed_items_report = add_series_is_over_flag_to_tv_shows(viewed_items_report, show_title_information)
        # Add original title
        app_logger.info('Getting original titles...')
        viewed_items_report = add_original_titles_to_titles(viewed_items_report, show_title_information, show_aliases)
    # return
    return viewed_items_report

## Generate watchlist report
def generate_watchlist_report(user_watchlist: list[dict], title_languages: list[str], trakt_api_client: APIClient) -> list[dict]:
    """Generate watchlist report"""
    # Initialise output
    watchlist_items_report = []
    if len(user_watchlist) > 0:
        # Extract the items from the watchlist
        app_logger.info('Extracting the items from the watchlist...')
        watchlist_items_report = extract_items_from_watchlist(user_watchlist)
        # Get show's detailed information
        app_logger.info('Getting detailed information for titles...')
        show_title_information = {}
        for shw in watchlist_items_report:
            show_title_information[shw.get('traktId')] = get_title_information(trakt_api_client, shw.get('traktId'), shw.get('type'), True)
        # Add aliases to titles
        app_logger.info('Getting aliases...')
        show_aliases = {}
        for shw in watchlist_items_report:
            show_aliases[shw.get('traktId')] = get_title_aliases(trakt_api_client, shw.get('traktId'), shw.get('type'))
        watchlist_items_report = add_aliases_to_titles(watchlist_items_report, show_aliases, title_languages)
        # Add original title
        app_logger.info('Getting original titles...')
        watchlist_items_report = add_original_titles_to_titles(watchlist_items_report, show_title_information, show_aliases)
    # return
    return watchlist_items_report

## Save report to CSV file
def save_report_to_csv_file(report: list[dict], filename: str) -> bool:
    """Save report to CSV file"""
    # Initialise output
    file_written = False
    try:
        if len(report) > 0:
            # Print report
            report, ordered_csv_header = fix_report_layout(report)
            file_written = write_csv_file(report, filename, ordered_csv_header)
    except:
        file_written = False
    # return
    return file_written

## Save report to Excel file
def save_report_to_excel_file(report: list[dict], filename: str, sheet_name: str) -> bool:
    """Save report to Excel file"""
    # Initialise output
    file_written = False
    try:
        if len(report) > 0:
            # Print report
            report, ordered_csv_header = fix_report_layout(report)
            output_workbook = write_spreadsheet_file(report, filename, sheet_name)
            file_written = True
    except:
        file_written = False
    # return
    return file_written