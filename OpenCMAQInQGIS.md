# Overview 
To use CMAQ data with QGIS, you need to create a custom projection and then import a raster file and set its projection. The examples is based on the EPA 12US2[1,2] and 12US1[3] and 36US3[4] projections. One oddity in QGIS is that the raster origin is set to the lop left instead of bottom left. These instructions account for the problem. This works with CMAQ emissions, concentration, and metcro data correctly in QGIS.

# Create a custom projection

This section will use meta-data that is available in the GRIDDESC text file or as IOAPI meta-data on the NetCDF file (ncdump -h). Values for the EPA's 12US2 domain are provided as examples. Example uses QGIS 3.2.


1. Click "Settings" and Select "Custom Projections..."
2. Add a new projection (green plus)
3. Name the projection (e.g. 12US2)
4. Enter a PROJ4 string from the header of the file or from a GRIDDESC
  * LCC template: `+proj=lcc +lon_0=<XCENT> +lat_0=<YCENT> +lat_1=<P_ALP> +lat_2=<P_BET> +x_0=<-XORIG> +y_0=<-YORIG - NROWS * YCELL> +to_meter=<XCELL>m +a=6370000 +a=6370000`
  * 12US1 example: `+proj=lcc +lon_0=-97.0 +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +x_0=2556000.0 +y_0=-1860000 +a=6370000.0 +b=6370000.0 +to_meter=12000.0 +no_defs`
  * 12US2 example: `+proj=lcc +lon_0=-97.0 +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +x_0=2412000.0 +y_0=-1332000.0 +to_meter=12000.0 +a=6370000.0 +b=6370000.0 +no_defs`
  * 36US3 example: `+proj=lcc +lon_0=-97.0 +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +x_0=2952000.0 +y_0=-2556000.0 +to_meter=36000.0 +a=6370000.0 +b=6370000.0 +no_defs`
5. Click "OK"

# Add a raster layer and set its projection

1. Click "Layer"
2. Click "Add Layer"
3. Click "Add Raster Layer"
4. Use the ellipse (`...`) to open a browser and select your file and click "Open"
5. Modify the path by adding `NETCDF:` before the path and `:<VARNAME>` after the path
  * VARNAME may be any variable in the file (e.g., O3)
6. Click "Add"
7. You should be prompted to select a coordinate reference. Choose the one you made (e.g., 12US2).
8. Click "OK"

 
 # Reference Data 
 
 [1] The 12US2 projection has IOAPI parameters: GDTYP=2, P_ALP=33., P_BET=45., P_GAM=-97., XCENT=-97., YCENT=40, XORIG=-2412000.0, YORIG=1620000.0, XCELL=12000., YCELL=12000, NROWS=246, NCOLS=396
 
 [2] "+proj=lcc +a=6370000.0 +b=6370000.0 +lon_0=-97.0 +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +x_0=2412000.0 +y_0=1620000.0 +to_meter=12000.0m +no_defs"
 
 [3] The 12US1 projection is the same as 12US2 with the following exceptions: XORIG=-2556000.0, YORIG=-1728000.0, NROWS=299, NCOLS=459.
 
 [4] The 36US3 projection is the same as the 12US2 with the following exceptions: XORIG=-2952000.0, YORIG=-2772000.0, NROWS=148, NCOLS=172, XCELL=36000., YCELL=36000.
