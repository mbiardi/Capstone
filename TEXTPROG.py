import sys
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib as plt
import scipy as spy
from math import *
datasetR1=xr.open_dataset('/Users/maddie/Desktop/Capstone/SAMPLE DATA/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r1i1p1f1_gn_19910101-19961231.nc')
datasetR2=xr.open_dataset('/Users/maddie/Desktop/Capstone/SAMPLE DATA/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r2i1p1f1_gn_19910101-19961231.nc')
datasetR3=xr.open_dataset('/Users/maddie/Desktop/Capstone/SAMPLE DATA/pr_day_MPI-ESM1-2-LR_volc-pinatubo-full_r3i1p1f1_gn_19910101-19961231.nc')
latR1=datasetR1.lat_bnds
lonR1=datasetR1.lon_bnds
tR1=datasetR1.time_bnds
precipR1=datasetR1.pr
day=86400
density=998.2
conversionR1=precipR1 #Initial definition of array with matching data to precip array, for later conversion of precip data.


conversionR1t0=(precipR1[0]*day)/density*1000 #conversion to mm/day using density of fresh water at 20C
for i in range(2191):
    conversionR1[i]=precipR1[i]


#Doing conversion across all times
for i in range(1):
    conversionR1[i]=(precipR1[i]*day)/density*1000
print("Conversion factor for first value in loop",conversionR1[0,:,:])#Have <xarray.DataArray 'pr' (lat: 96, lon: 192)> Size: 74kB
                                                                                                #[18432 values with dtype=float32]
print("")
print("")
print("")
print("")
print("")
print("Converstion factor for first value out of loop",conversionR1t0)#Have <xarray.DataArray 'pr' (lat: 96, lon: 192)> Size: 74kB
                                                                                #array([ values]), shape=(96, 192), dtype=float32)
# Won't show me any values after converting in loop, can't figure out why. Should be getting the same results if I print just the first time index, but nothing shows up.
print(conversionR1t0.sizes) #Doesn't have time dimension, because i'm doing one value.
#Need to figure out how to define conversion arrays that have same lat, lon, and times, so I can insert just the converted precipitation values.
