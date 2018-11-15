# This is an exploratory test of Geocodio API services.  API key: b42752c85bb22c5b5e924be26276bb246257c25
# The website can be found here:https://www.geocod.io/

import pandas as pd
from geocodio import GeocodioClient
from Address_Dictionary import address_dictionary_1 #,address_dictionary_2
import numpy as np

def clean_data(df):
    
    # setup dataframe
    temp = df.copy()
    
    # set up api keys to be used
    api_keys = [
        'b42752c85bb22c5b5e924be26276bb246257c25',
        'bb553e0bbff5b333b8bb9555a93b976f55e3e35',
        'e3b53edefba3e7a34673473470bf4a5e0fb765e',
        '6589fabe9f95daba2a255e9eb21fe111a55959a'
        ]
    current_key = 0
    client = GeocodioClient(api_keys[current_key])
    print('using key:')
    print(api_keys[current_key])
    
    for i, row in temp.iterrows():
        # if data is already processed skip
        if temp.loc[i,'Error'] == False or temp.loc[i,'Error'] == True:
            continue
        
        # if the cleaned location is empty, set up the address to be cleaned
        if np.isnan(temp.loc[i,'Cleaned_Location']) or temp.loc[i,'Cleaned_Location'] == '':
            temp.loc[i,'Cleaned_Location'] = temp.loc[i,'Location']
        
        # add milwaukee, WI to address if not already present
        if 'MILWAUKEE, WI' not in temp.loc[i,'Cleaned_Location']:
            if 'MKE' in temp.loc[i,'Cleaned_Location']:
                temp.loc[i,'Cleaned_Location'] = temp.loc[i,'Cleaned_Location'].replace('MKE',' MILWAUKEE, WI')
            else:
                temp.loc[i,'Cleaned_Location'] = temp.loc[i,'Cleaned_Location']+ ', MILWAUKEE, WI'

        # clean addresses of common abbreviations and typos
        temp.loc[i,'Cleaned_Location'] = address_dictionary_1(temp.loc[i,'Cleaned_Location'])
        
        # loop through api keys until a key works, otherwise save data
        while len(api_keys) > current_key:
            client = GeocodioClient(api_keys[current_key])
            try:
                # get and record coordinates of given address
                geocoded_location = client.geocode(temp.loc[i,'Cleaned_Location'])
                break
            except:
                print('using next key...')
                current_key = current_key + 1
        if len(api_keys) <= current_key:
            print('no more keys remaining...')
            return temp            
        
        # check whether data exists (works perfectly fine, but can be improved)
        if len(geocoded_location['results']) > 0:
            coordinates = dict(geocoded_location['results'][0]['location'])
            temp.loc[i,'Latitude'] = coordinates['lat']
            temp.loc[i,'Longitude'] = coordinates['lng']
            temp.loc[i,'Error'] = False
            
        # log errors
        else:            
            temp.loc[i,'Error'] = True

    return temp

data_path = '../data/'
file_name = 'addresses.csv'

data_df = pd.read_csv(data_path+file_name)
result = clean_data(data_df)
result.to_csv(data_path+file_name,index=False)
print('done')