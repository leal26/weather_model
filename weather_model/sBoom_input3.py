#!python3

'''
Creates a list of lists in the form [[altitude, weather_value], [...]]
 where altitude is the height above the ground and weather_value is the
 value of the temperature, humidity, or wind speed at that height.
 Python3 Version
'''

import copy
import pickle
import numpy as np
from scipy import interpolate

from functions3 import *
from rapidboom.pyldb import PyLdB
from rapidboom.sboomwrapper import SboomWrapper

# Define parameters           
ALT_ft = 45000.
ALT = ALT_ft * 0.3048
DAY = '17'
MONTH = '06'
YEAR = '2018'
HOUR = '12'

CASE_DIR = "." # folder where all case files for the tools will be stored
REF_LENGTH = 32.92
MACH = 1.6
R_over_L = 1

# Process data
data = process_data(DAY, MONTH, YEAR, HOUR, ALT,
                 outputs_of_interest=['temperature','height','humidity',
                                    'wind_speed', 'latitude', 'longitude',
                                    'wind_direction', ])
# Define altitude and longitude
key = list(data.keys())[0]
    
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
print(ground_sig)

g = open("pyldb_input_ex.p","wb")
pickle.dump(ground_sig,g)
g.close()

# grab the loudness level
# noise_level = sboom_results["signal_0"]["C_weighted"]
noise_level = PyLdB(ground_sig[:, 0], ground_sig[:, 1])