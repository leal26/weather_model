#!python3
'''
Makes a contour plot of noise values output from pyLdB.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata 
import pickle
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
import copy
import random
import functions3


# import pyLdB output
# z = output

lat, lon = functions3.openPickle('17','06','2018','12')[6:8]

i = 0
while '' in lon:
    if i > 0 and lon[i] == '':
            lon.pop(i)
            lat.pop(i)
    else:
        i += 1
numcols, numrows = len(lon), len(lat)

# REMOVE this when z should be pyLdB input
z = []
for i in range(len(lat)):
    z.append(random.randrange(0,100))

# Make lists into arrays to graph
lon = functions3.makeFloats(lon)
lat = functions3.makeFloats(lat)
lon = np.array(lon)
lat = np.array(lat)
z = np.array(z)

fig = plt.figure(figsize=(12,6))

# bounds = np.arange(0,110,10) - FIXME to match output
m = Basemap(projection='merc',llcrnrlat=13,urcrnrlat=58,
        llcrnrlon=-144,urcrnrlon=-53,resolution='c')
map_lon, map_lat = m(*(lon,lat))
   
m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()

# Titles
degree_sign = '\N{DEGREE SIGN}'
plt.title('06/17/18 12:00:00 UTC', fontsize=12)
plt.suptitle('Projected Loudness using sBoom and pyLdB', fontsize=20)
   
# target grid to interpolate to
xi = np.linspace(map_lon.min(), map_lon.max(), numcols)
yi = np.linspace(map_lat.min(), map_lat.max(), numrows)
xi,yi = np.meshgrid(xi,yi)

# interpolate
zi = griddata((map_lon,map_lat),z,(xi,yi),method='linear')

m.contourf(xi, yi, zi, cmap=cm.coolwarm)#, levels=bounds)

cbar = m.colorbar()
degree_sign = '\N{DEGREE SIGN}'
cbar.set_label("Loudness (dB)")

plt.show()


