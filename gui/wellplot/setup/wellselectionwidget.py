from PyQt4.QtGui import QWidget, QDialog, QStandardItem, QStandardItemModel



from PyQt4 import QtGui, QtCore
from globalvalues.appsettings import AppSettings
from statics.types.logtype import LogType
from PyQt4.Qt import Qt
from preferences.general.generalsettings import GeneralSettings, WorkflowType
from PyQt4.QtCore import QModelIndex
#from statics.templates.wellplottype import WellPlotTemplate
from gui.wellplot.wellplotdialog.wellplotpg import WellPlotPG
from views.core.centraltabwidget import CentralTabWidget
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from statics.templates.wellplottype import WellPlotType
from db.core.basedao import BaseDao

import logging
from db.core.well.welldao import WellDao
from gui.wellplot.setup.ui_wellSelection import Ui_WellSelectionDialog
from db.core.well.well import Well
from db.core.log.logdao import LogDao

from gui.wellplot.setup.ui_wellselectionwidget import Ui_wellSelectionWidget
from gui.signals.wellplotsignals import WellPlotSignals
logger = logging.getLogger('console')

class WellSelectionWidget(QWidget, Ui_wellSelectionWidget):
    UNKNOWN = "Unknown"
    
    def __init__(self, well, parent=None):
        super(WellSelectionWidget, self).__init__(parent)
        self.setupUi(self)
        self.well = well
        #Keep track of whether is connected to slot or not so dont connect twice
        self._wellsComboIndexConnected = False
        self.wellPlotSignals = WellPlotSignals()
        if well is None:
            self.populateWellsCombo(includeUnknown = True)
            self.connectSlots()
        else:
            self.handleExistingWell()
         
    def populateWellsCombo(self, includeUnknown):
        try:
            self.wellsComboBox.currentIndexChanged.disconnect(self.wellsComboIndexChanged)
            self._wellsComboIndexConnected = False
        except TypeError as ex:
            # will be disconnected on first run, log it and continue 
            logger.debug(str(ex))
            
        self.wellsComboBox.clear()
        session = BaseDao.getSession()
        wells = WellDao.getAllWells(session)
        if includeUnknown:
            #Force user to select a well
            self.wellsComboBox.addItem(self.UNKNOWN)
        for well in wells:
            self.wellsComboBox.addItem(well.name, well)
        if len(wells)>0:
            self.wellsComboBox.setCurrentIndex(0)
         
        self.wellsComboBox.currentIndexChanged.connect(self.wellsComboIndexChanged)
        self._wellsComboIndexConnected = True
            
            
    def handleExistingWell(self):
        self.setEnabled(False)
        #change from 'select well' to 'well'
        self.selectWellLabel.setText("Well")
        self.wellsComboBox.addItem(self.well.name)
        
    def wellsComboIndexChanged(self):
        logger.debug(">>wellsComboIndexChanged()")
        ind = self.wellsComboBox.currentIndex()
        well = self.wellsComboBox.itemData(ind)
        wellName = self.wellsComboBox.currentText() 
        if wellName != self.UNKNOWN:
            logger.debug("--wellsComboIndexChanged() emitting signal "+wellName)
            self.wellPlotSignals.wellSelectionChanged.emit(well)
        
    def connectSlots(self):
        if not self._wellsComboIndexConnected:
            logger.debug("--connectSlots() connecting wellsComboIndexChanged")
            self.wellsComboBox.currentIndexChanged.connect(self.wellsComboIndexChanged)
            self._wellsComboIndexConnected = True
            
    '''
    def accept(self):
        logger.debug(">>accept()")
        index = self.wellsComboBox.currentIndex() 
        data = self.wellsComboBox.itemData(index)
        if data is not None:
            if isinstance(data, Well):
                logs = LogDao.getWellLogs(data.id)
                if logs != None:
                    wellPlotSetupDialog = WellPlotSetupDialog(logs, well = data, logSet = None)
                    wellPlotSetupDialog.exec_()
                    self.close()
            else:
                logger.debug("type(data):{0}".format(type(data)))
        else:
            logger.debug("Data is None")
    '''

