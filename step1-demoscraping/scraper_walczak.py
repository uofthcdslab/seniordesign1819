# -*- coding: utf-8 -*-

import urllib3
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# make a web service call to get html page
http = urllib3.PoolManager()
url = 'https://itmdapps.milwaukee.gov/MPDCallData/'
response = http.request('GET', url)

# format html page into beautiful soup object
soup = BeautifulSoup(response.data, 'lxml')

# find table and its corresponding cells
table_cells = soup.find('tbody').find_all('td')

Call_Number = []
Datetime = []
Location = []
Police_District = []
Nature_of_Call = []
Status = []

data = {0 : Call_Number, 1 : Datetime, 2 : Location, 3 : Police_District, 
         4 : Nature_of_Call, 5 : Status}

column_index = 0

for table_cell in table_cells:
    
    strings_to_replace = [r'''<td style="border: 1px solid black; border-collapse: collapse;">''',r"</td>",r'''<td style="border: 1px solid black; border-collapse: collapse; text-align: center;">''']
    for string in strings_to_replace:
        table_cell = str(table_cell)
        table_cell = table_cell.replace(string, '')
    
    # update data with the table cell from web page with its corresponding index for column
    data[column_index].append(table_cell)
    
    column_index += 1
    if column_index == len(data):
        column_index = 0
        
df = pd.DataFrame.from_dict(data)
df.columns = ['Call_Number','Datetime','Location','Police_District','Nature_of_Call','Status']

# get time data was uploaded for logging purposes
df['Datetime_Created'] = datetime.now()

df.to_csv('MKE_Dispatched_Calls', mode='a', header=False)
