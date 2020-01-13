#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Required packages
import sys, os
import numpy as np
from scipy import stats


# os.chdir(r'C:\Users\noa\Desktop\Flamap_FireHModel\meteoData')
# os.getcwd()
txtfile = open(r'C:\Users\noa\Desktop\Flamap_FireHModel\meteoData\tanagra.txt')
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
    elif item == 'NNW':
        wind_direction[index] = item.replace('NNW', '337.5')
    else:
        wind_direction[index] = item.replace('---', '-9999')
        
        
wind_directionF = []
for w in wind_direction:
    wind_directionF.append(float(w))  

#print (wind_directionF)

#wD_array = np.array(wind_directionF)
#print(wD_array.T)

wD_array = np.vstack(np.array(wind_directionF))
#print(wD_array)

wS_high_array = np.vstack(np.array(windspeed_h))
#print(wS_high_array)


dataArray = np.column_stack((wD_array, wS_high_array))
#print(dataArray) 

#print(dataArray[:,0])


S_index = np.where(dataArray[:,0] == 180.)
WNW_index = np.where(dataArray[:,0] == 292.5)
NNW_index = np.where(dataArray[:,0] == 337.5)
N_index = np.where(dataArray[:,0] == 360)


wS_high_S = dataArray[:,1][S_index]
wS_high_WNW = dataArray[:,1][WNW_index]
wS_high_NNW = dataArray[:,1][NNW_index]
wS_high_N  = dataArray[:,1][N_index]


# Calculate the 95th percentile and the median per each np.wind_direction array

perc95_wS_S = np.percentile (wS_high_S, 95)
perc95_wS_WNW = np.percentile (wS_high_WNW, 95)
perc95_wS_NNW = np.percentile (wS_high_NNW, 95)
perc95_wS_N = np.percentile (wS_high_N, 95)

median_wS_S = np.median (wS_high_S)
median_wS_WNW = np.median(wS_high_WNW)
median_wS_NNW = np.median(wS_high_NNW)
median_wS_N = np.median(wS_high_N)

print ("{} {} {} {}".format(perc95_wS_S, perc95_wS_WNW, perc95_wS_NNW, perc95_wS_N))
print ("{} {} {} {}".format(median_wS_S, median_wS_WNW, median_wS_NNW, median_wS_N))

