# From settings file
version = '6+6'
base_location = '/Users/ivanov.ev/Work/Dashboard'


# file_folders


# Extract files
# fem_extract = (f'{base_location}/fem/loading/{version}', 'Основной лист')
# sip_extract = (f'{base_location}/fem/loading/{version}', 'Свод')
fem_folder_extract = f'{base_location}/fem/loading/{version}'
sip_file_extract = f'{base_location}/sip/data/sip.xlsx'
mapping_file_extract = f'{base_location}/mapping/mapping_main.xlsx'
fem_extraction_results = f'{base_location}/fem/results/extraction_07102022.xlsx'
sip_extraction_results = f'{base_location}/sip/results/*.xlsx'
OPENPYXL_EXTRACTION_PATH = f'{base_location}/openpyxl/openpyxl_test.xlsx'

# Sheet names
sip_sheet_name = 'Свод'
fem_sheet_name = 'Основной лист'
openpyxl_sheet_name = 'openpyxl'

# Folders to save files
fem_folder_save = f'{base_location}/fem/results'
sip_folder_save = f'{base_location}/sip/results'
mapping_folder_save = f'{base_location}/mapping/results'

# Write a function that creates structure of files and folders

if __name__ == '__main__':
    pass
