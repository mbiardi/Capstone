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
from glob import glob
import os
import re
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

full_tas_files="/home/maddiebiardi/Desktop/VolMIPPrecipData/TASData/volc-pinatubo-full/"
model = "MIROC-ES2L" 
experiment = "volc-pinatubo-full"
ensemble=[f"r{i}i{j}p{k}f{l}" for i in range (1,26) for j in range(1,26) for k in range(1,26) for l in range(1,26)]
years=["18510101-18511231","18520101-18521231","18530101-18531231"]
fname_template="tas_day_{model}_{experiment}_{ensemble}_gn_{years}.nc"
var="tas"
r_values = range(1, 26)
if hasattr(xr, "coders") and hasattr(xr.coders, "CFDatetimeCoder"):
    time_kw = {"decode_times": xr.coders.CFDatetimeCoder(use_cftime=True)} 
else: time_kw = {"use_cftime": True}
pattern = os.path.join(full_tas_files, f"{var}_day_{model}_{experiment}_r*i*p*f*_*_{years[0]}.nc")
member_re = re.compile(r"_(r(\d+)i(\d+)p(\d+)f(\d+))_([^_]+)_\d{8}-\d{8}\.nc$") 
found = [] 
for path in glob(pattern): 
    m = member_re.search(os.path.basename(path)) 
    if m and int(m.group(2)) in r_values:
        rnum, inum, pnum, fnum = (int(m.group(k)) for k in (2, 3, 4, 5)) 
        found.append(((rnum, inum, pnum, fnum), m.group(1), m.group(6))) 
        found.sort()
        print(f"Found {len(found)} member(s):", [mem for _, mem, _ in found]) 
        if not found:
            raise FileNotFoundError(f"No files match: {pattern}")

for _, member, grid in found:
    files = [os.path.join(full_tas_files, f"{var}_day_{model}_{experiment}_{member}_{grid}_{y}.nc") for y in years] 
    missing = [f for f in files if not os.path.isfile(f)] 
    if missing: 
        print(f"Skipping {member}, missing: {missing}") 
        continue 
    ds = xr.open_mfdataset(files, combine="nested", concat_dim="time", data_vars="minimal", coords="minimal", compat="override", **time_kw) 
    ds = ds.sortby("time") 
    tas = ds[var] 
    print(f"\n{member}: shape (time, lat, lon) = {tas.shape}") 
    print(" Time range:", tas.time.values[0], "to", tas.time.values[-1]) 
    output_file = os.path.join( full_tas_files, f"{var}_day_{model}_{experiment}_{member}_{grid}_1851-1853.nc") 
    out_ds = tas.to_dataset(name=var) 
    out_ds.attrs = ds.attrs
    out_ds.attrs["history"] = ( f"Combined {years[0]} to {years[-1]} with xarray. " + ds.attrs.get("history", "")) 
    out_ds.to_netcdf(output_file) 
    print(" Wrote:", output_file) 
    ds.close()
#Now have all data in own files for three years. Need to figure out how to convert to C for each file, and then average across all files.
print(tas) 
print("Shape (time, lat, lon):", tas.shape) 
print("Time range:", tas.time.values[0], "to", tas.time.values[-1])

for _, member, grid in found:
    datasetT=xr.open_dataset(os.path.join(full_tas_files, f"{var}_day_{model}_{experiment}_{member}_{grid}_1851-1853.nc"), engine="netcdf4")
    tasT=datasetT.tas
    tasConvert=tasT
    for i in range(1095):
        tasConvert[i]=tasT[i]-273.15
    convTavg=tasConvert.mean(axis=0)
    for j in range(1095):
        tasConvert[j]=tasT[j]-convTavg
    convTanomalies=tasConvert.mean(axis=0)#This should be anomalies
    latT=datasetT.lat
    lonT=datasetT.lon

    lonTgrid, latTgrid=np.meshgrid(lonT,latT)

    lonW=-140
    lonE=-50
    latS=15
    latN=65
    # cLat=(latN+latS)/2
    # cLon=(lonW+lonE)/2
    res='110m'
    projPC=ccrs.PlateCarree()
    fig=plt.figure(figsize=(11,8.5))
    ax=plt.subplot(1,1,1,projection=projPC)
    gl= ax.gridlines(draw_labels=True,linewidth=2,color='gray',alpha=0.5,linestyle='--')
    ax.set_extent([lonW,lonE,latS,latN],crs=projPC)
    ax.coastlines(resolution=res,linewidth=0.5,color='black')
    ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='black')
    ax.add_feature(cftr.STATES,linewidth=0.5,edgecolor='red')
    ax.set_title(f"Near-Surface Temperature Anomalies, {member}")

    dataplot = ax.contourf(lonTgrid, latTgrid, convTanomalies, transform=ccrs.PlateCarree())
    plt.colorbar(dataplot, orientation='horizontal');
    plt.show()
    #Now able to loop through all members to plot, now need to figure out how to concatenate all members to get mean anomaly for full forcing.


print(convTanomalies)


# latT=datasetT.lat
# lonT=datasetT.lon

# lonTgrid, latTgrid=np.meshgrid(lonT,latT)

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
# ax.coastlines(resolution=res,linewidth=0.5,color='black')
# ax.add_feature(cftr.BORDERS,linewidth=0.5,edgecolor='black')
# ax.add_feature(cftr.STATES,linewidth=0.5,edgecolor='red')
# ax.set_title("Near-Surface Temperature Anomalies, r25i1p1f2")

# dataplot = ax.contourf(lonTgrid, latTgrid, convTanomalies, transform=ccrs.PlateCarree())
# plt.colorbar(dataplot, orientation='horizontal');
# plt.show()