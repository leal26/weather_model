'''
pickle to csv
'''

import pickle
import csv
import copy

# opening noise pickle
filename = 'noise_test2018_06_18_12'
YEAR = '2018'
MONTH = '06'
DAY = '18'
HOUR = '12'
noise_data = pickle.load(open(filename + '.p', 'rb'))

# making latlon into seperate columns
lat = []
lon = []
location = []
latlon = copy.deepcopy(noise_data['latlon'])
for i in range(len(latlon)):
    latlon_temp = [int(s) for s in latlon[i].split(',')]
    lat.append(latlon_temp[0])
    lon.append(latlon_temp[1])
    location.append('<Polygon><outerBoundaryIs><LinearRing><coordinates>\
                    %f,%f %f,%f %f,%f %f,%f %f,%f\
                    </coordinates></LinearRing></outerBoundaryIs></Polygon>'
                    % ((latlon_temp[1])-0.5, latlon_temp[0]+0.5,
                       (latlon_temp[1])+0.5, latlon_temp[0]+0.5,
                       (latlon_temp[1])+0.5, latlon_temp[0]-0.5,
                       (latlon_temp[1])-0.5, latlon_temp[0]-0.5,
                       (latlon_temp[1])-0.5, latlon_temp[0]+0.5))

# making columns for csv file
rows = zip(lat, lon, noise_data['noise'], location)

# initializing csv file
f = open("Noise2d" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".csv",
         "w")
f.write('Latitude' + ',' + 'Longtitude' + ',' + 'Noise (PLdB)' + 'Location' +
        '\n')
f.close()

# adding data to csv file in table format
with open("Noise2d" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".csv",
          "a") as f:
    wtr = csv.writer(f)
    for row in rows:
        wtr.writerow(row)
