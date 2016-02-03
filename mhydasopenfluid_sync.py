from BVServiceWPSProcess import BVServiceWPSProcess
from BVServiceOpenFLUID import BVServiceOpenFLUID
import time
#import os
#import subprocess


#=============================================================================
#=============================================================================


class Process(BVServiceWPSProcess):

  def __init__(self):

    # Call of BVServiceWPSProcess constructor
    BVServiceWPSProcess.__init__(self,"mhydasopenfluid_sync","MHYDAS/OpenFLUID pour BVservice",
                                      """Calcul d'indicateurs avec MHYDAS/OpenFLUID""")
    
    # Creation of the form
    # Data sources
    
    
#    self.addInputCoordxy("Point1","Coordonnees xy d un point sur la carte",Default="None")
    
#    WSList = ['bourdic','moulinet']
#    self.addInputCombo("WS","Liste des espaces de travail",Default="bourdic")
#    self.addInputCombo("workspace","Liste des espaces de travail",Values = WSList,Default="None")

    self.addInputParam('email','E-mail input',Abstract=None,Default=None,MinOccurs=0)


    self.addInputWorkspace("workspace",Default=None)
    
    
    
    self.addInputWFS("fields","Parcellaire",MinOccurs=1)
    self.addInputWFS("hydronetwork","Reseau hydrographique",MinOccurs=1)
    
#    self.addInputWMS("mnt2","Modele Numerique de Terrain",Default="None")
#    self.addInputWMS("fields2","Parcellaire",Default="None")
#    self.addInputWMS("hydronetwork2","Reseau hydrographique",Default="None")

    self.addInputWCS("mnt","Modele Numerique de Terrain",MinOccurs=0)
#    self.addInputWCS("mnt2","Modele Numerique de Terrain2",Default="None")
    
    
    self.addInputCombo("Combo","Parametre scroll",Values=["Value1","Value1","Value2","Value3"],MinOccurs=0)
    
#    self.addInputGML("gml1","Entrez un fichier GML1",MinOccurs=0)
#    self.addInputGML("gml2","Entrez un fichier GML2",MinOccurs=0)
    
#    # SU
    self.addInputCheckbox("upperSU-count","Nombre de parcelles connectees en amont",Default=True)    
    self.addInputCheckbox("upperSU-totalarea","Surface totale des parcelles connectees en amont (m2)",Default=True)    
    self.addInputCheckbox("SU-totalvol","Volume total ruissele (m3)",Default=True)
    self.addInputCheckbox("SU-totalinfilt","Hauteur infiltree totale (m)",Default=True)
    self.addInputCheckbox("SU-maxQ","Debit maximum (m3/s)",Default=True) 
    self.addInputCheckbox("SU-contribvoltoRS","Volume contributif de chaque parcelle au reseau (m3)",Default=True) 
#
#    # RS
    self.addInputCheckbox("upperRS-count","Nombre de fosse connectes en amont ",Default=True) 
    self.addInputCheckbox("upperRS-totallength","Longueur totale de reseau en amont (m)",Default=True) 
    self.addInputCheckbox("RS-totalvolume","Volume total transfere (m3)",Default=True) 
    self.addInputCheckbox("RS-maxoverheight","Hauteur maximum debordee (m)",Default=True) 
    self.addInputCheckbox("RS-totalovervol","Volume total deborde (m3)",Default=True)
    
    
    self.addOutputWMS("SU","Indicateurs sur le parcellaire")
#    self.addOutputWMS("RS","Indicateurs sur le reseau hydrographique")
#    self.addOutputWMS("SU1","Indicateurs sur le parcellaire")
#    self.addOutputWMS("RS1","Indicateurs sur le reseau hydrographique")

    self.addOutputText("version","OpenFLUID version")
#    self.addOutputText("version1","OpenFLUID version1")
#    self.addOutputText("version2","OpenFLUID version2")
#    self.addOutputText("version3","OpenFLUID version3")
#    self.addOutputText("outputlog","Log of run")


  #=============================================================================
  #=============================================================================
    

  def execute(self):
   
    workspace = self.IOFields["input"]["workspace"].getValue()
    
    CurrentDateTime = time.strftime("%Y%m%d-%H%M%S")
    
    
    OFRun = BVServiceOpenFLUID("BourdicOF_haies",
                               { "publishing" : 
                                   { 
                                     "SU" : 
                                       { 
                                         "sld" : " ",
                                         "outsubdir" : "/home/utop/bvservice/projects/BourdicOF_haies/OUT",
                                         "fileroot" : "bourdic_su",
                                         "workspace" : "bourdic",
                                         "store" : "bourdicsu",
                                       },
                                     "RS" : 
                                       { 
                                         "sld" : " ",
                                         "outsubdir" : "/home/utop/bvservice/projects/BourdicOF_haies/OUT",
                                         "fileroot" : "bourdic_rs",
                                         "workspace" : "bourdic",
                                         "store" : "bourdicrs",
                                       }
                                   }
                               })

    # Download all wfs inputs using GetWFSLayer.py
    
    path_in = '/usr/local/mywps/processes/IN/'
#    path_in = '/usr/local/bvservice/processes/IN/'
#    path_out = '/usr/local/bvservice/processes/OUT/'
    

#    mygml = self.IOFields["input"]["gml"]["fields"].getValue()
#    
#    self.cmd("cp %s %s " % (mygml +'.gml', path_out))
    
#    data = gml.read()
#    f = open(path_out +'sdfsdfdf.gml','wb')
#    f.write(gml)
#    f.close()  
    
    for i in self.IOFields["input"]["wfs"]:
      urlWfs = self.IOFields["input"]["wfs"][i].getValue()
      
      if urlWfs is not None:
        self.cmd("/usr/local/mywps/processes/bvservice-wps/GetWFSLayer.py %s %s %s %s" % ('-u',urlWfs,
                                                                           '-p',path_in))
                                                                           
#        self.cmd("/usr/local/bvservice/processes/GetWFSLayer.py %s %s %s %s" % ('-u',urlWfs,
#                                                                           '-p',path_in))
        
#        commande = ['python','/usr/local/mywps/processes/bvservice-wps/GetWFSLayer.py',
#                '-u',urlWfs,
#                '-p',path_in]
#        Process = subprocess.Popen(commande)
#        Process.communicate()
#        Process.wait()
    

    # Download all wcs inputs using GetWCSLayer.py
    
    for i in self.IOFields["input"]["wcs"]:
      urlWcs = self.IOFields["input"]["wcs"][i].getValue()
      if urlWcs is not None:
        self.cmd("/usr/local/mywps/processes/bvservice-wps/GetWCSLayer.py %s %s %s %s" % ('-u',urlWcs,
                                                                           '-p',path_in))
                                                                           
#        self.cmd("/usr/local/bvservice/processes/GetWCSLayer.py %s %s %s %s" % ('-u',urlWcs,
#                                                                           '-p',path_in))
                                                                           
#        commande = ['python','/usr/local/mywps/processes/bvservice-wps/GetWCSLayer.py',
#                '-u',urlWcs,
#                '-p',path_in]
#        Process = subprocess.Popen(commande)
#        Process.communicate()
#        Process.wait()



#    OFRun.prepare()
#    OFRun.run()
#    OFRun.publishLayers()



    # Publishing layers  
#    self.cmd("/usr/local/mywps/processes/bvservice-wps/layerpublisher.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % ('--l','FinalSU_final',
#                                                                                     '--g','http://bvservice.fr/outputs/',
#                                                                                     '--d',path_out,
#                                                                                     '--p','user:password',
#                                                                                     '--w',workspace,
#                                                                                     '--st','bourdic' + CurrentDateTime,
#                                                                                     '--s','of_su_ConVol,of_su_QMax,of_su_UpArea,of_su_UpNum,of_su_VolTot,polygon'))
                                                                                     


#    self.setOutputWMSValue("SU",OFRun.getPublishedLayer("SU"))
#    self.setOutputWMSValue("RS",OFRun.getPublishedLayer("RS"))

#    self.setOutputWMSValue("SU", "http://bvservice.fr/outputs/"+workspace+"/wms?FinalSU_final")
    


    # Set of the output values
    self.setOutputWMSValue("SU", "http://bvservice.fr/outputs/moulinet/wms?bv_20150910-131316")
#    self.setOutputWMSValue("RS", "http://bvservice.fr/outputs/moulinet/wms?exutoires_20150609-174246")
#  
#    self.setOutputWMSValue("SU1", "http://bvservice.fr/outputs/moulinet/wms?arbre_20150617-145706")
#    self.setOutputWMSValue("RS1", "http://bvservice.fr/outputs/moulinet/wms?bv_20150609-1742060")



    self.setOutputTextValue("version", "OpenFLUID version : "+OFRun.getVersion())

#    self.setOutputTextValue("version", self.IOFields["input"]["param"]["Text"].getValue())
#    self.setOutputTextValue("version1", input_wmsID)
#    self.setOutputTextValue("version2", 'Text Output_2')
#    self.setOutputTextValue("version3", 'Text Output_3')

#    LogStr = OFRun.getLog()
#    LogStr = LogStr.replace('&','&amp;')
#    LogStr = LogStr.replace('<','&lt;')
#    LogStr = LogStr.replace('>','&gt;')    
#    self.setOutputTextValue("outputlog",LogStr)

    return

