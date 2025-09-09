import openpyxl
import os
from file_name_check.parse_name import parse_file_name, check_for_company, check_for_contract


def list_sheets(file_path):
    try:
        # Load the workbook
        workbook = openpyxl.load_workbook(file_path, read_only=True)
        
        # Get all sheet names
        sheets = workbook.sheetnames
        
        print("Sheets in the Excel file:")
        for sheet in sheets:
            print(f"- {sheet}")
            
    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    file_path = "./services/excel_preprocess/tests/data/format1/Quotation_Q2502BCN02373_CHROBI_538.xlsx"  # Replace with the path to your Excel file

    # first chec
    list_sheets(file_path)