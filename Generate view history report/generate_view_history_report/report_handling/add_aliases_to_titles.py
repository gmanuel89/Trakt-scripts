#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-10-18
#####

## Import libraries
import traceback

## Add the aliases to shows (use language codes) (in the extracted report)
def add_aliases_to_titles(viewed_items_report: list[dict], show_aliases: dict, languages=['it']) -> list[dict]:
    # For each viewed item
    for vwd in viewed_items_report:
        try:
            # Get all the aliases for the title
            title_aliases = show_aliases.get(vwd.get('traktId'))
            # Get aliases for each language
            for lang in languages:
                alias_dictionary_key = 'alias (%s)' %(str(lang).lower())
                vwd[alias_dictionary_key] = None
                for als in title_aliases:
                    if str(lang).lower() == str(als.get('country')).lower():
                        vwd[alias_dictionary_key] = als.get('title')
        except:
            traceback.print_exc()
    # Return
    return viewed_items_report
