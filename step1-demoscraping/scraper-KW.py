
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib.request as re

soup=bs(re.urlopen('https://itmdapps.milwaukee.gov/MPDCallData/'), 'html.parser')

table=soup.find('tbody')
l=len(table.find_all('tr'))
#print(l)
raw=pd.DataFrame(columns={'Call Number', 'Date/Time','Location','Police District', 'Nature of Call','Status'}, index={0:200} )

row_marker=0
for row in table.find_all('tr'):
    row_marker+=1
    column_marker=0
    columns=row.find_all('td')
    for column in columns:
        raw[row_marker,column_marker]=column.get_text()
        column_marker+=1
	#row_marker+=1
#So all of the data is technically in the file, its just formatted in a very awkward way for humans to read. In interest of time, I have elected not to reshape and prettify the csv except in the unlikely case the group decides to go ahead with my implementation
raw.to_csv('rawCallData.csv', sep='\t')
