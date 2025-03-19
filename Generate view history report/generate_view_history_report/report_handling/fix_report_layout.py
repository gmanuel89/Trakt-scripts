#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2025-03-19
#####

## Import functions and constants
from report_handling.rename_csv_headers import rename_csv_headers
from constants import *

## Fix the layout of the output report
def fix_report_layout(report_content: list[dict]) -> list[dict]:
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
    