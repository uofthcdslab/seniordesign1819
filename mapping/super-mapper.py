import shapefile
from pyproj import Proj, transform
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, Polygon
import sys
sys.path.append('../parsing')
import accessDB as db
import os

# load in maps
ald = shapefile.Reader('ald2016/alderman')
nbh = shapefile.Reader('hoods/neighborhood')
pol = shapefile.Reader('poldist/poldist')
ward = shapefile.Reader('wards/ward')
city = shapefile.Reader('corp/citylimit')

def plotOn(sf, df, sfName, figName):
    # create a new dataframe with just the coordinates
    coords = df[['Latitude', 'Longitude']]
    coords = coords.dropna()
    # some empty are missed I guess
    coords = coords[coords['Latitude'] != '']
    coords = coords[coords['Longitude'] != '']

    # initialize plot size
    plt.figure(figsize=(10,18)) # approx dimensions of MKE is 5:9
    # limit bounds of the plot
    plt.xlim(-88.1,-87.85)
    plt.ylim(42.9,43.2)
    m = plt

    # loop through shapes
    polys = []
    for i,shape in enumerate(sf.shapes()):
        xs = []
        ys = []
        points = []

        # loop through points
        for point in shape.points:
            # parse points
            coord = [float('%.3f' % coord) for coord in point]
            # convert points
            x, y = transform(inProj, outProj, coord[0], coord[1])
            # add to list
            xs.append(x)
            ys.append(y)
            points.append((x, y))

        # make a polygon out of the points
        poly = Polygon(points)
        polys.append(poly)

        # find the district, ward, etc that a point is in
        for index, row in coords.iterrows():
            point = Point(row['Longitude'], row['Latitude'])
            if poly.contains(point):
                coords.loc[index, sfName] = i

        # plot shape
        m.plot(xs, ys, '-')

    #for index, row in coords.iterrows():
    m.plot(coords['Longitude'], coords['Latitude'], '.')

    #plt.show()
    plt.savefig('plots/' + figName + '.png')
    plt.close()
    return polys

# converter for coordinates
inProj = Proj(init='EPSG:32054', preserve_units=True) # NAD27 Wisconsin South
outProj = Proj(proj='latlong', datum='WGS84', ellps='WGS84') # Latitude and Longitude

allCalls = db.filter(doGeoLoc=True)
natures = allCalls['Nature of Call'].unique()

days = range(0, 7)
weeks = range(36, 53)
for nature in natures:
    print('Running', nature)
    df = allCalls[allCalls['Nature of Call'] == nature]
    figName = nature.replace('/', ' ') + '-all'
    if not os.path.isfile('plots/' + figName + '.png'):
        plotOn(pol, df, 'Police District', figName)
    for dayOfWeek in days:
        figName = nature.replace('/', ' ') + '-day' + str(dayOfWeek)
        if not os.path.isfile('plots/' + figName + '.png'):
            df_day = df[df['Date/Time'].dt.dayofweek == dayOfWeek]
            plotOn(pol, df_day, 'Police District', figName)
    for week in weeks:
        figName = nature.replace('/', ' ') + '-week' + str(week)
        if not os.path.isfile('plots/' + figName + '.png'):
            df_week = df[df['Date/Time'].dt.week == week]
            plotOn(pol, df_week, 'Police District', figName)
