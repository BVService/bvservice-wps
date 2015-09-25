
from BVServiceWPSProcess import BVServiceWPSProcess   
from BVServiceOpenFLUID import BVServiceOpenFLUID


#=============================================================================
#=============================================================================


class Process(BVServiceWPSProcess):

  def __init__(self):

    # Call of BVServiceWPSProcess constructor
    BVServiceWPSProcess.__init__(self,"mhydasopenfluid_sync","MHYDAS/OpenFLUID pour BVservice",
                                      """Calcul d'indicateurs avec MHYDAS/OpenFLUID""")

    # Creation of the form
    # Data sources
    self.addInputWMS("mnt","Modele Numerique de Terrain",Default="None")
    self.addInputWMS("fields","Parcellaire",Default="None")
    self.addInputWMS("hydronetwork","Reseau hydrographique",Default="None")


    # SU
    self.addInputCheckbox("upperSU-count","Nombre de parcelles connectees en amont",Default=True)    
    self.addInputCheckbox("upperSU-totalarea","Surface totale des parcelles connectees en amont (m2)",Default=True)    
    self.addInputCheckbox("SU-totalvol","Volume total ruissele (m3)",Default=True)
    self.addInputCheckbox("SU-totalinfilt","Hauteur infiltree totale (m)",Default=True)
    self.addInputCheckbox("SU-maxQ","Debit maximum (m3/s)",Default=True) 
    self.addInputCheckbox("SU-contribvoltoRS","Volume contributif de chaque parcelle au reseau (m3)",Default=True) 

    #RS
    self.addInputCheckbox("upperRS-count","Nombre de fosse connectes en amont ",Default=True) 
    self.addInputCheckbox("upperRS-totallength","Longueur totale de reseau en amont (m)",Default=True) 
    self.addInputCheckbox("RS-totalvolume","Volume total transfere (m3)",Default=True) 
    self.addInputCheckbox("RS-maxoverheight","Hauteur maximum debordee (m)",Default=True) 
    self.addInputCheckbox("RS-totalovervol","Volume total deborde (m3)",Default=True)
    
    
    self.addOutputWMS("SU","Indicateurs sur le parcellaire")
    self.addOutputWMS("RS","Indicateurs sur le reseau hydrographique")

    self.addOutputText("version","OpenFLUID version")
    #self.addOutputText("outputlog","Log of run")


  #=============================================================================
  #=============================================================================
    

  def execute(self):

    OFRun = BVServiceOpenFLUID("BourdicOF_haies",
                               { "publishing" : 
                                   { 
                                     "SU" : 
                                       { 
                                         "sld" : " ",
                                         "outsubdir" : "/outshapefile",
                                         "fileroot" : "FinalSU_final",
                                         "workspace" : "bourdic",
                                         "store" : "bourdicsu"
                                       },
                                     "RS" : 
                                       { 
                                         "sld" : " ",
                                         "outsubdir" : "/outshapefile",
                                         "fileroot" : "FinalRS_final",
                                         "workspace" : "bourdic",
                                         "store" : "bourdicrs"
                                       }
                                   }
                               })


    OFRun.prepare()
    OFRun.run()
    OFRun.publishLayers()

    self.setOutputWMSValue("SU",OFRun.getPublishedLayer("SU"))
    self.setOutputWMSValue("RS",OFRun.getPublishedLayer("RS"))


    # Set of the output values
    self.setOutputTextValue("version",OFRun.getVersion())

#    LogStr = OFRun.getLog()
#    LogStr = LogStr.replace('&','&amp;')
#    LogStr = LogStr.replace('<','&lt;')
#    LogStr = LogStr.replace('>','&gt;')    
#    self.setOutputTextValue("outputlog",LogStr)

    return

