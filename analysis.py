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
import matplotlib.pyplot as plt
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

