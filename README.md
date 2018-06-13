# weather_model
Library for obtaining data online.

The twister_data_scrapper.py file can be used (and has been used) to scrape weather data from the GFS model from TwisterData.com.
The data obtained is Pressure, Height, Temperature, Relative Humidity, Wind Speed, and Wind Direction at 4232 locations across the
continental U.S. between -144 and -53 degrees West and 13 and 58 degrees North.

This data is then used to make a variety of plots and displays, all of which can be run after downloading the repective file.

However, some displays require the use of Basemap with is a python mpl_toolkits library for displaying maps. Basemap itself requires
PyProj. Therefore, Basemap and PyProj are provided for download here. Once downloaded to a location on your Path, they can be installed
with pip install.
