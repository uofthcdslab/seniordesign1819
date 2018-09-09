
# coding: utf-8

# In[1]:


import pandas as pd 
import csv
from bs4 import BeautifulSoup
import requests
import time
from time import gmtime, strftime


# In[2]:


def periodic_work(interval):
    while True:
        url = requests.get('https://itmdapps.milwaukee.gov/MPDCallData/index.jsp?district=All')

        outfile = open("calls.csv","w",newline='')
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        
        soup = BeautifulSoup(url.text,"lxml")
        table_tag = soup.select("table")[0]
        tab_data = [[item.text for item in row_data.select("th,td")]
                        for row_data in table_tag.select("tr")]
        
        for data in tab_data:
            writer.writerow(data)
            
        outfile.close()
        
        calls = pd.read_csv('calls.csv', skiprows=1)
        calls['Date/Time Scraped'] = strftime("%Y-%m-%d %I:%M:%S:%p", time.localtime())
        policeCalls = pd.read_csv('PoliceCalls.csv').iloc[:, 1:] 
        #calls.to_csv('PoliceCalls.csv', sep=',', encoding='utf-8')
        
        dfs = [calls, policeCalls]
        result = pd.concat(dfs)
        
        result.to_csv('PoliceCalls.csv', sep=',', encoding='utf-8')
        display(result.head(2), len(result))

        #interval should be an integer, the number of seconds to wait
        time.sleep(interval)


# In[3]:


periodic_work(360)

