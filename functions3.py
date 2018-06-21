#!python3
'''
Code that consolidates all functions3 needed to run any file in
 weather_module repository in alphabetical order.
'''
import pickle
import copy
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import griddata 
from mpl_toolkits.basemap import Basemap
import functions3


          
def appendToDictionary(latitude, longitude, all_data, soup):
    ''' appendToDictionary appends the data scraped from twisterdata.com
    to a dictionary for later use in this repository.  
    '''
    all_data['latitude'].append(latitude)
    all_data['longitude'].append(longitude)
    
    prevLength = len(all_data['pressure'])
    
    # Finding table data from accessed html file
    table = soup.find("table", attrs={"class":"soundingTable"})
    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    datasets = []
    for row in table.find_all("tr")[1:]:
        dataset = list(zip(headings, (td.get_text() 
                                 for td in row.find_all("td"))))
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
    
    
    
def combineLatLon(lat, lon):
    '''combineLatLon takes a list of latitudes and a list of longitudes 
    that are the same length and combines them into a double list.
    '''
    w_latlon = []
    for i in range(len(lat)):
        w_latlon.append([lat[i], lon[i]])
    
    return w_latlon


    
def contourfGenerator(ALT):
    '''contourfGenerator creates a contour plot for use in an animation
    creator. It takes a list of integer altitudes as an input.
    This function uses openPickle and myInterpolate.
    '''
    height, relh = functions3.openPickle('17', '06', '2018', '12')[1:3]
    lat, lon = functions3.openPickle('17', '06', '2018', '12')[6:8]
    # data = functions3.openPickle('12', '06', '2018', '12','all')
    # height = data['height']
    # relh = data['relh']
    # lat = data['lat']
    # lon = data['lon']

    # Finding humidity for each lat/long at set altitude
    w_variable = functions3.myInterpolate(lat, lon, relh, height, ALT)

    # remove empty cells from lat/long
    i = 0
    while '' in lon:
        if i > 0 and lon[i] == '':
                lon.pop(i)
                lat.pop(i)
        else:
            i += 1
    numcols, numrows = len(lon), len(lat)

    # Make lists into arrays to graph
    lon = functions3.makeFloats(lon)
    lat = functions3.makeFloats(lat)
    lon = np.array(lon)
    lat = np.array(lat)
    z = w_variable
    
    m = Basemap(projection='merc',llcrnrlat=13,urcrnrlat=58,
            llcrnrlon=-144,urcrnrlon=-53,resolution='c')
    map_lon, map_lat = m(*(lon,lat))
        
    # target grid to interpolate to
    xi = np.linspace(map_lon.min(), map_lon.max(), numcols)
    yi = np.linspace(map_lat.min(), map_lat.max(), numrows)
    xi,yi = np.meshgrid(xi,yi)
    
    # interpolate
    zi = griddata((map_lon,map_lat),z,(xi,yi),method='linear')
    return xi, yi, zi 

    
    
def getFlightPlan(Departure, Arrival):
    '''getFlightPlan takes the departure and landing locations as 
    inputs and outputs the latitude, longitude, altitude and distance 
    information from the flight plan.
    '''
    filename = Departure + '-' + Arrival
    
    height = []
    lat = []
    lon = []
    dist = []
    with open('Flight_Plan_Files/' + filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            height.append(row[2])
            lat.append(row[3])
            lon.append(row[4])
            dist.append(row[5])
            
    # changing flight plan data to floats and making height meters
    for i in range(len(height)):
        height[i] = float(height[i])
        height[i] = 0.3048 * height[i]
        lat[i] = float(lat[i])
        lon[i] = float(lon[i])
        dist[i] = float(dist[i])
    
    return height, lat, lon, dist

  
    
'''heightToMeters and heightToFeet are functions3 that convert a float
   input height to meters or feet, respectively.'''
def heightToMeters(height):
    height = height / 0.3048
    return height
def heightToFeet(height):
    height = height * 0.3048
    return height
 
 
 
def makeFloats(w_var):  
    '''makeFloats takes a weather variable as an input list and makes 
    every element in the list a float for use in mathematical 
    calculations. This function also converts any '' in the list to a 0.
    '''  
    for i in range(len(w_var)):
        if w_var[i] == '':
            w_var[i] = 0
            w_var[i] = 0
        
        w_var[i] = float(w_var[i])
        
    return w_var
 


def makeShortList(lat, li):
    ''' makeShortList makes a list of a weather variable at each latitude 
    and longitude location.
    '''
    for i in range(len(lat)):
        if i > 0:
            if lat[i] == 0 or lat[i] == '':
                temp_li.append(li[i])
            else:                  
                return temp_li
        else:
            temp_li.append(li[i])
 
 
 
def myInterpolate(lat, lon, w_name, height, ALT):
    '''myInterpolate executes a linear interpolation for a desired 
    weather variable at each sounding location. It takes the inputs lat,
    lon, and height (usually from openPickle), w_name (name of weather
    variable to interpoalte), and ALT (altitude). If the desired 
    altitude is below 3500 meters, the function outputs the ground 
    level data for the desired weather_variable.
    '''
    h = []
    w = []
    w_variable = []
    if ALT > 3500:
        for i in range(len(lon)):
            if i > 0:
                if lon[i] == '':
                    h.append(height[i])
                    w.append(w_name[i])
                else:
                    Alt = ALT
                    loc = -1
                    while loc == -1:
                        if Alt in h:
                            loc = h.index(Alt)
                        else:
                            Alt -= 1
                    w_variable.append(((ALT - h[loc])*((w[loc+1] 
                                        - w[loc])/(h[loc+1] - h[loc]))) 
                                        + w[loc])
                    
                    h = []
                    h.append(height[i])
                    w = []
                    w.append(w_name[i])
            else:
                h.append(height[i])
                w.append(w_name[i])
        # Getting last weather value        
        Alt = ALT
        loc = -1
        while loc == -1:
            if Alt in h:
                loc = h.index(Alt)
            else:
                Alt -= 1
        w_variable.append(((ALT - h[loc])*((w[loc+1] - w[loc])/(h[loc+1] 
                            - h[loc]))) + w[loc])
    
    elif ALT < 3500:
        for i in range(len(lon)):
            if lon[i] != '':
                w_variable.append(w_name[i])
    
    w_variable = np.array(w_variable)                  
    return w_variable

    
    
# def openPickle(DAY, MONTH, YEAR, HOUR,
               # outputs_of_interest=['temperature','height','pressure',
                                    # 'latitude', 'longitude', 'wind speed',
                                    # 'wind direction', 'humidity']):
    # ''' openPickle makes a dictionary output that contains the lists
    # specified by the strings given in outputs_of_interest
    # '''
    # all_data = pickle.load(open("Pickle_Data_Files/file" + YEAR + "_" 
                                # + MONTH + "_" + DAY + "_" + HOUR + ".p",
                                # "rb"))
    
    # if outputs_of_interest == 'all':
        # output = all_data
    # else:
        # output = {}
        # for key in outputs_of_interest:
            # output[key] = copy.deepcopy(all_data[key])
    
    # return output  
  
def openPickle(DAY, MONTH, YEAR, HOUR):
    '''openPickle opens the scraped data from the pickle and put the data 
    into usable lists. Takes input strings DAY, MONTH, YEAR, HOUR to
    identify filename.
    '''
    all_data = pickle.load(open("Pickle_Data_Files/file" + YEAR + "_" 
                                + MONTH + "_" + DAY + "_" + HOUR + ".p",
                                "rb"))
    
    w_temp = copy.deepcopy(all_data['temperature'])
    w_height = copy.deepcopy(all_data['height'])
    w_relh = copy.deepcopy(all_data['humidity'])
    w_pres = copy.deepcopy(all_data['pressure'])
    w_sknt = copy.deepcopy(all_data['wind_speed'])
    w_drct = copy.deepcopy(all_data['wind_direction'])
    w_lat = copy.deepcopy(all_data['latitude'])
    w_lon = copy.deepcopy(all_data['longitude'])
    
    return w_temp, w_height, w_relh, w_pres, w_sknt, w_drct, w_lat,w_lon
  
     
     
def sBoomDictMaker(li, keyName, ALT, lat, lon, height, data):
    ''' sBoomDictMaker takes a weather variable list, list keyName, and
    a max altitude (ALT) as user defined inputs. It also requires the
    existance of a dictionary data, and the lat, lon, and height lists
    from the openPickle function. Using these, it makes a dictionary
    with first key being a lat,lon point and second key being the 
    name of the weather variable.
    '''
    temp_height = []
    temp_li = []
    li_combos = []
    d = copy.deepcopy(data)
    k = 0
    for i in range(len(lat)):
        if i > 0:
            if temp_height == []:
                temp_height.append(height[i])
                temp_li.append(li[i])
                k += 1
            elif lat[i] == 0 and temp_height[-1] < ALT:
                temp_height.append(height[i])
                temp_li.append(li[i])
                k += 1
            else:
                # make ground level 0
                for j in range(len(temp_height)):
                    temp_height[j] = temp_height[j] - temp_height[0]
                
                f = interpolate.interp1d(temp_height[-2:], temp_li[-2:])
                
                temp_li[-1] = float(f(ALT))
                temp_height[-1] = ALT
                
                temp_combo_li = functions3.combineLatLon(temp_height, 
                                                        temp_li)
                
                key = '%i, %i' % (lat[i-k], lon[i-k])
                if d:
                    data[key][keyName] = temp_combo_li
                else:
                    data[key] = {keyName: temp_combo_li}
                
                temp_height = []
                temp_li = []
                k = 0
        else:
            temp_height.append(height[i])
            temp_li.append(li[i])
            k += 1
            
    return data


    
#FIXME - make me into a function pls
def threeDInterpolater(x1, y1, lon, lat, height, w_latlon, w_lat, w_lon,
                       w_height):
    '''threeDInterpolater finds the 4 closest points to a latitude and 
    longitude location along the flight path. Then, the function 
    linearly interpolates to find the desired weather variable at the 
    height of the aircraft at each of the 4 closest points. With these, 
    the function executes a 2D linear interpolation to find the value of
    the weather_variable at the location along the flight path.
    '''
    if lon > x1 and lat > y1:
        x2 = x1 - 1
        y2 = y1 - 1
    elif lon < x1 and lat > y1:
        x2 = x1 + 1
        y2 = y1 - 1
    elif lon < x1 and lat < y1:
        x2 = x1 + 1
        y2 = y1 + 1
    elif lon > x1 and lat < y1:
        x2 = x1 - 1
        y2 = y1 + 1
    else:
        print('ERROR')
    
    # finding indices of each location
    loc1 = w_latlon.index([y1,x1]) # same as [y1, x1]
    loc2 = w_latlon.index([y2,x1])
    loc3 = w_latlon.index([y1,x2])
    loc4 = w_latlon.index([y2,x2])
    
    # making height vectors for each location
    height1 = []
    height1.append(w_height[loc1])
    relh1 = []
    relh1.append(w_relh[loc1])
    height2 = []
    height2.append(w_height[loc2])
    relh2 = []
    relh2.append(w_relh[loc2])
    height3 = []
    height3.append(w_height[loc3])
    relh3 = []
    relh3.append(w_relh[loc3])
    height4 = []
    height4.append(w_height[loc4])
    relh4 = []
    relh4.append(w_relh[loc4])
    j = 1
    while w_lat[loc1 + j] == 0:
        height1.append(w_height[loc1 + j])
        relh1.append(w_relh[loc1 + j])
        j += 1
    j = 1
    while w_lat[loc2 + j] == 0:
        height2.append(w_height[loc2 + j])
        relh2.append(w_relh[loc2 + j])
        j += 1
    j = 1
    while w_lat[loc3 + j] == 0:
        height3.append(w_height[loc3 + j])
        relh3.append(w_relh[loc3 + j])
        j += 1
    j = 1
    while w_lat[loc4 + j] == 0:
        height4.append(w_height[loc4 + j])
        relh4.append(w_relh[loc4 + j])
        j += 1
    
    # linear 1d interpolation to get 4 humidities at 4 locations
    f1 = interpolate.interp1d(height1, relh1, fill_value="extrapolate")
    f2 = interpolate.interp1d(height2, relh2, fill_value="extrapolate")
    f3 = interpolate.interp1d(height3, relh3, fill_value="extrapolate")
    f4 = interpolate.interp1d(height4, relh4, fill_value="extrapolate")
    
    # making arrays for 2d interpolation at each location
    relh_loc = []
    relh_loc.append(f1(height))
    relh_loc.append(f2(height))
    relh_loc.append(f3(height))
    relh_loc.append(f4(height))
    
    w_lon_loc = []
    w_lon_loc.append(w_lon[loc1])
    w_lon_loc.append(w_lon[loc2])
    w_lon_loc.append(w_lon[loc3])
    w_lon_loc.append(w_lon[loc4])
    
    w_lat_loc = []
    w_lat_loc.append(w_lat[loc1])
    w_lat_loc.append(w_lat[loc2])
    w_lat_loc.append(w_lat[loc3])
    w_lat_loc.append(w_lat[loc4])
    
    # 2d interpolation
    f2d = interpolate.interp2d(w_lon_loc, w_lat_loc, relh_loc)
    final_relh = f2d(lon, lat)
    relh.append(final_relh[0])
    
    return relh

    
    
    
    
    
    
    
    