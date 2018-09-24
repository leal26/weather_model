from scipy import io
import numpy as np

data = io.loadmat('data.mat')

latitude = range(13, 14)  # 58)
longitude = range((360-144), (360-143))  # (360-92))
# 0 = height
# 1 = temperature
# 2 = wind_x
# 3 = wind_y
# 4 = relative humidity
# data['s'][lat][lon][w_var][0][item in w_var list]
print(data['s'][13][216][0][0][1])

point_data = {'height': [], 'temperature': [], 'wind_x': [], 'wind_y': [],
              'humidity': []}

shape = np.shape(data['s'])
print(shape)

for i in range(shape[0]):
    for j in range(shape[1]):
        point_data['height'].append(data['s'][i][j][0][0])
        point_data['temperature'].append(data['s'][i][j][1][0])
        point_data['wind_x'].append(data['s'][i][j][2][0])
        point_data['wind_y'].append(data['s'][i][j][3][0])
        point_data['humidity'].append(data['s'][i][j][4][0])


def output_for_sBoom_mat(li, keyName):
    data = io.loadmat('data.mat')
    shape = np.shape(data['s'])
    all_data = {}
    ground_altitudes = []
    lat = range(shape[0])
    lon = range(shape[1])
    for i in lat:
        for j in lon:
            # FIXME - check data and see if it is inverted... somehow
            point_data['height'].append(data['s'][i][j][0][0])
            point_data['temperature'].append(data['s'][i][j][1][0])
            point_data['wind_x'].append(data['s'][i][j][2][0])
            point_data['wind_y'].append(data['s'][i][j][3][0])
            point_data['humidity'].append(data['s'][i][j][4][0])

            key = '%i, %i' % (lat[i], lon[j])
            keyNames = ['temperature', 'wind_x', 'wind_y', 'humidity']
            for keyName in keyNames:
                all_data = [key][keyName] = point_data[keyName]

            # FIXME - heights minus ground height (make ground 0)?
            ground_altitudes.append(point_data['height'][0])

    return all_data, ground_altitudes
