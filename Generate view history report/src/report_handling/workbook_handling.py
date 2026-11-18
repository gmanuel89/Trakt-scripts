## Import libraries and functions
import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
import logging
import traceback

## Initialise logger
app_logger = logging.getLogger(__name__)

## Apply styling to spreadsheet
def apply_styling_to_spreadsheet(spreadsheet_sheet: Worksheet, freeze_header=True, freeze_first_column=False) -> Worksheet:
    # Make the header bold
    for col in range(spreadsheet_sheet.max_column):
        cell_letter = get_column_letter(col+1)
        spreadsheet_sheet[cell_letter+'1'].font = Font(bold=True)
    # Autoresize columns
    for col_index, col in enumerate(spreadsheet_sheet.columns, 1):
        spreadsheet_sheet.column_dimensions[get_column_letter(col_index)].auto_size = True
    spreadsheet_sheet = autoresize_columns(spreadsheet_sheet)
    """
    column_letters = tuple(get_column_letter(col_number + 1) for col_number in range(spreadsheet_sheet.max_column))
    for column_letter in column_letters:
            spreadsheet_sheet.column_dimensions[column_letter].bestFit = True
    """
    # Freeze the header
    if freeze_header and not freeze_first_column:
        spreadsheet_sheet.freeze_panes = 'A2'
    # Freeze first column
    elif freeze_first_column and not freeze_header:
        spreadsheet_sheet.freeze_panes = 'B1'
    # Freeze the header and the first column
    elif freeze_header and freeze_first_column:
        spreadsheet_sheet.freeze_panes = 'B2'
    # return
    return spreadsheet_sheet

## Autoresize columns
def autoresize_columns(worksheet: Worksheet) -> Worksheet:
    """Adjust column widths based on content length."""
    for column_cells in worksheet.columns:
        max_length = 0
        column_letter = get_column_letter(column_cells[0].column)
        for cell in column_cells:
            try:
                # Calculate length of cell content
                if cell.value:
                    cell_length = len(str(cell.value))
                    if cell_length > max_length:
                        max_length = cell_length
            except:
                pass
        # Set width with some padding (adjust multiplier as needed)
        adjusted_width = (max_length + 2) * 1.2
        worksheet.column_dimensions[column_letter].width = adjusted_width
    return worksheet

## Write spreadsheet to file
def remove_default_empty_sheet_from_workbook(spreadsheet_workbook: openpyxl.Workbook) -> openpyxl.Workbook:
    # Verify if there is a sheet named "Sheet"
    if 'Sheet' in spreadsheet_workbook.sheetnames:
        # Retrieve the "Sheet" content
        sheet_content = spreadsheet_workbook['Sheet']
        # Determine that it is empty
        if sheet_content.max_column == 1 and sheet_content.max_row == 1:
            # Retrieve the single cell value and determine that it's empty
            if sheet_content['A1'].value == '' or sheet_content['A1'].value is None:
                # Remove the sheet
                spreadsheet_workbook.remove(spreadsheet_workbook['Sheet'])
    # return
    return spreadsheet_workbook

## Write a CSV dictionary to a Spreadsheet
def write_spreadsheet_to_workbook(workbook_content: list[dict], sheet_name: str, spreadsheet_workbook: openpyxl.Workbook, freeze_header=True, freeze_first_column=False, custom_column_ordering=[]) -> openpyxl.Workbook:
    """Write a CSV dictionary to a Spreadsheet"""
    # Create a new Workbook if not provided
    if not spreadsheet_workbook:
        spreadsheet_workbook = openpyxl.Workbook()
    # Create dedicated sheet (truncate sheet name if it is too long)
    if len(sheet_name) > 31:
        sheet_name = sheet_name[:31]
    # Handle duplicate sheet names
    if sheet_name in spreadsheet_workbook.sheetnames:
        base_name = sheet_name[:28]  # leave room for suffix
        suffix = 1
        while f"{base_name}_{suffix}" in spreadsheet_workbook.sheetnames:
            suffix += 1
        sheet_name = f"{base_name}_{suffix}"
        app_logger.warning(f"Duplicate sheet name detected, renamed to: {sheet_name}")
    # Handle empty input
    if not workbook_content:
        app_logger.warning(f"No content to write for sheet: {sheet_name}")
        spreadsheet_workbook.create_sheet(sheet_name)
        return spreadsheet_workbook
    # Create the sheet in the Workbook
    spreadsheet_workbook.create_sheet(sheet_name)
    spreadsheet_sheet = spreadsheet_workbook[sheet_name]
    # CSV header
    csv_header = list(workbook_content[0].keys())
    # Custom column ordering (sort the ones specified, add back all the rest)
    if custom_column_ordering:
        # Keep specified columns first (only if they exist in the data)
        custom_csv_header = [col for col in custom_column_ordering if col in csv_header]
        # Append remaining columns not in the custom order
        custom_csv_header += [col for col in csv_header if col not in custom_column_ordering]
    else:
        custom_csv_header = csv_header
    try:
        # Write the content (using a numbered map)
        spreadsheet_column_map = {i + 1: col for i, col in enumerate(custom_csv_header)}
        spreadsheet_sheet.append(spreadsheet_column_map)
        # Content (get the position number from the header map), for each row...
        for row in workbook_content:
            row_map = {
                i + 1: row.get(col)  # returns None if key missing, no KeyError
                for i, col in enumerate(custom_csv_header)
            }
            spreadsheet_sheet.append(row_map)
        # Apply styling to worksheet
        spreadsheet_sheet = apply_styling_to_spreadsheet(spreadsheet_sheet, freeze_header, freeze_first_column)
        # Print console message
        app_logger.info(f'Writing spreadsheet: {sheet_name}')
    except Exception as e:
        app_logger.error(f'Cannot write spreadsheet {sheet_name}! (Reason: {e})')
        app_logger.debug(traceback.format_exc())
    # Return the same Workbook as input but with the added sheet
    return spreadsheet_workbook

## Write spreadsheet to file
def write_workbook(spreadsheet_workbook: openpyxl.Workbook, output_file_name: str, remove_default_empty_sheet=True) -> bool:
    """Write a Workbook to file"""
    # Exit if there is no content
    if not spreadsheet_workbook: return False
    # Initialise output
    file_written = False
    # Remove the default empty sheet
    if remove_default_empty_sheet:
        spreadsheet_workbook = remove_default_empty_sheet_from_workbook(spreadsheet_workbook)
    # Fix the filename
    if not output_file_name: output_file_name = 'Spreadsheet'
    if not output_file_name.endswith('.xlsx'): output_file_name = output_file_name + '.xlsx'
    # Save the file (not if empty)
    try:
        if len(spreadsheet_workbook.worksheets) > 0:
            spreadsheet_workbook.save(output_file_name)
            file_written = True
            app_logger.info(f'Successfully written file to {output_file_name}!')
    except:
        file_written = False
        app_logger.error(f'Failed to write file to {output_file_name}!')
        app_logger.debug(traceback.format_exc())
    # return
    return file_written
