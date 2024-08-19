#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com / manuel.galli@revvity.com
# Updated date: 2022-10-07
#####

## Import libraries and functions
import openpyxl
from report_handling.apply_styling_to_spreadsheet import apply_styling_to_spreadsheet

## Write a CSV dictionary to a Spreadsheet
def write_spreadsheet_to_workbook(workbook_content: list[dict], sheet_name: str, spreadsheet_workbook: openpyxl.Workbook) -> openpyxl.Workbook:
    # Create a new Workbook if not provided
    if not spreadsheet_workbook or spreadsheet_workbook is None:
        spreadsheet_workbook = openpyxl.Workbook()
    # Create dedicated sheet (truncate sheet name if it is too long)
    if len(sheet_name) > 31:
        sheet_name = sheet_name[0:30]
    spreadsheet_workbook.create_sheet(sheet_name)
    spreadsheet_sheet = spreadsheet_workbook[sheet_name]
    # Write the content (using a numbered map)
    spreadsheet_column_map = {}
    # Header numbered map
    csv_header = list(workbook_content[0].keys())
    for i in range(len(csv_header)):
        spreadsheet_column_map[i+1] = csv_header[i]
    spreadsheet_sheet.append(spreadsheet_column_map)
    # Content (get the position number from the header map), for each row...
    for r in range(len(workbook_content)):
        row = workbook_content[r]
        row_dictionary_fixed_for_spreadsheet = row
        # Replace the key with the positional number (to write the cells in the spreadsheet)
        for i in range(len(csv_header)):
            row_dictionary_fixed_for_spreadsheet[i+1] = row.pop(csv_header[i])
        spreadsheet_sheet.append(row_dictionary_fixed_for_spreadsheet)
    # Apply styling to worksheet
    spreadsheet_sheet = apply_styling_to_spreadsheet(spreadsheet_sheet)
    # Print console message
    print('Writing spreadsheet: ' + str(sheet_name))
    # Return the same Workbook as input but with the added sheet
    return spreadsheet_workbook