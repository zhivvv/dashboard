import settings
import pandas as pd
import func

sip_folder_path = '/Users/ivanov.ev/Work/Dashboard/sip'
sip_data = 'Свод_СИП_2023-2025_v20.xlsx'
sip_meta = 'meta.xlsx'
sip_data_sheet_name = 'Свод'
sip_meta_sheet_name = 'meta'
sip_data_path = os.path.join(sip_folder_path, sip_data)
sip_meta_path = os.path.join(sip_folder_path, sip_meta)

sip_data_file = pd.read_excel(sip_data_path, sheet_name=sip_data_sheet_name)
sip_meta_file = pd.read_excel(sip_meta_path, sheet_name=sip_meta_sheet_name)
df = sip_data_file
columns = sip_meta_file

df.columns = list(df.loc[0,])
df = df.loc[1:,]
columns = columns.dropna()
rename = columns.set_index([columns.columns.to_list()[0]]).to_dict()[columns.columns.to_list()[1]]
df = df.rename(columns=rename)[list(rename.values())]

categorical_data = ['programme', 'code', 'project', 'investment object', 'allocation', 'criticality', 'sanctions', 'expert_opinion', 'effect_type', 'investment_category', 'investment_goal', 'scenario', 'stage', 'bucket', 'platform', 'architecture_appraisal_platform', 'dbms', 'architecture_appraisal_dbms', 'operational_system', 'architecture_appraisal_os', 'infrastructure', 'architecture_appraisal_inf', 'in_prod', 'portfel', 'circulation', 'challenge_2022']
metric_data = ['factcapexopex_2022', 'capex_2022', 'capex_2022/1', 'capex_2023/2','capex_2024', 'capex_2025', 'capex_2026', 'capex_2027', 'opex_2022', 'opex_2023/1', 'opex_2023/2', 'opex_2024', 'opex_2025', 'opex_2026','opex_2027', 'npv_2022', 'npv_2023', 'npv_2024', 'npv_2025', 'npv_2026','npv_2027', 'npv_2028', 'npv_2029', 'npv_2030', 'umv_2022', 'umv_2023','umv_2024', 'umv_2025', 'umv_2026', 'umv_2027', 'umv_2028', 'umv_2029','umv_2030', 'dmv_2022', 'dmv_2023', 'dmv_2024', 'dmv_2025', 'dmv_2026', 'dmv_2027', 'dmv_2028', 'dmv_2029', 'dmv_2030', 'capexinvestmentdecision_2023', 'opexinvestmentdecision_2023', 'budgeteconomy_2023']

id_vars = categorical_data
value_vars = list(set(df.columns) - set(categorical_data))
check_list = id_vars + value_vars
print('Without data missing - ', set(df.columns.to_list()) == set(check_list))

# df = pd.melt(df, id_vars=id_vars, var_name='metrics', value_name='value', )
# df['metrics'] = df['metrics'].astype('int')
df = df.melt(id_vars=categorical_data,
             value_vars=value_vars,
             var_name='metrics',
             value_name='value',
             ignore_index=False)
df[['metric', 'year']] = df['metrics'].str.split('_', expand=True)
df = df.drop(columns=['metrics'])
func.safe_dataframes_to_excel(dataframes=[df],
                              sheet_names=['sip'],
                              folder_to_save=settings.sip_save,
                              file_name='sip')


if __name__ == '__main__':
    pass