## Import libraries
import json
import sys

## Import functions
from trakt import *
from report_handling import *

# Read configuration file
configuration_file_path = 'parameters.json'
configuration = json.loads(open(configuration_file_path).read())
client_id = configuration.get('trakt').get('clientId')
client_secret = configuration.get('trakt').get('clientSecret')
access_token = configuration.get('trakt').get('accessToken')
trakt_username = configuration.get('trakt').get('username')
redirect_debug_messages_to_log_file = configuration.get('data').get('redirectDebugMessagesToLogFile')
output_format = configuration.get('data').get('outputFormat')

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
        trakt_device_code_confirmation = get_user_auth_confirmation(trakt_device_code.get('device_code'), client_id, client_secret)
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
# Add aliases to titles
print('Getting show aliases...')
watchlist_items_report = add_aliases_to_titles(watchlist_items_report, client_id, ['it'])
# Print report
print('Writing output report file...')
watchlist_items_report = fix_report_layout(watchlist_items_report)
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    output_workbook = write_spreadsheet_to_workbook(watchlist_items_report, 'Trakt watchlist report', output_workbook)
else:
    write_csv_file(watchlist_items_report, 'Trakt watchlist report.csv')
## WATCH HISTORY
# Get user's history
print('Getting user watch history...')
user_watch_history = get_watch_history_for_user(trakt_username, client_id, access_token, None, None)
# Extract the viewed items from the history
print('Extracting the viewed items from the watch history...')
viewed_items_report = extract_viewed_items_from_watch_history(user_watch_history)
# Add aliases to titles
print('Getting show aliases...')
viewed_items_report = add_aliases_to_titles(viewed_items_report, client_id, ['it'])
# Add the progress to TV shows
print('Getting watch progress for shows...')
viewed_items_report = add_progress_to_tv_shows(viewed_items_report, user_watch_history)
# Add percentage of completion to shows
print('Getting percentage of completion for shows...')
viewed_items_report = add_percentage_of_completion_to_tv_shows(viewed_items_report, user_watch_history, client_id)
# Add if series is over
print('Getting status for shows...')
viewed_items_report = add_series_is_over_flag_to_tv_shows(viewed_items_report, client_id)
# Print report
print('Writing output report file...')
viewed_items_report = fix_report_layout(viewed_items_report)
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    output_workbook = write_spreadsheet_to_workbook(viewed_items_report, 'Trakt history report', output_workbook)
else:
    write_csv_file(viewed_items_report, 'Trakt history report.csv')
## OUTPUT
if 'xls' in str(output_format).lower() or 'excel' in str(output_format).lower():
    write_workbook(output_workbook, None, 'Trakt report.xlsx', True)
## LOG FILE
# Write the log file
if redirect_debug_messages_to_log_file:
    log_file.close()
