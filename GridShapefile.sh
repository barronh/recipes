#!/bin/bash

# Goal: Create a CMAQ file with data from a shapefile attribute
# Example uses data:
#  - shapefile ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/CONUS_CLIMATE_DIVISIONS.shp.zip
#  - EPA emissions file on 12US2 domain 

# Step 1: USE GRIDDESC to reproject shapefile
# Get metadata from emissions file global properties: 
# use ncdump to view global properties copy :
#  - P_ALP into lat_1,
#  - P_BET into lat_2,
#  - P_GAM into lon_0,
#  - YCENT into lat_0,
#  - negative XORIG into x_0, and
#  - negative YORIG into y_0
#  - a and b should be consistent with met model
#
# Final string looks like this
PROJ4STR="+proj=lcc +a=6370000 +b=6370000 +lat_0=40 +lon_0=-97 +lat_1=33 +lat_2=45 +x_0=2412000 +y_0=1620000 +no_defs"

# Step 2: Use ogr2ogr to reproject to model projection
ogr2ogr -t_srs "${PROJ4STR}" NEW.shp GIS.OFFICIAL_CLIM_DIVISIONS.shp

# Step 3: Find attributes that you want to write out by name
ogrinfo -geom=NO NEW.shp NEW| less

# Step 4: Rasterize the attribute based on polygon overlap and set extent and cols/rows
# Uses NCOLS, NROWS, XCELL, and YCELL from emission metadata
# -ts NCOLS NROWS
# -te 0 0 NCOLS*XCELL NROWS*YCELL
#
# Complete command below
gdal_rasterize -of netCDF -at -a STATE_FIPS  -ts 396 246 -te 0 0 4752000 2952000 -l NEW NEW.shp gridded.nc

# Step 5: Create an IOAPI file to hold the results
# This is mainly to make it easy to interact with other files
ncks -vTFLAG,NO -dTSTEP,0 -dVAR,0 ../emis_mole_onroad_20140701_12US2_cmaq_cb6_2014fd_nata_cb6_14j.nc4 holder.nc4
ncrename -v NO,FIPS holder.nc4
ncatted -a VAR-LIST,global,o,c,"FIPS            " -a NVARS,global,o,i,1 -a long_name,FIPS,o,c,"FIPS" -a var_desc,FIPS,o,c,"2-digit FIPS code" holder.nc4

# Step 6: Write data into IOAPI file
python -c "
import netCDF4
import numpy as np
# Read from gridded.
f = netCDF4.Dataset('gridded.nc')
# Write to panoply
h = netCDF4.Dataset('holder.nc4', 'a')
h.variables['FIPS'][:] = f.variables['Band1'][:][None, None].filled(np.nan)
h.sync()
"

# Step 7: visualize in your favorite view (e.g., Panoply)
