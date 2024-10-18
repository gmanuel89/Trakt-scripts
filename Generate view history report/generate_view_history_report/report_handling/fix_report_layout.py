#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-10-18
#####

## Import functions and constants
from report_handling.rename_csv_headers import rename_csv_headers
from constants import *

## Fix the layout of the report
def fix_report_layout(report_content: list[dict]) -> list[dict]:
    # Rename and order headers
    csv_header_renamed_and_ordered = {'title': OUTPUT_REPORT_COLUMN_TITLE,
                                      'year': OUTPUT_REPORT_COLUMN_YEAR,
                                      'type': OUTPUT_REPORT_COLUMN_TYPE,
                                      'traktId': OUTPUT_REPORT_COLUMN_TRAKT_ID,
                                      'imdbId': OUTPUT_REPORT_COLUMN_IMDB_ID,
                                      'latestWatchedEpisode': OUTPUT_REPORT_COLUMN_LAST_WATCHED_EPISODE,
                                      'watchedEpisodes': OUTPUT_REPORT_COLUMN_WATCHED_EPISODES,
                                      'percentageOfCompletion': OUTPUT_REPORT_COLUMN_PERCENTAGE_OF_COMPLETION,
                                      'showStatus': OUTPUT_REPORT_COLUMN_STATUS,
                                      'alias (it)': OUTPUT_REPORT_COLUMN_TITLE + ' (italian)',
                                      'listedAt': OUTPUT_REPORT_COLUMN_LISTED_AT
    }
    report_content = rename_csv_headers(report_content, csv_header_renamed_and_ordered)
    # Return
    return report_content
    