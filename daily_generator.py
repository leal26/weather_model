'''
File to run entire weather_model functional package from scraping data to
generating contour of ground level percieved loudness. Designed to be run once
each day.
'''

import datetime
# from boomRunner import boomRunner
import subprocess
import os.path


DAY = str(datetime.date.today().strftime('%d'))
MONTH = str(datetime.date.today().strftime('%m'))
YEAR = str(datetime.date.today().strftime('%Y'))
HOUR1 = '00'
HOUR2 = '12'

# while "file" + YEAR + MONTH + DAY + HOUR1 + ".p" doesn't exsist:
while not os.path.isfile("Pickle_Data_Files/file" + YEAR + "_" + MONTH + "_" +
                         DAY + "_" + HOUR2 + ".p"):
    # run twister_data_scrapper.py
    print('hi')
    subprocess.call(["python.exe", "twister_data_scrapper.py"])
    print('hi2')
'''
# while "file" + YEAR + MONTH + DAY + HOUR2 + ".p" doesn't exsist:
while not os.path.isfile("Pickle_Data_Files/file" + YEAR + "_" + MONTH + "_" +
                         DAY + "_" + HOUR1 + ".p"):
    # run twister_data_scrapper3.py
    subprocess.call("twister_data_scrapper3.py")
'''
print('it worked :)')
# run boomRunner for each file
# FIXME - boomRunner needs to either be fixed so it runs continuously or a
# babysitter needs to be written to keep sBOOM from crashing
# subprocess.call("boomRunner.py")
