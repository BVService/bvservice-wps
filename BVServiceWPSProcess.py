"""This file proposes a class implementing the BVservice layer upon the WPS protocol"""

__author__ = "Jean-Christophe Fabre"
__license__ = "GPL"


from pywps.Process import WPSProcess


#=============================================================================
#=============================================================================


class BVServiceWPSProcess(WPSProcess):
  """This class implements the BVservice layer upon the WPS protocol"""


  def __init__(self,Identifier,Title,Abstract): 

    # Call of WPSProcess constructor
    WPSProcess.__init__(self,
            identifier = Identifier,
            title = Title,
            abstract = Abstract,
            version = "1.0",
            storeSupported = True,
            statusSupported = True)

    # Initialization of structure for form widgets 
    self.IOFields = dict()
    self.IOFields["input"] = dict()
    self.IOFields["input"]["wfs"] = dict()
    self.IOFields["input"]["wcs"] = dict()
    self.IOFields["input"]["param"] = dict()
    self.IOFields["input"]["scroll"] = dict()
    self.IOFields["input"]["checkbox"] = dict()
    self.IOFields["input"]["gml"] = dict()
    self.IOFields["input"]["coordxy"] = dict()
    self.IOFields["input"]["workspace"] = dict()
    
    self.IOFields["output"] = dict()
    self.IOFields["output"]["param"] = dict()
    self.IOFields["output"]["wms"] = dict()


  #=============================================================================================================================
  # AddInputs
  #=============================================================================================================================
  
  def addInputWorkspace(self,Title,Abstract=None,Default=None,MinOccurs=0):
    """ Adds a workspace input field
    
    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    """

    self.IOFields["input"]["workspace"] = self.addLiteralInput(identifier = "L_input_workspace",
                                                                title = Title, 
                                                                abstract = Abstract,
                                                                default=Default,
                                                                minOccurs=MinOccurs,
                                                                type = type("")) 

  #=============================================================================================================================
  # AddInputs
  #=============================================================================================================================

  def addInputCoordxy(self,ID,Title,Abstract=None,Default=None,MinOccurs=0):
    """ Adds a coordinates x & y point input field
    
    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    """

    self.IOFields["input"]["coordxy"][ID] = self.addLiteralInput(identifier = "L_input_coordxy"+ID,
                                                                title = Title, 
                                                                abstract = Abstract,
                                                                default=Default,
                                                                minOccurs=MinOccurs,
                                                                type = type("")) 


  #=============================================================================
  #=============================================================================                                                               type = type("")) 
                                                                

  def addInputGML(self,ID,Title,Abstract=None,MinOccurs=0):
    """ Adds a GML input field
    
    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    """

    self.IOFields["input"]["gml"][ID] = self.addComplexInput(identifier = "C_input_gml"+ID,
                                                                title = Title, 
                                                                abstract = Abstract,
                                                                minOccurs=MinOccurs,
                                                                formats = [{'mimeType': 'text/xml'}]) 


  #=============================================================================
  #=============================================================================


  def addInputParam(self,ID,Title,Abstract=None,Default=None,MinOccurs=0):
    """ Adds a text input field
    
    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    """

    self.IOFields["input"]["param"][ID] = self.addLiteralInput(identifier = "L_input_param"+ID,
                                                                title = Title, 
                                                                abstract = Abstract,
                                                                default=Default,
                                                                minOccurs=MinOccurs,
                                                                type = type("")) 


  #=============================================================================
  #=============================================================================


  def addInputCombo(self,ID,Title,Abstract=None,Values=[],Default=None,MinOccurs=0):
    """ Adds a combobox input field
    
    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    :param Values : allowed values for the field
    :param Abstract : defauklt value for the field    
    """

    self.IOFields["input"]["scroll"][ID] = self.addLiteralInput(identifier="L_input_scroll"+ID,
                                                                  title = Title, 
                                                                  abstract = Abstract,
                                                                  type = type(""),
                                                                  allowedValues=Values,
                                                                  minOccurs=MinOccurs,
                                                                  default=Default) 


  #=============================================================================
  #=============================================================================


  def addInputCheckbox(self,ID,Title,Abstract=None,Default=False,MinOccurs=0):
    """ Adds a checkbox input field

    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    """

    self.IOFields["input"]["checkbox"][ID] = self.addLiteralInput(identifier="L_input_checkbox"+ID,
                                                                   title = Title, 
                                                                   abstract = Abstract,
                                                                   default=Default,
                                                                   minOccurs=MinOccurs,
                                                                   type = type("")) 


  #=============================================================================
  #=============================================================================


  def addInputWFS(self,ID,Title,Abstract=None,Default=None,MinOccurs=0):
    """ Adds a WFS input field
    
    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    """
    
    self.IOFields["input"]["wfs"][ID] = self.addLiteralInput(identifier="L_input_wfs"+ID,
                                                              title = Title, 
                                                              abstract = Abstract,
                                                              default=Default,
                                                              minOccurs = MinOccurs,
                                                              type = type(""))
                                                              
  #=============================================================================
  #=============================================================================


  def addInputWCS(self,ID,Title,Abstract=None,Default=None,MinOccurs=0):
    """ Adds a WCS input field
    
    :param ID : the ID of the field
    :param Title : the title of the field
    :param Abstract : the optional abstract associated with the field
    """
    
    self.IOFields["input"]["wcs"][ID] = self.addLiteralInput(identifier="L_input_wcs"+ID,
                                                              title = Title, 
                                                              abstract = Abstract,
                                                              default=Default,
                                                              minOccurs = MinOccurs,
                                                              type = type(""))

  #=============================================================================================================================
  # AddOutputs
  #=============================================================================================================================


  def addOutputText(self,ID,Title,Abstract=None):
    """ Adds a text output data
    
    :param ID : the ID of the data
    :param Title : the title of the data
    :param Abstract : the optional abstract associated with the data
    """

    self.IOFields["output"]["param"][ID] = self.addLiteralOutput(identifier="L_output_param"+ID,
                                                                 title = Title, 
                                                                abstract = Abstract,
                                                                type = type("")) 

  #=============================================================================
  #=============================================================================


  def addOutputWMS(self,ID,Title,Abstract=None):
    """ Adds a WMS output data

    :param ID : the ID of the data
    :param Title : the title of the data
    :param Abstract : the optional abstract associated with the data
    """

    self.IOFields["output"]["wms"][ID] = self.addLiteralOutput(identifier="L_output_wms"+ID,
                                                                title = Title, 
                                                                abstract = Abstract,
                                                                type = type(""))








  #=============================================================================================================================
  # SetOutputs
  #=============================================================================================================================


  def setOutputTextValue(self,ID,Val):
    """ Sets the value for a text output data

    :param ID : the ID of the data
    :param Val : the value of the data
    """

    self.IOFields["output"]["param"][ID].setValue(Val)


  #=============================================================================
  #=============================================================================


  def setOutputWMSValue(self,ID,Val):
    """ Sets the value for a WMS output data

    :param ID : the ID of the data
    :param Val : the value of the data
    """
    self.IOFields["output"]["wms"][ID].setValue(Val)

