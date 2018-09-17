'''
attempt to make isoparametric basemap and a few plots of weather data
(temperature, relative humidity, and wind speed/direction) at locations
across the continental U.S.
'''

import matplotlib.pyplot as plt
from functions3 import process_data
from functions3 import process_data_nonzero
from mpl_toolkits.basemap import Basemap

DAY = '01'
MONTH = '08'
YEAR = '22018'
HOUR = '12'

ALT_ft = 45000.
ALT = ALT_ft * 0.3048

# getting data to plot
data, altitudes = process_data_nonzero(DAY, MONTH, YEAR, HOUR, ALT,
                                       outputs_of_interest=['temperature',
                                                            'height',
                                                            'humidity',
                                                            'wind_speed',
                                                            'latitude',
                                                            'longitude',
                                                            'wind_direction'])

# picking points to make graphs of
plot_keys = [list(data.keys())[1704]]  # list(data.keys())[1000],
# list(data.keys())[2000], list(data.keys())[3000], list(data.keys())[4000]]

print(list(data.keys())[1704])
'''
31, -96  (College Station)   1704
41, -74  (New York City)     2646
39, -105 (Colorado Springs)  2431
48, -122 (Seattle)           3242
34, -118 (Los Angeles)       1958
42, -88  (Chicago)           2724
'''
lat = [31]
lon = [-96]
# initializing basemap of U.S.
m = Basemap(projection='merc', llcrnrlat=13, urcrnrlat=58,
            llcrnrlon=-144, urcrnrlon=-53, resolution='l')
# m.drawstates()
map_lon, map_lat = m(*(lon, lat))
m.drawcountries(linewidth=1.0)
m.drawcoastlines()
m.plot(map_lon, map_lat, '.k', ms=1)


for i in range(len(plot_keys)):
    fig, host = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    par1 = host.twiny()
    # par2 = host.twiny()
    par1.xaxis.set_ticks_position("bottom")
    par1.xaxis.set_label_position("bottom")
    par1.spines["bottom"].set_position(("axes", -0.15))

    temperature = data[plot_keys[i]]['temperature']
    humidity = data[plot_keys[i]]['humidity']
    xT = []
    xH = []
    yT = []
    yH = []
    for i in range(len(temperature)):
        yT.append(temperature[i][0])
        yH.append(humidity[i][0])
        xT.append(temperature[i][1])
        xH.append(humidity[i][1])
    p1, = host.plot(xT, yT, "b-", label="Temperature")
    p2, = par1.plot(xH, yH, "k-", label="Humidity")

    host.set_xlim(-80, 40)
    host.set_ylim(0, 18000)
    par1.set_xlim(0, 100)

    host.set_xlabel("Temperature")
    par1.set_xlabel("Humidity")
    host.set_ylabel("Altitude")

    host.xaxis.label.set_color(p1.get_color())
    par1.xaxis.label.set_color(p2.get_color())

    host.tick_params(axis='x', colors=p1.get_color())
    par1.tick_params(axis='x', colors=p2.get_color())

    lines = [p1, p2]
    host.legend(lines, [l.get_label() for l in lines])

    # plt.xlabel('Temperature (C)')
    # plt.ylabel('Altitude (m)')

plt.savefig("test.pdf", transparent=True)
plt.show()
