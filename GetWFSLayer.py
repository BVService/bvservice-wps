#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:00:02 2015

@author: Mounirsky
"""

import os
import time
import argparse
from zipfile import ZipFile as zipp
from owslib.wfs import WebFeatureService
####################################################################################
# GetWFSLayer
# usage : python GetWFSLayer.py -u <WMS_URL> -p <PATH>
####################################################################################

# --------------------------------------------------------------
# I - Parse the arguments
# --------------------------------------------------------------
parser = argparse.ArgumentParser(description="GetWFSLayer -u <WFS_URL> -p <PATH>")
#parser.add_argument('-u', required=True, help='layer WFS URL (for example : http://bvservice.fr/geoserver/wfs?workspace:layername)')
parser.add_argument('-u', required=True, help='layer WFS URL (for example : http://bvservice.fr/geoserver/bourdic/wfs?bourdic_rs)')

#parser.add_argument('-p', required=True, help='download layer directory (for example : /var/www/layer/IN/)')
parser.add_argument('-p', required=True, help='download layer directory (for example : /usr/local/mywps/processes/IN)')

args = vars(parser.parse_args())

if args['u']:
    layerWFSURL = args['u']
if args['p']:
    path = args['p']

# --------------------------------------------------------------
# II - GetWFSLayer function
# --------------------------------------------------------------

def GetWFSLayer(u, p):
  start = time.time()
  # Separate the WFS URL & the layer name
  split_url = u.split('?')
  server_url = split_url[0]
  ows = server_url[-3:]
  print 'The OGC standard is: '+ ows
  
  spacename_wfs = split_url[1]
  tmp_chemin = p + spacename_wfs+"_.zip"
  chemin = tmp_chemin[:-5]+".zip"
  
  if not os.path.exists(chemin):
    # Get the vector layer using OGC WFS standard
    wfs = WebFeatureService(server_url ,version='1.0.0')
    getFeature = wfs.getfeature(typename = [spacename_wfs], outputFormat ="shape-zip") 
    
    print('Downloading... : '+ spacename_wfs)
    print("From: "+ server_url)
    
    # Download the zipped shapefile
    data = getFeature.read()
    f = open(tmp_chemin ,'wb')
    f.write(data)
    f.close()
    
    # Delete .txt & .cst files from the zipped file
    zin = zipp(tmp_chemin, 'r')
#    zin.extractall(p)
    zout = zipp(chemin, 'w')
    for item in zin.infolist():
      buffer = zin.read(item.filename)
      ext = item.filename[-4:]
      if (ext != '.txt' and ext != '.cst'):
          zout.writestr(item, buffer)
          
    zout.close()
    zin.close()
    os.remove(tmp_chemin)
    
    # Unzip zipped shapefile
    os.system("unzip "+ chemin + ' -d '+ p)
  
  # Calculat time
  temps =time.time() - start
  tps = round(temps,2)
  temps_ms = str(tps)
  
  print "GetWFSLayer download time : " + temps_ms +" ms"
  
  return
 
# --------------------------------------------------------------
# II - Execute function
# --------------------------------------------------------------
if __name__ == '__main__':
#  layerWFSURL = 'http://bvservice.fr/geoserver/wms?bourdic:bourdic_rs'
#  path = '/home/utop/Bureau/IN/'
  GetWFSLayer(layerWFSURL, path)
  
  
  
  
