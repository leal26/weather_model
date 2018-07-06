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
import functions


# plot basemap
plt.figure(figsize=(12,6))
m = Basemap(projection='merc',llcrnrlat=13,urcrnrlat=58,
            llcrnrlon=-144,urcrnrlon=-53,resolution='c')
m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()

# generate grid for contourf
ALT = 3499
xi, yi, zi = functions.contourfGenerator(ALT)

# apply contourf to basemap
bounds = np.arange(0,110,10)
m.contourf(xi,yi,zi, cmap=cm.Blues, levels=bounds)

# colorbar
cbar = m.colorbar()
# degree_sign = u'\N{DEGREE SIGN}'
cbar.set_label("Relative Humidity (%)")
# m.plot(map_lon,map_lat,'.k',ms=1)

# titles
ALT_txt = int(ALT/0.3048)
plt.suptitle('Relative Humidity at %s feet' % ALT_txt, fontsize=20)
plt.title('06/12/18 at 12z', fontsize=12)
plt.show()
