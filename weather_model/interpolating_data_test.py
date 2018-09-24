'''
Attempt to replicate result format from rounding_data_test.py
 using linear interpolation for altitude then double interpolation
 for latitude and longitude.

 Creates a plot of the change in a desired weather variable vs. distance
 as altitude and location above the Continental US changes using Linear
 Interpolation.
'''

import pickle
import copy
import csv
import matplotlib.pyplot as plt
from bisect import bisect_left
from mpl_toolkits.basemap import Basemap
from scipy import interpolate
import numpy as np

# Get all_data from pickle
DAY = '30'
all_data = pickle.load(open("Pickle_Data_Files/file" + DAY + ".p", "rb"))

# get flight plan from csv
height = []
lat = []
lon = []
dist = []
flightplan = 'KJFK-KLAX'
filename = 'Flight_Plan_Files/' + flightplan + '.csv'
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        height.append(row[2])
        lat.append(row[3])
        lon.append(row[4])
        dist.append(row[5])

# changing flight plan data to floats and making height meters for comparisons
for i in range(len(height)):
    height[i] = float(height[i])
    height[i] = 0.3048 * height[i]
    lat[i] = float(lat[i])
    lon[i] = float(lon[i])
    dist[i] = float(dist[i])

# deepcopy
w_lat = copy.deepcopy(all_data['latitude'])
w_lon = copy.deepcopy(all_data['longitude'])
w_height = copy.deepcopy(all_data['height'])
w_relh = copy.deepcopy(all_data['humidity'])


for i in range(len(w_lat)):
    if w_lat[i] == '':
        w_lat[i] = 0  # impossible filler number
        w_lon[i] = 0
    w_lat[i] = float(w_lat[i])
    w_lon[i] = float(w_lon[i])
    w_height[i] = float(w_height[i])
    w_relh[i] = float(w_relh[i])

w_latlon = []
for i in range(len(w_lat)):
    w_latlon.append([w_lat[i], w_lon[i]])

relh = []
# finding locations of 4 closest lat/lon pairs
for i in range(len(lat)):
    loc_x = min(range(len(w_lon)), key=lambda x: abs(w_lon[x]-lon[i]))
    x1 = float(w_lon[loc_x])
    loc_y = min(range(len(w_lat)), key=lambda x: abs(w_lat[x]-lat[i]))
    y1 = float(w_lat[loc_y])

    # finding other 3 latlon pairs from first 1
    if x1 == lon[i] and y1 == lat[i]:
        # print 'height'
        loc1 = w_latlon.index([y1, x1])  # same as [y1, x1]
        height1 = []
        height1.append(w_height[loc1])
        relh1 = []
        relh1.append(w_relh[loc1])
        j = 1
        while w_lat[loc1 + j] == 0:
            height1.append(w_height[loc1 + j])
            relh1.append(w_relh[loc1 + j])
            j += 1

        f1 = interpolate.interp1d(height1, relh1, fill_value="extrapolate")
        relh.append(f1(height[i]))

    elif x1 == lon[i] and y1 != lat[i]:
        if lat[i] > y1:
            y2 = y1 + 1
        elif lat[i] < y1:
            y2 = y1 - 1
        else:
            print "ERROR"
        # print 'single interpolate y'

        loc1 = w_latlon.index([y1, x1])  # same as [y1, x1]
        loc2 = w_latlon.index([y2, x1])
        height1 = []
        height1.append(w_height[loc1])
        height2 = []
        height2.append(w_height[loc2])

        relh1 = []
        relh1.append(w_relh[loc1])
        relh2 = []
        relh2.append(w_relh[loc2])

        j = 1
        while w_lat[loc1 + j] == 0:
            height1.append(w_height[loc1 + j])
            relh1.append(w_relh[loc1 + j])
            j += 1
        j = 1
        while w_lat[loc2 + j] == 0:
            height2.append(w_height[loc2 + j])
            relh2.append(w_relh[loc2 + j])
            j += 1

        f1 = interpolate.interp1d(height1, relh1, fill_value="extrapolate")
        f2 = interpolate.interp1d(height2, relh2, fill_value="extrapolate")

        relh_loc = []
        relh_loc.append(f1(height[i]))
        relh_loc.append(f2(height[i]))

        w_lat_loc = []
        w_lat_loc.append(w_lat[loc1])
        w_lat_loc.append(w_lat[loc2])

        f_p2 = interpolate.interp1d(w_lat_loc, relh_loc,
                                    fill_value="extrapolate")
        relh.append(f_p2(lat[i]))

    elif x1 != lon[i] and y1 == lat[i]:
        # print 'single interpolate x'

        if lon[i] > y1:
            x2 = x1 + 1
        elif lon[i] < y1:
            x2 = x1 - 1
        else:
            print "ERROR"

        loc1 = w_latlon.index([y1, x1])  # same as [y1, x1]
        loc2 = w_latlon.index([y1, x2])
        height1 = []
        height1.append(w_height[loc1])
        height2 = []
        height2.append(w_height[loc2])

        relh1 = []
        relh1.append(w_relh[loc1])
        relh2 = []
        relh2.append(w_relh[loc2])

        j = 1
        while w_lon[loc1 + j] == 0:
            height1.append(w_height[loc1 + j])
            relh1.append(w_relh[loc1 + j])
            j += 1
        j = 1
        while w_lon[loc2 + j] == 0:
            height2.append(w_height[loc2 + j])
            relh2.append(w_relh[loc2 + j])
            j += 1

        f1 = interpolate.interp1d(height1, relh1, fill_value="extrapolate")
        f2 = interpolate.interp1d(height2, relh2, fill_value="extrapolate")

        relh_loc = []
        relh_loc.append(f1(height[i]))
        relh_loc.append(f2(height[i]))

        w_lon_loc = []
        w_lon_loc.append(w_lon[loc1])
        w_lon_loc.append(w_lon[loc2])

        f_p2 = interpolate.interp1d(w_lon_loc, relh_loc,
                                    fill_value="extrapolate")
        relh.append(f_p2(lon[i]))

    else:
        if lon[i] > x1 and lat[i] > y1:
            x2 = x1 - 1
            y2 = y1 - 1
        elif lon[i] < x1 and lat[i] > y1:
            x2 = x1 + 1
            y2 = y1 - 1
        elif lon[i] < x1 and lat[i] < y1:
            x2 = x1 + 1
            y2 = y1 + 1
        elif lon[i] > x1 and lat[i] < y1:
            x2 = x1 - 1
            y2 = y1 + 1
        else:
            print 'ERROR'

        # finding indices of each location
        loc1 = w_latlon.index([y1, x1])  # same as [y1, x1]
        loc2 = w_latlon.index([y2, x1])
        loc3 = w_latlon.index([y1, x2])
        loc4 = w_latlon.index([y2, x2])

        # making height vectors for each location
        height1 = []
        height1.append(w_height[loc1])
        relh1 = []
        relh1.append(w_relh[loc1])
        height2 = []
        height2.append(w_height[loc2])
        relh2 = []
        relh2.append(w_relh[loc2])
        height3 = []
        height3.append(w_height[loc3])
        relh3 = []
        relh3.append(w_relh[loc3])
        height4 = []
        height4.append(w_height[loc4])
        relh4 = []
        relh4.append(w_relh[loc4])
        j = 1
        while w_lat[loc1 + j] == 0:
            height1.append(w_height[loc1 + j])
            relh1.append(w_relh[loc1 + j])
            j += 1
        j = 1
        while w_lat[loc2 + j] == 0:
            height2.append(w_height[loc2 + j])
            relh2.append(w_relh[loc2 + j])
            j += 1
        j = 1
        while w_lat[loc3 + j] == 0:
            height3.append(w_height[loc3 + j])
            relh3.append(w_relh[loc3 + j])
            j += 1
        j = 1
        while w_lat[loc4 + j] == 0:
            height4.append(w_height[loc4 + j])
            relh4.append(w_relh[loc4 + j])
            j += 1

        # linear 1d interpolation to get 4 humidities at 4 locations
        f1 = interpolate.interp1d(height1, relh1, fill_value="extrapolate")
        f2 = interpolate.interp1d(height2, relh2, fill_value="extrapolate")
        f3 = interpolate.interp1d(height3, relh3, fill_value="extrapolate")
        f4 = interpolate.interp1d(height4, relh4, fill_value="extrapolate")

        # making arrays for 2d interpolation at each location
        relh_loc = []
        relh_loc.append(f1(height[i]))
        relh_loc.append(f2(height[i]))
        relh_loc.append(f3(height[i]))
        relh_loc.append(f4(height[i]))

        w_lon_loc = []
        w_lon_loc.append(w_lon[loc1])
        w_lon_loc.append(w_lon[loc2])
        w_lon_loc.append(w_lon[loc3])
        w_lon_loc.append(w_lon[loc4])

        w_lat_loc = []
        w_lat_loc.append(w_lat[loc1])
        w_lat_loc.append(w_lat[loc2])
        w_lat_loc.append(w_lat[loc3])
        w_lat_loc.append(w_lat[loc4])

        # 2d interpolation
        f2d = interpolate.interp2d(w_lon_loc, w_lat_loc, relh_loc)
        final_relh = f2d(lon[i], lat[i])
        relh.append(final_relh[0])


# Height back into feet
for i in range(len(height)):
    height[i] = height[i] / 0.3048

# Plotting Variable and Height vs. Distance
plt.subplot(2, 1, 1)
plt.plot(dist, relh)
plt.title('Relative Humidity for %s' % flightplan)
# degree_sign = u'\N{DEGREE SIGN}'
plt.ylabel('Relative Humidity (%)')

plt.subplot(2, 1, 2)
plt.plot(dist, height)
plt.xlabel('Distance (nmi)')
plt.ylabel('Height (ft)')

# Plotting flight path
plt.figure(2)
m = Basemap(projection='merc', llcrnrlat=13, urcrnrlat=58,
            llcrnrlon=-144, urcrnrlon=-53, resolution='c')
m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()

map_x, map_y = m(lon, lat)
m.plot(map_x, map_y)
plt.title('%s' % flightplan)

plt.show()
