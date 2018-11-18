%% Dataset Inputs

clc; clear; close all; echo off;
%Date and Time of GFS Analysis Dataset
yr='2018';              %year
mo='09';                %month
day='25';               %Day
hr='1800';              %Valid values: '0000', '0600', '1200', '1800'

%Check if grib data object (nco) already exists
%If not, download the dataset to "testgrib.grb2"
if exist('nco','var') == 0
url=['https://nomads.ncdc.noaa.gov/data/gfsanl/',yr,mo,'/',yr,mo,day,...
    '/gfsanl_4_',yr,mo,day,'_',hr,'_000.grb2']; 
outfilename = websave('testgrib.grb',url);
end

%% Extract key parameters from grib datafile

nco = ncgeodataset(outfilename);          %nco: geodataset object

temp = nco.geovariable('Temperature_isobaric'); % temperature (K)
hght = nco.geovariable('Geopotential_height_isobaric'); % height above sea level (m)
relh = nco.geovariable('Relative_humidity_isobaric'); % relative humidity
vel_v = nco.geovariable('v-component_of_wind_isobaric'); % wind in y (m/s)
vel_u = nco.geovariable('u-component_of_wind_isobaric'); % wind in x (m/s)
% p_height = nco.geovariable('Pressure_height_above_ground');

lat = nco.geovariable('lat'); % latitude (90,-90,0.5)
lat = lat(:);
disp(lat)
lon = nco.geovariable('lon'); % longitude (0,360,0.5)
lon = lon(:);
[Lat,Lon] = meshgrid(lat,lon);

%% Format data into usable form and export to excel and pickle if possible

% creating empty python lists for weather variables
% py_hght = py.list();
% py_temp = py.list();
% py_wind_x = py.list();
% py_wind_y = py.list();
% py_relh = py.list();
N = length(temp(1,:,1,1)); % length of each array (number of points per variable)
disp(N)

m_hght = zeros(1,N);
m_temp = zeros(1,N);
m_wind_x = zeros(1,N);
m_wind_y = zeros(1,N);
m_relh = zeros(1,N);

data = py.dict();
s = struct();

% Data can be scraped for lat=90:-90) and for lon=(0,360) by 0.5 degrees

for i = (721-288):2:(721-106) %-53 % lon
    for j = (181-26):-2:(181-116) %58 % lat
        fprintf('%i,%i\n',j,i);
        for k = 1:N
            % creating lists of each variable for all heights
%             py_hght.append(hght(1,k,j,i))
%             py_temp.append(temp(1,k,j,i))
%             py_wind_x.append(vel_u(1,k,j,i))
%             py_wind_y.append(vel_v(1,k,j,i))
%             py_relh.append(relh(1,k,j,i))
            
            m_hght(k) = hght(1,k,j,i);
            m_temp(k) = temp(1,k,j,i);
            m_wind_x(k) = vel_u(1,k,j,i);
            m_wind_y(k) = vel_v(1,k,j,i);
            m_relh(k) = relh(1,k,j,i);
            
        end
        s(j,i).height = m_hght;
        s(j,i).temperature = m_temp;
        s(j,i).wind_x = m_wind_x;
        s(j,i).wind_y = m_wind_y;
        s(j,i).humidity = m_relh;
        s(j,i).temperature = m_temp;
        
        % collecting lists into weather data dictionary for each location
%         single_point = py.dict(pyargs('height', py_hght, 'temperature',...
%                py_temp, 'wind_x', py_wind_x, 'wind_y', py_wind_y,...
%                'humidity', py_relh));
%            
%         % adding each location dictionary to complete dictionary
%         key = sprintf('%i,%i',j,i);
%         data{key} = single_point;
%         
%         % clearing lists for next iteration
%         py_hght = py.list();
%         py_temp = py.list();
%         py_wind_x = py.list();
%         py_wind_y = py.list();
%         py_relh = py.list();
        
        m_hght = zeros(1,N);
        m_temp = zeros(1,N);
        m_wind_x = zeros(1,N);
        m_wind_y = zeros(1,N);
        m_relh = zeros(1,N);
    end
end

save('data_3.mat','s')
