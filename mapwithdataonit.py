'''
Contour Plots ?
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import pickle
from mpl_toolkits.basemap import Basemap

DAY = '29'
all_data = pickle.load(open("file" + DAY + ".p", "rb"))

# Getting non-repeating list of lat/long
x = all_data['longitude']
y = all_data['latitude']

# Finding temperature for each lat/long at set altitude
ALT = 15000 # Doesn't Change
h = []
t = []
Temperature = []
for i in range(len(x)):
    if i > 0:
        if x[i] == '':
            h.append(all_data['height'][i])
            t.append(all_data['temperature'][i])
        else:
            Alt = ALT
            loc = 0
            while loc == 0:
                try:
                    loc = h.index(Alt)
                except:
                    Alt -= 1
            Temperature.append( ((ALT - h[loc])*((t[loc+1] - t[loc])/(h[loc+1] - h[loc]))) + t[loc] )
            
            h = []
            h.append(all_data['height'][i])
            t = []
            t.append(all_data['temperature'][i])
    else:
        h.append(all_data['height'][i])
        t.append(all_data['temperature'][i])
# Getting last Temperature value        
Alt = ALT
loc = 0
while loc == 0:
    try:
        loc = h.index(Alt)
    except:
        Alt -= 1
Temperature.append( ((ALT - h[loc])*((t[loc+1] - t[loc])/(h[loc+1] - h[loc]))) + t[loc] )

# Make remove empty cells from lat/long
i = 0
while '' in x:
    if i > 0 and x[i] == '':
            x.pop(i)
            y.pop(i)
    else:
        i += 1
numcols, numrows = len(x), len(y)

# Make lists into arrays to graph
for i in range(len(x)):
        x[i] = float(x[i])
        y[i] = float(y[i])
x = np.array(x)
y = np.array(y)
Temperature = np.array(Temperature)
z = Temperature


plt.figure(figsize=(12,6))
m = Basemap(projection='merc',llcrnrlat=25,urcrnrlat=50,
            llcrnrlon=-130,urcrnrlon=-65,resolution='c')
m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()
map_lon, map_lat = m(*(x,y))
        
# target grid to interpolate to

xi = np.linspace(map_lon.min(), map_lon.max(), numcols)
yi = np.linspace(map_lat.min(), map_lat.max(), numrows)

xi,yi = np.meshgrid(xi,yi)


# interpolate
zi = griddata((map_lon,map_lat),z,(xi,yi),method='linear')
# print(xi)
# print(yi) 
# print(zi)
# plot
m.contourf(xi,yi,zi)
cbar = plt.colorbar()
degree_sign = u'\N{DEGREE SIGN}'
cbar.set_label("Temperature %sC" % degree_sign, fontsize=14)
m.plot(map_lon,map_lat,'.k')

# plt.xlabel('Longitude',fontsize=12)
# plt.ylabel('Latitude',fontsize=12)
plt.title('Contour Map Test - Temperature at %s meters' % ALT, fontsize=20)
plt.show()


