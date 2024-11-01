#  Copyright (c) 2024.
import pandas as pd
import os


store_location = r'C:\Users\64guu\Documents\UT - Computer Science\Thesis lokaal\Validation\for_latex'

df_overall = pd.read_csv(r'results/transformation_results 2024-10-21 12-57-22 Special Letters allowed.csv')

# df_overall_success = df_overall[df_overall['transformation_successful']]
# df_overall_success = df_overall_success[['model', 'n_classes', 'transformation_time_s', 'atl_warnings_present', 'generated_code_compiles']]
# df_overall_success['transformation_time_s'] = df_overall_success['transformation_time_s'].round(2)
# print(f"Length of df_overall_success = {len(df_overall_success)}")
# print(df_overall_success)
# df_overall_success.to_csv(os.path.join(store_location, '79 successful.csv'))



df_fault_modes = pd.read_csv(
    r'results/transformation_results 2024-10-21 12-57-22 Special Letters allowed fault modes analysed.csv')

df_fault_modes = df_fault_modes[['model', 'compile_error_category', 'compile_error_category_detail']]
print(df_fault_modes)

df_fault_modes.to_csv(os.path.join(store_location, 'faultmodes.csv'))
