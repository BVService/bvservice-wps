#!/bin/sh 

# $1 -> email,
# $2 -> workspace,
# $3 -> nom de la couche1,
# $4 -> nom de la couche2,
# $5 -> tps sec,
# $6 -> tps min


echo "Sending mail..."
/usr/sbin/sendmail -t <<EOT
From: no-replay@bvservice.fr
To: $1
Subject: Résultat de la simulation
MIME-Version: 1.0
Content-Type: multipart/related;boundary="XYZ"

--XYZ
Content-Type: text/html; charset=utf-8
Content-Transfer-Encoding: 7bit

<html>
<body><img src='cid:image1' align='right'/><div align='left'>

<h2> Résultats de la simulation OpenFLUID </h2>

<p>Le taitement et terminé et votre couche a été publiée avec succé !</p>

<p>Pour visualiser sur un visualiseur avancé <a href ="http://bvservice.fr/mapfishapp/?wmc=http://bvservice.fr/context/wmc/$3.wmc" >Cliquez ici</a> </p>

<p>Pour visualiser sur un visualiseur mobile <a href ="http://geoxxx.agrocampus-ouest.fr/mviewer/?wmc=http://bvservice.fr/context/wmc/$3.wmc" >Cliquez ici</a> ou <a href ="http://geoxxx.agrocampus-ouest.fr/sviewer/?wmc=http://bvservice.fr/context/wmc/$3.wmc" >ici</a> </p>

<p>Pour télécharger le ShapeFile de la couche n° 1 <a href ="http://bvservice.fr/outputs/$2/wfs?service=WFS&version=1.0.0&request=GetFeature&typename=$3&outputFormat=SHAPE-ZIP" >Cliquez ici</a></p>

<p>Pour télécharger le ShapeFile de la couche n° 2 <a href ="http://bvservice.fr/outputs/$2/wfs?service=WFS&version=1.0.0&request=GetFeature&typename=$4&outputFormat=SHAPE-ZIP" >Cliquez ici</a></p>

<p>Pour télécharger le KML (Google Earth) de la couche n° 1 <a href ="http://bvservice.fr/outputs/$2/wms/kml?layers=$3" >Cliquez ici</a></p>

<p>Pour télécharger le KML (Google Earth) de la couche n° 2 <a href ="http://bvservice.fr/outputs/$2/wms/kml?layers=$4" >Cliquez ici</a></p>

<p>Le temps de traitement et de $5 sec, ( ~ $6 min)</p>

</div></body>
</html>

--XYZ
Content-Type: image/jpeg;name="openfluid_thumb.png"
Content-Transfer-Encoding: base64
Content-ID: <image1>
Content-Disposition: inline; filename="openfluid_thumb.png"

$(base64 '/usr/local/bvservice/processes/bvservice-wps/apps/openfluid_thumb.png')
--XYZ--
EOT
echo "Mail OK!"
