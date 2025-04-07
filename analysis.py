import kagglehub
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

# Download latest version
path = kagglehub.dataset_download("khafre/elizabeth-station-air-quality-monitoring")

print("Path to dataset files:", path)

folder_path = r'C:\Users\danie\.cache\kagglehub\datasets\khafre\elizabeth-station-air-quality-monitoring\versions\1'

# Find all CSV files in the directory
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Read each CSV and concatenate into one DataFrame
df_list = [pd.read_csv(file) for file in csv_files]
df_combined = pd.concat(df_list, ignore_index=True)

print(df_combined.head())
print(df_combined.info())

def parse_mixed_dates(date_str):
    try:
        return pd.to_datetime(date_str, format="%d/%m/%Y %H:%M")  # 24-hour format
    except ValueError:
        try:
            return pd.to_datetime(date_str, format="%d/%m/%Y %I:%M %p")  # 12-hour AM/PM format
        except ValueError:
            return pd.NaT  # If it still fails, return NaT

# Apply function to column
df_combined['Date/Time'] = df_combined['Date/Time'].apply(parse_mixed_dates)

# Sort DataFrame by Date/Time
df_combined = df_combined.sort_values(by='Date/Time')

# Confirm sorting
print(df_combined.head())
print(df_combined.tail())
print(df_combined.columns)

# Fix the date format
df_combined['Date/Time'] = pd.to_datetime(df_combined['Date/Time'])
df_combined.set_index('Date/Time', inplace=True)

# Plot the data
df_combined[['O3 UVA ppm', 'NO Chemiluminescence ppm', 'CO GPC ppm']].plot()
plt.show()

# Plot the missing data
plt.figure(figsize=(12,4))
df_combined['O3 UVA ppm'].isnull().resample('M').mean().plot(kind='bar')
plt.ylabel('Fraction of Missing Data')
plt.title('Fraction of Missing O3 UVA Data by Month')
plt.show()

# check for missing data between 2020 and 2022
missing_data = df_combined['2020':'2022']
print(missing_data.isna().mean())

# how many 03 data points are there?
num_o3 = df_combined.loc['2014':'2018', 'O3 UVA ppm'].count()
print(f'Number of O3 data points (2014-2018): {num_o3}')

# peak NO2 concentration
peak_no2 = df_combined.loc['2014':'2018', 'NO Chemiluminescence ppm'].max()
print(f'Peak NO2 concentration (2014-2018): {peak_no2}')

# plot the conentration of NO2 over time
df_combined.loc['2014':'2018', 'NO Chemiluminescence ppm'].plot(kind='line')
plt.xlabel('Date')
plt.ylabel('NO2 concentration (ppm)')
plt.title('NO2 concentration over time (2014-2018)')
plt.show()

# plot the concentration of NO2 in 2014
df_combined.loc['2014', 'NO Chemiluminescence ppm'].plot(kind='line')
plt.xlabel('Date')
plt.ylabel('NO2 concentration (ppm)')
plt.title('NO2 concentration in 2014')
plt.show()

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# Select data between 2014 and 2018
df_period = df_combined.loc['2014':'2018']

# Prepare monthly NO2 averages
monthly_no2 = df_period['NO2 calc Chemiluminescence ppm'].resample('M').mean().to_frame()
monthly_no2['Year'] = monthly_no2.index.year
monthly_no2['Month'] = monthly_no2.index.month
pivot_no2 = monthly_no2.pivot(index='Month', columns='Year', values='NO2 calc Chemiluminescence ppm')

# Prepare monthly O3 averages
monthly_o3 = df_period['O3 UVA ppm'].resample('M').mean().to_frame()
monthly_o3['Year'] = monthly_o3.index.year
monthly_o3['Month'] = monthly_o3.index.month
pivot_o3 = monthly_o3.pivot(index='Month', columns='Year', values='O3 UVA ppm')

# Plotting stacked vertically
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Plot NO2
pivot_no2.plot(ax=ax1, marker='o', legend=True)
ax1.set_title('Average Monthly NO₂ Concentration (2014-2018)')
ax1.set_ylabel('NO₂ concentration (ppm)')
ax1.grid(False)
ax1.legend(title='Year')

# Plot O3
pivot_o3.plot(ax=ax2, marker='o', legend=False)
ax2.set_title('Average Monthly O₃ Concentration (2014-2018)')
ax2.set_ylabel('O₃ concentration (ppm)')
ax2.set_xlabel('Month')
ax2.grid(False)
ax2.set_xticks(range(1,13))
ax2.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])

plt.tight_layout()
# Save the figure (add this line)
plt.savefig('Figures/no2_o3_monthly_avg.png', dpi=300, bbox_inches='tight')
plt.show()