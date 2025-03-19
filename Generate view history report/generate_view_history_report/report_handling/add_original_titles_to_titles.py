#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2025-03-19
#####

## Import libraries
import traceback

## Add the original title to titles (in the extracted report)
def add_original_titles_to_titles(viewed_items_report: list[dict], show_title_information: dict, show_aliases: dict) -> list[dict]:
    # For each viewed item
    for vwd in viewed_items_report:
        # Initialise
        vwd['originalTitle'] = vwd.get('title')
        try:
            # Retrieve information for the show
            title_information = show_title_information.get(vwd.get('traktId'), None)
            # Determine the origin country of the title
            origin_country = title_information.get('country', None)
            # Fetch the corresponding alias
            for als in show_aliases.get(vwd.get('traktId')):
                if str(als.get('country')) == str(origin_country):
                    # Store it in the output
                    vwd['originalTitle'] = als.get('title')
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report
