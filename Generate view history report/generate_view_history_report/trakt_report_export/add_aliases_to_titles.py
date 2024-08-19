#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Import libraries
import traceback

## Import functions
from trakt_report_export.get_title_aliases import get_title_aliases

## Add the aliases to shows (use language codes) (in the extracted report)
def add_aliases_to_titles(viewed_items_report: list[dict], client_id: str, languages=['it']) -> list[dict]:
    # For each viewed item
    for vwd in viewed_items_report:
        try:
            # Get all the aliases for the title
            title_aliases = get_title_aliases(vwd.get('traktId'), vwd.get('type'), client_id)
            # Get aliases for each language
            for lang in languages:
                vwd['alias (%s)' %lang] = None
                for als in title_aliases:
                    if str(lang).lower() == str(als.get('country')).lower():
                        vwd['alias (%s)' %lang] = als.get('title')
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report
