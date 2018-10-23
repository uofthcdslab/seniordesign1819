# This is an exploratory test of Geocodio API services.  API key: b42752c85bb22c5b5e924be26276bb246257c25
# The website can be found here:https://www.geocod.io/

import pandas as pd
from geocodio import GeocodioClient
from Address_Dictionary import address_dictionary_1,address_dictionary_2
from os import walk
from pathlib import Path

def clean_data(df):
    
    # setup dataframe and geocodio client
    temp = df.copy()
    client = GeocodioClient("b42752c85bb22c5b5e924be26276bb246257c25")
    
    # add additional columns
    temp['Cleaned_Location'] = temp['Location']
    temp['Coordinates'] = ''
    temp['Error_Logging'] = ''
    
    for i, row in temp.iterrows():
        
        # add milwaukee to address if not already present
        if 'MKE' in temp.loc[i,'Cleaned_Location']:
            temp.loc[i,'Cleaned_Location'] = temp.loc[i,'Cleaned_Location'].replace('MKE','MILWAUKEE')
        else:
            temp.loc[i,'Cleaned_Location'] = temp.loc[i,'Cleaned_Location']+ ', MILWAUKEE'

        # clean addresses of common abbreviations and typos
        temp.loc[i,'Cleaned_Location'] = address_dictionary_1(temp.loc[i,'Cleaned_Location'])

        # get and record coordinates of given address
        
        geocoded_location = client.geocode(temp.loc[i,'Cleaned_Location'])
        
        if len(geocoded_location['results']) > 0:
            coordinates = str(geocoded_location['results'][0]['location'])
        else:
            coordinates = ''
            temp.loc[i,'Error_Logging'] = str(geocoded_location)
            error = pd.DataFrame({'location':temp['Cleaned_Location'],'geocoding_result':temp['Error_Logging']})
            error.to_csv('../geocoding_data/Error_Logging.csv', mode='a', header=False)

        temp.loc[i,'Coordinates'] = coordinates
        
    return temp

data_path = '../data/'
geocoding_data_path = '../geocoding_data/'

remaining_calls = 2500

f = []
for (dir_path, dir_names, file_names) in walk(data_path):
    f.extend(file_names)
    break
if 'readme.txt' in file_names:
    file_names.remove('readme.txt')

for file_name in file_names:
    print(file_name)
    df = pd.read_csv(data_path+file_name)
    
    # 2500 max calls per day
    # average daily-file contains ~1500 rows
    # does file already exist with more than x rows?
    file = Path(geocoding_data_path+file_name)
    if file.is_file():
        continue
    # do we have enough calls remaining to continue?
    if df.shape[0] > remaining_calls:
        continue
    else:
        remaining_calls = remaining_calls - df.shape[0]
        result = clean_data(df)
        result.to_csv(geocoding_data_path+file_name)
        print(result.head(3))

