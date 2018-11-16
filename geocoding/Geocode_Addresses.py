# This is an exploratory test of Geocodio API services.
# The website can be found here:https://www.geocod.io/

import pandas as pd
from geocodio import GeocodioClient
from Address_Dictionary import address_dictionary_1 #,address_dictionary_2

def clean_data(df):
    
    # setup dataframe
    temp = df.copy()
    temp['Cleaned Location'] = temp['Cleaned Location'].fillna('')
    
    # set up api keys to be used
    api_keys = [
        'b42752c85bb22c5b5e924be26276bb246257c25',
        'bb553e0bbff5b333b8bb9555a93b976f55e3e35',
        'e3b53edefba3e7a34673473470bf4a5e0fb765e',
        '6589fabe9f95daba2a255e9eb21fe111a55959a',
        'a27856bccaec6b36eba866877e60262bc83e535',
        '5611b20511d00d6365e6eb10b51e1e0e562a02e'
        ]
    current_key = 0
    client = GeocodioClient(api_keys[current_key])
    print('using key:', api_keys[current_key])
    
    for i, row in temp.iterrows():
        # if data is already processed skip
        if temp.loc[i,'Error'] == False or temp.loc[i,'Error'] == True:
            continue
        
        # if the cleaned location is empty, set up the address to be cleaned
        if not temp.loc[i,'Cleaned Location']:
            temp.loc[i,'Cleaned Location'] = temp.loc[i,'Location']
        
        # add Milwaukee, WI to address if not already present
        if 'MILWAUKEE, WI' not in temp.loc[i,'Cleaned Location']:
            if 'MKE' in temp.loc[i,'Cleaned Location']:
                temp.loc[i,'Cleaned Location'] = temp.loc[i,'Cleaned Location'].replace('MKE',' MILWAUKEE, WI')
            else:
                temp.loc[i,'Cleaned Location'] = temp.loc[i,'Cleaned Location']+ ', MILWAUKEE, WI'

        # clean addresses of common abbreviations and typos
        temp.loc[i,'Cleaned Location'] = address_dictionary_1(temp.loc[i,'Cleaned Location'])
        
        # loop through api keys until a key works, otherwise save data
        while len(api_keys) > current_key:
            try:
                # get and record coordinates of given address
                geocoded_location = client.geocode(temp.loc[i,'Cleaned Location'])
                break
            except:
                current_key += 1
                if len(api_keys) <= current_key:
                    print('no more keys remaining...')
                    return temp            
                client = GeocodioClient(api_keys[current_key])
                print('using next key: ', api_keys[current_key])
        
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