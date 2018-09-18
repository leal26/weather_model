%% Dataset Inputs

clc; clear; close all;
%Date and Time of GFS Analysis Dataset
yr='2018';              %year
mo='05';                %month
day='01';               %Day
hr='0000';              % Time, Valid values: '0000', '0600', '1200', '1800'

%Check if grib data object (nco) already exists
%If not, download the dataset to "testgrib.grb2"
if exist('nco','var') == 0
url=['https://nomads.ncdc.noaa.gov/data/gfsanl/',yr,mo,'/',yr,mo,day,...
    '/gfsanl_4_',yr,mo,day,'_',hr,'_000.grb2']; 
outfilename = websave('testgrib.grb2',url);
end

%% Extract key parameters from grib datafile

nco = ncgeodataset(outfilename);          %nco: geodataset object

temp = nco.geovariable('Temperature_isobaric'); % temperature
hght = nco.geovariable('Geopotential_height_isobaric'); % height above sea level
relh = nco.geovariable('Relative_humidity_isobaric'); % relative humidity
vel_v = nco.geovariable('v-component_of_wind_isobaric'); % wind in y (lat)
vel_u = nco.geovariable('u-component_of_wind_isobaric'); % wind in x (lon)
p_height = nco.geovariable('Pressure_height_above_ground');
% p_h2 = nco.geovariable('isobaric');
%'Pressure_height_above_ground'
param = 'Pressure_surface'; %(1x361x720)
p_surf = nco.geovariable(param); 

lat = nco{'lat'}(:); % latitude (-90,90,0.5)
lon = nco{'lon'}(:); % longitude (0,360,0.5)
[Lat,Lon] = meshgrid(lat,lon);

%% Format data into usable form and export to excel and pickle if possible

% creating empty python lists for weather variables
py_hght = py.list();
py_temp = py.list();
py_wind_x = py.list();
py_wind_y = py.list();
py_relh = py.list();

m_hght = zeros(1,31);
m_temp = zeros(1,31);
m_wind_x = zeros(1,31);
m_wind_y = zeros(1,31);
m_relh = zeros(1,31);

data = py.dict();
s = struct;

% Data can be scraped for lat=(-90:90) and for lon=(0,360) by 0.5 degrees

for i = (360-144):(360-143) %-53 % lon
    for j = 13:14 %58 % lat
        for k = 1:31
            % creating lists of each variable for all heights
            py_hght.append(hght(1,k,j,i))
            py_temp.append(temp(1,k,j,i))
            py_wind_x.append(vel_u(1,k,j,i))
            py_wind_y.append(vel_v(1,k,j,i))
            py_relh.append(relh(1,k,j,i))
            
            m_hght(k) = hght(1,k,j,i);
            m_temp(k) = temp(1,k,j,i);
            m_wind_x(k) = vel_u(1,k,j,i);
            m_wind_y(k) = vel_v(1,k,j,i);
            m_relh(k) = relh(1,k,j,i);
            
        end
        s_inner = struct('height',m_hght,'temperature',m_temp,'wind_x',m_wind_x,...
                   'wind_y',m_wind_y,'humidity',m_relh);
        
        m_key = sprintf('L%i%i',j,i);
        s_outer = struct(m_key,s_inner);
        
        % collecting lists into weather data dictionary for each location
        single_point = py.dict(pyargs('height', py_hght, 'temperature',...
               py_temp, 'wind_x', py_wind_x, 'wind_y', py_wind_y,...
               'humidity', py_relh));
           
        % adding each location dictionary to complete dictionary
        key = sprintf('%i,%i',j,i);
        data{key} = single_point;
        
        % clearing lists for next iteration
        py_hght = py.list();
        py_temp = py.list();
        py_wind_x = py.list();
        py_wind_y = py.list();
        py_relh = py.list();
        
        m_hght = zeros(1,31);
        m_temp = zeros(1,31);
        m_wind_x = zeros(1,31);
        m_wind_y = zeros(1,31);
        m_relh = zeros(1,31);
    end
end
            
