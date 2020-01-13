#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Required packages
import sys, os
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
from plotly import __version__
from plotly.offline import download_plotlyjs, plot

import plotly.express as px


txtfile = open(r'tanagra.txt')
meteo_data = []

for line in txtfile:
    #print (line)
    fields = line.split()
    meteo_data.append(fields)
  

date = []; windspeed_av= []; windspeed_h= []; wind_direction = []

for list in meteo_data:
    if len(list)==13:
        date.append(int(list[0]))
        windspeed_av.append(float(list[9]))
        windspeed_h.append(float(list[10]))
        wind_direction.append(list[12])
        
        
for index, item in enumerate(wind_direction):
    if item == 'N':
        wind_direction[index] = item.replace('N' , '360')
    elif item =='NNE':
        wind_direction[index] = item.replace('NNE' , '22.5')
    elif item == 'NE':
        wind_direction[index] = item.replace('NE' , '45')
    elif item == 'ENE':
        wind_direction[index] = item.replace('ENE', '67.5')
    elif item == 'E':
        wind_direction[index] = item.replace('E', '90')
    elif item == 'ESE':
        wind_direction[index] = item.replace('ESE', '112.5')
    elif item == 'SE':
        wind_direction[index] = item.replace('SE', '135')
    elif item == 'SSE':
        wind_direction[index] = item.replace('SSE', '157.5')
    elif item == 'S':
        wind_direction[index] = item.replace('S', '180')
    elif item == 'SSW':
        wind_direction[index] = item.replace('SSW', '202.5')
    elif item == 'SW':
        wind_direction[index] = item.replace('SW', '225')
    elif item == 'WSW':
        wind_direction[index] = item.replace('WSW', '247.5')
    elif item == 'W':
        wind_direction[index] = item.replace('W', '270')
    elif item == 'WNW':
        wind_direction[index] = item.replace('WNW', '292.5')
    elif item == 'NW':
        wind_direction[index] = item.replace('NW', '315')
    elif item == 'NNW':
        wind_direction[index] = item.replace('NNW', '337.5')
    else:
        wind_direction[index] = item.replace('---', 'nan')
        
# Conversion of wind direction to degrees   
wind_directionF = []
for w in wind_direction:
    wind_directionF.append(float(w))  

wD_array = np.vstack(np.array(wind_directionF))
wS_high_array = np.vstack(np.array(windspeed_h))
dataArray = np.column_stack((wD_array, wS_high_array))

# Conversion to data frame
dataset = pd.DataFrame({'wind_dir': dataArray[:,0], 'wind_speed':dataArray[:,1]})
print (dataset)

# Keep only the rows with the wind speed > 40 and 60 
dataset_over40 = dataset[dataset['wind_speed'] > 40] 
dataset_over60 = dataset[dataset['wind_speed'] > 60] 

# Calculation of the categories of wind speed based on normal distribution
mean_ws = np.mean(dataset['wind_speed'])
std_ws = np.std(dataset['wind_speed'])

print (mean_ws, std_ws)

categories = {
    '-inf - 0.32': [-np.inf, mean_ws - 3*std_ws],
    '0.32 - 11.08': [mean_ws - 3*std_ws, mean_ws - 2*std_ws],
    '11.08 - 21.84': [mean_ws - 2*std_ws, mean_ws - 1*std_ws],
    '21.84 - 32.60': [mean_ws - 1*std_ws, mean_ws],
    '32.60 - 43.36': [mean_ws, mean_ws + 1*std_ws],
    '43.36 - 54.12': [mean_ws + 1*std_ws, mean_ws + 2*std_ws],
    '54.12 - 64.89': [mean_ws + 2*std_ws, mean_ws + 3*std_ws],
    '64.88 - inf': [mean_ws + 3*std_ws, np.inf]
}

#print (categories)

# Include the category in the data frame
dataset ["category"] = ""
# 
for keys, values in categories.iteritems():  
      
    dataset.loc[(dataset['wind_speed'] > values[0]) & (dataset['wind_speed'] <= values[1]), 'category'] = keys

freq_dataset = dataset.groupby(['wind_dir', 'category']).size().reset_index(name="frequency")

final_freq_dataset = freq_dataset.sort_values(by ='category')
 
 
print (final_freq_dataset)

# Wind rose plot
fig = px.bar_polar(final_freq_dataset, r="frequency", theta="wind_dir",
                   color="category", template='plotly_dark', title="Wind Speed Distribution based on meteorological data (2007-2019)",
                   color_discrete_sequence= px.colors.sequential.Rainbow_r)

plot(fig , show_link=False)
