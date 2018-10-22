# A simple scaper to download that latest call page and go through each row of the table
import urllib, os, sys, datetime
import pandas as pd

oneFile = sys.argv[1]
twoFile = sys.argv[2]

# open pandas db
one = pd.read_csv(oneFile, header=0, index_col=0)
two = pd.read_csv(twoFile, header=0, index_col=0)

# loop through each row
for index, row in two.iterrows():
    if index not in one.index:
        one.loc[index] = row

# save record
one.to_csv('merged-' + oneFile)
