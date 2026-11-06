## Import libraries
import json
import sys
import traceback
import pandas
import urllib3

## Import functions
from session_manager.APIClient import APIClient
from trakt.authentication import *
from trakt.title_management import *
from trakt.watch_history_management import *
from report_handling.csv_handling import *
from report_handling.workbook_handling import *
from report_handling.report_generation import *
from report_handling.title_management import *
from report_handling.dataframe_handling import *
from log_handling.log_handling import *
## Import constants
from constants.constants import *
## Suppress warning messages
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

## Initialise logger
setup_logging('logging_config.json')
app_logger = logging.getLogger(__name__)

# Read configuration file
configuration_file_path = CONFIGURATION_FILE_PATH
configuration = json.loads(open(configuration_file_path).read())
client_id = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_CLIENT_ID)
access_token = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_ACCESS_TOKEN)
trakt_username = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_USERNAME)
check_ssl_certificate = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_CHECK_SSL_CERTIFICATE)
output_format = configuration.get(PARAMETERS_JSON_KEY_DATA).get(PARAMETERS_JSON_KEY_DATA_OUTPUT_FORMAT)
title_languages = configuration.get(PARAMETERS_JSON_KEY_DATA).get(PARAMETERS_JSON_KEY_DATA_TITLE_LANGUAGES)
remove_duplicate_entries_from_watch_list_report = configuration.get(PARAMETERS_JSON_KEY_DATA).get(PARAMETERS_JSON_KEY_DATA_REMOVE_DUPLICATE_ENTRIES_FROM_WATCH_REPORT)

# Fix input
title_languages = fix_input_language_codes(title_languages)

### API CLIENT
trakt_api_client = APIClient(
    base_url='https://api.trakt.tv/',
    api_server_url='',
    headers={
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': str(client_id),
        'Authorization': f'Bearer {access_token}'
    },
    ssl_certificate_verification=check_ssl_certificate
)

### ACCESS
# Test if the provided token is valid
access_token_validity = check_trakt_access_token_validity(trakt_api_client, trakt_username)
if access_token_validity:
    app_logger.info('The provided access token is valid!')
else:
    app_logger.warning('The provided access token is not valid, generating a new one...')
    # Generate a new Access Token
    trakt_device_code = generate_trakt_device_code(trakt_api_client, client_id)
    if trakt_device_code is not None:
        access_token = get_user_auth_confirmation(trakt_api_client, trakt_device_code.get('device_code'), client_id)
        trakt_api_client.session.headers.update({'Authorization': f'Bearer {access_token}'})
        try:
            app_logger.info(f'Attempting to automatically put the access token in the {configuration_file_path} file...')
            configuration[PARAMETERS_JSON_KEY_TRAKT][PARAMETERS_JSON_KEY_TRAKT_ACCESS_TOKEN] = access_token
            with open(configuration_file_path, 'w') as param_file:
                json.dump(configuration, param_file, indent=4)
            app_logger.info(f'New access token put in the {configuration_file_path} file!')
        except:
            app_logger.debug(traceback.format_exc())
    else:
        app_logger.error('Could not generate a new access token, please check the provided client ID and client secret!')
        sys.exit(1)

### WATCHLIST
# Get user's watchlist
app_logger.info('Getting user watchlist...')
user_watchlist = get_watchlist_for_user(trakt_api_client, trakt_username, None)
if len(user_watchlist) > 0:
    # Extract the items from the watchlist
    app_logger.info('Extracting the items from the watchlist...')
    watchlist_items_report = extract_items_from_watchlist(user_watchlist)
    # Get show's detailed information
    app_logger.info('Getting detailed information for titles...')
    show_title_information = {}
    for shw in watchlist_items_report:
        show_title_information[shw.get('traktId')] = get_title_information(trakt_api_client, shw.get('traktId'), True)
    # Add aliases to titles
    app_logger.info('Getting aliases...')
    show_aliases = {}
    for shw in watchlist_items_report:
        show_aliases[shw.get('traktId')] = get_title_aliases(trakt_api_client, shw.get('traktId'), shw.get('type'))
    watchlist_items_report = add_aliases_to_titles(watchlist_items_report, show_aliases, title_languages)
    # Add original title
    app_logger.info('Getting original titles...')
    watchlist_items_report = add_original_titles_to_titles(watchlist_items_report, show_title_information, show_aliases)

### WATCH HISTORY
# Get user's history
app_logger.info('Getting user watch history...')
user_watch_history = get_watch_history_for_user(trakt_api_client, trakt_username, None)
if len(user_watch_history) > 0:
    # Extract the viewed items from the history
    app_logger.info('Extracting the viewed items from the watch history...')
    viewed_items_report = extract_viewed_items_from_watch_history(user_watch_history)
    # Get show's detailed information
    app_logger.info('Getting detailed information for titles...')
    show_title_information = {}
    for shw in viewed_items_report:
        show_title_information[shw.get('traktId')] = get_title_information(trakt_api_client, shw.get('traktId'), True)
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

## EPISODE WATCH HISTORY
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

### SAVE FILES
if len(user_watchlist) > 0:
    # Convert it to DataFrame
    watchlist_items_report = pandas.DataFrame(watchlist_items_report)
    # Print report
    app_logger.info('Writing watchlist report file...')
    watchlist_items_report = fix_report_layout(watchlist_items_report)
    if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
        output_workbook = write_spreadsheet_file(watchlist_items_report, REPORT_EXCEL_FILE_NAME + '.xlsx', WATCHLIST_REPORT_FILE_NAME)
    else:
        watchlist_items_report.to_csv(WATCHLIST_REPORT_FILE_NAME + '.csv', index=False)
if len(user_watch_history) > 0:
    # Convert it to DataFrame
    viewed_items_report = pandas.DataFrame(viewed_items_report)
    # Print report
    app_logger.info('Writing watch history report file...')
    viewed_items_report = fix_report_layout(viewed_items_report)
    if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
        output_workbook = write_spreadsheet_file(viewed_items_report, REPORT_EXCEL_FILE_NAME + '.xlsx', HISTORY_REPORT_FILE_NAME)
    else:
        viewed_items_report.to_csv(HISTORY_REPORT_FILE_NAME + '.csv', index=False)
if len(user_watch_history) > 0:
    # Convert to DataFrame
    viewed_show_episodes_report = pandas.DataFrame(viewed_show_episodes_report)
    viewed_movies_report = pandas.DataFrame(viewed_movies_report)
    # Print report
    app_logger.info('Writing viewed items report file...')
    viewed_show_episodes_report = fix_report_layout(viewed_show_episodes_report)
    viewed_movies_report = fix_report_layout(viewed_movies_report)
    if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
        output_workbook = write_spreadsheet_file(viewed_show_episodes_report, REPORT_EXCEL_FILE_NAME + '.xlsx', EPISODE_HISTORY_REPORT_FILE_NAME)
        output_workbook = write_spreadsheet_file(viewed_movies_report, REPORT_EXCEL_FILE_NAME + '.xlsx', MOVIE_HISTORY_REPORT_FILE_NAME)
    else:
        viewed_show_episodes_report.to_csv(EPISODE_HISTORY_REPORT_FILE_NAME + '.csv', index=False)
        viewed_movies_report.to_csv(MOVIE_HISTORY_REPORT_FILE_NAME + '.csv', index=False)
    app_logger.info('DONE!')
