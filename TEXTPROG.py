import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
import cartopy
from cartopy import crs as ccrs, feature as cftr
from matplotlib.colors import Normalize
from matplotlib import colorbar, colors
from matplotlib import cm
from math import *


datasetR1=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r1i1p1f1_gn_19910101-19961231.nc')
datasetR2=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r2i1p1f1_gn_19910101-19961231.nc')
datasetR3=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r3i1p1f1_gn_19910101-19961231.nc')
#Vars for dataset 1
latR1=datasetR1.lat_bnds
lonR1=datasetR1.lon_bnds
tR1=datasetR1.time_bnds
precipR1=datasetR1.pr
latR1=latR1.lat
lonR1=lonR1.lon

#Vars for dataset 2
latR2=datasetR2.lat_bnds
lonR2=datasetR2.lon_bnds
tR2=datasetR2.time_bnds
precipR2=datasetR2.pr
latR2=latR2.lat
lonR2=lonR2.lon

#Vars for dataset 3
latR3=datasetR3.lat_bnds
lonR3=datasetR3.lon_bnds
tR3=datasetR3.time_bnds
precipR3=datasetR3.pr
latR3=latR3.lat
lonR3=lonR3.lon

day=86400
density=998.2
conversionR1=precipR1 #Initial definition of array with matching data to precip array, for later conversion of precip data.
conversionR2=precipR2
conversionR3=precipR3

#Doing conversion across all times
for i in range(2191):
    conversionR1[i]=((precipR1[i]*day)/density)*1000
    conversionR2[i]=((precipR2[i]*day)/density)*1000
    conversionR3[i]=((precipR3[i]*day)/density)*1000
#Now that conversion has been done, do we need to start averaging over time?
#Have 2192 time values, so do we want to average between 2 side values & center (i.e i-1, i+1, i?) to get average value of time[i]?
#Also consider that I have 2d array at each time slice, so do I also need to average over area? (Each slice is 96x192, or 18432 values, which is expected)

convR1avg=conversionR1.mean(axis=0)
convR2avg=conversionR2.mean(axis=0)
convR3avg=conversionR3.mean(axis=0)

#What would make more sense? For graphing, compressing all time values into a single 2d array of location would work (i.e array[i,j,k] -> array[j,k])
#To average across all time values, would i need to do two sums instead? one over time, and one for precip?

#Well, what do I already have?
#   -> I have precip values for a 96x192 grid
#   -> I have one of these for every slice of time
#What do I need?
#   -> I need the average precipitation over all time
#What is relevant?
#   -> Time
#   -> Precipitation
#What do I need to leave alone?
#   -> The area grid of 96x192
#What does this tell me?
#   -> I need to add together precipitation over every time slice, and take its average at every location on the 96x192 grid across all time.

#How to take average over so many values? Obviously, divide by 2192, since it's the number of timestamps. But how can I add every single precip value at a location in a for loop?

#I need to do it by location. at each [j,k] stamp, I do array[i,j,k]=array[i,j,k]+array[i+1,j,k], this should get me final amount of precipitation over all time at array[2191,j,k]?
#Then after it has all been added, I do the division?
#Maybe worry about compression of time values later?
#DRAW THIS OUT ON PAPER!!!!

#Now plotting precip for ONE timestamp across lat and lon
#want latitude as x, longitude as y.
#Need to create a plotting matrix where every x value has a corresponding y value
lonR1grid, latR1grid = np.meshgrid(lonR1,latR1)
lonR2grid, latR2grid = np.meshgrid(lonR2,latR2)
lonR3grid, latR3grid = np.meshgrid(lonR3,latR3)


#Cartopy Practice
# fig=plt.figure(figsize=(11,8.5))
# ax=plt.subplot(1,1,1,projection=ccrs.PlateCarree(central_longitude=-75))
# ax.set_title("Geo-referenced subplot, Plate Carree projection")
# ax.coastlines()
# ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='black')
# plt.show()

lonW=-140
lonE=-50
latS=15
latN=65
cLat=(latN+latS)/2
cLon=(lonW+lonE)/2
res='110m'
projPC=ccrs.PlateCarree()
Norm= Normalize(vmin=0,vmax=16)

fig=plt.figure(figsize=(11,8.5)) #Goes to 16
ax=plt.subplot(1,1,1,projection=projPC)
gl= ax.gridlines(draw_labels=True,linewidth=2,color='gray',alpha=0.5,linestyle='--')
ax.set_title("Time-Averaged Precipitation across 5 years, MPI: r1i1p1f1", fontsize=18, fontname='Times New Roman')
ax.set_extent([lonW,lonE,latS,latN],crs=projPC)
ax.coastlines(resolution=res,linewidth=0.5,color='white')
ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='white')
ax.add_feature(cftr.STATES,linewidth=0.5,edgecolor='red')
dataplot = ax.contourf(lonR1grid, latR1grid, convR1avg, transform=ccrs.PlateCarree())
plt.colorbar(dataplot, orientation='vertical',label="mm/day"); #Tried adding vmin=0, vmax=14, no luck
#Also tried to normalize for norm=Norm in colorbar function
# plt.show()

fig=plt.figure(figsize=(11,8.5))
ax=plt.subplot(1,1,1,projection=projPC)
gl= ax.gridlines(draw_labels=True,linewidth=2,color='gray',alpha=0.5,linestyle='--')
ax.set_title("Time-Averaged Precipitation across 5 years, MPI: r2i1p1f1", fontsize=18, fontname='Times New Roman')
ax.set_extent([lonW,lonE,latS,latN],crs=projPC)
ax.coastlines(resolution=res,linewidth=0.5,color='white')
ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='white')
ax.add_feature(cftr.STATES,linewidth=0.5,edgecolor='red')
dataplot = ax.contourf(lonR2grid, latR2grid, convR2avg, transform=ccrs.PlateCarree())
plt.colorbar(dataplot, orientation='vertical',label="mm/day");
# cbar_kwargs={'shrink':0.4, 'ticks':list(range(2)),'extend':'max'}

fig=plt.figure(figsize=(11,8.5)) #Goes to 16
ax=plt.subplot(1,1,1,projection=projPC)
gl= ax.gridlines(draw_labels=True,linewidth=2,color='gray',alpha=0.5,linestyle='--')
ax.set_title("Time-Averaged Precipitation across 5 years, MPI: r3i1p1f1", fontsize=18, fontname='Times New Roman')
ax.set_extent([lonW,lonE,latS,latN],crs=projPC)
ax.coastlines(resolution=res,linewidth=0.5,color='white')
ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='white')
ax.add_feature(cftr.STATES,linewidth=0.5,edgecolor='red')
dataplot = ax.contourf(lonR3grid, latR3grid, convR3avg, transform=ccrs.PlateCarree())
plt.colorbar(dataplot, orientation='vertical',label="mm/day");
plt.show()


