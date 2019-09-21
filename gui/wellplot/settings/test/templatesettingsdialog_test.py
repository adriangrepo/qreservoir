
from globalvalues.appsettings import AppSettings


from PyQt4.QtGui import QApplication


import unittest

from gui.wellplot.settings.templatesettingsdialog import TemplateSettingsDialog



#import logging
import logging.config

from db.test.dummydbsetup import DummyDbSetup

from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from statics.templates.wellplottype import WellPlotType
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess
from gui.wellplot.wellplotdialog.wellplotpg import WellPlotPG
import sys

logging.config.fileConfig(AppSettings.getLoggingConfig())
# create logger
logger = logging.getLogger('console')


class DummyCell(object):
    def __init__(self):
        self.checkState = False
    
    def checkState(self):
        return self.checkState

class DummyTableWidget(object):
    def __init__(self):
        # Create a list.
        self.elements = []
        self.createCells()
        
        
    def createCells(self):
        #see http://www.dotnetperls.com/2d-list-python
        # Append empty lists in first two indexes.
        self.elements.append([])
        self.elements.append([])
        # Add elements to empty lists.
        cell1 = DummyCell()
        cell2 = DummyCell()
        cell3 = DummyCell()
        cell4 = DummyCell()
        self.elements[0].append(cell1)
        self.elements[0].append(cell2)
        self.elements[1].append(cell3)
        self.elements[1].append(cell4)
    
    def item(self, row, column):
        return self.elements[row][column]
    
    def setItem(self, row, column, item):
        #not sure if this will work
        self.elements[row][column] = item

class TemplateSettingsDialogTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TemplateSettingsDialogTest, self).__init__(*args, **kwargs)
        #QWidget: Must construct a QApplication before a QPaintDevice
        #self.app = QApplication(sys.argv)
        self.dummyDbSetup = DummyDbSetup()

        
    def test_init(self):
        #test that all input logs are automatically checked in the table
        logger.debug("=================================================================")
        logger.debug(">>test_init() ")
        app = QApplication(sys.argv)
            
        well, logPlotData = self.generateLogPlotData()
            
        layoutDialog = TemplateSettingsDialog(logPlotData, well)
        self.assertEqual(WellPlotType.ALLLOGS.name, layoutDialog._itemWidget.nameLineEdit.text(), "Name is incorrect")  
        self.assertEqual(WellPlotType.ALLLOGS.typeName, layoutDialog._itemWidget.classLineEdit.text(), "Type name is incorrect")  
            
        
    def getCurrentlyPlottedLogs(self, logPlotData):
        plotLogs = []
        plotList = logPlotData.sub_plots
        for subPlotData in plotList:
            for log in subPlotData.getLogs():
                plotLogs.append(log)
        return plotLogs
        
    def generateLogPlotData(self):
        ''' using wellplot method to create data - preferred way 
        may want to put data creation outside wellplot?
        '''
        logger.debug(">>test_generateLogPlotData() ")
        self.dummyDbSetup.setupDatabase()
        #QWidget: Must construct a QApplication before a QPaintDevice
        #app = QApplication(sys.argv)
        well = self.dummyDbSetup.createWell()
        logs = self.dummyDbSetup.create3Logs(well.id)
        templateDao = WellPlotTemplateDao()
        allTemplates = templateDao.getAllWellPlotTemplates()
        template = None
        uid = 42
        for item in allTemplates:
            if item.uid == WellPlotType.ALLLOGS.uid:
                template = item
        wellPlot = WellPlotPG(logs, well, template)
        wellPlotModelAccess = WellPlotModelAccess()
        wellPlotData = wellPlotModelAccess.createWellPlotData(logs, uid, well, template)

        return well, wellPlotData
 

    

    
    '''
    def test_logData(self):
        logger.debug(">>test_logData() ")
        self.setupDatabase()
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)
        well = self.createWell()
        logs = self.createLogs(well.id)
        for log in logs:
            logger.debug("--test_logData() log name: {0} type: {1} id: {2}".format(log.name, log.log_type, log.id))
            units = LogDao.getUnits(log)
            logger.debug("--test_logData() units: {0} ".format(units))
        logger.debug("--------------------------------------")
    '''
    
    '''
    def createWellPlotData(self):
        logger.debug(">>createWellPlotData() ")
        logPlotData = WellPlotData()

        #well_id = Column(Integer, nullable = False)
        
        logPlotData.title = "Plot title"
        logPlotData.title_on = True
        logPlotData.widget_width = 2
        logPlotData.widget_height = 6
        logPlotData.dpi= 100
        logPlotData.hold = True
        logPlotData.y_label='MD'
        #logPlotData.y_limit = Column(String(), nullable = True)
        #logPlotData.y_data_string = Column(String(), nullable = True)
        logPlotData.y_scale='linear'
    
        #user can display multiple depth axes simultaneously
        #logPlotData.depth_axes_ids = Column(String(), nullable = True)
        logPlotData.display_depth_axes = True
        #logPlotData.log_ids = Column(String(), nullable = True)
            
        #store plots in a list
        #logPlotData.sub_plot_ids = Column(String(), nullable = True)
        #logPlotData.depth_sub_plot_ids = Column(String(), nullable = True)
        logPlotData.renderer = PlotRenderer.matplotlib.name
        
        logPlotData.plot_background_rgb = "0,0,0"
        logPlotData.plot_background_alpha = "255"
        logPlotData.label_background_rgb = "0,0,0"
        logPlotData.label_background_alpha = "255"
        logPlotData.label_foreground_rgb = "200,200,200"
        logPlotData.label_foreground_alpha = "255"
        
        #DUG type vs HRS type labels 
        logPlotData.expanded_header_labels = True
        
        logPlotData.grid_on = True
        logPlotData.grid_rgb = "200,200,200"
        logPlotData.grid_alpha = "255"
        logPlotData.grid_line_style = LineStyles.dashed.name
        logPlotData.grid_vertical_divisions = 10
        
        logPlotData.track_header_titles_on = True
    
        return logPlotData
    '''
        
if __name__ == '__main__':
    unittest.main()
    