#!python3
'''
Code that consolidates all functions3 needed to run any file in
 weather_module repository in alphabetical order.
'''
import pickle
import copy
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy import io
from scipy.interpolate import griddata
from scipy.interpolate import interp1d
from mpl_toolkits.basemap import Basemap


def appendToDictionary(latitude, longitude, all_data, soup):
    ''' appendToDictionary appends the data scraped from twisterdata.com
    to a dictionary for later use in this repository.
    '''
    all_data['latitude'].append(latitude)
    all_data['longitude'].append(longitude)

    prevLength = len(all_data['pressure'])

    # Finding table data from accessed html file
    table = soup.find("table", attrs={"class": "soundingTable"})
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
    height, relh = openPickle('18', '06', '2018', '12')[1:3]
    lat, lon = openPickle('18', '06', '2018', '12')[6:8]

    # Finding humidity for each lat/long at set altitude
    w_variable = myInterpolate(lat, lon, relh, height, ALT)

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
    lon = makeFloats(lon)
    lat = makeFloats(lat)
    lon = np.array(lon)
    lat = np.array(lat)
    z = w_variable

    m = Basemap(projection='merc', llcrnrlat=13, urcrnrlat=58,
                llcrnrlon=-144, urcrnrlon=-53, resolution='c')
    map_lon, map_lat = m(*(lon, lat))

    # target grid to interpolate to
    xi = np.linspace(map_lon.min(), map_lon.max(), numcols)
    yi = np.linspace(map_lat.min(), map_lat.max(), numrows)
    xi, yi = np.meshgrid(xi, yi)

    # interpolate
    zi = griddata((map_lon, map_lat), z, (xi, yi), method='linear')
    return xi, yi, zi


def getFlightPlan(Departure, Arrival):
    '''getFlightPlan takes the departure and landing locations as
    inputs and outputs the latitude, longitude, altitude and distance
    information from the flight plan.
    '''
    filename = Departure + '-' + Arrival + '.csv'

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


def heightToMeters(height):
    '''heightToMeters and heightToFeet are functions3 that convert a float
       input height to meters or feet, respectively.'''
    height = height / 0.3048
    return height


def heightToFeet(height):
    '''heightToMeters and heightToFeet are functions3 that convert a float
       input height to meters or feet, respectively.'''
    height = height * 0.3048
    return height


def MachModifier(direction, Mach, ALT, wind):
    '''Takes a direction of the aircraft in degrees counterclockwise
        from East (+x) and outputs a modified Mach number based on the
        wind speed at the altitude of the aircraft.'''

    # find wind at altitude with linear interpolation
    wind_height = []
    wind_x = []
    wind_y = []
    for i in range(len(wind)):
        wind_height.append(wind[i][0])
        wind_x.append(wind[i][1])
        wind_y.append(wind[i][2])

    f_x = interp1d(wind_height, wind_x)
    f_y = interp1d(wind_height, wind_y)

    x_wind = f_x(ALT)
    y_wind = f_y(ALT)

    theta = math.radians(direction)  # making direction radians
    velocity = 340.2778 * Mach  # converting Mach number to m/s

    # Finding new speed of aircraft based on wind speed
    mach_new1 = velocity + (x_wind*np.cos(theta))
    mach_new = mach_new1 + (y_wind*np.sin(theta))

    # converting from m/s back to mach
    mach_new = mach_new / 340.2778

    return mach_new


def makeFloats(w_var):
    '''makeFloats takes a weather variable as an input list and makes
    every element in the list a float for use in mathematical
    calculations. This function also converts any '' in the list to a 0.
    '''
    for i in range(len(w_var)):
        if w_var[i] == '':
            w_var[i] = 0

        w_var[i] = float(w_var[i])

    return w_var


def makeShortList(lat, li):
    ''' makeShortList makes a list of a weather variable at each latitude
    and longitude location.
    '''
    temp_li = []
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
    if ALT >= 3500:
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
                    w_variable.append(((ALT - h[loc])*((w[loc+1] -
                                                        w[loc])/(h[loc+1] -
                                                                 h[loc]))) +
                                      w[loc])

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
        w_variable.append(((ALT - h[loc])*((w[loc+1] - w[loc])/(h[loc+1] -
                                                                h[loc]))) +
                          w[loc])

    elif ALT < 3500:
        for i in range(len(lon)):
            if lon[i] != '':
                w_variable.append(w_name[i])

    w_variable = np.array(w_variable)
    return w_variable


def openPickle(DAY, MONTH, YEAR, HOUR,):
    '''openPickle opens the scraped data from the pickle and put the data
    into usable lists. Takes input strings DAY, MONTH, YEAR, HOUR to
    identify filename.
    '''
    all_data = pickle.load(open("Pickle_Data_Files/file" + YEAR + "_" +
                                MONTH + "_" + DAY + "_" + HOUR + ".p",
                                "rb"))

    w_temp = copy.deepcopy(all_data['temperature'])
    w_height = copy.deepcopy(all_data['height'])
    w_relh = copy.deepcopy(all_data['humidity'])
    w_pres = copy.deepcopy(all_data['pressure'])
    w_sknt = copy.deepcopy(all_data['wind_speed'])
    w_drct = copy.deepcopy(all_data['wind_direction'])
    w_lat = copy.deepcopy(all_data['latitude'])
    w_lon = copy.deepcopy(all_data['longitude'])

    return w_temp, w_height, w_relh, w_pres, w_sknt, w_drct, w_lat, w_lon


def output_for_sBoom(li, keyName, ALT, lat, lon, height, data):
    '''output_for_sBoom takes a weather variable list, list keyName, and
    a max altitude (ALT) as user defined inputs. It also requires the
    existance of a dictionary data, and the lat, lon, and height lists
    from the openPickle function. Using these, it makes a dictionary
    with first key being a lat,lon point and second key being the
    name of the weather variable.
    '''
    temp_height = []
    temp_li = []
    temp_combo_li = []
    d = copy.deepcopy(data)
    k = 0
    i = 0
    ground_level = 0
    ground_altitudes = []
    # ground_level = 0
    # ground_altitudes = []
    while i < len(lat):
        if i > 0:
            # appending to mini-list
            if lat[i] == 0:
                temp_height.append(height[i] - ground_level)
                temp_li.append(li[i])
                k += 1
                i += 1
            else:
                # combining height and weather mini lists for storage
                temp_combo_li = combineLatLon(temp_height, temp_li)

                # making sure first two heights aren't the same
                if temp_combo_li[0][0] == temp_combo_li[1][0]:
                    temp_combo_li.pop(0)

                # TEMPORARY TEST-forcing list to be a certain length
                # while len(temp_combo_li) > 20:
                    # temp_combo_li.pop()

                # getting to next latlon value in big list if not already there
                # while lat[i] == 0:
                    # i += 1
                    # k += 1

                # key is location of previous latlon in big list
                key = '%i, %i' % (lat[i-k], lon[i-k])

                # appending mini-list to dictionary at latlon key
                if d:
                    data[key][keyName] = temp_combo_li
                else:
                    data[key] = {keyName: temp_combo_li}

                # clearing mini-list and restarting
                temp_height = []
                temp_li = []
                temp_combo_li = []
                k = 0
                temp_height.append(height[i])
                ground_level = temp_height[0]
                ground_altitudes.append(ALT - ground_level)
                temp_height[0] = temp_height[0] - ground_level
                temp_li.append(li[i])
                k += 1
                i += 1

        # getting first element in big list
        else:
            temp_height.append(height[i])
            ground_level = temp_height[0]
            ground_altitudes = [ALT - ground_level]
            temp_height[0] = temp_height[0] - ground_level
            temp_li.append(li[i])
            k += 1
            i += 1

    # getting data from final mini-list
    temp_combo_li = combineLatLon(temp_height, temp_li)
    # making sure first two heights aren't the same
    if temp_combo_li[0][0] == temp_combo_li[1][0]:
        temp_combo_li.pop(0)

    # while len(temp_combo_li) > 20:
        # temp_combo_li.pop()

    # dictionary key
    key = '%i, %i' % (lat[i-k], lon[i-k])

    # making dictionary
    if d:
        data[key][keyName] = temp_combo_li
    else:
        data[key] = {keyName: temp_combo_li}

    return data, ground_altitudes


def output_for_sBoom2(li, keyName, ALT, lat, lon, height, data):
    '''output_for_sBoom2 performs the same tasks as output_for_sBoom
    except 2 does not set the ground level height to be 0
    '''
    temp_height = []
    temp_li = []
    temp_combo_li = []
    d = copy.deepcopy(data)
    k = 0
    i = 0
    ground_altitudes = []
    while i < len(lat):
        if i > 0:
            # appending to mini-list
            if lat[i] == 0:
                temp_height.append(height[i])  # - ground_level)
                temp_li.append(li[i])
                k += 1
                i += 1
            else:
                # combining height and weather mini lists for storage
                temp_combo_li = combineLatLon(temp_height, temp_li)

                # making sure first two heights aren't the same
                if temp_combo_li[0][0] == temp_combo_li[1][0]:
                    temp_combo_li.pop(0)

                # key is location of previous latlon in big list
                key = '%i, %i' % (lat[i-k], lon[i-k])

                # appending mini-list to dictionary at latlon key
                if d:
                    data[key][keyName] = temp_combo_li
                else:
                    data[key] = {keyName: temp_combo_li}

                # clearing mini-list and restarting
                temp_height = []
                temp_li = []
                temp_combo_li = []
                k = 0
                temp_height.append(height[i])
                # ground_level = temp_height[0]
                ground_altitudes.append(ALT)  # - ground_level)
                # temp_height[0] = temp_height[0] - ground_level
                temp_li.append(li[i])
                k += 1
                i += 1

        # getting first element in big list
        else:
            temp_height.append(height[i])
            # ground_level = temp_height[0]
            ground_altitudes = [ALT]  # - ground_level]
            # temp_height[0] = temp_height[0] - ground_level
            temp_li.append(li[i])
            k += 1
            i += 1

    # getting data from final mini-list
    temp_combo_li = combineLatLon(temp_height, temp_li)
    # making sure first two heights aren't the same
    if temp_combo_li[0][0] == temp_combo_li[1][0]:
        temp_combo_li.pop(0)

    # dictionary key
    key = '%i, %i' % (lat[i-k], lon[i-k])

    # making dictionary
    if d:
        data[key][keyName] = temp_combo_li
    else:
        data[key] = {keyName: temp_combo_li}

    return data, ground_altitudes


def output_for_sBoom_mat():
    # FIXME - Incomplete, see openMat.py for latest changes
    '''Takes a weather data output from matlab and converts it into the form
    the form needed by boomRunner.py
    '''
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

            key = '%i, %i' % (lat[i-13], lon[j-216])
            keyNames = ['temperature', 'wind_x', 'wind_y', 'humidity']
            all_data[key] = {'temperature': [], 'wind_x': [], 'wind_y': [],
                             'humidty': []}
            for keyName in keyNames:
                all_data[key][keyName] = point_data[keyName]

            # FIXME - heights minus ground height (make ground 0)?
            h = np.array(point_data['height'])
            height = h - point_data['height'][0]
            ground_altitudes.append(height)

    return all_data, ground_altitudes


def process_data(day, month, year, hour, altitude,
                 outputs_of_interest=['temperature', 'height',
                                      'humidity', 'wind_speed',
                                      'wind_direction', 'pressure',
                                      'latitude', 'longitude']):
    ''' process_data makes a dictionary output that contains the lists
    specified by the strings given in outputs_of_interest
    '''

    all_data = pickle.load(open("Pickle_Data_Files/file" + year +
                                "_" + month + "_" + day + "_" + hour +
                                ".p", 'rb'))

    # Reading data for selected properties
    if outputs_of_interest == 'all':
        output = all_data
    else:
        output = {}

        for key in outputs_of_interest:
            output[key] = copy.deepcopy(all_data[key])

    # Make everything floats
    for key in outputs_of_interest:
        output[key] = makeFloats(output[key])

    # Convert wind data
    wind_x, wind_y = windToXY(output['wind_speed'],
                              output['wind_direction'])
    output['wind_x'] = wind_x
    output['wind_y'] = wind_y
    output.pop('wind_speed', None)
    output.pop('wind_direction', None)

    # Prepare for sBOOM
    data = {}
    for key in output.keys():
        lat = output['latitude']
        lon = output['longitude']
        height = output['height']
        if key not in ['latitude', 'longitude', 'height']:
            data, ground_altitudes = output_for_sBoom(output[key],
                                                      key, altitude, lat,
                                                      lon, height, data)
    return data, ground_altitudes


def process_data_nonzero(day, month, year, hour, altitude,
                         outputs_of_interest=['temperature', 'height',
                                              'humidity', 'wind_speed',
                                              'wind_direction', 'pressure',
                                              'latitude', 'longitude']):
    ''' process_data makes a dictionary output that contains the lists
    specified by the strings given in outputs_of_interest
    '''

    all_data = pickle.load(open("Pickle_Data_Files/file" + year +
                                "_" + month + "_" + day + "_" + hour +
                                ".p", 'rb'))

    # Reading data for selected properties
    if outputs_of_interest == 'all':
        output = all_data
    else:
        output = {}

        for key in outputs_of_interest:
            output[key] = copy.deepcopy(all_data[key])

    # Make everything floats
    for key in outputs_of_interest:
        output[key] = makeFloats(output[key])

    # Convert wind data
    wind_x, wind_y = windToXY(output['wind_speed'],
                              output['wind_direction'])
    output['wind_x'] = wind_x
    output['wind_y'] = wind_y
    output.pop('wind_speed', None)
    output.pop('wind_direction', None)

    # Prepare for sBOOM
    data = {}
    for key in output.keys():
        lat = output['latitude']
        lon = output['longitude']
        height = output['height']
        if key not in ['latitude', 'longitude', 'height']:
            data, ground_altitudes = output_for_sBoom2(output[key],
                                                       key, altitude, lat,
                                                       lon, height, data)
    return data, ground_altitudes


def windToXY(sknt, drct):
    ''' windToXY takes wind speed in knots and wind direction in degrees
    clockwise from North lists and converts them to wind velocities in
    m/s along the x (East) and y (North) axes
    '''

    # conversion to m/s
    wind_speed = np.array([x*0.51444 for x in sknt])
    # converting degrees to radians
    wind_direction = np.array([math.radians(x) for x in drct])

    # directions are from North, clockwise so x is sin(drct)
    wind_x = wind_speed*np.sin(wind_direction)
    wind_y = wind_speed*np.cos(wind_direction)

    # making sure there is no -0.0 value in wind lists
    # for i in range(len(wind_x)):
    # if wind_x[i] == 0:
    # wind_x[i] = abs(wind_x[i])
    # if wind_y[i] == 0:
    # wind_y[i] = abs(wind_y[i])

    # making sure there is no -0.0 value in wind lists
    # for i in range(len(wind_x)):
    # if wind_x[i] == 0:
    # wind_x[i] = abs(wind_x[i])
    # if wind_y[i] == 0:
    # wind_y[i] = abs(wind_y[i])

    return wind_x, wind_y


# FIXME - make me into a function pls
def threeDInterpolater(x1, y1, lon, lat, height, w_latlon, w_lat, w_lon,
                       w_height, w_relh):
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
    loc1 = w_latlon.index([y1, x1])  # same as [y1, x1]
    loc2 = w_latlon.index([y2, x1])
    loc3 = w_latlon.index([y1, x2])
    loc4 = w_latlon.index([y2, x2])

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
    relh = []
    f2d = interpolate.interp2d(w_lon_loc, w_lat_loc, relh_loc)
    final_relh = f2d(lon, lat)
    relh.append(final_relh[0])

    return relh
