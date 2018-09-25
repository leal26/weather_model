from scipy import io
import numpy as np

data = io.loadmat('data_3.mat')

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

for i in range(13, shape[0]):
    for j in range(216, shape[1]):
        point_data['height'].append(data['s'][i][j][0][0])
        point_data['temperature'].append(data['s'][i][j][1][0])
        point_data['wind_x'].append(data['s'][i][j][2][0])
        point_data['wind_y'].append(data['s'][i][j][3][0])
        point_data['humidity'].append(data['s'][i][j][4][0])


def output_for_sBoom_mat():
    data = io.loadmat('data_3.mat')
    shape = np.shape(data['s'])
    all_data = {}
    point_data = {'height': [], 'temperature': [], 'wind_x': [], 'wind_y': [],
                  'humidity': []}
    ground_altitudes = []
    lat = np.arange(13, shape[0])
    lon = np.arange(216, shape[1])
    for i in lat:
        for j in lon:
            # NOTE - data is inverted for GFS 3 and not for GFS 4
            point_data['height'] = data['s'][i][j][0][0][::-1]
            point_data['temperature'] = data['s'][i][j][1][0][::-1]
            point_data['wind_x'] = data['s'][i][j][2][0][::-1]
            point_data['wind_y'] = data['s'][i][j][3][0][::-1]
            point_data['humidity'] = data['s'][i][j][4][0][::-1]

            # FIXME - heights minus ground height (make ground 0)?
            h = np.array(point_data['height'])
            height = h - point_data['height'][0]
            ground_altitudes.append(height)

            key = '%i, %i' % (lat[i-13], lon[j-216])
            keyNames = ['temperature', 'wind_x', 'wind_y', 'humidity']
            all_data[key] = {'temperature': [], 'wind_x': [], 'wind_y': [],
                             'humidty': []}
            for keyName in keyNames:
                all_data[key][keyName] = [ground_altitudes,
                                          point_data[keyName]]

    return all_data, ground_altitudes


data, altitudes = output_for_sBoom_mat()
