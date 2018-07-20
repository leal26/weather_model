'''
fix pickle
'''

import pickle
import copy

filename = 'noise_test2018_06_18_12'
YEAR = '2018'
MONTH = '06'
DAY = '18'
HOUR = '12'
noise_data = pickle.load(open(filename + '.p','rb'))
data = copy.deepcopy(noise_data)

data['latlon'].pop(4037)
data['noise'].pop(4037)
data['latlon'].pop(4090)
data['noise'].pop(4090)
data['latlon'].pop(4118)
data['noise'].pop(4118)

print(len(noise_data['latlon']))
print(len(data['latlon']))
g = open("noise_test_fix" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".p","wb")
pickle.dump(data,g)
g.close()