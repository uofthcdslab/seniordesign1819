import shapefile
from pyproj import Proj, transform
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon
import sys
sys.path.append('../parsing')
import accessDB as db
import os

plotDir = 'plots/'
if not os.path.exists(plotDir):
    os.mkdir(plotDir)

# load in maps
ald = shapefile.Reader('../mapping/ald2016/alderman')
nbh = shapefile.Reader('../mapping/hoods/neighborhood')
pol = shapefile.Reader('../mapping/poldist/poldist')
ward = shapefile.Reader('../mapping/wards/ward')
city = shapefile.Reader('../mapping/corp/citylimit')

def getIn(sf, df, sfName):
    # create a new dataframe with just the coordinates
    coords = df[['Latitude', 'Longitude']]
    coords = coords.dropna()
    # some empty are missed I guess
    coords = coords[coords['Latitude'] != '']
    coords = coords[coords['Longitude'] != '']

    # loop through shapes
    polys = []
    for i,shape in enumerate(sf.shapes()):
        points = []

        # loop through points
        for point in shape.points:
            # parse points
            coord = [float('%.3f' % coord) for coord in point]
            # convert points
            x, y = transform(inProj, outProj, coord[0], coord[1])
            points.append((x, y))

        # make a polygon out of the points
        poly = Polygon(points)
        polys.append(poly)

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
allCalls = allCalls.drop_duplicates(subset='Call Number')

# use top 25 calls
natures = allCalls['Nature of Call'].value_counts()[:25].index

# for every nature
for nature in natures:
    print('Running', nature)
    # gather all calls
    df = allCalls[allCalls['Nature of Call'] == nature]
    coords = getIn(pol, df, 'Police District')
    print(coords.head)
