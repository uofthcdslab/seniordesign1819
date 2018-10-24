import pandas as pd
import os
import numpy as np

root = os.path.expanduser('~/raw_data/liam/')

files = [root + f for f in os.listdir(root) if f.endswith('.csv')]
dfs = [pd.read_csv(f, header=0, index_col=0, parse_dates=['Date/Time']) for f in files]
df = pd.concat(dfs)

print()
print('Rows:', len(df.index))
print('Unique Calls:', len(df['Call Number'].unique()))
print('Rows with missing data:', len(df[df.isnull().any(axis=1)].index))
print('Non-MKE Calls:', len(df[df['Location'].str.contains('MKE') == False]))
print('Unique Addresses:', len(df['Location'].value_counts()))
print()
print(df['Nature of Call'].value_counts())
print()
print(df['Status'].value_counts())
print()
print(df['Police District'].value_counts())
print()
print(df['Location'].value_counts())
print()
print(df[df['Police District'] == 'NLA'])

print()
print(df[df['Status'] == 'False Alarm (Weather Related)'])

pd.DataFrame(df['Nature of Call'].unique()).to_csv('natures.csv')
