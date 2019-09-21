from PyQt4.QtGui import QWidget, QDialog, QStandardItem, QStandardItemModel,\
    QVBoxLayout, QHBoxLayout



from PyQt4 import QtGui
from globalvalues.appsettings import AppSettings

from PyQt4.QtCore import pyqtSlot
#from statics.templates.wellplottype import WellPlotTemplate
from gui.wellplot.wellplotdialog.wellplotpg import WellPlotPG
from views.core.centraltabwidget import CentralTabWidget
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from statics.templates.wellplottype import WellPlotType
from db.core.basedao import BaseDao

import logging

from gui.wellplot.setup.ui_wellplotsetupdialog import Ui_WellPlotSetupDialog
from gui.wellplot.setup.wellselectionwidget import WellSelectionWidget
from gui.signals.wellplotsignals import WellPlotSignals
from db.core.well.well import Well
from gui.wellplot.setup.quickplotdialog import QuickPlotDialog
from db.windows.wellplot.wellplotdata.wellplotdatadao import WellPlotDataDao
from db.core.log.logdao import LogDao
from gui.wellplot.settings.templatesettingsdialog import TemplateSettingsDialog

logger = logging.getLogger('console')

class WellPlotSetupDialog(QDialog, Ui_WellPlotSetupDialog):
    DEFAULT_WELL_PLOT_PREFIX = "Well plot"
    DEFAULT_TEMPLATE_PREFIX = "Template"
    
    def __init__(self, logs = None, well = None, logSet = None, parent=None):
        logger.debug(">>__init__() ")
        #QWidget.__init__(self, parent)
        super(WellPlotSetupDialog, self).__init__(parent)
        self._logs = logs
        self._well = well
        self._logSet = logSet
        self._dataListToListWidget = None
        self._template = None
        self._wellPlotData = None
        self.wellSelectionWidget = None
        self.wellSelectionEvent = None
        self.existingWellPlotCount = None
        self.wellPlotSignals = WellPlotSignals()
        self.setupUi(self)
        self.setupWellFunctionality()
        self.connectWellSelectionSlot()

    def setupWellFunctionality(self):
        hbox = QHBoxLayout()
        self.wellHolderWidget.setLayout(hbox)
        self.wellSelectionWidget = WellSelectionWidget(self._well)
        hbox.addWidget(self.wellSelectionWidget)
        if self._well is None:
            self.plotSelectionWidget.setEnabled(False)
        else:
           self.setupTemplateFunctionality() 
            
    @pyqtSlot(Well) 
    def wellSelected(self, well):
        logger.debug(">> wellSelected() "+well.name)
        if well is not None:
            self._well = well
            self._logs = LogDao.getWellLogs(well.id)
            #now that well is selected, disable user selection of 'Unknown'
            self.wellSelectionWidget.populateWellsCombo(includeUnknown = False)
            self.setupTemplateFunctionality()
        
    def setupTemplateFunctionality(self):
        #self.setQuickPlotWidget()
        self.plotSelectionWidget.setEnabled(True)
        self.setTitle()
        self.setInitialState()
        self.populateQuickPlotCombo()
        self.populateWellPlotCombo()
        self.populateTemplatesCombo()
        self.connectSlots()
        
    def setInitialState(self):
        self.group = QtGui.QButtonGroup()
        self.group.addButton(self.quickPlotRadioButton)
        self.group.addButton(self.selectWellPlotRadioButton)
        self.group.addButton(self.createWellPlotRadioButton)
        self.group.addButton(self.selectTemplateRadioButton)
        self.group.addButton(self.createNewTemplateRadioButton)      
        self.quickPlotRadioButton.setChecked(True)
        self.selectQuickPlotClicked()
        self.existingWellPlots = self.setWellPlotLineEditText()
        if len(self.existingWellPlots) == 0:
            self.selectWellPlotRadioButton.setEnabled(False)
            self.selectWellPlotComboBox.setEnabled(False)
        self.setTemplateLineEditText()
        

    def setTitle(self):
        if self._logSet is not None and self._well is not None:
            #RMB on log set in tree->wellPlot
            self.setWindowTitle("Well plot setup: {0}".format(self._logSet.name))
        elif self._well is not None:
            #RMB on well in tree->wellPlot
            self.setWindowTitle("Well plot setup: {0}".format(self._well.name))
            
    def checkForActiveLogs(self, logs):
        '''Return True if have any active logs in list '''
        if logs is not None:
            for log in logs:
                if log.active:
                    return True
        return False
        
    def populateQuickPlotCombo(self):
        #check if have any active logs
        haveActiveLogs = self.checkForActiveLogs(self._logs)
        self.quickPlotComboBox.clear()
        isModifiable = False
        unModifiableTemplates = WellPlotTemplateDao.getWellPlotTemplatesFilterModifiable(isModifiable)
        unModifiableTemplates.sort(key=lambda x: x.name)

        for template in unModifiableTemplates:
            if template.name == WellPlotType.ACTIVELOGS.name:
                #only add active template name if have active logs
                if haveActiveLogs:
                    self.quickPlotComboBox.addItem(template.name, template.uid)
            else:
                self.quickPlotComboBox.addItem(template.name, template.uid)
            
    def populateWellPlotCombo(self):
        if (self.existingWellPlotCount is not None) and (self.existingWellPlotCount > 0):
            self.selectWellPlotComboBox.clear()
            self.existingWellPlots.sort(key=lambda x: x.uid)
    
            for wellPLot in self.existingWellPlots:
                self.quickPlotComboBox.addItem(wellPLot.uid, wellPLot.id)

    def populateTemplatesCombo(self):
        self.templatesComboBox.clear()
        isModifiable = True
        modifiableTemplates = WellPlotTemplateDao.getWellPlotTemplatesFilterModifiable(isModifiable)
        modifiableTemplates.sort(key=lambda x: x.name)
        isModifiable = False
        
        for template in modifiableTemplates:
            self.templatesComboBox.addItem(template.name, template.uid)
            
    def setWellPlotLineEditText(self):
        existingWellPlots = WellPlotDataDao.getAllDynamicWellPlots()
        items = len(existingWellPlots)
        self.createNewWellPlotLineEdit.setText(self.DEFAULT_WELL_PLOT_PREFIX+" "+str(items+1))
        return existingWellPlots
        
    def setTemplateLineEditText(self):
        isModifiable = True
        templates = WellPlotTemplateDao.getWellPlotTemplatesFilterModifiable(isModifiable)
        self.newTemplateNameLineEdit.setText(self.DEFAULT_TEMPLATE_PREFIX+" "+str(len(templates)+1))
        
    def selectQuickPlotClicked(self):
        logger.debug("selectQuickPlotClicked")
        self.quickPlotComboBox.setEnabled(True)
        self.newTemplateNameLineEdit.setEnabled(False)
        self.templatesComboBox.setEnabled(False)
        self.createNewWellPlotLineEdit.setEnabled(False)
        self.selectWellPlotComboBox.setEnabled(False)

    def quickPlotComboIndexChanged(self):
        index = self.quickPlotComboBox.currentIndex() 
        data = str(self.quickPlotComboBox.itemData(index))
        quickPlotUid = WellPlotType.QUICKPLOT.uid
        if quickPlotUid == data:
            logger.debug("Quick plot selected")
        if data is None or len(data) == 0:
            logger.debug("No data set for {0}".format(self.templatesComboBox.currentText()))

    def selectWellPlotClicked(self):
        logger.debug(">>selectWellPlotClicked")
        self.quickPlotComboBox.setEnabled(False)
        self.selectWellPlotComboBox.setEnabled(True)
        self.createNewWellPlotLineEdit.setEnabled(False)
        self.newTemplateNameLineEdit.setEnabled(False)
        self.templatesComboBox.setEnabled(False)
        
    def wellPlotComboIndexChanged(self):
        logger.debug(">>wellPlotComboIndexChanged")
        #index = self.selectWellPlotComboBox.currentIndex() 
        #data = str(self.selectWellPlotComboBox.itemData(index))
        pass
        
    def createNewWellPlotClicked(self):
        logger.debug(">>createNewWellPlotClicked")
        self.quickPlotComboBox.setEnabled(False)
        self.createNewWellPlotLineEdit.setEnabled(True)
        self.selectWellPlotComboBox.setEnabled(False)
        self.templatesComboBox.setEnabled(False)
        
    def selectTemplateClicked(self):
        logger.debug(">>selectTemplateClicked")
        self.templatesComboBox.setEnabled(True)
        self.newTemplateNameLineEdit.setEnabled(False)
        self.quickPlotComboBox.setEnabled(False)
        self.createNewWellPlotLineEdit.setEnabled(False)
        self.selectWellPlotComboBox.setEnabled(False)
        
    def createNewTemplateClicked(self):
        logger.debug("createNewTemplateClicked")
        self.newTemplateNameLineEdit.setEnabled(True)
        self.templatesComboBox.setEnabled(False)
        self.quickPlotComboBox.setEnabled(False)
        self.createNewWellPlotLineEdit.setEnabled(False)
        self.selectWellPlotComboBox.setEnabled(False)

    def openCreateTemplateDialog(self):
        logger.debug(">>openCreateTemplateDialog")
        
    def connectWellSelectionSlot(self):
        self.wellPlotSignals.wellSelectionChanged.connect(self.wellSelected)
            
    def connectSlots(self):
        logger.debug(">>connectSlots()")
        self.quickPlotRadioButton.clicked.connect(self.selectQuickPlotClicked)
        self.quickPlotComboBox.currentIndexChanged.connect(self.quickPlotComboIndexChanged)
        
        self.selectWellPlotRadioButton.clicked.connect(self.selectWellPlotClicked)
        self.selectWellPlotComboBox.currentIndexChanged.connect(self.wellPlotComboIndexChanged)
        self.createWellPlotRadioButton.clicked.connect(self.createNewWellPlotClicked)
        
        self.selectTemplateRadioButton.clicked.connect(self.selectTemplateClicked)
        self.createNewTemplateRadioButton.clicked.connect(self.createNewTemplateClicked)
        
    def handleWellPlotSelection(self):
        wellPlotName = str(self.selectWellPlotComboBox.currentText())
        index = self.selectWellPlotComboBox.currentIndex() 
        data = self.selectWellPlotComboBox.itemData(index)
        self._wellPlotData = WellPlotDataDao.getWellPlotDatasFromId(str(data))  
        
    def handleTemplateSelection(self):
        templateName = str(self.templatesComboBox.currentText())
        index = self.templatesComboBox.currentIndex() 
        data = self.templatesComboBox.itemData(index)
        self._template = WellPlotTemplateDao.getWellPlotTemplateFromUid(str(data))
        
    def handleQuickPlotSelection(self):
        quickTemplateName = str(self.quickPlotComboBox.currentText())
        #currentItem = self.getComboBoxItemFromIndex(self.trackListView.model(), self.templatesComboBox.currentIndex())
        #push logTypes into QuickPlot template
        index = self.quickPlotComboBox.currentIndex() 
        data = self.quickPlotComboBox.itemData(index)
        if quickTemplateName == WellPlotType.QUICKPLOT.name:
            quickplotDialog = QuickPlotDialog(self._logs, self._well, quickTemplateName)
            self.setVisible(False)
            quickplotDialog.exec_()
            self.close()
        elif (quickTemplateName == WellPlotType.ALLLOGS.name) or (quickTemplateName == WellPlotType.ACTIVELOGS.name) or (quickTemplateName == WellPlotType.EMPTY.name):
            self._template = WellPlotTemplateDao.getWellPlotTemplateFromUid(str(data))
        else:
            logger.error("Plot type not found")
            if AppSettings.isDebugMode:
                raise ValueError

    def accept(self):
        logger.debug(">>accept()")
        template = None
        if self.quickPlotRadioButton.isChecked():
            self.handleQuickPlotSelection()
            self.openWellPlotAndClose()
        elif self.selectWellPlotRadioButton.isChecked():
            self.handleWellPlotSelection()          
            self.openWellPlotAndClose()
        elif self.createWellPlotRadioButton.isChecked():
            self.setVisible(False)
            self.openWellPlot()
            templateSettingsDialog = TemplateSettingsDialog(self._wellPlotData, self._well)
            #open as modeless see http://stackoverflow.com/questions/11920401/pyqt-accesing-main-windows-data-from-a-dialog
            templateSettingsDialog.show()
            self.close()
        elif self.selectTemplateRadioButton.isChecked():
            self.handleTemplateSelection()
        elif self.createNewTemplateRadioButton.isChecked():
            logger.debug("TODO open template settings dialog")
            self._template = self.openCreateTemplateDialog(self.newTemplateNameLineEdit.text())


    def openWellPlotAndClose(self):
        self.setVisible(False)
        self.openWellPlot()
        self.close()

    def openWellPlot(self):
        #need to connect WellPlotMPL to main application so can receive signals
        centralTabWidget = CentralTabWidget()
        wellPlotPyQtGraph = WellPlotPG(logs= self._logs, well = self._well, template = self._template, wellPlotData = self._wellPlotData, logSet = self._logSet, parent = centralTabWidget)
    
    #def reject(self):
    #   logger.debug("reject")
        
    #TODO do we need to test for any reason why can't exit?
    def canExit(self):
        logger.debug("canExit")
        return True
        
    def closeEvent(self, event):
        # do stuff
        if self.canExit():
            event.accept() # let the window close
        else:
            event.ignore()