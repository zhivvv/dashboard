# From settings file
version = '6+6'
base_location = '/Users/ivanov.ev/Work/Dashboard'


# Extract folders
fem_folder_extract = f'{base_location}/fem/loading/{version}'

# Extract files
mapping_file_extract = f'{base_location}/mapping/mapping_main.xlsx'
sip_file_extract = f'{base_location}/sip/data/sip.xlsx'
OPENPYXL_EXTRACTION_PATH = f'{base_location}/openpyxl/openpyxl_test.xlsx'

# Results folder
fem_folder_results = f'{base_location}/fem/results'
mapping_folder_results = f'{base_location}/mapping/results'
sip_folder_results = f'{base_location}/sip/results'
report_folder_results = f'{base_location}/reports'
calculation_folder_results = f'{base_location}/reports'

# Sheet names
sip_sheet_name = 'Свод'
fem_sheet_name = 'Основной лист'
openpyxl_sheet_name = 'openpyxl'
mapping_sheet_name = 'mapping'

# Write a function that creates structure of files and folders

if __name__ == '__main__':
    pass
