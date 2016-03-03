#!/usr/bin/python
# -*- coding: utf-8 -*-


#import sys     
import os
import time
#import datetime
import argparse
####################################################################################
# layerpublisher v.0.0
# How to use it : 
#  python /var/www/pywps/processes/layerpublisher.py --l FinalRS_final20150430-165805 --g http://localhost:8080/geoserver/ --d /home/openfluid202-from-git/lib-from-michael/BourdicOFfast20150430-165805/OUT/outshapefile/ --p admin:jonathan29 --w jvh --st testlolxd --s of_rs_VolTot,of_rs_HeighMax,of_rs_OverTot
####################################################################################

# --------------------------------------------------------------
# I - Parse the arguments
# --------------------------------------------------------------
current_datetime = time.strftime("%Y%m%d-%H%M%S")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='layerpublisher v.0.0')
    parser.add_argument('--l', required=True, help='layer name')
    parser.add_argument('--s', required=False, help='style name (separate with comma if more than one, the first one is the default style)')
    parser.add_argument('--g', required=True, help='geoserver url (for example : http://geoxxx.agrocampus-ouest.fr/geoserverwps/)')
    parser.add_argument('--d', required=True, help='layer directory (for example : /var/www/layer/)')
    parser.add_argument('--p', required=True, help='login:pass (for example : john:doe)')
    parser.add_argument('--w', required=True, help='workspace name (for example : testworkspace)')
    parser.add_argument('--st', required=True, help='store name (for example : teststore)')
    args = vars(parser.parse_args())

    if args['l']:
        layerName = args['l']
    if args['s']:
        layerStyle = args['s'].split(',')
    else:
		layerStyle = ""
    if args['g']:
        geoserverUrl = args['g']
    if args['d']:
        layerDirectory = args['d']
    if args['p']:
        loginPassword = args['p']
    if args['w']:
        workspaceName = args['w']
    if args['st']:
        storeName = args['st']
# --------------------------------------------------------------
# II - Zip and Upload
# --------------------------------------------------------------
pth = layerDirectory + layerName+'.zip'

if not os.path.exists(pth):
  # Zip
  os.system('zip -j '+ pth + ' ' + layerDirectory+layerName+'.*')
else:
  print (pth + " Exist")
  
# Upload
# The name of the layer on the geoserver will be the same as the layer contained in the zip
os.system("curl -v -u "+loginPassword+" -XPUT -H 'Content-type: application/zip'   --data-binary @"+layerDirectory+layerName+".zip "+geoserverUrl+"rest/workspaces/"+workspaceName+"/datastores/"+storeName+"/file.shp")
# --------------------------------------------------------------
# III - Optional : Add Style
# --------------------------------------------------------------
if layerStyle != "" : 
	additionalSld = ""
	for i in range(len(layerStyle)):
		additionalSld = additionalSld + "<name>"+layerStyle[i]+"</name>"
	# Add default SLD
	os.system("curl -u "+loginPassword+" -XPUT -H 'Content-type: text/xml' -d '<layer><defaultStyle><name>"+layerStyle[0]+"</name><workspace>"+workspaceName+"</workspace></defaultStyle></layer>' "+geoserverUrl+"rest/layers/"+workspaceName+":"+layerName)
	# Add extra SLD
	# It is advisable to have a single layer name because geoserver (v2.5) renames duplicate layers (adding a variable increment at the end of the name), which then causes problems for the style association.
	os.system("curl -u "+loginPassword+" -XPUT -H 'Content-type: text/xml' -d '<layer><styles>"+additionalSld+"<workspace>"+workspaceName+"</workspace></styles></layer>' "+geoserverUrl+"rest/layers/"+workspaceName+":"+layerName)
 
  
  
