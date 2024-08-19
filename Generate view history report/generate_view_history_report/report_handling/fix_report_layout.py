#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries and functions
from report_handling.rename_csv_headers import rename_csv_headers

## Fix the layout of the report
def fix_report_layout(report_content: list[dict]) -> list[dict]:
    # Rename and order headers
    csv_header_renamed_and_ordered = {'title': 'Title',
                                      'year': 'Year',
                                      'type': 'Type',
                                      'traktId': 'Trakt ID',
                                      'imdbId': 'IMDB ID',
                                      'latestWatchedEpisode': 'Last Watched Episode',
                                      'watchedEpisodes': 'Watched Episodes',
                                      'percentageOfCompletion': 'Percentage Of Completion',
                                      'showStatus': 'Status',
                                      'alias (it)': 'Title (italian)',
                                      'listedAt': 'Listed At'
    }
    report_content = rename_csv_headers(report_content, csv_header_renamed_and_ordered)
    # Return
    return report_content
    