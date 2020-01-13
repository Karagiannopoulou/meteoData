# -*- coding: utf-8 -*-

# Required packages
import sys, os
import numpy as np
from scipy import stats
import pandas as pd
from plotly import __version__
from plotly.offline import download_plotlyjs, plot

#import plotly.plotly as py
import plotly.graph_objs as go


# os.chdir(r'C:\Users\noa\Desktop\Flamap_FireHModel\meteoData')
# os.getcwd()
txtfile = open(r'tanagra.txt')
meteo_data = []

for line in txtfile:
    #print (line)
    fields = line.split()
    meteo_data.append(fields)
  
#print("{}".format(len(meteo_data)))
#print meteo_data    

#sys.exit()

date = []; windspeed_av= []; windspeed_h= []; wind_direction = []

for list in meteo_data:
    if len(list)==13:
        date.append(int(list[0]))
        windspeed_av.append(float(list[9]))
        windspeed_h.append(float(list[10]))
        wind_direction.append(list[12])
        
#print("{}".format(wind_direction))

#print (wind_direction)

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
    else:
        wind_direction[index] = item.replace('NNW', '337.5')
        
        
        
#print (wind_direction)

wind_directionF = []
for w in wind_direction:
    if w == '---':
        continue
    
    wind_directionF.append(float(w))  

#print len((wind_directionF))


# Compute frequencies
wD_array = np.array(wind_directionF)
#wS_average_array = np.array(windspeed_av)
wS_high_array = np.array(windspeed_h)

freq_wD_array = stats.itemfreq(wD_array)
# print (freq_wD_array[:,1])
# print (freq_wD_array)

freq_wS_high_array = stats.itemfreq(wS_high_array)
# print (freq_wS_high_array[:,1])

# Compute the percentage of the frequencies
# 1. Compute the sum of the frequencies. 
sum_freq_wD_array = sum(freq_wD_array[:,1])
sum_freq_wS_high_array = sum(freq_wS_high_array[:,1])


#print ("{} {}". format(sum_freq_wD_array, sum_freq_wS_high_array))

# 2. Create empty arrays to append the percentage of the frequencies 
per_freq_wD_array = np.array([]) 
per_freq_wS_high_array = np.array([])


for line in freq_wD_array[:,1]:
    #print line
    result = (line / sum_freq_wD_array)*100.0
    per_freq_wD_array = np.append(per_freq_wD_array, [result])
    per_freq_wD_array = np.round(per_freq_wD_array, 2)

#print (per_freq_wD_array)

for line in freq_wS_high_array[:,1]:
    #print line
    result = (line/sum_freq_wS_high_array)*100.0
    per_freq_wS_high_array = np.append(per_freq_wS_high_array, [result])
    per_freq_wS_high_array = np.round(per_freq_wS_high_array, 2)
 
#print (per_freq_wS_high_array)   

# Calculate the percentiles (25, 50, 75, 95) for (a) wind_speed_high and (b) wind_direction
percentiles_wD_array = ([])
percentiles_wS_high_array = ([])

perc25_wD = np.percentile (wD_array, 25)
perc50_wD = np.percentile (wD_array, 50)
perc75_wD = np.percentile (wD_array, 75)
perc95_wD = np.percentile (wD_array, 95)

percentiles_wD_array = np.append([perc25_wD,perc50_wD,perc75_wD, perc95_wD], percentiles_wD_array)

perc25_wS_high_array = np.percentile (wS_high_array, 25)
perc50_wS_high_array = np.percentile (wS_high_array, 50)
perc75_wS_high_array = np.percentile (wS_high_array, 75)
perc95_wS_high_array = np.percentile (wS_high_array, 95)

percentiles_wS_high_array = np.append([perc25_wS_high_array, perc50_wS_high_array, perc75_wS_high_array, perc95_wS_high_array], percentiles_wS_high_array)

# Data plotting
# print (freq_wD_array[:,0])
# print(freq_wD_array[:,1])

# # print (freq_wS_high_array[:,0])
# print(freq_wS_high_array[:,1])


# Plotting data
fig = go.Figure(data=[go.Bar(
            x=freq_wD_array[:,0], 
            y=freq_wD_array[:,1],
            text=freq_wD_array[:,1],  
            textposition='auto',
            marker_color='crimson'
        )])
fig.update_layout(
    title = 'Wind directions frequencies',
    yaxis = dict(
        title = 'Number of occurrence (in days)',
        titlefont_size = 16),)

plot(fig, show_link=False)


fig2 = go.Figure(data=[go.Bar(
            x=freq_wS_high_array[:,0], 
            y=freq_wS_high_array[:,1],
            text=freq_wS_high_array[:,1],  
            textposition='auto',
        )])
fig2.update_layout(
    title = 'Wind speed frequencies',
    yaxis = dict(
        title = 'Number of occurrence (in days)',
        titlefont_size = 16),)

plot(fig2, show_link=False)














