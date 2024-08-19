#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import traceback

## Import functions
from trakt_report_export.get_title_information import get_title_information

## Add the flag of "is the series over" to TV shows (in the extracted report)
def add_series_is_over_flag_to_tv_shows(viewed_items_report: list[dict], client_id: str) -> list[dict]:
    # For each viewed item
    for vwd in viewed_items_report:
        # Initialise
        vwd['showStatus'] = None
        try:
            # Proceed only if it is a TV show
            if vwd.get('type') == 'episode' or vwd.get('type') == 'show':
                # Retrieve information for the show
                title_information = get_title_information(vwd.get('traktId'), client_id, True)
                # Determine if the series is over
                series_status = title_information.get('status', None)
                # Store it in the output
                vwd['showStatus'] = series_status
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report
