# weather_model
Library for obtaining data online.

The twister_data_scrapper.py file can be used (and has been used) to scrape weather data from the GFS model from TwisterData.com.
The data obtained is Pressure, Height, Temperature, Relative Humidity, Wind Speed, and Wind Direction at 4232 locations across the
continental U.S. between -144 and -53 degrees West and 13 and 58 degrees North.

This data is then used to make a variety of plots and displays, all of which can be run after downloading the repective file.

However, some displays require the use of Basemap with is a python mpl_toolkits library for displaying maps. Basemap itself requires
PyProj. Unfortunately, Basemap is larger than 100 MB so I can't include it in this repository. By going to https://www.lfd.uci.edu/~gohlke/pythonlibs/ and following the instructions there for installing PyProj and Basemap you will be able to
run all scripts in this repository.
