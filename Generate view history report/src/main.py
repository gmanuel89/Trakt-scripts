## Import libraries
import json
import sys
import urllib3
from datetime import datetime

## Import functions
from session_manager.APIClient import APIClient
from trakt.authentication import *
from trakt.watch_history_management import *
from report_handling.helpers import *
from report_handling.report_generation import *
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
        'trakt-api-key': str(client_id)
    },
    ssl_certificate_verification=check_ssl_certificate
)

### ACCESS
# Authentication
app_logger.info('Authenticating to Trakt...')
# Generate a new Access Token
trakt_device_code = generate_trakt_device_code(trakt_api_client, client_id)
if trakt_device_code is not None:
    access_token = get_user_auth_confirmation(trakt_api_client, trakt_device_code.get('device_code'), client_id)
    # Update API client headers with Bearer Token
    trakt_api_client.session.headers.update({'Authorization': f'Bearer {access_token}'})
else:
    app_logger.error('Could not generate a new access token, please check the provided client ID and client secret!')
    sys.exit(1)

### WATCHLIST
# Get user's watchlist
app_logger.info('Getting user watchlist...')
user_watchlist = get_watchlist_for_user(trakt_api_client, trakt_username, None)
watchlist_items_report = generate_watchlist_report(user_watchlist, title_languages, trakt_api_client)

### WATCH HISTORY
# Get user's history
app_logger.info('Getting user watch history...')
user_watch_history = get_watch_history_for_user(trakt_api_client, trakt_username, None)
viewed_items_report = generate_watch_history_report(user_watch_history, title_languages, client_id, trakt_api_client)

## EPISODE WATCH HISTORY
viewed_show_episodes_report, viewed_movies_report = generate_viewed_items_report(user_watch_history, remove_duplicate_entries_from_watch_list_report)

### SAVE FILES
date_file_suffix = datetime.now().strftime("%Y%m%d")
app_logger.info('Writing watchlist report file...')
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    trakt_report_workbook = save_report_to_excel_workbook(watchlist_items_report, WATCHLIST_REPORT_FILE_NAME, None)
    trakt_report_workbook = save_report_to_excel_workbook(viewed_items_report, HISTORY_REPORT_FILE_NAME, trakt_report_workbook)
    trakt_report_workbook = save_report_to_excel_workbook(viewed_show_episodes_report, EPISODE_HISTORY_REPORT_FILE_NAME, trakt_report_workbook)
    trakt_report_workbook = save_report_to_excel_workbook(viewed_movies_report, MOVIE_HISTORY_REPORT_FILE_NAME, trakt_report_workbook)
    save_report_workbook_to_file(trakt_report_workbook, f'{REPORT_EXCEL_FILE_NAME} {date_file_suffix}.xlsx')
else:
    save_report_to_csv_file(watchlist_items_report, f'{WATCHLIST_REPORT_FILE_NAME} {date_file_suffix}.csv')
    save_report_to_csv_file(viewed_items_report, f'{HISTORY_REPORT_FILE_NAME} {date_file_suffix}.csv')
    save_report_to_csv_file(viewed_show_episodes_report, f'{EPISODE_HISTORY_REPORT_FILE_NAME} {date_file_suffix}.csv')
    save_report_to_csv_file(viewed_movies_report, f'{MOVIE_HISTORY_REPORT_FILE_NAME} {date_file_suffix}.csv')

app_logger.info('DONE!')

sys.exit(0)
