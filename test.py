
import pickle
import copy
from scipy import interpolate
from functions3 import *
#i=415
data = {}
all_data = pickle.load(open("Pickle_Data_Files/file" + '2018' + "_" 
                                + '06' + "_" + '18' + "_" + '12' + ".p", "rb"))
lat = copy.deepcopy(all_data['latitude'])
lon = copy.deepcopy(all_data['longitude'])
height = copy.deepcopy(all_data['height'])
li = copy.deepcopy(all_data['humidity'])

ALT_ft = 40000
ALT = ALT_ft * 0.3048
keyName = 'humidity'

temp_height = []
temp_li = []
temp_combo_li = []
d = copy.deepcopy(data)
k = 0
i = 0
while i < len(lat):
    if i > 0:
        # appending to mini-list
        if lat[i] == '': #and temp_height[-1] < ALT:
            temp_height.append(height[i]-ground_level)
            temp_li.append(li[i])
            k += 1
            i += 1
        else:            
            # interpolating to get last item in mini-list
            # f = interpolate.interp1d(temp_height[-2:], temp_li[-2:], fill_value='extrapolate')
            
            # replacing last piece of mini-list with interpolation
            # temp_li[-1] = float(f(ALT))
            # temp_height[-1] = ALT
            
            # combining height and weather mini lists for storage
            temp_combo_li = combineLatLon(temp_height, temp_li)
            
            # getting to next latlon value in big list if not already there
            # while lat[i] == '':
                # i += 1
                # k += 1
            
            # key is location of previous latlon in big list
            key = '%s, %s' % (lat[i-k], lon[i-k])
            print(key)
            
            # appending mini-list to dictionary at latlon key
            if d:
                data[key][keyName] = temp_combo_li
            else:
                data[key] = {keyName: temp_combo_li}
            
            # clearing mini-list and restarting
            temp_height = []
            temp_li = []
            temp_combo_li = []
            k = 0
            temp_height.append(height[i])
            ground_level = temp_height[0]
            # ground level height
            temp_height[0] = temp_height[0] - ground_level
            temp_li.append(li[i])
            k += 1
            i += 1
    
    # getting first element in big list
    else:
        temp_height.append(height[i])
        ground_level = temp_height[0]
        # ground level height
        temp_height[0] = temp_height[0] - ground_level
        temp_li.append(li[i])
        k += 1
        i += 1
        
# getting data from final mini-list

# interpolating using last 2 points
# f = interpolate.interp1d(temp_height[-2:], temp_li[-2:])

# replacing last point in mini-list with interpolation
# temp_li[-1] = float(f(ALT))
# temp_height[-1] = ALT

# combinging height and weather mini-lists for storage
temp_combo_li = combineLatLon(temp_height, temp_li)
print(temp_height,temp_li)
# dictionary key
key = '%s, %s' % (lat[i-k], lon[i-k])

# making dictionary
if d:
    data[key][keyName] = temp_combo_li
else:
    data[key] = {keyName: temp_combo_li}
        
# r = 0        
# for key in data.keys():
    # print(key)
    # print(r)
    # r += 1