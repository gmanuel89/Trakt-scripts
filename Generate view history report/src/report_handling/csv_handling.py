## Import libraries
import csv
import logging
import traceback

## Initialise logger
logger = logging.getLogger(__name__)

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

## Write CSV content into a file
def write_csv_file(csv_file_content: list[dict], output_file_name: str, custom_column_ordering=[]) -> bool:
    """Write CSV content into a file"""
    # Exit if there is no content
    if len(csv_file_content) == 0: return False
    # Initialise output
    file_written = False
    # Check output file name
    if output_file_name == '' : output_file_name = 'CSV file'
    if not output_file_name.endswith('.csv') : output_file_name = output_file_name + '.csv'
    # Get header (harmonised)
    csv_header = list(csv_file_content[0].keys())
    # Custom column ordering (sort the ones specified, add back all the rest)
    if custom_column_ordering is not None and len(custom_column_ordering) > 0:
        custom_csv_header = []
        for cust_col in custom_column_ordering:
            for col in csv_header:
                if col == cust_col:
                    custom_csv_header.append(col)
                    break
        for col in csv_header:
            if col not in custom_column_ordering:
                custom_csv_header.append(col)
    else:
        custom_csv_header = csv_header
    # Write file content
    try:
        with open(output_file_name, 'w+', encoding='UTF8', newline='') as output_file:
            # Write content to file
            csv_writer = csv.DictWriter(output_file, fieldnames=custom_csv_header)
            csv_writer.writeheader()
            csv_writer.writerows(csv_file_content)
        file_written = True
        logger.info(f'Successfully written file to {output_file_name}!')
    except:
        file_written = False
        logger.error(f'Failed to write file to {output_file_name}!')
        logger.debug(traceback.format_exc())
    # return
    return file_written
