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
DAY = '17'
MONTH = '06'
YEAR = '2018'
HOUR = '12'


noise_data = pickle.load(open("noise" + YEAR + "_" 
                                + MONTH + "_" + DAY + "_" + HOUR + ".p", "rb"))

                                
#print(noise_data['noise'])
lat = []
lon = []
latlon = copy.deepcopy(noise_data['latlon'])
#print(latlon)
for i in range(len(latlon)):
    latlon_temp = [int(s) for s in latlon[i].split(',')]
    lat.append(latlon_temp[0])
    lon.append(latlon_temp[1])

numcols, numrows = len(lon), len(lat)
#print(lat,lon)

# REMOVE this when z should be pyLdB input
z = copy.deepcopy(noise_data['noise'])
# for i in range(len(lat)):
    # z.append(random.randrange(0,100))

# Make lists into arrays to graph
lon = functions3.makeFloats(lon)
lat = functions3.makeFloats(lat)
lon = np.array(lon)
lat = np.array(lat)
# print(z)
# print(len(z))
# print(len(latlon))

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

