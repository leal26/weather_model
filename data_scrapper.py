"""
Code developed to obtain weather data online.

Developed by: Pedro Leal and Justin Cabezuela
"""

#import urllib2
from bs4 import BeautifulSoup
import sys
import requests
import csv
import numpy as np
from scipy import interpolate
import pylab as py

### INPUT YEAR AND MONTH
YEAR = '2018'
MONTH = '01'

### INPUT BEGIN AND END TIME (FORMAT IS DAY/HOUR)
DAY = '07'
FROM = DAY + "00"
TO = DAY + "00"

### LIST OF LOCATIONS ACROSS NA
locations = ['03953','04220','04270','04360','08508','70133','70200','70219',
			 '70231','70261','70273','70316','70326','70350','70398','70414',
			 '71043','71081','71109','71119','71126','71600','71603','71722',
			 '71811','71815','71816','71823','71836','71845','71867','71906',
			 '71907','71908','71909','71913','71924','71925','71926','71934',
			 '71945','71957','71964','72201','72202','72206','72208','72210',
			 '72214','72215','72230','72233','72235','72240','72248','72249',
			 '72251','72261','72265','72274','72293','72305','72317','72318',
			 '72327','72340','72357','72363','72364','72365','72376','72388',
			 '72393','72402','72403','72426','72440','72451','72456','72469',
			 '72476','72489','72493','72501','72518','72520','72528','72558',
			 '72562','72572','72582','72597','72632','72634','72645','72649',
			 '72659','72662','72672','72681','72694','72712','72747','72764',
			 '72768','72776','72786','72797','74005','74389','74455','74494',
			 '74560','74646','74794','76256','76394','76458','76526','76595',
			 '76612','76644','76654','76679','76805','78016','78073','78384',
			 '78397','78486','78526','78583','78807','78897','78954','78970',
			 '91285','80222','82022','91165','91285']

f = open('WBData.csv', 'w')
counter_x = 0
counter_filter = 0
'''f.write('Latitude' + ',' + 'Longtitude' + ',' + 'Pressure [hPa]' + ',' 
			+ 'Height [m]' + ',' + 'Temperature [C]' + ',' 
			+ 'Relative Humidity [%]' + '\n')
'''
all_data = {'latitude':[], 'longitude':[], 'pressure':[], 'height':[], 
			'temperature':[], 'humidity':[],'wind_direction':[], 'wind_speed':[]}
			
for location in locations[0:10]:
    valid_data = True
    counter_x += 1
    page = ('http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR=' 
			+ YEAR + '&MONTH=' + MONTH + '&FROM=' + FROM + '&TO=' + TO + '&STNM=' + location)
    print(counter_x)
    #print(page)
    page = requests.get(page)
    page
    page.content
    data = []
    soup = BeautifulSoup(page.content, 'html.parser')
    the_original_soup = soup.text
    soup = soup.text.split('\n')

    # For loop will find two lines that start with '-' and start processing from there
    counter = 0

    if len(soup) > 100:
        while counter != 2:
            #print(len(soup))
            if len(soup[0]) != 0:
                if soup[0][0] == '-':
                    counter += 1                                    
            soup.pop(0)
        new_soup = []

        # For loop will add new lines until finds a string starting with 'S'
        i = 0
        while soup[i][0] != 'S':
            new_soup.append(soup[i])
            i += 1
        after_soup = soup[i:]
        soup = new_soup

        # Replace all multiple spacing for a single one
        for i in range(len(soup)):
            while '  ' in soup[i]:
                soup[i] = soup[i].replace('  ',' ')
                if soup[i][0] == ' ':
                    soup[i] = soup[i][1:]

        # Search for latitude and longitude
        for i in range(len(after_soup)):
            try:
                if 'Station latitude:' in after_soup[i]:
                    temp = after_soup[i].replace('Station latitude:', '')
                    temp = temp.replace('\n','')
                    latitude = float(temp)
                if 'Station longitude:' in after_soup[i]:
                    temp = after_soup[i].replace('Station longitude:', '')
                    temp = temp.replace('\n','')
                    longitude = float(temp)
            except:
                valid_data = False
        # Replace all spaces for commas
        if valid_data:
            for i in range(len(soup)):
                while ' ' in soup[i]:  
                    soup[i] = soup[i].replace(' ',',')
                    if soup[i][0] == ',':
                        soup[i] = soup[i][1:]
                if soup[i].count(',') == 10:
                    counter_filter += 1
                    if counter_filter == 8:
                        counter_filter = 0
                    if counter_filter == 0:
                        f.write(str(latitude) + ',' + str(longitude) + ',' + soup[i]+'\n')
    obj = soup

    #Delete Unnecessary Columns
f.close() 

f = open("WB" + YEAR + "_" + MONTH + "_" + DAY + ".csv","w")
f.write('Latitude' + ',' + 'Longtitude' + ',' + 'Pressure [hPa]' + ',' + 'Height [m]' 
		+ ',' + 'Temperature [C]' + ',' + 'Relative Humidity [%]' +  ',' 
		+ 'Wind Direction [deg]' +  ',' + 'Wind Speed [knot]' + '\n')
f.close()

with open("WBData.csv", "r") as source:
    rdr= csv.reader(source)
    with open("WB" + YEAR + "_" + MONTH + "_" + DAY + ".csv","a") as result:
        wtr= csv.writer(result)
        for r in rdr:
            wtr.writerow((r[0], r[1], r[3], r[2], r[4], r[6], r[8], r[9]))
            all_data['latitude'].append(float(r[0]))
            all_data['longitude'].append(float(r[1]))
            all_data['pressure'].append(float(r[3]))
            all_data['height'].append(float(r[2]))
            all_data['temperature'].append(float(r[4]))
            all_data['humidity'].append(float(r[6]))
            all_data['wind_direction'].append(float(r[8]))
            all_data['wind_speed'].append(float(r[9]))
#Data = {'lat':[],'long':[], 'Pressure':[]}
#Data.['Pressure'].append(soup[0])

print(all_data)
import pickle

g = open("file.p","wb")
pickle.dump(all_data,g)
g.close()