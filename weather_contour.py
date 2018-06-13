'''
Attempt to make a 2D contour graph of weather data

Plot 2d graph of variable vs time or distance with the altitude noted
 on the x-axis.  Attempt to make a simultaneous plot of the path of 
 the flight.  
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pickle

all_data = pickle.load( open( "file.p", "rb" ))
# print(all_data)
x = np.array(all_data['latitude'])
y = np.array(all_data['longitude'])
d = all_data['temperature']
# [X,Y] = np.meshgrid(x,y)

# Average Temperature at each location
i = 0
j = 0
temp = np.ones((len(x),len(x)),)
# print(len(x)-1)
while j < len(x):
    while i < len(x)-1:
        if x[i] == x[i+1]:
            temp[i,j] = d[i]
            if i == len(x)-2:
                temp[i+1,j] = d[-1]
            i += 1
            # print(i)
        else:
            temp[i,j] = d[i]
            j += 1
            i += 1
            # print('j',j)
    j += 1
    
# print temp
avgT = []
avgTemp = []
for j in range(len(temp)):
    for i in range(len(temp)):
        if temp[i,j] != 1:
            avgT.append(temp[i,j])
            # print(avgT[i])
    if len(avgT) > 0:
        avgTemp.append(np.mean(avgT))
        avgT = []

x2 = all_data['latitude']
y2 = all_data['longitude']        
i = 0
while len(x2) > len(avgTemp):
    if x2[i] == x2[i+1]:
        x2.pop(i+1)
        y2.pop(i+1)
    else: 
        i += 1

y = np.array(x2)
x = np.array(y2)
print(x,y,avgTemp)    
# plt.scatter(x,y)
# plt.show()

''' Part 2: Interpolation?
'''
# data coordinates and values
x = np.array(x)
y = np.array(y)
# x = -x
z = np.array(avgTemp)
z = -z

# target grid to interpolate to
xi = np.arange(0,-180,-1)
yi = np.arange(0,180,1)
xi,yi = np.meshgrid(xi,yi)

# set mask
# mask = (xi > 100) & (xi < 101) & (yi > 100) & (yi < 101)

# interpolate
zi = griddata((x,y),z,(xi,yi),method='linear')

# mask out the field
# zi[mask] = np.nan

# plot

# ax = fig.add_subplot(111)
plt.contourf(xi,yi,zi,np.arange(0,180,1))
plt.plot(x,y,'k.')
plt.xlabel('Longitude',fontsize=16)
plt.ylabel('Latitude',fontsize=16)
plt.show()











