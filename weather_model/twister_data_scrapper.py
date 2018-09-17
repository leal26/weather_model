"""
Code developed to scrape weather data online from TwisterData.com.
 Data is scraped from the input Date and Time.
 Data is from the GFS weather model used by TwisterData.com.
"""

import requests
import csv
from bs4 import BeautifulSoup
import pickle
import unicodedata as ud
import copy
import datetime
import numpy as np
import functions3


# INPUT YEAR AND MONTH
YEAR = str(datetime.date.today().strftime('%Y'))
MONTH = str(datetime.date.today().strftime('%m'))
# INPUT DAY AND HOUR
DAY = str(datetime.date.today().strftime('%d'))
HOUR = '12'

start = '{:%H:%M:%S}'.format(datetime.datetime.now())

# Initialize data dictionary
all_data = {'latitude': [], 'longitude': [], 'pressure': [], 'height': [],
            'temperature': [], 'humidity': [], 'wind_direction': [],
            'wind_speed': []}

# Lat, Lon Locations on TwisterData.com grid
x = np.linspace(13, 14, 1)  # 58, 46)  # lat - (13,58)
y = np.linspace(-144, -53, 92)  # lon - (-144,-53)


for j in range(len(x)):
    for k in range(len(y)):
        X = str(x[j])
        Y = str(y[k])
        print(X, Y)
        # Access Website
        q = 0
        while q < 1:
            try:
                r = requests.get('http://www.twisterdata.com/index.php?' +
                                 'sounding.lat=' + X + '&sounding.lon=' + Y +
                                 '&prog=forecast&model=GFS&grid=3&model_' +
                                 'yyyy=' + YEAR + '&model_mm=' + MONTH +
                                 '&model_dd=' + DAY + '&model_init_hh=' +
                                 HOUR + '&fhour=00' + '&parameter=TMPF&level' +
                                 '=2&unit=M_ABOVE_GROUND&maximize=n&mode=sin' +
                                 'glemap&sounding=y&output=text&view=large&a' +
                                 'rchive=false&sndclick=y', timeout=5)
                q += 1
            except IOError:
                print('ERROR')
                q = 0

        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            # Finding Latitude and Longitude for each accessed webpage
            lat = soup.find("div", attrs={"class": "soundingLatLonHeader"})
            label = lat.get_text()
            words = ud.normalize('NFKD', label).encode('ascii', 'ignore')
            word_list = words.split()
            latitude = word_list[12]
            long_1 = word_list[15]
            longitude = long_1[:-52]

            # check if latitude and longitude are a numbers
            latnum = latitude
            latnum = float(latnum)
            longnum = longitude
            longnum = float(longnum)

            # add elements to dictionary
            functions3.appendToDictionary(latitude, longitude, all_data, soup)

        except ValueError:
            doNothingVariable = 0
            print('Value Error - Invalid Date')
            # do nothing

# making colums to put into the csv file
rows = zip(all_data['latitude'], all_data['longitude'],
           all_data['pressure'], all_data['height'],
           all_data['temperature'], all_data['humidity'],
           all_data['wind_direction'], all_data['wind_speed'])

# initializing csv file
f = open("Twister" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".csv", "w")
f.write('Latitude' + ',' + 'Longtitude' + ',' + 'Pressure [hPa]' + ',' +
        'Height [m]' + ',' + 'Temperature [C]' + ',' +
        'Relative Humidity [%]' + ',' + 'Wind Direction [deg]' + ',' +
        'Wind Speed [knot]' + '\n')
f.close()

# adding data to csv file in table format
with open("Twister" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".csv",
          "a") as f:
    wtr = csv.writer(f)
    for row in rows:
        wtr.writerow(row)

# creating pickle file for later use
g = open("file" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".p", "wb")
pickle.dump(all_data, g)
g.close()

print(start)
print('{:%H:%M:%S}'.format(datetime.datetime.now()))
# send email when complete
