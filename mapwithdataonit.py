'''
Creates a contour plot of a selected weather variable at a height
 determined by the user.
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata 
import pickle
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
import copy


DAY = '29'
all_data = pickle.load(open("Pickle_Data_Files/file" + DAY + ".p", "rb"))

# Getting non-repeating list of lat/long
x = copy.deepcopy(all_data['longitude'])
y = copy.deepcopy(all_data['latitude'])

# Finding humidity for each lat/long at set altitude
ALT = 5400 # Doesn't Change
ALT_txt = int(ALT / 0.3048)
h = []
t = []
Temperature = []
for i in range(len(x)):
    if i > 0:
        if x[i] == '':
            h.append(all_data['height'][i])
            t.append(all_data['humidity'][i])
        else:
            Alt = ALT
            loc = -1
            while loc == -1:
                if Alt in h:
                    loc = h.index(Alt)
                else:
                    Alt -= 1
            Temperature.append( ((ALT - h[loc])*((t[loc+1] - t[loc])/(h[loc+1] - h[loc]))) + t[loc] )
            
            h = []
            h.append(all_data['height'][i])
            t = []
            t.append(all_data['humidity'][i])
    else:
        h.append(all_data['height'][i])
        t.append(all_data['humidity'][i])
# Getting last Temperature value        
Alt = ALT
loc = -1
while loc == -1:
    if Alt in h:
        loc = h.index(Alt)
    else:
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

# plot basemap
plt.figure(figsize=(12,6))
m = Basemap(projection='merc',llcrnrlat=13,urcrnrlat=58,
            llcrnrlon=-144,urcrnrlon=-53,resolution='c')
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

# plot
bounds = np.arange(0,110,10)
m.contourf(xi,yi,zi, cmap=cm.Blues, levels=bounds)
cbar = m.colorbar()
degree_sign = u'\N{DEGREE SIGN}'
# cbar.set_label("Temperature %sC" % degree_sign, fontsize=14)
cbar.set_label("Relative Humidity (%)")
m.plot(map_lon,map_lat,'.k',ms=1)

# plt.title('Contour Map Test - Temperature at %s feet' % ALT_txt, fontsize=20)
plt.suptitle('Relative Humidity at %s feet' % ALT_txt, fontsize=20)
plt.title('05/30/18 at 06 UTC', fontsize=12)
plt.show()

