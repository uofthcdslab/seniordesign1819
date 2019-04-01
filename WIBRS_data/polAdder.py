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
    coords = df
    coords = coords.dropna()
    # some empty are missed I guess
    coords = coords[coords['y_lat'] != '']
    coords = coords[coords['x_long'] != '']

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
            point = Point(row['x_long'], row['y_lat'])
            if poly.contains(point):
                coords.loc[index, sfName] = i

    return coords

# converter for coordinates
inProj = Proj(init='EPSG:32054', preserve_units=True) # NAD27 Wisconsin South
outProj = Proj(proj='latlong', datum='WGS84', ellps='WGS84') # Latitude and Longitude

wibrs=pd.read_csv('testdata.csv')

# get all regions
coords = getIn(pol, wibrs, 'Police District')
coords.to_csv('WIBRS_with_pol.csv')
