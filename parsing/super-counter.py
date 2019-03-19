import shapefile
from pyproj import Proj, transform
import pandas as pd
from shapely.geometry import Point, Polygon
import sys
import accessDB as db
import os

# load in maps
ald = shapefile.Reader('../mapping/ald2016/alderman')
nbh = shapefile.Reader('../mapping/hoods/neighborhood')
pol = shapefile.Reader('../mapping/poldist/poldist')
ward = shapefile.Reader('../mapping/wards/ward')
city = shapefile.Reader('../mapping/corp/citylimit')

def getIn(sf, df, sfName):
    # create a new dataframe with just the coordinates
    coords = df[['Latitude', 'Longitude', 'Nature of Call']]
    coords = coords.dropna()
    # some empty are missed I guess
    coords = coords[coords['Latitude'] != '']
    coords = coords[coords['Longitude'] != '']

    # loop through shapes
    for i,shape in enumerate(sf.shapes()):
        points = []

        # loop through points of shape
        for point in shape.points:
            # parse points
            coord = [float('%.3f' % coord) for coord in point]
            # convert points
            x, y = transform(inProj, outProj, coord[0], coord[1])
            points.append((x, y))

        # make a polygon out of the points
        poly = Polygon(points)

        # find the district, ward, etc that a point is in
        for index, row in coords.iterrows():
            point = Point(row['Longitude'], row['Latitude'])
            if poly.contains(point):
                coords.loc[index, sfName] = i

    return coords

# converter for coordinates
inProj = Proj(init='EPSG:32054', preserve_units=True) # NAD27 Wisconsin South
outProj = Proj(proj='latlong', datum='WGS84', ellps='WGS84') # Latitude and Longitude

allCalls = db.filter(doGeoLoc=True)

# remove duplicate calls
allCalls = allCalls.drop_duplicates(subset='Call Number')#[0:1000]

# use top 25 calls
natures = ['All'] + list(allCalls['Nature of Call'].value_counts()[:25].index
)
# get all regions
coords = getIn(pol, allCalls, 'Region')
counts = coords['Region'].value_counts()

# make header of table
columns = ['Nature'] + list(coords['Region'].unique()) + ['Total']
print(columns)

countTab = []

i = 0
# for every nature
for nature in natures:
    # gather all calls
    if nature == 'All':
        selection = coords
    else:
        selection = coords[coords['Nature of Call'] == nature]

    # compute numbers for nature
    counts = selection['Region'].value_counts()
    countTab.append([nature] + ([0] * (len(columns)-1)))
    for idx,count in counts.iteritems():
        if idx in columns:
            countTab[i][columns.index(idx)] = count
    countTab[i][-1] = len(selection)

    print(countTab[i])
    i += 1

# write table to file
with open('nature-region-counts.csv', 'w') as f:
    f.write(','.join(str(x) for x in columns) + '\n')
    for row in countTab:
        f.write(','.join(str(x) for x in row) + '\n')
