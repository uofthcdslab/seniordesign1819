# This is an exploratory test of Geocodio API services.  API key: b42752c85bb22c5b5e924be26276bb246257c25
# The website can be found here:https://www.geocod.io/

import pandas as pd
from geocodio import GeocodioClient
from Address_Dictionary import address_dictionary_1 #,address_dictionary_2
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
    
    # retrieve all addresses previously geocoded
    coordinate_df = pd.read_csv('Coordinate_Dictionary.csv')
    
    for i, row in temp.iterrows():
        
        # use address dictionary for coordinates if location exists in address dictionary
        location = temp.loc[i,'Location']
        if location in coordinate_df['Location'].unique():
            temp.loc[i,'Cleaned_Location'] = coordinate_df.loc[coordinate_df['Location'] == location, 'Cleaned_Location'].iloc[0]
            temp.loc[i,'Coordinates'] = coordinate_df.loc[coordinate_df['Location'] == location,'Coordinates'].iloc[0]
            continue
        
        # add milwaukee, WI to address if not already present
        if 'MKE' in temp.loc[i,'Cleaned_Location']:
            temp.loc[i,'Cleaned_Location'] = temp.loc[i,'Cleaned_Location'].replace('MKE',' MILWAUKEE, WI')
        else:
            temp.loc[i,'Cleaned_Location'] = temp.loc[i,'Cleaned_Location']+ ', MILWAUKEE, WI'

        # clean addresses of common abbreviations and typos
        temp.loc[i,'Cleaned_Location'] = address_dictionary_1(temp.loc[i,'Cleaned_Location'])

        # get and record coordinates of given address
        try:
            geocoded_location = client.geocode(temp.loc[i,'Cleaned_Location'])
        # catch error when our api key has run out of calls
        except:
            print('No calls remaining...')
#### TODO: Check whether data is written to csv when we have run out of calls...
            # save all processed addresses only
            temp = temp.loc[temp['Cleaned_Location'] != '', :]
            # last failed call will go in csv... we don't want that...
            temp = temp.drop(df.tail(1).index,inplace=True)
            break
        
        # check whether data exists (works perfectly fine, but can be improved)
        if len(geocoded_location['results']) > 0:
            
            coordinates = str(geocoded_location['results'][0]['location'])
            
            # add new coordinates to coordinate dictionary
            coordinate_entry = pd.DataFrame({'Location':[temp.loc[i,'Location']],
                                             'Cleaned_Location':[temp.loc[i,'Cleaned_Location']],
                                             'Coordinates':[coordinates]
                                             })
            coordinate_df = coordinate_df.append(coordinate_entry, ignore_index=True)
        # log errors
        else:            
            coordinates = ''
            temp.loc[i,'Error_Logging'] = str(geocoded_location)
            error = pd.DataFrame({'location':[temp.loc[i,'Location']],
                                  'cleaned_location':[temp.loc[i,'Cleaned_Location']],
                                  'geocoding_result':[temp.loc[i,'Error_Logging']]})
            error.to_csv('../geocoding_data/Error_Logging.csv', mode='a', header=False)

        temp.loc[i,'Coordinates'] = coordinates
        
    coordinate_df.to_csv('Coordinate_Dictionary.csv',index=False,mode='w')
    return temp

data_path = '../data/'
geocoding_data_path = '../geocoding_data/'

f = []
for (dir_path, dir_names, file_names) in walk(data_path):
    f.extend(file_names)
    break
if 'readme.txt' in file_names:
    file_names.remove('readme.txt')

for file_name in file_names:
    
    data_df = pd.read_csv(data_path+file_name)
    length_of_data_df = data_df.shape[0]
    
    file = Path(geocoding_data_path+file_name)
    
    # check whether a geocoding data file has already been generated
    if file.is_file():
        geocoding_data_df = pd.read_csv(geocoding_data_path+file_name)
        length_of_geocoding_data_df = geocoding_data_df.shape[0]
        remaining_instances = length_of_data_df - length_of_geocoding_data_df
        
        # geocoding file already exists and only some addresses have been converted to coordinates
        if remaining_instances > 0:
            result = clean_data(data_df.tail(remaining_instances))
            result.to_csv(geocoding_data_path+file_name,mode='a',header=False)
            
        # geocoding file already exists and all addresses have been converted to coordinates
        else:
            print(file_name)
            continue
        
    # geocoding file does not exist
    else:
        result = clean_data(data_df)
        result.to_csv(geocoding_data_path+file_name)
        
    print(file_name)
        
    # if no calls are remaining, then break out of loop
    geocoding_data_df = pd.read_csv(geocoding_data_path+file_name)
    length_of_geocoding_data_df = geocoding_data_df.shape[0]
    if length_of_data_df > length_of_geocoding_data_df:
        break
        

