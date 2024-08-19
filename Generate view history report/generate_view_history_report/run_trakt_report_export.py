## Import libraries
import json
import sys

## Import functions
from trakt_report_export import *

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
csv_header_renamed = {'title': 'Title', 'year': 'Year', 'type': 'Type', 'traktId': 'Trakt ID', 'imdbId': 'IMDB ID', 'latestWatchedEpisode': 'Last Watched Episode', 'watchedEpisodes': 'Watched Episodes', 'percentageOfCompletion': 'Percentage Of Completion', 'showStatus': 'Status'}
viewed_items_report = rename_csv_headers(viewed_items_report, csv_header_renamed)
write_csv_file(viewed_items_report, 'Trakt history report.csv')
# Write the log file
if redirect_debug_messages_to_log_file:
    log_file.close()
