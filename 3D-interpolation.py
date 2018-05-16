from scipy.interpolate import RegularGridInterpolator, Rbf
import numpy as np
from numpy import linspace, zeros, array
import pickle
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

all_data = pickle.load( open( "file.p", "rb" ))

#print(all_data)
x =  np.array(all_data['latitude'])
y = np.array(all_data['longitude'])
z = np.array(all_data['height'])
d = all_data['temperature']


x1=np.array(x)
y1=np.array(y)
z1=np.array(z)
d1=np.abs(array(d))

print('Generating Rbf surface')
rbfi = Rbf(x, y, z, d1)
#xi = yi = zi = np.linspace(d1.min(),d1.max(),108)
#di = rbfi(xi, yi, zi)   # interpolated values

angle = np.linspace(0,1,108)
Z,ANG = np.meshgrid(z,angle)
T,ANG = np.meshgrid(d1,angle)

# create the figure, add a 3d axis, set the viewing angle
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.view_init(45,60)

#xx, yy = np.meshgrid(x,y)
zz, dd = np.meshgrid(z,d1)
#ddp = np.transpose(dd)

# Plot the surface.
#ax.plot_surface(x, y, z, facecolors=cm.Oranges(di))
ax.plot_surface(x, y, zz, rstride=1, cstride=1, facecolors=cm.jet(T/float(T.max())))
#plt.contour(x, y, zz, facecolors=cm.Oranges(dd))
plt.show()
