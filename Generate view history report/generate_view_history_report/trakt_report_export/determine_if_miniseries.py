#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Determine if it is a miniseries based on summary info
def determine_if_miniseries(tv_show_summary_info: list[dict]) -> bool:
    # Initialise
    is_miniseries = False
    # Get the seasons
    tv_seasons = []
    for seasn in tv_show_summary_info:
        tv_seasons.append(int(seasn.get('number')))
    # Convert it to a set and sort it
    tv_seasons_unique = set(tv_seasons)
    tv_seasons_unique = sorted(tv_seasons_unique)
    # Determine if it is a miniseries
    if len(tv_seasons_unique) == 1 and tv_seasons_unique[0] == 0:
        is_miniseries = True
    # Return
    return is_miniseries
