'''
Attempt to make a 2D contour graph of weather data

Plot 2d graph of variable vs time or distance with the altitude noted on the
x-axis.  Attempt to make a simultaneous plot of the path of the flight.  
'''

import numpy as np
import matplotlib.pyplot as plt
import pickle

all_data = pickle.load( open( "file.p", "rb" ))
# print(all_data)
x = np.array(all_data['latitude'])
y = np.array(all_data['height'])
d = all_data['temperature']
print(d)

[X,Y] = np.meshgrid(x,y)




plt.contour(X,Y,temp)
plt.show()