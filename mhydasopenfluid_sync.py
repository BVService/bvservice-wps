from BVServiceWPSProcess import BVServiceWPSProcess
import time
import os
import subprocess
import shutil


#=============================================================================
#=============================================================================


class Process(BVServiceWPSProcess):

  def __init__(self):

    # Call of BVServiceWPSProcess constructor
    BVServiceWPSProcess.__init__(self,"mhydasopenfluid_sync","MHYDAS/OpenFLUID pour BVservice",
                                      """Calcul d'indicateurs avec MHYDAS/OpenFLUID""")
    
    # Creation of the form
    # Data sources

    self.addInputWorkspace("workspace",Default=None)
    
    self.addInputWFS("fields","Parcellaire",MinOccurs=0)
    self.addInputWFS("hydronetwork","Reseau hydrographique",MinOccurs=0)
    

    self.addInputWCS("mnt","Modele Numerique de Terrain",MinOccurs=0)
    
    self.addInputParam('email','E-mail input',Abstract=None,Default=None,MinOccurs=0)
    
    # SU
    self.addInputCheckbox("upperSU-count","Nombre de parcelles connectees en amont",Default=True)    
    self.addInputCheckbox("upperSU-totalarea","Surface totale des parcelles connectees en amont (m2)",Default=True)    
    self.addInputCheckbox("SU-totalvol","Volume total ruisselunzip chemine (m3)",Default=True)
    self.addInputCheckbox("SU-totalinfilt","Hauteur infiltree totale (m)",Default=True)
    self.addInputCheckbox("SU-maxQ","Debit maximum (m3/s)",Default=True) 
    self.addInputCheckbox("SU-contribvoltoRS","Volume contributif de chaque parcelle au reseau (m3)",Default=True) 

    # RS
    self.addInputCheckbox("upperRS-count","Nombre de fosse connectes en amont ",Default=True) 
    self.addInputCheckbox("upperRS-totallength","Longueur totale de reseau en amont (m)",Default=True) 
    self.addInputCheckbox("RS-totalvolume","Volume total transfere (m3)",Default=True) 
    self.addInputCheckbox("RS-maxoverheight","Hauteur maximum debordee (m)",Default=True) 
    self.addInputCheckbox("RS-totalovervol","Volume total deborde (m3)",Default=True)
    
    
    self.addOutputWMS("SU","Indicateurs sur le parcellaire")
    self.addOutputWMS("RS","Indicateurs sur le reseau hydrographique")

    self.addOutputText("Time","temps de traitement")

  #=============================================================================
  #=============================================================================
    

  def execute(self):
    
    start = time.time()
   
    workspace = self.IOFields["input"]["workspace"].getValue()
        
    CurrentDateTime = time.strftime("%Y%m%d-%H%M%S")
    
    simulatorsPath = "/var/local/bvserviceOpenFlUID/install/lib/openfluid/simulators"
    
    SourceProjectsPath = "/home/smounir/projects"
    ProjectToRun = "BourdicOF"
    ExecPath = "/home/smounir/BVServiceOpenFLUID"
    
    SourceProject = SourceProjectsPath +"/"+ ProjectToRun
    
    ExecProject = ExecPath +"/"+ ProjectToRun +"_" + CurrentDateTime
    
    ExecIN = ExecProject +"/IN"
    ExecOUT = ExecProject +"/OUT"
    ProcessLogfile = ExecProject +"/process.log"    
    
    apps = '/usr/local/bvservice/processes/bvservice-wps/apps/'
    
    # Download all wfs inputs using GetWFSLayer.py
    path_in = SourceProject +'/IN/GeoData/'
    path_out = ExecProject +'/OUT/outshapefile/'
        
    for i in self.IOFields["input"]["wfs"]:
      urlWfs = self.IOFields["input"]["wfs"][i].getValue()
      if urlWfs is not None:
        self.cmd(apps + "GetWFSLayer.py %s %s %s %s" % ('-u',urlWfs,'-p',path_in))    

    # Download all wcs inputs using GetWCSLayer.py
    
    for i in self.IOFields["input"]["wcs"]:
      urlWcs = self.IOFields["input"]["wcs"][i].getValue()
      if urlWcs is not None:
        self.cmd(apps + "GetWCSLayer.py %s %s %s %s" % ('-u',urlWcs,'-p',path_in))
      
    # Run Openfluid
    shutil.copytree(SourceProject, ExecProject)
#    os.system('mkdir '+ExecProject)
#    os.system('cp -R '+SourceProject+'/* '+ExecProject+'/')
    
    Env = os.environ.copy()
    Env["LD_LIBRARY_PATH"] = "/var/local/bvserviceOpenFlUID/install/lib"
    
    Command = ["openfluid","run",ExecProject,'-p', simulatorsPath, "-c",ExecIN, ExecOUT]
    
    with open(ProcessLogfile, 'a') as Log:
      P = subprocess.Popen(Command,env=Env,stdout=Log,stderr=Log)
      P.communicate()
      P.wait()
    
    # Ajouter les fichiers de projection (EPSG:2154) !
    os.system('cp '+ ExecIN+'/prj/* '+ExecOUT+'/outshapefile')

    # Publishing layers
    list_out = ['FinalSU_final','FinalRS_final']

    def rename(dirr,name):
        for ext in "dbf shp shx prj".split():
            os.rename(dirr+name+'.'+ ext, dirr+name+'-'+CurrentDateTime+'.'+ ext)
    
    dirr = ExecOUT+"/outshapefile/"
    
    rename(dirr, list_out[0])
    rename(dirr, list_out[1])
    
    login = ''
    password = ''
    
    SU_styles = 'of_su_ConVol,of_su_QMax,of_su_UpArea,of_su_UpNum,of_su_VolTot,polygon'
    RS_styles = 'of_rs_UpNum,of_rs_VolTot,of_rs_HeighMax,of_rs_OverTot,of_rs_UpLenght,of_rs_UpNum,polygon'
    
    self.cmd(apps + "layerpublisher.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (
                                                                                   '--l',list_out[0]+'-'+CurrentDateTime,
                                                                                   '--g','http://bvservice.fr/outputs/',
                                                                                   '--d',path_out,
                                                                                   '--p',login+':'+password,
                                                                                   '--w',workspace,
                                                                                   '--st',list_out[0]+'-'+ CurrentDateTime,
                                                                                   '--s',SU_styles))
                                                                                   
                                                                                   
    self.cmd(apps + "layerpublisher.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (
                                                                                     '--l',list_out[1]+'-'+CurrentDateTime,
                                                                                     '--g','http://bvservice.fr/outputs/',
                                                                                     '--d',path_out,
                                                                                     '--p',login+':'+password,
                                                                                     '--w',workspace,
                                                                                     '--st',list_out[1]+'-'+ CurrentDateTime,
                                                                                     '--s',RS_styles))

    
    
    # Calcule du temps de traitement
    temps = int(time.time() - start)
    temps_sec = str(temps)
    temps_min = str(temps/60)
    
    # Generate a WMC
    # sys.argv[1] : URL du geoserver ou la couche en sortie
    # sys.argv[2] : nom de la couche1 
    # sys.argv[3] : nom de la couche2
    
    url_geoserver = 'http://bvservice.fr/outputs/'+workspace+'/'

    self.cmd(apps + "wmc_generator.py %s %s %s" % (url_geoserver,
                                                   list_out[0]+'-'+CurrentDateTime,
                                                    list_out[1]+'-'+CurrentDateTime))
                                                    
                                                    
                                                    
    # Send mail
    email = self.IOFields["input"]["param"]["email"].getValue()
    
    if email is not None:
      self.cmd(apps + "mailSender.sh %s %s %s %s %s %s" % (email, 
                                                         workspace, 
                                                         list_out[0]+'-'+CurrentDateTime, 
                                                          list_out[1]+'-'+CurrentDateTime,
                                                          temps_sec, 
                                                          temps_min))

    # Set of the output values

    self.setOutputWMSValue("RS", "http://bvservice.fr/outputs/"+ workspace +"/wms?" + list_out[0]+'-'+CurrentDateTime)
    self.setOutputWMSValue("SU", "http://bvservice.fr/outputs/"+ workspace +"/wms?" + list_out[1]+'-'+CurrentDateTime)

    
    self.setOutputTextValue("Time", "Temps de traitement: \n "+temps_sec+" sec, ( ~ "+temps_min+" min)")

    return
