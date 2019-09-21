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
from gui.wellplot.setup.wellplotsetupdialog import WellPlotSetupDialog
logger = logging.getLogger('console')

class WellSelectionDialog(QDialog, Ui_WellSelectionDialog):
    
    def __init__(self, parent=None):
        super(WellSelectionDialog, self).__init__(parent)
        self.setupUi(self)
        self.populateWellsCombo()
        self.well = None
        
    def populateWellsCombo(self):
        session = BaseDao.getSession()
        wells = WellDao.getAllWells(session)
        for well in wells:
            self.wellsComboBox.addItem(well.name, well)
        if len(wells)>0:
            self.wellsComboBox.setCurrentIndex(0)
            
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

