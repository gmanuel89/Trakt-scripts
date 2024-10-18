#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-10-18
#####

## Import libraries
from langcodes import *

## Fix the input language code
def fix_input_language_codes(language_codes: str | list[str]) -> list[str]:
    # If not provided...
    if language_codes is None or language_codes == '' or len(language_codes) > 0:
        return ['it']
    # Fix input type
    if isinstance(language_codes, str): title_languages = [title_languages]
    # Initialise output
    fixed_language_codes = []
    # For each line
    for lc in language_codes:
        # Get the mapping for the language
        if Language.get(lc).is_valid():
            fixed_language_codes.append(lc)
    # Return
    return fixed_language_codes
