from PyQt4.QtGui import QWidget, QButtonGroup


import logging
from gui.wellplot.settings.layout.widgets.ui_overviewlayoutwidget import Ui_OverviewLayoutWidget
from enum import Enum
from gui.wellplot.settings.layout.widgets.overviewlayouthandler import OverviewLayoutHandler
from db.core.log.log import Log
from statics.types.logtype import LogType
from db.core.wavelet.wavelet import Wavelet
from globalvalues.appsettings import AppSettings
from db.core.log.logdao import LogDao
from PyQt4 import QtCore
from globalvalues.constants.wellplotconstants import WellPlotConstants


logger = logging.getLogger('console')


class OverviewLayoutWidget(QWidget, Ui_OverviewLayoutWidget):
    '''
    OverviewLayoutWidget for well plot settings
    '''

    
    def __init__(self, wellPlotData, parent=None):
        super(OverviewLayoutWidget, self).__init__(parent)
        self._wellPlotData = wellPlotData
        #store this, when apply cliked and isDirty, get and plot
        self.hasGRLog = False
        self.dataToPlot = None
        self.dataTypeToPlot = None
        self.isDirty = False
        self.setupUi(self)
        self.createButtonGroup()
        self.setWidgetProperties()
        
        self.connectSlots()
        
    def createButtonGroup(self):
        buttonGroup = QButtonGroup()
        buttonGroup.addButton(self.grRadioButton)
        buttonGroup.addButton(self.longestLogRadioButton)
        buttonGroup.addButton(self.specifyDataRadioButton)

    def setWidgetProperties(self):
        if self._wellPlotData is not None:

            overviewLayoutHandler = OverviewLayoutHandler()
            self.hasGRLog = overviewLayoutHandler.checkHasGR(self._wellPlotData)
            selection = self._wellPlotData.overview_layout_selection
            if WellPlotConstants.OVERVIEW_LONGEST_GR_LOG == selection:
                if self.hasGRLog:
                    self.grRadioButton.setChecked(True)
                    self.grRadioButtonClicked(setUp = True)
                    self.grRadioButton.setEnabled(True)
                else:
                    self.grRadioButton.setChecked(False)
                    self.logRadioButtonClicked(setUp = True)
                    self.grRadioButton.setEnabled(False)
                    self.longestLogRadioButton.setChecked(True)
            elif WellPlotConstants.OVERVIEW_LONGEST_LOG == selection:
                self.longestLogRadioButton.setChecked(True)
            else:
                self.specifyDataRadioButton.setChecked(True)
                self.setDataComboSelection()
            
    def setDataComboSelection(self):
        '''Sets initial combo selection if manual when load page'''
        index = self.dataClassComboBox.findText(self._wellPlotData.overview_layout_data_class, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.dataClassComboBox.setCurrentIndex(index)
            
        log = LogDao.getLog(self._wellPlotData.overview_layout_log_id)
        logType = log.log_type_name
        index = self.dataComboBox.findData(log.id, QtCore.Qt.UserRole)
        if index >= 0:
            self.dataComboBox.setCurrentIndex(index)
            
        index = self.typeComboBox.findText(logType.name, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.typeComboBox.setCurrentIndex(index)
            
    
    
    def populateCombos(self):
        try: 
            self.dataClassComboBox.currentIndexChanged.disconnect(self.populateDataTypeCombo)
            self.typeComboBox.currentIndexChanged.disconnect(self.populateDataCombo)
        except TypeError as ex:
            # will be disconnected on first run, log it and continue
            logger.debug(str(ex))
        self.populateClassCombo()
        
        self.populateDataCombo()
        self.populateDataTypeCombo()
        
        self.dataClassComboBox.currentIndexChanged.connect(self.populateDataTypeCombo)
        self.typeComboBox.currentIndexChanged.connect(self.populateDataCombo)
    
    def populateClassCombo(self):
        '''At moment only log classes are allowed, later add Wavelet, Seismic trace, Seismic stack'''
        log = Log()
        self.dataClassComboBox.addItem(log.qr_classname)
        #reset data types
        self.populateDataTypeCombo()
        
        
    def populateDataTypeCombo(self):
        log = Log()
        typeList = []
        if log.qr_classname == self.dataClassComboBox.currentText():
            logTypeList = LogDao.getLogTypeNamesInWell(self._wellPlotData.well.id)
            self.typeComboBox.clear()
            self.typeComboBox.addItems(logTypeList)
        else:
            self.typeComboBox.clear()
            logger.error("Error in text value")
            if AppSettings.isDebugMode:
                raise ValueError
        #reset data combo
        
    def populateDataCombo(self):
        log = Log()
        if log.qr_classname == self.dataClassComboBox.currentText():
            logTypeName = self.typeComboBox.currentText()
            logs = LogDao.getLogTypeLogs(self._wellPlotData.well.id, logTypeName)
            self.dataComboBox.clear()
            #add id as data
            for log in logs:
                self.dataComboBox.addItem(log.name, userData = log.id)
        else:
            self.dataComboBox.clear()
            
    def dataComboChanged(self):
        index = self.dataComboBox.currentIndex() 
        self.dataToPlot = self.dataComboBox.currentText()
        self.dataTypeToPlot = self.dataClassComboBox.currentText()
        self.isDirty = True
            
    def clearCombos(self):
        self.dataClassComboBox.clear()
        self.typeComboBox.clear()
        self.dataComboBox.clear()
          
    def grRadioButtonClicked(self, setUp = None):
        logger.debug(">>grRadioButtonClicked")
        overviewLayoutHandler = OverviewLayoutHandler()
        self.dataToPlot = overviewLayoutHandler.findLongestGRLog(self._wellPlotData.well)
        if self.dataToPlot is not None:
            self.selectDataWidget.setEnabled(False)
            self.lineEditLongestGRLog.setText(self.dataToPlot.name)
            self.lineEditLongestLog.setText('')
            log = Log()
            self.dataTypeToPlot = log.qr_classname
            #dont set dirty if setting up page
            if setUp is None:
                self.isDirty = True
        
    def logRadioButtonClicked(self, setUp = None):
        logger.debug(">>logRadioButtonClicked")
        overviewLayoutHandler = OverviewLayoutHandler()
        self.dataToPlot = overviewLayoutHandler.findLongestLog(self._wellPlotData.well)
        if self.dataToPlot is not None:
            self.selectDataWidget.setEnabled(False)
            self.lineEditLongestLog.setText(self.dataToPlot.name)
            self.lineEditLongestGRLog.setText('')
            log = Log()
            self.dataTypeToPlot = log.qr_classname
            if setUp is None:
                self.isDirty = True
        
    def specifyDataRadioButtonClicked(self):
        logger.debug(">>specifyDataRadioButtonClicked")
        self.selectDataWidget.setEnabled(True)
        self.populateCombos()
    
    def connectSlots(self):
        self.grRadioButton.clicked.connect(self.grRadioButtonClicked)
        self.longestLogRadioButton.clicked.connect(self.logRadioButtonClicked)
        self.specifyDataRadioButton.clicked.connect(self.specifyDataRadioButtonClicked)
        self.dataClassComboBox.currentIndexChanged.connect(self.populateDataTypeCombo)
        self.typeComboBox.currentIndexChanged.connect(self.populateDataCombo)
        self.dataComboBox.currentIndexChanged.connect(self.dataComboChanged)
