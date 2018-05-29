'''
Attempt to make a map plot of a mission across the U.S. with various
 weather data as the dependent vaiable and distance or time as the 
 x-variable.  Also, altitude will be labeled on the x-axis.  
'''

import numpy as np
import matplotlib.pyplot as plt
import pickle
DAY = '29'
all_data = pickle.load(open("file" + DAY + ".p", "rb"))
lat = all_data['latitude']

lat0 = lat[0]
long0 = all_data['longitude'][0]

temp = []
hght = []
pres = []
relh = []
drct = []
sknt = []

temp.append(all_data['temperature'][0])
hght.append(all_data['height'][0])
pres.append(all_data['pressure'][0])
relh.append(all_data['humidity'][0])
drct.append(all_data['wind_direction'][0])
sknt.append(all_data['wind_speed'][0])
i = 1
while lat[i] == '':
    temp.append(all_data['temperature'][i])
    hght.append(all_data['height'][i])
    pres.append(all_data['pressure'][i])
    relh.append(all_data['humidity'][i])
    drct.append(all_data['wind_direction'][i])
    sknt.append(all_data['wind_speed'][i])
    i += 1

plt.figure(1)
plt.plot(temp,hght)
degree_sign = u'\N{DEGREE SIGN}'
plt.xlabel('Temperature (%sC)' % degree_sign, fontsize=12)
plt.ylabel('Height (m)', fontsize=12)
plt.title("Height vs Temperature at %.2s %sN, %.4s %sW" % (lat0, degree_sign, long0, degree_sign), fontsize=16)

plt.figure(2)
plt.plot(pres,hght)
plt.xlabel('Pressure (hPa)', fontsize=12)
plt.ylabel('Height (m)', fontsize=12)
plt.title("Height vs Pressure at %.2s %sN, %.4s %sW" % (lat0, degree_sign, long0, degree_sign), fontsize=16)

plt.figure(3)
plt.plot(relh,hght)
plt.xlabel('Relative Humidity (%)', fontsize=12)
plt.ylabel('Height (m)', fontsize=12)
plt.title("Height vs Relative Humidity at %.2s %sN, %.4s %sW" % (lat0, degree_sign, long0, degree_sign), fontsize=16)

plt.figure(4)
plt.plot(drct,hght)
plt.xlabel('Wind Direction (%s)' % degree_sign, fontsize=12)
plt.ylabel('Height (m)', fontsize=12)
plt.title("Height vs Wind Direction at %.2s %sN, %.4s %sW" % (lat0, degree_sign, long0, degree_sign), fontsize=16)

plt.figure(5)
plt.plot(sknt,hght)
plt.xlabel('Wind Speed (kn)', fontsize=12)
plt.ylabel('Height (m)', fontsize=12)
plt.title("Height vs Wind Speed at %.2s %sN, %.4s %sW" % (lat0, degree_sign, long0, degree_sign), fontsize=16)

plt.show()










