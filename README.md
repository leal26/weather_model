# weather_model
Library for obtaining data online.

The twister_data_scrapper.py file can be used (and has been used) to scrape weather data from the GFS model from TwisterData.com. In the current and future versions, a matlab file (data_scrapper.m) will be used to scrape the same weather data directly from the https://nomads.ncdc.noaa.gov/data/gfsanl/ website. The data obtained is Pressure, Height, Temperature, Relative Humidity, Wind Speed, and Wind Direction at 4232 locations across the continental U.S. between -144 and -53 degrees West and 13 and 58 degrees North.

This data is then used to make a variety of plots and displays, all of which can be run after downloading the respective files.

However, some displays require the use of Basemap with is a python mpl_toolkits library for displaying maps. Basemap itself requires PyProj. Unfortunately, Basemap is larger than 100 MB so I can't include it in this repository. By going to https://www.lfd.uci.edu/~gohlke/pythonlibs/ , downloading PyProj (must be done first) and Basemap to your Path, and installing both of them using "pip install filename.whl" you will be able to run any script in this repository.
