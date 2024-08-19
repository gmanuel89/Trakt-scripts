#####
# Author: Manuel Galli
# e-mail: gmanuel89@gmail.com
# Updated date: 2022-10-07
#####

## Import libraries
import csv

## Write CSV content into a file
def write_csv_file(csv_file_content: list[list] | list[dict], output_file_name: str) -> None:
    # Check output file name
    if output_file_name == '' : output_file_name = 'CSV file'
    if not output_file_name.endswith('.csv') : output_file_name = output_file_name + '.csv'
    # Write file content
    with open (output_file_name, 'w+', encoding='UTF8', newline='') as output_file:
        # If it is a list of row...
        if isinstance(csv_file_content[0], list):
            csv_writer = csv.writer(output_file)
            csv_writer.writerows(csv_file_content)
        elif isinstance(csv_file_content[0], dict):
            csv_writer = csv.DictWriter(output_file, fieldnames=csv_file_content[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(csv_file_content)
        else:
            import openpyxl
            if isinstance(csv_file_content, openpyxl.worksheet.worksheet.Worksheet):
                csv_writer = csv.writer(output_file)
                for row in csv_file_content.rows:
                    excel_output_row = []
                    for c in row:
                        excel_output_row.append(c.value)
                    csv_writer.writerow(excel_output_row)
            else:
                pass
