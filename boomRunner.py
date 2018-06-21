import copy
import pickle
import numpy as np
from scipy import interpolate

from functions3 import *
from rapidboom.pyldb import PyLdB
from rapidboom.sboomwrapper import SboomWrapper

import functions3



def boomRunner(data,i):
    '''
    Runs sBOOM
     Python3 Version
    '''

    # Define parameters           
    ALT_ft = 45000.
    ALT = ALT_ft * 0.3048

    CASE_DIR = "." # folder where all case files for the tools will be stored
    REF_LENGTH = 32.92
    MACH = 1.6
    R_over_L = 1

    # Define altitude and longitude
    key = list(data.keys())[i]
        
    # do sBoom things here

    # get pressure signature from pickle
    nearfield_sig = pickle.load( open( "nearfiled_signature.p", "rb" ) )

    # initialize sBOOM
    sboom = SboomWrapper(CASE_DIR, exe="sboom_windows.dat.allow")

    # temperature input (altitude ft, temperature F)
    temperature = data[key]['temperature']

    # wind input (altitude ft, wind X, wind Y)
    wind = data[key]['wind_x']
    for i in range(len(wind)):
        wind[i].append(data[key]['wind_y'][i][1])

    # wind input (altitude ft, humidity %)
    humidity = data[key]['humidity']

    # update sBOOM settings and run
    sboom.set(mach_number=MACH,
              altitude=ALT_ft,
              propagation_start=R_over_L*REF_LENGTH*3.28084,
              altitude_stop=0.,
              output_format=0,
              input_xdim=2,
              signature=nearfield_sig,
              input_temp=temperature,
              input_wind=wind,
              input_humidity=humidity)

    sboom_results = sboom.run()
    ground_sig = sboom_results["signal_0"]["ground_sig"]

    # grab the loudness level
    # noise_level = sboom_results["signal_0"]["C_weighted"]
    noise_level = PyLdB(ground_sig[:, 0], ground_sig[:, 1])
    
    return noise_level
    

DAY = '17'
MONTH = '06'
YEAR = '2018'
HOUR = '12'

ALT_ft = 45000.
ALT = ALT_ft * 0.3048
    
# Process data
data = process_data(DAY, MONTH, YEAR, HOUR, ALT,
                 outputs_of_interest=['temperature','height','humidity',
                                    'wind_speed', 'latitude', 'longitude',
                                    'wind_direction', ])
                                                                      
                                    
noise = []
latlon = []

noise_data = {'latlon':[], 'noise':[]}
#print(list(data.keys()))

for i in range(100):
    #latlon.append(list(data.keys())[i])
    noise_data['latlon'].append(list(data.keys())[i])
    #noise.append(boomRunner(data,i))
    noise_data['noise'].append(boomRunner(data,i))
                   
# print(latlon, noise)
# print(len(noise))
# print(len(noise_data['noise']))

g = open("noise" + YEAR + "_" + MONTH + "_" + DAY + "_" + HOUR + ".p","wb")
pickle.dump(noise_data,g)
g.close()
                                    
                                    
