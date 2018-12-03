import os
import pandas as pd
from datetime import datetime as dt

# Read raw data in
root = os.path.expanduser('data/')

files = [root + f for f in os.listdir(root) if f.endswith('.csv') and f != 'addresses.csv']
dfs = [pd.read_csv(f, header=0, index_col=0, parse_dates=['Date/Time']) for f in files]
df = pd.concat(dfs)

addrDB = pd.read_csv('data/addresses.csv', header=0, index_col=0)

# Function to get the date of a given address
def geoLoc(addr):
    if addr in addrDB.index:
        return [addrDB.loc[addr, 'Latitude'], addrDB.loc[addr, 'Longitude']]
    return ['', ''];

# Function to get a set of data
def filter(startDate='', endDate='', dayOfWeek=-1, call='', nature='', status='', doGeoLoc=False):
    filtered = df
    if call != '':
        filtered = filtered[filtered['Call Number'] == call]
    if nature != '':
        filtered = filtered[filtered['Nature of Call'] == nature]
    if status != '':
        filtered = filtered[filtered['Status'] == status]
    if startDate != '':
        filtered = filtered[filtered['Date/Time'] >= dt.strptime(startDate, '%m/%d/%Y')]
    if endDate != '':
        filtered = filtered[filtered['Date/Time'] < dt.strptime(endDate, '%m/%d/%Y')]
    if dayOfWeek >= 0:
        filtered = filtered[filtered['Date/Time'].dt.dayofweek == dayOfWeek]
    if doGeoLoc:
        results = filtered.loc[:, 'Location'].apply(geoLoc)
        filtered[['Latitude', 'Longitude']] = pd.DataFrame(results.values.tolist(), index=results.index, columns=['Latitude', 'Longitude'])
    return filtered.sort_values(by='Date/Time')