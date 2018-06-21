#!python3

'''
Creates a list of lists in the form [[altitude, weather_value], [...]]
 where altitude is the height above the ground and weather_value is the
 value of the temperature, humidity, or wind speed at that height.
 Python3 Version
'''

import functions3
from functions3 import makeFloats
from functions3 import sBoomDictMaker
import pickle
import copy
from scipy import interpolate

            
ALT_ft = 45000
ALT = ALT_ft * 0.3048

temp, height, relh = functions3.openPickle('17', '06', '2018', '12')[0:3]
sknt = functions3.openPickle('17', '06', '2018', '12')[4]
lat, lon = functions3.openPickle('17', '06', '2018', '12')[6:8]


temp = makeFloats(temp)
height = makeFloats(height)
relh = makeFloats(relh)
sknt = makeFloats(sknt)
lat = makeFloats(lat)
lon = makeFloats(lon)

data = {}
data = sBoomDictMaker(relh, 'humidity', ALT, lat, lon, height, data)
data = sBoomDictMaker(temp, 'temperature', ALT, lat, lon, height, data)
data = sBoomDictMaker(sknt, 'wind speed', ALT, lat, lon, height, data)
 

printKey = '%i, %i' % (lat[0],lon[0])
for key in data[printKey]:
    print(key)
    print(data[printKey][key])
    
'''    
g = open("sBoom_input.p","wb")
pickle.dump(data,g)
g.close()
'''
# do sBoom things here