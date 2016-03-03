#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 18:32:21 2015

@author: Mounirsky
"""

import os
import time
import argparse
from owslib.wcs import WebCoverageService
####################################################################################
# GetWCSLayer
# usage : python GetWCSLayer.py -u <WCS_URL> -p <PATH>
####################################################################################

# --------------------------------------------------------------
# I - Parse the arguments
# --------------------------------------------------------------
parser = argparse.ArgumentParser(description="GetWCSLayer -u <WCS_URL> -p <PATH>")
#parser.add_argument('-u', required=True, help='layer WCS URL (for example : http://bvservice.fr/geoserver/wcs?workspace:layername)')
parser.add_argument('-u', required=True, help='layer WCS URL (for example : http://bvservice.fr/geoserver/bourdic/wcs?bourdic_dem)')

#parser.add_argument('-p', required=True, help='download layer directory (for example : /var/www/layer/IN/)')
parser.add_argument('-p', required=True, help='download layer directory (for example : /usr/local/mywps/processes/IN)')

args = vars(parser.parse_args())

if args['u']:
    layerWCSURL = args['u']
if args['p']:
    path = args['p']

# --------------------------------------------------------------
# II - GetWCSLayer function
# --------------------------------------------------------------

def GetWCSLayer(u, p):
  start = time.time()
  # Manage the WFS URL & the layer name
  split_url = u.split('?')
  server_url = split_url[0]
  ows = server_url[-3:]
  print 'The OGC standard is: '+ ows
  
  if ows == 'ows' or ows == 'wcs':
    server_url = server_url[:-3]+ 'wcs' 
    spacename_wcs = split_url[1]
    chemin = p + spacename_wcs +'.tif'
    
    if not os.path.exists(chemin):
      
      # Get the raster layer using OGC WCS standard
      wcs = WebCoverageService(server_url ,version='1.0.0')
      image = wcs[spacename_wcs]
      
      # Download the GeoTIFF image file
      info = (image.boundingboxes)[0]
          
      epsg = info['nativeSrs']
      bboxx = info['bbox']
      
      offset = image.grid.offsetvectors
      cellsize_x= offset[0]
      x = cellsize_x[0]
      X = str(abs(float(x)))
      
      cellsize_y= offset[1]
      y = cellsize_y[1]
      Y = str(abs(float(y)))
      
  #    img_formats = image.supportedFormats
  #    img_format = img_formats[0]
      img_format = 'GeoTIFF'        
      
      print "Downloading the GeoTIFF file... : "+spacename_wcs
      print "From: "+server_url
      output = wcs.getCoverage(identifier = spacename_wcs,
                                 bbox = bboxx,
                                   crs = epsg,
                                     format = img_format,
                                       resx = X,
                                         resy = Y)                            
                               
      data = output.read()
      f = open(chemin,'wb')
      f.write(data)
      f.close()
    
    # Calculat time
    temps =time.time() - start
    tps = round(temps,2)
    temps_ms = str(tps)
    print "GetWCSLayer download time : " + temps_ms +" ms"

# --------------------------------------------------------------
# II - Execute function
# --------------------------------------------------------------
if __name__ == '__main__':
  GetWCSLayer(layerWCSURL, path)