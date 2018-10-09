from scipy import io
import numpy as np
from functions3 import makeFloats

'''
data = io.loadmat('data_3.mat')
'''

latitude = range(13, 14)  # 58)
longitude = range((360-144), (360-143))  # (360-92))
# 0 = height
# 1 = temperature
# 2 = wind_x
# 3 = wind_y
# 4 = relative humidity
# data['s'][lat][lon][w_var][0][item in w_var list]
# print(data['s'][13][216][4][0][0])
'''
point_data = {'height': [], 'temperature': [], 'wind_x': [], 'wind_y': [],
              'humidity': []}

shape = np.shape(data['s'])
# print(shape)

for i in range(13, shape[0]):
    for j in range(216, shape[1]):
        point_data['height'].append(data['s'][i][j][0][0])
        point_data['temperature'].append(data['s'][i][j][1][0])
        point_data['wind_x'].append(data['s'][i][j][2][0])
        point_data['wind_y'].append(data['s'][i][j][3][0])
        point_data['humidity'].append(data['s'][i][j][4][0])
'''


def output_for_sBoom_mat(ALT):
    data = io.loadmat('data_3.mat')
    shape = np.shape(data['s'])
    all_data = {}
    point_data = {'height': [], 'temperature': [], 'wind_x': [], 'wind_y': [],
                  'humidity': []}
    cruise_altitudes = []
    lat = np.arange(13, shape[0])
    lon = np.arange(216, shape[1])
    for i in lat:
        for j in lon:
            # NOTE - data is inverted for GFS 3 and not for GFS 4
            point_data['height'] = list(data['s'][i][j][0][0][::-1])
            point_data['temperature'] = list(data['s'][i][j][1][0][::-1])
            point_data['wind_x'] = list(data['s'][i][j][2][0][::-1])
            point_data['wind_y'] = list(data['s'][i][j][3][0][::-1])
            point_data['humidity'] = list(data['s'][i][j][4][0][::-1])

            # Heights minus ground height (make ground 0)
            print(point_data['height'][0])
            h = point_data['height'][0]
            cruise_altitudes.append(ALT - h)

            height = []
            for k in range(len(point_data['height'])):
                height.append(point_data['height'][k] - h)

            key = '%i, %i' % (lat[i-13], lon[j-216])
            keyNames = ['temperature', 'wind_x', 'wind_y', 'humidity']
            all_data[key] = {'temperature': [], 'wind_x': [], 'wind_y': [],
                             'humidty': []}
            for keyName in keyNames:
                for i in range(len(height)):
                    all_data[key][keyName].append([height[i],
                                                   point_data[keyName][i]])

    return all_data, cruise_altitudes


ALT = 45000. * 0.3048
data, altitudes = output_for_sBoom_mat(ALT)
print(data['13, 216']['humidity'][1])
print(altitudes[0])
