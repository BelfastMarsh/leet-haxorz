import pandas as pd
import numpy as np

mig_df = pd.read_csv('C:\\Users\\Hackathon_05\\Downloads\\PEA15.20250402T130435.csv')
print(mig_df.head())

mig_filtered = mig_df[mig_df['Component'] == 'Net migration']
mig_filtered = mig_filtered[mig_filtered['Year'] >= 2010]
print(mig_filtered)




potato_df = pd.read_csv('C:\\Users\\Hackathon_05\\Downloads\\AQA04.20250402T130456.csv')
print(potato_df.head())

potato_filtered = potato_df[potato_df['Type of Crop'] == 'Potatoes']
potato_filtered = potato_filtered[potato_filtered['Year'] >= 2010] 
potato_filtered = potato_filtered[potato_filtered['Statistic Label'] == 'Crop Production']
print(potato_filtered)


