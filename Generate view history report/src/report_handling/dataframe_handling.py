## Import libraries
import pandas
import os

## Rename CSV headers
def rename_csv_headers(csv_content: pandas.DataFrame, renaming_map: dict) -> pandas.DataFrame:
    """Rename CSV headers"""
    # Return
    return csv_content.rename(columns=renaming_map)

## Sort CSV content (in form of dataframe)
def sort_csv_file(csv_file_content: pandas.DataFrame, column_names_to_sort_by: list[str], sort_type='ascending') -> pandas.DataFrame:
    """Sort CSV content (in form of dataframe)"""
    if len(column_names_to_sort_by) > 0:
        # Sort type
        if 'asc' in sort_type.lower():
            ascending_sorting = True
        else:
            ascending_sorting = False
        # Return the sorted values
        return csv_file_content.sort_values(by=column_names_to_sort_by, ascending=ascending_sorting)
    else:
        return csv_file_content

## Write CSV content (in form of dataframe) into a file
def write_csv_file(csv_file_content: pandas.DataFrame, output_file_name: str, custom_column_ordering=[]) -> None:
    """Write CSV content (in form of dataframe) into a file"""
    # Check output file name
    if output_file_name == '' : output_file_name = 'CSV file'
    if not output_file_name.endswith('.csv') : output_file_name = output_file_name + '.csv'
    # Custom column ordering (sort the ones specified, add back all the rest)
    csv_header = csv_file_content.columns.tolist()
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
    # Get the custom column ordering  
    csv_file_content = csv_file_content[custom_csv_header]
    # Write file content
    csv_file_content.to_csv(output_file_name, index=False)
    # return
    return None

## Write CSV content (in form of dataframe) into a spreadsheet file
def write_spreadsheet_file(csv_file_content: pandas.DataFrame, output_file_name: str, sheet_name='Sheet 1', custom_column_ordering=[], overwrite_existing_file=False) -> None:
    """Write CSV content (in form of dataframe) into a spreadsheet file"""
    # Check output file name
    if output_file_name == '' : output_file_name = 'XLSX file'
    if not output_file_name.endswith('.xlsx') : output_file_name = output_file_name + '.xlsx'
    # Truncate sheet name if too long
    if len(sheet_name) > 31:
        sheet_name = sheet_name[0:30]
    # Custom column ordering (sort the ones specified, add back all the rest)
    csv_header = csv_file_content.columns.tolist()
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
    # Get the custom column ordering  
    csv_file_content = csv_file_content[custom_csv_header]
    # Write file content
    if overwrite_existing_file:
        csv_file_content.to_excel(output_file_name, sheet_name=sheet_name, index=False)
    else:
        if not os.path.exists(output_file_name):
            csv_file_content.to_excel(output_file_name, sheet_name=sheet_name, index=False)
        else:
            with pandas.ExcelWriter(output_file_name, mode='a', engine='openpyxl') as excel_writer:
                csv_file_content.to_excel(excel_writer, sheet_name=sheet_name, index=False)
    # return
    return None
