#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Feb 24 00:37:32 2016

@author: Mounirsky
"""

#================================================================================================
# Cette application permet de générer un fichier (.wmc) depuis un ficher de cotexte (WCS) de base
# les changements déponderants de la chouche créé par le wps :

# sys.argv[1] : URL du geoserver où la couche à été publiée
# sys.argv[2] : nom de la couche1 créé
# sys.argv[3] : nom de la couche2 créé

#================================================================================================

import sys
import os
from owslib.wms import WebMapService
from SSHConnection import SSHConnection

print "Strat generating WMC"

url_geoserver = sys.argv[1]

layer1 = sys.argv[2]
layer2 = sys.argv[3]

# Récupération de la bonding-box et EPSG des couches en sortie
wms1 = WebMapService(url_geoserver + layer1 +'/wms', version='1.1.1')
bboxx1 = wms1[layer1].boundingBox

wms2 = WebMapService(url_geoserver + layer2 + '/wms', version='1.1.1')
bboxx2 = wms2[layer2].boundingBox


wmc_file = """<?xml version="1.0" encoding="UTF-8"?>
<ViewContext xmlns="http://www.opengis.net/context" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1.0" id="7f16e33e0fd0b8" xsi:schemaLocation="http://www.opengis.net/context http://schemas.opengis.net/context/1.1.0/context.xsd">
  <General>
    """+'<Window width="1613" height="980"/><BoundingBox minx="'+str(bboxx1[0])+'" miny="'+str(bboxx1[1])+'" maxx="'+str(bboxx1[2])+'" maxy="'+str(bboxx1[3])+'" SRS="'+bboxx1[4]+'"/>'+"""
    <Title />
    <Extension>
      <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-372808.257798769977" miny="6129195.05338540021" maxx="1599878.56818510010" maxy="7185860.53239960037" />
    </Extension>
  </General>
  <LayerList>
    <Layer queryable="0" hidden="0">
      <Server service="OGC:WMS" version="1.3.0">
        <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://bvservice.fr/geoserver/bourdic/ows?SERVICE=WMS&amp;" />
      </Server>
      <Name>OSM-WMS</Name>
      <Title>OpenStreetMap WMS - by terrestris</Title>
      <sld:MinScaleDenominator xmlns:sld="http://www.opengis.net/sld">266.5911979812228</sld:MinScaleDenominator>
      <sld:MaxScaleDenominator xmlns:sld="http://www.opengis.net/sld">559082264.0287180</sld:MaxScaleDenominator>
      <FormatList>
        <Format current="1">image/png</Format>
        <Format>application/atom+xml</Format>
        <Format>application/pdf</Format>
        <Format>application/rss+xml</Format>
        <Format>application/vnd.google-earth.kml+xml</Format>
        <Format>application/vnd.google-earth.kml+xml;mode=networklink</Format>
        <Format>application/vnd.google-earth.kmz</Format>
        <Format>image/geotiff</Format>
        <Format>image/geotiff8</Format>
        <Format>image/gif</Format>
        <Format>image/jpeg</Format>
        <Format>image/png; mode=8bit</Format>
        <Format>image/svg+xml</Format>
        <Format>image/tiff</Format>
        <Format>image/tiff8</Format>
        <Format>text/html; subtype=openlayers</Format>
      </FormatList>
      <StyleList>
        <Style current="1">
          <Name />
          <Title>Default</Title>
        </Style>
      </StyleList>
      <Extension>
        <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-372808.257798769977" miny="6129195.05338540021" maxx="1599878.56818510010" maxy="7185860.53239960037" />
        <ol:tileSize xmlns:ol="http://openlayers.org/context" width="512" height="512" />
        <ol:transparent xmlns:ol="http://openlayers.org/context">true</ol:transparent>
        <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">22</ol:numZoomLevels>
        <ol:units xmlns:ol="http://openlayers.org/context">m</ol:units>
        <ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer>
        <ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher>
        <ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile>
        <ol:transitionEffect xmlns:ol="http://openlayers.org/context">map-resize</ol:transitionEffect>
        <ol:gutter xmlns:ol="http://openlayers.org/context">10</ol:gutter>
      </Extension>
    </Layer>
    
    
    
    <Layer queryable="1" hidden="0">
      <Server service="OGC:WMS" version="1.3.0">
   """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?SERVICE=WMS&amp;" />'+"""
      </Server>
      """+'<Name>'+ layer1 +'</Name><Title>'+ layer1 +'</Title>'+"""
      <sld:MinScaleDenominator xmlns:sld="http://www.opengis.net/sld">266.5911979812228</sld:MinScaleDenominator>
      <sld:MaxScaleDenominator xmlns:sld="http://www.opengis.net/sld">559082264.0287180</sld:MaxScaleDenominator>
      <FormatList>
        <Format current="1">image/png</Format>
        <Format>application/atom+xml</Format>
        <Format>application/pdf</Format>
        <Format>application/rss+xml</Format>
        <Format>application/vnd.google-earth.kml+xml</Format>
        <Format>application/vnd.google-earth.kml+xml;mode=networklink</Format>
        <Format>application/vnd.google-earth.kmz</Format>
        <Format>image/geotiff</Format>
        <Format>image/geotiff8</Format>
        <Format>image/gif</Format>
        <Format>image/jpeg</Format>
        <Format>image/png; mode=8bit</Format>
        <Format>image/svg+xml</Format>
        <Format>image/tiff</Format>
        <Format>image/tiff8</Format>
        <Format>text/html; subtype=openlayers</Format>
      </FormatList>
      <StyleList>
        <Style>
          <Name>of_su_ConVol</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
            """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer1 +'" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_su_VolTot</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
            """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer1 +'&amp;style=of_su_VolTot" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_su_UpNum</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer1 +'&amp;style=of_su_UpNum" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_su_ConVol</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer1 +'&amp;style=of_su_ConVol" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_su_QMax</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer1 +'&amp;style=of_su_QMax" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>polygon</Name>
          <Title>Default Polygon</Title>
          <Abstract>A sample style that draws a polygon</Abstract>
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer1 +'&amp;style=polygon" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_su_UpArea</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
            <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://bvservice.fr/outputs/bourdic/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer=FinalSU_final-20160301-122325&amp;style=of_su_UpArea" />
          </LegendURL>
        </Style>
      </StyleList>
      <Extension>
        <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-372808.257798769977" miny="6129195.05338540021" maxx="1599878.56818510010" maxy="7185860.53239960037" />
        <ol:tileSize xmlns:ol="http://openlayers.org/context" width="512" height="512" />
        <ol:transparent xmlns:ol="http://openlayers.org/context">true</ol:transparent>
        <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">22</ol:numZoomLevels>
        <ol:units xmlns:ol="http://openlayers.org/context">m</ol:units>
        <ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer>
        <ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher>
        <ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile>
        <ol:transitionEffect xmlns:ol="http://openlayers.org/context">map-resize</ol:transitionEffect>
        <ol:gutter xmlns:ol="http://openlayers.org/context">10</ol:gutter>
      </Extension>
    </Layer>
    
    
    
    
    <Layer queryable="1" hidden="0">
      <Server service="OGC:WMS" version="1.3.0">
   """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?SERVICE=WMS&amp;" />'+"""
      </Server>
      """+'<Name>'+ layer2 +'</Name><Title>'+ layer2 +'</Title>'+"""
      <sld:MinScaleDenominator xmlns:sld="http://www.opengis.net/sld">266.5911979812228</sld:MinScaleDenominator>
      <sld:MaxScaleDenominator xmlns:sld="http://www.opengis.net/sld">559082264.0287180</sld:MaxScaleDenominator>
      <FormatList>
        <Format current="1">image/png</Format>
        <Format>application/atom+xml</Format>
        <Format>application/pdf</Format>
        <Format>application/rss+xml</Format>
        <Format>application/vnd.google-earth.kml+xml</Format>
        <Format>application/vnd.google-earth.kml+xml;mode=networklink</Format>
        <Format>application/vnd.google-earth.kmz</Format>
        <Format>image/geotiff</Format>
        <Format>image/geotiff8</Format>
        <Format>image/gif</Format>
        <Format>image/jpeg</Format>
        <Format>image/png; mode=8bit</Format>
        <Format>image/svg+xml</Format>
        <Format>image/tiff</Format>
        <Format>image/tiff8</Format>
        <Format>text/html; subtype=openlayers</Format>
      </FormatList>
      <StyleList>
        <Style>
          <Name>of_rs_UpNum</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer2 +'" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_rs_HeighMax</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer2 +'&amp;style=of_rs_HeighMax" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_rs_UpNum</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer2 +'&amp;style=of_rs_UpNum" />'+"""
          </LegendURL>
        </Style>
        <Style>utopmounir2015
          <Name>of_rs_OverTot</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer2 +'&amp;style=of_rs_OverTot" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>polygon</Name>
          <Title>Default Polygon</Title>
          <Abstract>A sample style that draws a polygon</Abstract>
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer2 +'&amp;style=polygon" />'+"""
          </LegendURL>
        </Style>
        <Style>
          <Name>of_rs_VolTot</Name>
          <Title />
          <LegendURL width="20" height="20" format="image/png">
          """+'<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="'+ url_geoserver +'/ows?service=WMS&amp;request=GetLegendGraphic&amp;format=image%2Fpng&amp;width=20&amp;height=20&amp;layer='+ layer2 +'&amp;style=of_rs_VolTot" />'+"""
          </LegendURL>
        </Style>
      </StyleList>
      <Extension>
        <ol:maxExtent xmlns:ol="http://openlayers.org/context" minx="-372808.257798769977" miny="6129195.05338540021" maxx="1599878.56818510010" maxy="7185860.53239960037" />
        <ol:tileSize xmlns:ol="http://openlayers.org/context" width="512" height="512" />
        <ol:transparent xmlns:ol="http://openlayers.org/context">true</ol:transparent>
        <ol:numZoomLevels xmlns:ol="http://openlayers.org/context">22</ol:numZoomLevels>
        <ol:units xmlns:ol="http://openlayers.org/context">m</ol:units>
        <ol:isBaseLayer xmlns:ol="http://openlayers.org/context">false</ol:isBaseLayer>
        <ol:displayInLayerSwitcher xmlns:ol="http://openlayers.org/context">true</ol:displayInLayerSwitcher>
        <ol:singleTile xmlns:ol="http://openlayers.org/context">false</ol:singleTile>
        <ol:transitionEffect xmlns:ol="http://openlayers.org/context">map-resize</ol:transitionEffect>
        <ol:gutter xmlns:ol="http://openlayers.org/context">10</ol:gutter>
      </Extension>
    </Layer>
  </LayerList>
</ViewContext>"""

print 'WMC changes are :'
print url_geoserver
print layer1
print layer2

path = '/var/local/wmc/'

os.system('mkdir -p '+path)

with open(r'/var/local/wmc/'+layer1+'.wmc', "w") as f:
    f.write(wmc_file)

os.system('chmod 777 '+path+layer1+'.wmc')

host = "bvservice.fr"
username = "login"
pw = "password"
 
origin = path+layer1+'.wmc'
dst = '/var/www/georchestra/htdocs/context/wmc/'+layer1 +'.wmc'
 
ssh = SSHConnection(host, username, pw)
ssh.put(origin, dst)
ssh.close()

print "Done"