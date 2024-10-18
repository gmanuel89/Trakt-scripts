## Import libraries
import json
import sys
import traceback

## Import functions
from trakt import *
from report_handling import *
## Import constants
from constants import *

# Read configuration file
configuration_file_path = CONFIGURATION_FILE_PATH
configuration = json.loads(open(configuration_file_path).read())
client_id = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_CLIENT_ID)
client_secret = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_CLIENT_SECRET)
access_token = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_ACCESS_TOKEN)
trakt_username = configuration.get(PARAMETERS_JSON_KEY_TRAKT).get(PARAMETERS_JSON_KEY_TRAKT_USERNAME)
redirect_debug_messages_to_log_file = configuration.get(PARAMETERS_JSON_KEY_DATA).get(PARAMETERS_JSON_KEY_DATA_REDIRECT_TO_LOG_FILE)
output_format = configuration.get(PARAMETERS_JSON_KEY_DATA).get(PARAMETERS_JSON_KEY_DATA_OUTPUT_FORMAT)
title_languages = configuration.get(PARAMETERS_JSON_KEY_DATA).get(PARAMETERS_JSON_KEY_DATA_TITLE_LANGUAGES)

# Fix input
title_languages = fix_input_language_codes(title_languages)

##### SCRIPT EXECUTION
# Initialise log file
if redirect_debug_messages_to_log_file:
    log_file = open("trakt_report_export.log", "w")
    sys.stdout = log_file
## ACCESS
# Test if the provided token is valid
access_token_validity = check_trakt_access_token_validity(access_token, client_id, trakt_username)
if access_token_validity:
    print('The provided access token is valid!')
else:
    print('The provided access token is not valid, generating a new one...')
    # Generate a new Access Token
    trakt_device_code = generate_trakt_device_code(client_id)
    if trakt_device_code is not None:
        access_token = get_user_auth_confirmation(trakt_device_code.get('device_code'), client_id, client_secret)
        try:
            print('Attempting to automatically put the access token in the %s file...' %configuration_file_path)
            configuration[PARAMETERS_JSON_KEY_TRAKT][PARAMETERS_JSON_KEY_TRAKT_ACCESS_TOKEN] = access_token
            with open(configuration_file_path, 'w') as param_file:
                json.dump(configuration, param_file, indent=4)
            print('New access token put in the %s file!' %configuration_file_path)
        except:
            traceback.print_exc()
## OUTPUT
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    import openpyxl
    output_workbook = openpyxl.Workbook()
## WATCHLIST
# Get user's watchlist
print('Getting user watchlist...')
user_watchlist = get_watchlist_for_user(trakt_username, client_id, access_token, None, None)
# Extract the items from the watchlist
print('Extracting the items from the watchlist...')
watchlist_items_report = extract_items_from_watchlist(user_watchlist)
# Get show's detailed information
"""
show_title_information = {}
for shw in watchlist_items_report:
    show_title_information[shw.get('traktId')] = get_title_information(shw.get('traktId'), client_id, True)
"""
# Add aliases to titles
print('Getting show aliases...')
show_aliases = {}
for shw in watchlist_items_report:
    show_aliases[shw.get('traktId')] = get_title_aliases(shw.get('traktId'), shw.get('type'), client_id)
watchlist_items_report = add_aliases_to_titles(watchlist_items_report, show_aliases, title_languages)
# Print report
print('Writing output report file...')
watchlist_items_report = fix_report_layout(watchlist_items_report)
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    output_workbook = write_spreadsheet_to_workbook(watchlist_items_report, WATCHLIST_REPORT_FILE_NAME, output_workbook, True, True)
else:
    write_csv_file(watchlist_items_report, WATCHLIST_REPORT_FILE_NAME + '.csv')
## WATCH HISTORY
# Get user's history
print('Getting user watch history...')
user_watch_history = get_watch_history_for_user(trakt_username, client_id, access_token, None, None)
# Extract the viewed items from the history
print('Extracting the viewed items from the watch history...')
viewed_items_report = extract_viewed_items_from_watch_history(user_watch_history)
# Get show's detailed information
show_title_information = {}
for shw in viewed_items_report:
    show_title_information[shw.get('traktId')] = get_title_information(shw.get('traktId'), client_id, True)
# Add aliases to titles
print('Getting show aliases...')
show_aliases = {}
for shw in viewed_items_report:
    show_aliases[shw.get('traktId')] = get_title_aliases(shw.get('traktId'), shw.get('type'), client_id)
viewed_items_report = add_aliases_to_titles(viewed_items_report, show_aliases, title_languages)
# Add the progress to TV shows
print('Getting watch progress for shows...')
viewed_items_report = add_progress_to_tv_shows(viewed_items_report, user_watch_history)
# Add percentage of completion to shows
print('Getting percentage of completion for shows...')
viewed_items_report = add_percentage_of_completion_to_tv_shows(viewed_items_report, user_watch_history, client_id)
# Add if series is over
print('Getting status for shows...')
viewed_items_report = add_series_is_over_flag_to_tv_shows(viewed_items_report, show_title_information)
# Print report
print('Writing output report file...')
viewed_items_report = fix_report_layout(viewed_items_report)
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    output_workbook = write_spreadsheet_to_workbook(viewed_items_report, HISTORY_REPORT_FILE_NAME, output_workbook, True, True)
else:
    write_csv_file(viewed_items_report, HISTORY_REPORT_FILE_NAME + '.csv')
## OUTPUT
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    write_workbook(output_workbook, None, REPORT_EXCEL_FILE_NAME + '.xlsx', True)
## LOG FILE
# Write the log file
if redirect_debug_messages_to_log_file:
    log_file.close()
