# A simple scaper to download that latest call page and go through each row of the table
import urllib, os, sys
import pandas as pd
from bs4 import BeautifulSoup as BS

# get info for adding to file name
nameAppend = ''
if len(sys.argv) > 1:
    nameAppend = sys.argv[1]

# download the page
url = 'https://itmdapps.milwaukee.gov/MPDCallData/'
pageData = urllib.request.urlopen(url).read()
# pull the table out of the page (ignoring headers)
soup = BS(pageData, features='html.parser')
table = soup.tbody

# open pandas db
dbFile = 'logged-calls' + nameAppend + '.csv'
if not os.path.exists(dbFile):
    with open(dbFile, 'w+') as f:
        f.write('ID,Call Number,Date/Time,Location,Police District,Nature of Call,Status')
df = pd.read_csv(dbFile, header=0, index_col=0, parse_dates=['Date/Time'])

# loop through each row
for row in table.find_all('tr'):
    # get all the cells in the row
    cells = row.find_all('td')
    
    # get the content of each cell
    callNum = int(cells[0].contents[0])
    time = cells[1].contents[0]
    loc = cells[2].contents[0]
    dist = cells[3].contents[0]
    nature = cells[4].contents[0]
    status = cells[5].contents[0]
    rowId = str(callNum) + '-' + status

    # add to record
    if rowId not in df.index:
        df.loc[rowId] = [callNum, time, loc, dist, nature, status]
    else:
        existingData = df.loc[rowId]

print(df)

# save record
df.to_csv(dbFile)
