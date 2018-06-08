'''
Rounding to get plot instead of interpolating.
 Future work will use interpolation instead of rounding.
'''

import pickle
import copy
import csv
import matplotlib.pyplot as plt
from bisect import bisect_left
from mpl_toolkits.basemap import Basemap

# Get all_data from pickle
DAY = '30'
all_data = pickle.load(open("file" + DAY + ".p", "rb"))

# get flight plan from csv
height = []
lat = []
lon = []
dist = []
flightplan = 'KJFK-KLAX'
filename = flightplan + '.csv'
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        height.append(row[2])
        lat.append(row[3])
        lon.append(row[4])
        dist.append(row[5])
        
lat_rounded = []
lon_rounded = []
# changing flight plan data to floats and making height meters for comparisons
for i in range(len(height)):
    height[i] = float(height[i])
    height[i] = 0.3048 * height[i]
    lat[i] = float(lat[i])
    lon[i] = float(lon[i])
    dist[i] = float(dist[i])
    
    # rounding lat and lon to nearest whole number to compare with GFS data
    lat_rounded.append(round(lat[i]))
    lon_rounded.append(round(lon[i]))

# creating searchable double list of lat-lon from flight plan    
latlon = []
for i in range(len(lat_rounded)):
    lat_rounded[i] = str(lat_rounded[i])+'000'
    lon_rounded[i] = str(lon_rounded[i])+'000'
    latlon.append([lat_rounded[i], lon_rounded[i]])

# creating searchable double list of lat-lon from weather data  
w_lat = all_data['latitude']
w_lon = all_data['longitude']
w_latlon = []
for i in range(len(w_lat)):
    w_latlon.append([w_lat[i], w_lon[i]])

# intitializing height and variable from weather data
w_height = all_data['height']
w_relh = all_data['humidity']
relh = []
num = 0

# loop to find variable at all locations
for j in range(len(latlon)):
    wnum_height = []
    wnum_relh = []
    
    # first element in temporary vectors
    num = w_latlon.index(latlon[j])
    wnum_height.append(w_height[num])
    wnum_relh.append(w_relh[num])
    num += 1
    
    # creating temporary height and variable vectors for each location
    while w_latlon[num] == ['', '']:
        wnum_height.append(w_height[num])
        wnum_relh.append(w_relh[num])
        num += 1
    
    # converting to float
    for i in range(len(wnum_height)):
        wnum_height[i] = float(wnum_height[i])
    
    # modifying height so that it is above ground level, not sea level
    height[j] = height[j] + wnum_height[0]
    
    # getting index of desired variable from temporary height vector and appending
    hToIndex = bisect_left(wnum_height,height[j])
    if hToIndex > len(wnum_relh)-1:
        hToIndex -= 1
    relh.append(wnum_relh[hToIndex])

# Converting Height back to feet
for i in range(len(height)):
    height[i] = height[i] / 0.3048

# Plotting Variable and Height vs. Distance
plt.subplot(2, 1, 1)
plt.plot(dist,relh)
plt.title('Relative Humidity for %s' % flightplan)
# degree_sign = u'\N{DEGREE SIGN}'
plt.ylabel('Relative Humidity (%)')

plt.subplot(2, 1, 2)
plt.plot(dist,height)
plt.xlabel('Distance (nmi)')
plt.ylabel('Height (ft)')

# Plotting flight path
plt.figure(2)
m = Basemap(projection='merc',llcrnrlat=13,urcrnrlat=58,
            llcrnrlon=-144,urcrnrlon=-53,resolution='c')
m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()

map_x, map_y = m(lon, lat)
m.plot(map_x,map_y)
plt.title('%s' % flightplan)

plt.show()