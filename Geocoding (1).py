# This is an exploratory test of Geocodio API services.  API key: b42752c85bb22c5b5e924be26276bb246257c25
# 
# The website can be found here:https://www.geocod.io/
# Username:john.kearns@marquette.edu
# Password:Senior_DesigN18!


import pandas as pd
from geocodio import GeocodioClient
from gis_san_lst import gis_san_lst_0,gis_san_lst_1

def clean_data(df):
    temp = df.copy()
    client = GeocodioClient("b42752c85bb22c5b5e924be26276bb246257c25")
    temp.columns = ["call_number", "date_time", "location", "district", "nature", "status"]
    temp["cords"] = 'a'
    temp['location'] = temp['location'].str[0]
    for i in range(len(temp)):
        #clean and add milwaukee to address
        if(temp.iloc[i,2].find('MKE') !=-1):
            temp.iloc[i,2] = temp.iloc[i,2].replace('MKE','MILWAUKEE')
        else:
            temp.iloc[i,2] = temp.iloc[i,2]+ ', MILWAUKEE'

        #clean up address
        temp.iloc[i,2] = gis_san_lst_1(temp.iloc[i,2])

        #enter cordinates
        geocoded_location = client.geocode(temp.iloc[i,2])
        temp.iloc[i,6] = geocoded_location.coords
        
    return temp

