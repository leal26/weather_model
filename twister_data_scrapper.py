"""
Code developed to obtain weather data online from twisterdata.com. 

"""

import urllib
import csv
from bs4 import BeautifulSoup
import pickle
import unicodedata as ud
import copy


### INPUT YEAR AND MONTH
YEAR = '2018'
MONTH = '05'
### INPUT BEGIN AND END TIME 
DAY = '29'
HOUR = '06'


# Initialize data dictionary
all_data = {'latitude':[], 'longitude':[], 'pressure':[], 'height':[], 
			'temperature':[], 'humidity':[],'wind_direction':[], 
            'wind_speed':[]}

# Define Function to add data points to dictionary            
def appendToDictionary(latitude, longitude):
    all_data['latitude'].append(latitude)
    all_data['longitude'].append(longitude)
    
    prevLength = len(all_data['pressure'])
    
    # Finding table data from accessed html file
    table = soup.find("table", attrs={"class":"soundingTable"})
    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)   
    
    # Adding each datapoint to dictionary
    for i in range(len(datasets)):
        for j in range(13):
            tuple = datasets[i][j]
            element = list(tuple)
            if element[0] == 'PRES':
                all_data['pressure'].append(float(element[1]))
            elif element[0] == 'HGHT':
                all_data['height'].append(float(element[1]))
            elif element[0] == 'TEMP':
                all_data['temperature'].append(float(element[1]))
            elif element[0] == 'RELH':
                all_data['humidity'].append(float(element[1]))
            elif element[0] == 'DRCT':
                all_data['wind_direction'].append(float(element[1]))
            elif element[0] == 'SKNT':
                all_data['wind_speed'].append(float(element[1]))

    for i in range(len(all_data['pressure'])-1-prevLength):
        all_data['latitude'].append('')
        all_data['longitude'].append('')
        

# X,Y Locations on TwisterData.com grid            
# x = [212, 465, 444, 446, 456, 250, 216, 474, 611, 778]
# y = [418, 439, 347, 331, 335, 278, 174, 233, 251, 151]
x = range(431,442) #(972)
y = range(383,394) #(696)

counter = 0
print(counter)
for j in range(len(x)):
    for k in range(len(y)):
        X = str(x[j])
        Y = str(y[k])
        print X, Y
        # Access Website
        html = urllib.urlopen('http://www.twisterdata.com/index.php?'
                              + 'sounding.x=' + X + '&sounding.y=' + Y 
                              + '&prog=forecast&model=GFS&grid=3&model_yyyy='
                              + YEAR + '&model_mm=' + MONTH + '&model_dd=' 
                              + DAY + '&model_init_hh=' + HOUR + '&fhour=00'
                              + '&parameter=TMPF&level=2&unit=M_ABOVE_GROUND'
                              + '&maximize=n&mode=singlemap&sounding=y&output'
                              + '=text&view=large&archive=false&sndclick=y')             
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

        except:
            doNothingVariable = 0
            # do nothing


# making colums to put into the csv file
rows = zip(all_data['latitude'], all_data['longitude'], 
           all_data['pressure'], all_data['height'], 
           all_data['temperature'], all_data['humidity'],
           all_data['wind_direction'], all_data['wind_speed'])

# initializing csv file
f = open("Twister" + YEAR + "_" + MONTH + "_" + DAY + ".csv","w")
f.write('Latitude' + ',' + 'Longtitude' + ',' + 'Pressure [hPa]' + ',' 
        + 'Height [m]' + ',' + 'Temperature [C]' + ',' 
        + 'Relative Humidity [%]' +  ',' + 'Wind Direction [deg]' +  ',' 
        + 'Wind Speed [knot]' + '\n')
f.close()

# adding data to csv file in table format
with open("Twister" + YEAR + "_" + MONTH + "_" + DAY + ".csv", "a") as f:
        wtr= csv.writer(f)
        for row in rows:
            wtr.writerow(row)

# creating pickle file for later use
g = open("file" + DAY + ".p","wb")
pickle.dump(all_data,g)
g.close()
