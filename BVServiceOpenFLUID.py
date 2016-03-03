import os
import time
#import datetime
import subprocess
import shutil
#from BVServiceWPSProcess import BVServiceWPSProcess


#=============================================================================
#=============================================================================
# TODO
#   - be consistent on local temporary directories
#=============================================================================
#=============================================================================


class BVServiceOpenFLUID:
  
  def __init__(self,Project,Parameters):

    self.Parameters = Parameters

    self.CurrentDateTime = time.strftime("%Y%m%d-%H%M%S")

#    self.SourceProjectsPath = "/var/bvservice/projects"    
    self.SourceProjectsPath = "/home/utop/bvservice/projects"
    self.ProjectToRun = Project
    self.ExecPath = "/tmp/BVServiceOpenFLUID"

    self.SourceProject = self.SourceProjectsPath +"/"+ self.ProjectToRun

    self.ExecProject = self.ExecPath +"/"+ self.ProjectToRun +"_"+ self.CurrentDateTime
#    self.ExecProject = self.ExecPath +"/"+ self.ProjectToRun
    self.ExecIN = self.ExecProject +"/IN"
    self.ExecOUT = self.ExecProject +"/OUT"

    self.ProcessLogfile = self.ExecProject+"/process.log"        

#    self.CurrentDateTime = time.strftime("%Y%m%d-%H%M%S")


  #=============================================================================
  #=============================================================================


  def prepare(self):

    shutil.rmtree(self.ExecProject,ignore_errors=True)
    os.makedirs(self.ExecProject)
    
    shutil.copytree(self.SourceProject+"/IN",self.ExecIN)

    with open(self.ProcessLogfile, 'w') as Log:
      Log.write("Process launched at "+self.CurrentDateTime+"\n")
      Log.write("Parameters:\n")
      Log.write(str(self.Parameters)+"\n")
      Log.write("\n\n")
      
  #=============================================================================
  #=============================================================================





  #=============================================================================
  #=============================================================================

  def run(self):
    Command = ["openfluid","run","-p","/home/utop/.openfluid/wares/simulators/","-c",self.ExecIN,self.ExecOUT]
    #Command = ["openfluid","run","-c",self.ExecIN,self.ExecOUT]
#    openfluid run -p /root/.openfluid/wares/simulators -c /home/utop/bvservice/projects/BourdicOF_haies/IN /home/utop/bvservice/projects/BourdicOF_haies/OUT

    Env = os.environ.copy()
    Env["LD_LIBRARY_PATH"] = "/opt/lib"
    
    with open(self.ProcessLogfile, 'a') as Log:
      P = subprocess.Popen(Command,env=Env,stdout=Log,stderr=Log)
      P.communicate()
      P.wait()


  #=============================================================================
  #=============================================================================


  def publishLayers(self):
    
#    CurrentDateTime = self.CurrentDateTime

    with open(self.ProcessLogfile,'a') as Log:
      Log.write('\n')
      Log.write("============== Publishing ==============\n\n")

    for Layer,Params in self.Parameters["publishing"].iteritems():

#      # setup of coordinate system
#      Command = ['ogr2ogr',
#                 '-f','ESRI Shapefile',
#                 '-a_srs','EPSG:2154',
#                 self.ExecOUT+Params["outsubdir"]+'/'+Params["fileroot"]+self.CurrentDateTime+'.shp',
#                 self.ExecOUT+Params["outsubdir"]+'/'+Params["fileroot"]+'.shp']
#
#      with open(self.ProcessLogfile,'a') as Log:
#        Log.write(' '.join(Command))
#        Log.write('\n')
#        Log.write('\n')
#
#
#      with open(self.ProcessLogfile,'a') as Log:
#        P = subprocess.Popen(Command,stdout=Log,stderr=Log)
#        P.communicate()
#        P.wait()


      # publication to bvservice.fr
        
      Command = ['python',os.path.dirname(os.path.abspath(__file__))+'/layerpublisher.py',
#                 '--l',Params["fileroot"]+self.CurrentDateTime,
                 '--l',Params["fileroot"],
                 '--g','http://bvservice.fr/outputs/',
#                 '--d',self.ExecOUT+Params["outsubdir"]+'/',
                 '--d',self.ExecOUT+'/',
                 '--p','testadmin:corsen292!',
                 '--w',Params["workspace"],
                 '--st',Params["store"]+self.CurrentDateTime,
                 '--s',Params["sld"]]
    
#      self.Parameters["publishing"][Layer]["wms"] = 'http://bvservice.fr/outputs/wms?'+Params["workspace"]+':'+Params["fileroot"]+self.CurrentDateTime
      self.Parameters["publishing"][Layer]["wms"] = 'http://bvservice.fr/outputs/wms?'+Params["workspace"]+':'+Params["fileroot"]

      with open(self.ProcessLogfile,'a') as Log:
        Log.write('\n')
        Log.write('\n')
        Log.write(' '.join(Command))
        Log.write('\n')

      with open(self.ProcessLogfile, 'a') as Log:
        P = subprocess.Popen(Command,stdout=Log,stderr=Log)
        P.communicate()
        P.wait()


  #=============================================================================
  #=============================================================================


  def getPublishedLayer(self,Name):

    return self.Parameters["publishing"][Name]["wms"]


  #=============================================================================
  #=============================================================================


  def getVersion(self):

    return subprocess.check_output(["openfluid","--version"]).replace("\n","")


  #=============================================================================
  #=============================================================================


  def getLog(self):

    Contents = "Not found!"

    if os.path.isfile(self.ProcessLogfile):
      with open (self.ProcessLogfile, "r") as Log:
        Contents = Log.read()

    return Contents

