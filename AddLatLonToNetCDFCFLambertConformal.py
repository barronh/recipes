#!/bin/env python

from optparse import OptionParser

parser = OptionParser()
parser.set_usage("""

Usage: python %prog [-m CF|IOAPI] ifile [lccname]

  ifile - path to NetCDF file with lccname variable
  lccname - name of CF variable that defines the Lambert 
            Conical Conformal Projection. defaults to 
            LambertConformalProjection (e.g., CAMx or
            CMAQ file converted to NetCDF using netcdf-java)
""")


(options, args) = parser.parse_args()

if len(args) not in (1, 2):
    parser.print_help()
    exit()
else:
    args = dict(zip('ifile lccname'.split(), args))
    ifile = args['ifile']
    lccname = args.get('lccname', 'LambertConformalProjection')
# Import libraries
import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import pyproj

# Open inputfile (ifile should be some path to a file
ifileo = Dataset(ifile, 'a')

if 'CF' in options.conventions:
    try:
        lccdef = ifileo.variables[lccname]
    except KeyError as e:
        raise KeyError(e.message + ' -- Available keys: ' + ', '.join(ifileo.variables.keys()))
    x, y = ifileo.variables['x'][:], ifileo.variables['y'][:]
    lunit = ifileo.variables['x'].units.strip()
elif 'IOAPI' in options.conventions:
    lccdef = object()
    lccdef.latitude_projection_origin = ifileo.YCENT
    lccdef.standard_parallel = [ifileo.P_ALP, ifileo.P_BET]
    lccdef.earth_radius = 6371000. # Add search for earth radius later
    lccdef.longitude_of_central_meridian = ifileo.XCENT
    x = np.linspace(0, ifileo.NCOLS * ifileo.XCELL, ifileo.NCOLS + 1) + ifileo.XORIG
    y = np.linspace(0, ifileo.NROWS * ifileo.XCELL, ifileo.NROWS + 1) + ifileo.YORIG
    lunit = 'm'

lcc = pyproj.Proj('+proj=lcc +lon_0=%s +lat_1=%s +lat_2=%s +a=%s +lat_0=%s' % (lccdef.longitude_of_central_meridian, lccdef.standard_parallel[0], lccdef.standard_parallel[1], lccdef.earth_radius, lccdef.latitude_of_projection_origin,)  )

if 'IOAPI' in options.conventions:
    x = arrange
scale = {'km': 1000., 'm': 1.}[lunit]
lcc_x, lcc_y = np.meshgrid(x, y)
lcc_x *= scale
lcc_y *= scale

lon, lat = lcc(lcc_x, lcc_y, inverse = True)
if 'latitude' not in ifileo.variables.keys():
    var = ifileo.createVariable('latitude', lat.dtype.char, ('ROW', 'COL'))
    var[:] = lat
    var.units = 'degrees_north'
    var.standard_name = 'latitude'

if 'longitude' not in ifileo.variables.keys():
    var = ifileo.createVariable('longitude', lon.dtype.char, ('ROW', 'COL'))
    var[:] = lon
    var.units = 'degrees_north'
    var.standard_name = 'longitude';

for varkey in ifileo.variables.keys():
    var = ifileo.variables[varkey]
    olddims = list(var.dimensions)
    dims = map(lambda x: {'ROW': 'latitude', 'COL': 'longitude', 'TSTEP': 'time', 'LAY': 'level'}.get(x, x), olddims)
    if olddims != dims:
        var.coordinates = ' '.join(dims)

ifileo.close()
