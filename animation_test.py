'''
Creates an animation of contour plots of a desired weather variable
 over the continental US which starts at 50,000 feet and descends 
 incrementally to 18,000 feet.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.interpolate import griddata 
import pickle
from mpl_toolkits.basemap import Basemap
from matplotlib import cm
import copy
from matplotlib.animation import PillowWriter
import functions


fig = plt.figure(figsize=(12,6))

# plotting United States
bounds = np.arange(0,110,10)
m = Basemap(projection='merc',llcrnrlat=13,urcrnrlat=58,
            llcrnrlon=-144,urcrnrlon=-53,resolution='c')
m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()

# Titles
degree_sign = u'\N{DEGREE SIGN}'
plt.title('06/12/18 12:00:00 UTC', fontsize=12)
plt.suptitle('Relative Humidity', fontsize=20)

# Animation
ALT = [15240, 12000, 9000, 5905]
ims = []
for i in range(len(ALT)):
    X, Y, Z = functions.contourfGenerator(ALT[i])
    im = m.contourf(X, Y, Z, cmap=cm.Blues, levels=bounds)
    text = 'Altitude={0!r}'.format(int(ALT[i]/0.3048))
    an = plt.annotate(text, xy=(0.85,1.01), xycoords='axes fraction')
    art = im.collections
    ims.append(art + [an])

ani = animation.ArtistAnimation(fig, ims, interval=2000, blit=False)

# adding colorbar to contour
cbar = m.colorbar()
degree_sign = u'\N{DEGREE SIGN}'
cbar.set_label("Relative Humidity (%)")

# Saving as gif
gifName = '18061212.gif'
ani.save(gifName, writer=PillowWriter())

plt.show()
