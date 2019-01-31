#!python3
'''
Makes a contour plot of ground level heights.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pickle
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
import matplotlib
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap as LSC
import copy
import random
import functions3


class FixPointNormalize(matplotlib.colors.Normalize):
    """
    This may be useful for a `terrain` map, to set the "sea level"
    to a color in the blue/turquise range.
    """

    def __init__(self, vmin=None, vmax=None, sealevel=0, col_val=0.21875,
                 clip=False):
        # sealevel is the fix point of the colormap (in data units)
        self.sealevel = sealevel
        # col_val is the color value in the range [0,1] that should represent
        # the sealevel.
        self.col_val = col_val
        matplotlib.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.sealevel, self.vmax], [0, self.col_val, 1]
        return np.ma.masked_array(np.interp(value, x, y))

# Combine the lower and upper range of the terrain colormap with a gap in the
# middle to let the coastline appear more prominently.


colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 56))
colors_land = plt.cm.terrain(np.linspace(0.25, 1, 200))
# combine them and build a new colormap
colors = np.vstack((colors_undersea, colors_land))
cut_terrain_map = LSC.from_list('cut_terrain', colors)

# import pyLdB output
# z = output
DAY = '18'
MONTH = '06'
YEAR = '2018'
HOUR = '12'

filename = "file" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR

data = pickle.load(open("Pickle_Data_Files/" + filename + '.p', 'rb'))

lat = copy.deepcopy(data['latitude'])
lon = copy.deepcopy(data['longitude'])
height = copy.deepcopy(data['height'])

lon = functions3.makeFloats(lon)
lat = functions3.makeFloats(lat)
height = functions3.makeFloats(height)

ground_height = []
for i in range(len(lat)):
    if lat[i] != 0:
        ground_height.append(height[i] / 0.3048)
ground_height = np.array(ground_height)
# ground_height = functions3.heightToFeet(ground_height)

i = 0
while 0 in lon:
    if lon[i] == 0:
        lon.pop(i)
    else:
        # ground_height.append(height[i])
        i += 1

i = 0
while 0 in lat:
    if lat[i] == 0:
        lat.pop(i)
    else:
        i += 1

numcols, numrows = len(lon), len(lat)

lon = np.array(lon)
lat = np.array(lat)

fig = plt.figure(figsize=(12, 6))

# bounds = np.arange(0,110,10) - FIXME to match output
m = Basemap(projection='merc', llcrnrlat=13, urcrnrlat=58,
            llcrnrlon=-144, urcrnrlon=-53, resolution='c')
map_lon, map_lat = m(*(lon, lat))

m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()

# Titles
degree_sign = '\N{DEGREE SIGN}'
plt.title('Ground Level Height', fontsize=20)

# target grid to interpolate to
xi = np.linspace(map_lon.min(), map_lon.max(), numcols)
yi = np.linspace(map_lat.min(), map_lat.max(), numrows)
xi, yi = np.meshgrid(xi, yi)

# interpolate
zi = griddata((map_lon, map_lat), ground_height, (xi, yi), method='linear')
# contour plot
# FIXME - try to get rid of blue land
norm2 = FixPointNormalize(sealevel=0, vmax=11480)
bounds = np.arange(-820, 12300, 820)
m.contourf(xi, yi, zi, norm=norm2, cmap=cut_terrain_map, levels=bounds)

# colorbar
cbar = m.colorbar()
degree_sign = '\N{DEGREE SIGN}'
cbar.set_label("Height (ft)")

plt.show()
