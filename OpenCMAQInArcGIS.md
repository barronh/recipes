# Overview 
To use CMAQ data with ArcGIS it is most convenient to use a CMAQ/WRF projection system for the project. Then use the "Make NetCDF Raster Layer" tool. This example is based on the EPA 12US2 projection[1]. This works with CMAQ emissions, concentration, and metcro data correctly in ArcGIS.  Help me by correcting any of the steps that aren’t clear or quite correct.

# Create the projection

This section will use meta-data that is available in the GRIDDESC text file or as IOAPI meta-data on the NetCDF file (ncdump -h). Values for the EPA's 12US2 domain are provided as examples.

1. Open ArcGIS
2. Right click on "Layers"; Choose "Properties"
3. Go to tab for coordinate system (approximate instruction)
4. Select new projected coordinate system (world with asterisk in upper left of dialog box).
5. Give the new name "EPA 12US2"
6. Choose "Lambert_Conic_Conformal" for Projection Name from the dropdown menu
7. Enter False Easting: -XORIG - XCELL/2 (12US2: 2412000 - 6000  = 2406000)
8. Enter False Northing: -YORIG - YCELL/2 (12US2: 1620000 - 6000 = 1614000)
9. Enter Central Meridian: XCENT (12US2: -97)
10. Enter Standard Parallel 1: P_ALP (12US2: 33)
11. Enter Standard Parallel 2: P_BET (12US2: 45)
12. leave scale factor set to 1
13. Enter Latitude of Origin: YCENT (12US2: 40)
14. Choose custom unit and give it a name (e.g., "12km") and enter XCELL (12US2: 12000)
15. Choose a new geographic transformation
16. Make a new one called WRF Sphere
17. set Datum as "D_Sphere_EMEP" or Set "Semi Major" and "Semi Minor" axes = 6370000
18. Select OK
19. Select OK
20. You may be warned that datum projections may have some misalignment.
 
# Make NetCDF Raster

Follow instructions from ESRI on "Reading NetCDF data as a raster"[2]. Import the data and choose COL as X dimension, ROW as Y dimension, and optionally LAY or TSTEP as band.

# Import Other Data

Now bring in whatever you want and ArcGIS will reproject that data on the fly.

# References

[1] "+proj=lcc +a=6370000.0 +b=6370000.0 +lon_0=-97.0 +lat_1=33.0 +lat_2=45.0 +lat_0=40.0 +x_0=2412000.0 +y_0=1620000.0 +to_meter=12000.0m +no_def"

[2] http://desktop.arcgis.com/en/arcmap/10.3/manage-data/netcdf/reading-netcdf-data-as-a-raster-layer.htm
