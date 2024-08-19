#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com / manuel.galli@revvity.com
# Updated date: 2024-08-19
#####

## Import libraries and functions
import openpyxl
from report_handling.remove_default_empty_sheet_from_workbook import remove_default_empty_sheet_from_workbook

## Write spreadsheet to file
def write_workbook(spreadsheet_workbook: openpyxl.Workbook, output_folder='', file_name='', remove_default_empty_sheet=True) -> None:
    # Remove the default empty sheet
    if remove_default_empty_sheet:
        spreadsheet_workbook = remove_default_empty_sheet_from_workbook(spreadsheet_workbook)
    # Fix the filename
    if file_name is None or file_name == '':
        file_name = 'Spreadsheet'
    if not file_name.endswith('.xlsx'):
        file_name = file_name + '.xlsx'
    if output_folder is not None and output_folder != '':
        file_name = output_folder + '/' + file_name
    # Save the file (not if empty)
    if len(spreadsheet_workbook.worksheets) > 0:
        spreadsheet_workbook.save(file_name)