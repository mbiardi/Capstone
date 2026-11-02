import sys
import matplotlib
# matplotlib.use('TkAgg')
# import pandas as pd
import numpy as np
import xarray as xr
# from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import cartopy
from cartopy import crs as ccrs, feature as cftr
from matplotlib import cm
# import scipy as spy
from math import *
datasetR1=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/PrecipData/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r1i1p1f1_gn_19910101-19961231.nc',engine='netcdf4')
datasetR2=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/PrecipData/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r2i1p1f1_gn_19910101-19961231.nc')
datasetR3=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/PrecipData/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r3i1p1f1_gn_19910101-19961231.nc')
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

#Vars for dataset 3
latR3=datasetR3.lat_bnds
lonR3=datasetR3.lon_bnds
tR3=datasetR3.time_bnds
precipR3=datasetR3.pr
day=86400
density=998.2
conversionR1=precipR1 #Initial definition of array with matching data to precip array, for later conversion of precip data.
conversionR2=precipR2
conversionR3=precipR3

conversionR1t0=((precipR1[0]*day)/density)*1000 #conversion to mm/day using density of fresh water at 20C



#Doing conversion across all times
for i in range(2191):
    conversionR1[i]=((precipR1[i]*day)/density)*1000
    conversionR2[i]=((precipR2[i]*day)/density)*1000
    conversionR3[i]=((precipR3[i]*day)/density)*1000

timeavgR1=conversionR1
timeavgR2=conversionR2
timeavgR3=conversionR3

convR1avg=conversionR1.mean(axis=0)
# print(convR1avg.sizes)



#Now plotting precip for ONE timestamp across lat and lon
#want latitude as x, longitude as y.
#Need to create a plotting matrix where every x value has a corresponding y value
lonR1grid, latR1grid = np.meshgrid(lonR1,latR1)



# lonW=-140
# lonE=-50
# latS=15
# latN=65
# cLat=(latN+latS)/2
# cLon=(lonW+lonE)/2
# res='110m'
# projPC=ccrs.PlateCarree()
# fig=plt.figure(figsize=(11,8.5))
# ax=plt.subplot(1,1,1,projection=projPC)
# gl= ax.gridlines(draw_labels=True,linewidth=2,color='gray',alpha=0.5,linestyle='--')
# ax.set_extent([lonW,lonE,latS,latN],crs=projPC)
# ax.coastlines(resolution=res,linewidth=0.5,color='white')
# ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='white')
# ax.add_feature(cftr.STATES,linewidth=0.5,edgecolor='red')

# dataplot = ax.contourf(lonR1grid, latR1grid, convR1avg, transform=ccrs.PlateCarree())
# plt.colorbar(dataplot, orientation='horizontal');
# plt.show()


#TEMPERATURE DATA
convTavg=np.zeros(100) #Array for storing average converted temp for each file in volc-pinatubo-full
for i in range(99): #Volc-pinatubo-full, 100 files, need to open each one and convert temp, create array that stores converted temp for each file, then average
    datasetT=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/TASData/volc-pinatubo-full/*',engine='netcdf4')
    tasT=datasetT.tas
    tasConvert=tasT
    for j in range(364):
        tasConvert[j]=tasT[j]-273.15
    convTavg[i]=tasConvert.mean(axis=0)
    
datasetT1=xr.open_dataset('/home/maddiebiardi/Desktop/VolMIPPrecipData/TASData/volc-pinatubo-full/tas_day_MIROC-ES2L_volc-pinatubo-full_r1i1p1f2_gn_18530101-18531231.nc',engine='netcdf4')
# # print(datasetT1.tas)
latT1=datasetT1.lat
lonT1=datasetT1.lon
# tasT1=datasetT1.tas
# tasConvertT1=tasT1


# for i in range(364):
#     tasConvertT1[i]=tasT1[i]-273.15
fullTconv=convTavg.mean(axis=0)#This should stay out of the loop
print(fullTconv.sizes) 

lonT1grid, latT1grid=np.meshgrid(lonT1,latT1)

lonW=-140
lonE=-50
latS=15
latN=65
cLat=(latN+latS)/2
cLon=(lonW+lonE)/2
res='110m'
projPC=ccrs.PlateCarree()
fig=plt.figure(figsize=(11,8.5))
ax=plt.subplot(1,1,1,projection=projPC)
gl= ax.gridlines(draw_labels=True,linewidth=2,color='gray',alpha=0.5,linestyle='--')
# ax.set_extent([lonW,lonE,latS,latN],crs=projPC)
ax.coastlines(resolution=res,linewidth=0.5,color='white')
ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='white')
ax.add_feature(cftr.STATES,linewidth=0.5,edgecolor='red')

dataplot = ax.contourf(lonT1grid, latT1grid, fullTconv, transform=ccrs.PlateCarree())
plt.colorbar(dataplot, orientation='horizontal');
plt.show()