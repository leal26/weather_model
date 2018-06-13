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
from matplotlib.animation import Pillow



fig = plt.figure(figsize=(12,6))

DAY = '12'
MONTH = '06'
YEAR = '18'
HOUR = '12'
all_data = pickle.load(open("Pickle_Data_Files/file" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".p", "rb"))



def contourfGenerator(ALT):
    # Getting non-repeating list of lat/long
    x = copy.deepcopy(all_data['longitude'])
    y = copy.deepcopy(all_data['latitude'])
    
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

    # remove empty cells from lat/long
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
    
    map_lon, map_lat = m(*(x,y))
        
    # target grid to interpolate to
    xi = np.linspace(map_lon.min(), map_lon.max(), numcols)
    yi = np.linspace(map_lat.min(), map_lat.max(), numrows)
    xi,yi = np.meshgrid(xi,yi)
    
    # interpolate
    zi = griddata((map_lon,map_lat),z,(xi,yi),method='linear')
    return xi, yi, zi

    


    
    
# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []


ALT_ft = 50000
bounds = np.arange(0,110,10)
m = Basemap(projection='merc',llcrnrlat=13,urcrnrlat=58,
            llcrnrlon=-144,urcrnrlon=-53,resolution='c')
m.drawstates()
m.drawcountries(linewidth=1.0)
m.drawcoastlines()

degree_sign = u'\N{DEGREE SIGN}'
plt.title('05/30/18 06:00:00 UTC', fontsize=12)
plt.suptitle('Relative Humidity', fontsize=20)

ALT = [15240, 12000, 9000, 5905]

for i in range(len(ALT)):
    X, Y, Z = contourfGenerator(ALT[i])
    im = m.contourf(X, Y, Z, cmap=cm.Blues, levels=bounds)
    text = 'Altitude={0!r}'.format(int(ALT[i]/0.3048))
    an = plt.annotate(text, xy=(0.85,1.01), xycoords='axes fraction')
    art = im.collections
    ims.append(art + [an])

ani = animation.ArtistAnimation(fig, ims, interval=2000, blit=False)
                                #repeat_delay=2000)

cbar = m.colorbar()
degree_sign = u'\N{DEGREE SIGN}'
cbar.set_label("Relative Humidity (%)")

#FIXME - saving issue
gifName = YEAR + MONTH + DAY + HOUR + '.gif'
ani.save(gifName, writer=PillowWriter())

plt.show()

