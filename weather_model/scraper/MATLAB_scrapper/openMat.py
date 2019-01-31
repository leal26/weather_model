from scipy import io
import numpy as np
from functions3 import makeFloats

'''
Practice Function for converting .mat files to pickle files
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
    data = io.loadmat('data_092518.mat')
    # shape = np.shape(data['s'])
    all_data = {}
    # point_data = {'height': [], 'temperature': [], 'wind_x': [],
    # 'wind_y': [], 'humidity': []}
    cruise_altitudes = []
    lat = range(64, 156, 2)  # FIXME: These numbers need to be checked
    lon = range(432, 616, 2)
    for i in lat:
        for j in lon:
            # NOTE - data is inverted for GFS 3 and not for GFS 4
            '''
            point_data['height'] = list(data['s'][i][j][0][0][::-1])
            point_data['temperature'] = list(data['s'][i][j][1][0][::-1])
            point_data['wind_x'] = list(data['s'][i][j][2][0][::-1])
            point_data['wind_y'] = list(data['s'][i][j][3][0][::-1])
            point_data['humidity'] = list(data['s'][i][j][4][0][::-1])
            '''
            height = list(data['s'][i][j][0][0])
            temperature = list(data['s'][i][j][1][0])
            wind_x = list(data['s'][i][j][2][0])
            wind_y = list(data['s'][i][j][3][0])
            humidity = list(data['s'][i][j][4][0])

            # Heights minus ground height (make ground 0)
            # print(point_data['height'][0])
            # h = point_data['height'][0]
            # print(data['s'][64][614][0][0])
            # print(i, j)
            h = height[0]
            cruise_altitudes.append(ALT - h)

            relative_height = []
            for k in range(len(height)):
                relative_height.append(height[k] - h)
                temperature[k] = temperature[k] - 273.15
                wind_x[k] = wind_x[k] * 1.94384
                wind_y[k] = wind_y[k] * 1.94384

            key = '%i, %i' % (int(i/2), int(360-(j/2)))
            # keyNames = ['temperature', 'wind_x', 'wind_y', 'humidity']
            all_data[key] = {'temperature': [], 'wind_x': [], 'wind_y': [],
                             'humidity': []}
            for l in range(len(relative_height)):
                all_data[key]['temperature'].append([relative_height[l],
                                                     temperature[l]])
                all_data[key]['wind_x'].append([relative_height[l],
                                                wind_x[l]])
                all_data[key]['wind_y'].append([relative_height[l],
                                                wind_y[l]])
                all_data[key]['humidity'].append([relative_height[l],
                                                  humidity[l]])

    return all_data, cruise_altitudes


ALT = 45000. * 0.3048
data, altitudes = output_for_sBoom_mat(ALT)
print(data['32, 90']['temperature'][0])
print(altitudes[0])
