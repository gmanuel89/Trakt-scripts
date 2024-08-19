#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com / manuel.galli@revvity.com
# Updated date: 2022-10-07
#####

## Import libraries and functions
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

## Apply styling to spreadsheet
def apply_styling_to_spreadsheet(spreadsheet_sheet: Worksheet) -> Worksheet:
    # Freeze the header
    spreadsheet_sheet.freeze_panes = 'B2'
    # Make the header bold
    for col in range(spreadsheet_sheet.max_column):
        cell_letter = get_column_letter(col+1)
        spreadsheet_sheet[cell_letter+'1'].font = Font(bold=True)
    # Autoresize columns
    for col_index, col in enumerate(spreadsheet_sheet.columns, 1):
        spreadsheet_sheet.column_dimensions[get_column_letter(col_index)].auto_size = True
    # return
    return spreadsheet_sheet

