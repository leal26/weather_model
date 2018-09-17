import numpy as np
import matplotlib.pyplot as plt
import pickle

from rapidboom.sboomwrapper import SboomWrapper
from rapidboom.pyldb import PyLdB

# folder where all case files for the tools will be stored
CASE_DIR = "."

REF_LENGTH = 32.92
MACH = 1.6
R_over_L = 1

# get pressure signature from pickle
nearfield_sig = pickle.load( open( "nearfiled_signature.p", "rb" ) )

# initialize sBOOM
sboom = SboomWrapper(CASE_DIR, exe="sboom_windows.dat.allow")

# temperature input (altitude ft, temperature F)
temperature = [[0.0,     60],
               [5000.0,  74],
               [20000.0, 24],
               [30000.0, 0],
               [40000.0, -10],
               [50000.0, -20],
               [60000.0, -30]]

# wind input (altitude ft, wind X, wind Y)
wind = [[0.0,       0,  0],
        [5000.0,    0,  0],
        [20000.0,   0,  0],
        [30000.0,   0,  0],
        [40000.0,   0,  0],
        [50000.0,   0,  0],
        [60000.0,   0,  0]]

# wind input (altitude ft, humidity %)
humidity = [[0.0,     60],
            [5000.0,  74],
            [20000.0, 24],
            [30000.0, 0],
            [40000.0, 0],
            [50000.0, 0],
            [60000.0, 0]]

# update sBOOM settings and run
sboom.set(mach_number=MACH,
          altitude=50000.0,
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