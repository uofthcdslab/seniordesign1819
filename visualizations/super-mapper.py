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
    plt.savefig(plotDir + figName + '.png')
    plt.close()
    return polys

# converter for coordinates
inProj = Proj(init='EPSG:32054', preserve_units=True) # NAD27 Wisconsin South
outProj = Proj(proj='latlong', datum='WGS84', ellps='WGS84') # Latitude and Longitude

allCalls = db.filter(doGeoLoc=True)

# remove duplicate calls
allCalls = allCalls.drop_duplicates(subset='Call Number')

# use top 25 calls
natures = allCalls['Nature of Call'].value_counts()[:25].index

days = range(0, 7)
hours = range(0, 24)
weeks = (allCalls['Date/Time'].dt.year.astype(str) + '-' + allCalls['Date/Time'].dt.week.astype(str)).unique()
# for every nature
for nature in natures:
    print('Running', nature)
    figName = nature.replace('/', ' ')
    # gather all calls
    df = allCalls[allCalls['Nature of Call'] == nature]
    
    # plot all calls
    allName = figName + '-all'
    if not os.path.isfile('plots/' + allName + '.png'):
        plotOn(ald, df, 'Aldermanic District', allName)
            
    # plot for every hour
    for hour in hours:
        hourName = figName + '-hour-' + str(hour)
        if not os.path.isfile('plots/' + hourName + '.png'):
            df_hour = df[df['Date/Time'].dt.hour == hour]
            plotOn(ald, df_hour, 'Aldermanic District', hourName)
        
    # plot for every day of the week
    for dayOfWeek in days:
        dayName = figName + '-day-' + str(dayOfWeek)
        if not os.path.isfile('plots/' + dayName + '.png'):
            df_day = df[df['Date/Time'].dt.dayofweek == dayOfWeek]
            plotOn(ald, df_day, 'Aldermanic District', dayName)
            
    # plot for every week
    for week in weeks:
        weekStr = str(week)
        weekName = figName + '-week-' + weekStr
        if not os.path.isfile('plots/' + weekName + '.png'):
            df_week = df[(df['Date/Time'].dt.year.astype(str) + '-' + df['Date/Time'].dt.week.astype(str)) == week]
            plotOn(ald, df_week, 'Aldermanic District', weekName)
