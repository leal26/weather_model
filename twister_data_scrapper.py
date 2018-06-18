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
import functions


### INPUT YEAR AND MONTH
YEAR = '2018'
MONTH = '06'
### INPUT DAY AND HOUR 
DAY = '13'
HOUR = '12'

start = '{:%H:%M:%S}'.format(datetime.datetime.now())

# Initialize data dictionary
all_data = {'latitude':[], 'longitude':[], 'pressure':[], 'height':[], 
			'temperature':[], 'humidity':[],'wind_direction':[], 
            'wind_speed':[]}      

# Lat, Lon Locations on TwisterData.com grid            
x = np.linspace(13,16,4) #lat - (13,58)
y = np.linspace(-144,-53,92) #lon - (-144,-53)


for j in range(len(x)):
    for k in range(len(y)):
        X = str(x[j])
        Y = str(y[k])
        print X, Y
        # print('{:%H:%M:%S}'.format(datetime.datetime.now()))
        # Access Website
        try:
            q = 0
            while q < 1:
                r = requests.get('http://www.twisterdata.com/index.php?'
                              + 'sounding.lat=' + X + '&sounding.lon=' + Y 
                              + '&prog=forecast&model=GFS&grid=3&model_yyyy='
                              + YEAR + '&model_mm=' + MONTH + '&model_dd=' 
                              + DAY + '&model_init_hh=' + HOUR + '&fhour=00'
                              + '&parameter=TMPF&level=2&unit=M_ABOVE_GROUND'
                              + '&maximize=n&mode=singlemap&sounding=y&output'
                              + '=text&view=large&archive=false&sndclick=y', timeout=5)
                q += 1
        except:
            print 'ERROR'
                
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        try:
            # Finding Latitude and Longitude for each accessed webpage
            lat = soup.find("div", attrs={"class":"soundingLatLonHeader"})
            label = lat.get_text()
            words = ud.normalize('NFKD',label).encode('ascii','ignore')
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
            functions.appendToDictionary(latitude, longitude)
               
            ''' NO LONGER NEEDED since lat and lon are changed in url
            ydict = copy.deepcopy(all_data)
            yy = ydict['latitude']
            xx = ydict['longitude']
            i = 0
            bigList = []
            while '' in xx:
                if i > 0 and xx[i] == '':
                        xx.pop(i)
                        yy.pop(i)
                else:
                    bigList.append([xx[i], yy[i]])
                    i += 1
            if [longitude, latitude] not in bigList:
                appendToDictionary(latitude, longitude)
                counter += 1
                print(counter)
            '''
        except:
            doNothingVariable = 0
            # do nothing


# making colums to put into the csv file
rows = zip(all_data['latitude'], all_data['longitude'], 
           all_data['pressure'], all_data['height'], 
           all_data['temperature'], all_data['humidity'],
           all_data['wind_direction'], all_data['wind_speed'])

# initializing csv file
f = open("Twister" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".csv","w")
f.write('Latitude' + ',' + 'Longtitude' + ',' + 'Pressure [hPa]' + ',' 
        + 'Height [m]' + ',' + 'Temperature [C]' + ',' 
        + 'Relative Humidity [%]' +  ',' + 'Wind Direction [deg]' +  ',' 
        + 'Wind Speed [knot]' + '\n')
f.close()

# adding data to csv file in table format
with open("Twister" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".csv", "a") as f:
        wtr= csv.writer(f)
        for row in rows:
            wtr.writerow(row)

# creating pickle file for later use
g = open("file2" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".p","wb")
pickle.dump(all_data,g)
g.close()

print start
print('{:%H:%M:%S}'.format(datetime.datetime.now()))
