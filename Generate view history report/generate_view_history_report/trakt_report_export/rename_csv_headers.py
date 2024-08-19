#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2024-08-19
#####

## Rename CSV headers
def rename_csv_headers(csv_content: list[dict], renaming_map: dict) -> list[dict]:
    # For each line
    for line in csv_content:
        # Get the mapping for rename
        for old_hdr in renaming_map.keys():
            if old_hdr in line.keys():
                line[renaming_map.get(old_hdr)] = line.pop(old_hdr)
    # Return
    return csv_content
