from __future__ import unicode_literals

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import (Qt, SIGNAL)
from PyQt4.QtGui import (QComboBox, QDialog,  QTableWidgetItem, QTableWidget, QWizardPage, QWizard, QMessageBox, QWidget)

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
#import lasio.pylasdev.las_reader
import logging
import totaldepth.PlotLogs
import sqlite3
import inout.las.reader.ui.logtablemodel as logtablemodel

from db.core.logset.logset import LogSet
from db.databasemanager import Session
from inout.las.reader.ui.wizard.ui_logservicelaswizardpage import Ui_LogServiceLasWizardPage
from inout.las.reader.lasreader import LasReader
from inout.las.reader.ui.notepad import Notepad
from statics.types.logtype import LogType
from statics.types.logunitstype import LogUnitsType
from qrutilities.namingutils import NamingUtils
from globalvalues.constants.dataitemconstants import DataItemConstants
from globalvalues.constants.colorconstants import ColorConstants
from inout.validation.realvalidator import RealValidator
from qrutilities.numberutils import NumberUtils


logger = logging.getLogger('console')

class LogServiceWizardPage(QWizardPage, Ui_LogServiceLasWizardPage):
    '''
    Log service data wizard page, all data related to logging operations
    '''

    def __init__(self, reader, parent=None):
        logger.debug(">>__init__() ")
        super(LogServiceWizardPage, self).__init__(parent)
        self._parent = parent
        self.setupUi(self)
        self._logService = reader.logService
        self._logDomain = reader.logDomain
        self._logSet = reader.logSet
        self.setExistingLogSetNames()
        self.populateWidgets()
        self.populateComboBoxes()
        self.connectSlots()
        self.setValidators()
        self.attachNonRequiredCheckers()
        self.attachRequiredCheckers()
        self.setDefaultState()
        
        
    def populateWidgets(self):
        
        self.analysisByLineEdit.setText(self._logService.analysis_by)
        self.analysisLocationLineEdit.setText(self._logService.analysis_location)
        if self._logService.default_rw is None: 
            self.defaultRwLineEdit.setText("")
        else:
            self.defaultRwLineEdit.setText(str(self._logService.default_rw))

        if self._logService.default_rwt is None: 
            self.defaultRwtLineEdit.setText("")
        else:
            self.defaultRwtLineEdit.setText(str(self._logService.default_rwt))
        self.depthTypeLineEdit.setText(self._logDomain.z_measure_type_name)

        if self._logDomain.log_start is None: 
            self.logStartLineEdit.setText("")
        else:
            self.logStartLineEdit.setText(str(self._logDomain.log_start))
        if self._logDomain.log_step is None: 
            self.logStepLineEdit.setText("")
        else:
            (str(self._logDomain.log_step))
        if self._logDomain.log_stop is None: 
            self.logStopLineEdit.setText("")
        else:
            self.logStopLineEdit.setText(str(self._logDomain.log_stop))
        self.loggingReferenceLineEdit.setText(self._logService.z_measure_reference)
        if self._logService.null_value is None: 
            self.nullValueLineEdit.setText("")
        else:
            self.nullValueLineEdit.setText(str(self._logService.null_value))
        if self._logService.run_number is None: 
            self.runNumberLineEdit.setText("")
        else:
            self.runNumberLineEdit.setText(str(self._logService.run_number))
        self.serviceCompanyLineEdit.setText(self._logService.service_company)
        self.serviceDateLineEdit.setText(self._logService.service_date)
        if self._logService.td_logger is None: 
            self.tdLoggerLineEdit.setText("")
        else:
            self.tdLoggerLineEdit.setText(str(self._logService.td_logger))
        self.typeOfFluidInHoleLineEdit.setText(self._logService.type_of_fluid_in_hole)
        if self._logDomain.total_samples is None: 
            logger.error("total_samples is None")
        else:
            self.totalSamplesLineEdit.setText(str(self._logDomain.total_samples))
         
    def populateComboBoxes(self):
        resistivityUnits = LogType.getLogUnitsForType(LogType.RESIS)
        for item in resistivityUnits:
            self.defaultRwUnitComboBox.addItem(str(item))
            self.defaultRwtComboBox.addItem(str(item))
        #eg m, ft etc
        depthUnits = LogType.getLogUnitsForType(LogType.DEPTH)
        for item in depthUnits:
            self.logStartUnitComboBox.addItem(str(item))
            self.logStopUnitComboBox.addItem(str(item))
            self.logStepUnitComboBox.addItem(str(item))
            self.tdLoggerUnitComboBox.addItem(str(item))             
            
    def setValidators(self):
        doubleValidator = QtGui.QDoubleValidator()
        intValidator = QtGui.QIntValidator()
        regexValidator = QtGui.QRegExpValidator()
        realValidator = RealValidator()
        
        self.analysisByLineEdit.text()
        self.analysisLocationLineEdit.setValidator(regexValidator)
        self.defaultRwLineEdit.setValidator(realValidator)
        self.defaultRwtLineEdit.setValidator(realValidator)
        self.depthTypeLineEdit.setValidator(regexValidator)
        self.logStartLineEdit.setValidator(doubleValidator)
        self.logStepLineEdit.setValidator(doubleValidator)
        self.logStopLineEdit.setValidator(doubleValidator)
        self.loggingReferenceLineEdit.setValidator(realValidator)
        self.nullValueLineEdit.setValidator(realValidator)
        self.runNumberLineEdit.setValidator(intValidator)
        self.serviceCompanyLineEdit.setValidator(regexValidator)
        self.serviceDateLineEdit.setValidator(regexValidator)
        self.tdLoggerLineEdit.setValidator(realValidator)
        self.typeOfFluidInHoleLineEdit.setValidator(regexValidator)
        self.totalSamplesLineEdit.setValidator(intValidator)
        
    
    def checkNonReqiredState(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        #Note all lineedits will have a validator
        if validator is not None:
            state = validator.validate(sender.text(), 0)[0]
            s = sender.text()
            if state == QtGui.QValidator.Acceptable and sender.text() is not "":
                color = ColorConstants.QLE_GREEN
            elif state == QtGui.QValidator.Intermediate or sender.text() is "":
                color = ColorConstants.QLE_YELLOW
            else:
                color = ColorConstants.QLE_RED
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            logger.debug("--checkState() no validator for: "+str(sender.objectName()))
            
    def checkReqiredState(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        #Note all lineedits will have a validator
        if validator is not None:
            state = validator.validate(sender.text(), 0)[0]
            s = sender.text()
            if state == QtGui.QValidator.Acceptable and sender.text() is not "":
                color = ColorConstants.QLE_GREEN
            #elif state == QtGui.QValidator.Intermediate or sender.text() is "":
            #    color = '#fff79a' # yellow
            else:
                color = ColorConstants.QLE_RED
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            logger.debug("--checkState() no validator for: "+str(sender.objectName()))
    
            
    def attachNonRequiredCheckers(self):
        nonReqLineEdits = self.scrollArea.findChildren(QtGui.QLineEdit)
        for lineedit in nonReqLineEdits:
            lineedit.textChanged.connect(self.checkNonReqiredState)
            lineedit.textChanged.emit(lineedit.text())
            
    def attachRequiredCheckers(self):
        reqLineEdits = self.upperGroupBox.findChildren(QtGui.QLineEdit)
        for lineedit in reqLineEdits:
            lineedit.textChanged.connect(self.checkNonReqiredState)
            lineedit.textChanged.emit(lineedit.text())
    
    def setExistingLogSetNames(self):
        ''' Check existing LogSet names in database and populate combobox '''
        if self._parent._wellExistsInDB:
            session = self._parent._session
            try:
                rs = session.query(LogSet, LogSet.name).all()
                for row in rs:
                    self.existingLogSetComboBox.addItem(row.name)
            except sqlite3.OperationalError as e:
                logger.error(str(e))         
    
    def checkIfLogSetNameExists(self):
        logger.debug(">>checkIfLogSetNameExists()")
        if self._parent._wellExistsInDB:
            session = self._parent._session
            try:
                rs = session.query(LogSet, LogSet.name).all()
                for row in rs:
                    if row.name == self.newLogSetNameLineEdit.text():
                        logger.debug("Log set name exists")
                        self.newLogSetNameLineEdit.setFocus()
                    elif str(row.name).lower == str(self.wellNameLineEdit.text()).lower:
                        QMessageBox.warning(QWidget, 'Existing log set message', 'The log set name is similar to an existing log set name. It is recommended to import this data into the existing log set: '+row.name, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton)
                        logger.warn("The log set name is similar to an existing log set name. It is recommended to import this data into the existing log set: "+row.name)
            except sqlite3.OperationalError as e:
                logger.error(str(e))
    

                                                   
    def checkIfLogSetNameIsEmpty(self):
        if self.newLogSetRadioButton.isChecked():
            if len(self.newLogSetNameLineEdit.text()) == 0:
                logger.warn("A new log set name is required if not adding to an existing log set")
                self.wellNameLineEdit.setFocus()
                color = '#f6989d' # red
                self.newLogSetNameLineEdit.setStyleSheet('QLineEdit { background-color: %s }' % color)
                return True
                
    def setDefaultState(self):
        self.newLogSetNameLineEdit.setText(DataItemConstants.DEFAULT_LOGSET)
        self.setLogSetRadioButtons()      
        if self._parent._importAllData:
            self.scrollArea.setEnabled(True)
        else:
            self.scrollArea.setEnabled(False)
        
    def setLogSetRadioButtons(self):
        ''' runs prior to user entering any data '''
        if self._parent._wellExistsInDB:
            existingLogSets = [self.existingLogSetComboBox.itemText(i) for i in range(self.existingLogSetComboBox.count())]
            if self.newLogSetNameLineEdit.text() in existingLogSets:
                index = self.existingLogSetComboBox.findText(self.newLogSetNameLineEdit.text())
                self.existingLogSetComboBox.setCurrentIndex(index)
                self.newLogSetRadioButton.setChecked(False)
                self.existingLogSetRadioButton.setEnabled(True)
                self.existingLogSetComboBox.setEnabled(True)
                self.existingLogSetRadioButton.setChecked(True)
            else:
                #check if matches regardless of case and inform user
                existingLogSetsLowerCase = [x.lower() for x in existingLogSets]
                if str(self.newLogSetNameLineEdit.text()).lower in existingLogSetsLowerCase:
                    logger.warn("A log set with a similar name to: "+str(self.newLogSetNameLineEdit.text())+" exists in the database")
        else:
                self.newLogSetRadioButton.setChecked(True)
                self.existingLogSetRadioButton.setChecked(False)
                self.existingLogSetRadioButton.setEnabled(False)
                self.existingLogSetComboBox.setEnabled(False)
            
    def connectSlots(self):
            logger.debug(">>connectSlots()")
            self._filter = Filter()
            # adjust for your QLineEdit
            self.newLogSetNameLineEdit.installEventFilter(self._filter)
            self.connect(self.newLogSetNameLineEdit, SIGNAL("newLogSetNameLineEdit_exited"),
                         self.checkIfLogSetNameExists)  
            #self._parent.button(QWizard.NextButton).clicked.connect(self.nextButtonClicked) 
            #self.nextPushButton.clicked.connect(self.nextPushButtonClicked)
            

        
    #TODO Qmessage box?
    def nextButtonClicked(self):
        logger.debug(">>nextButtonClicked()")
        if self.newLogSetRadioButton.isChecked():
            if len(self.newLogSetNameLineEdit.text()) == 0:
                logger.warn("A new log set name is required if not adding to an existing set")
                self.newLogSetNameLineEdit.setFocus()
                color = '#f6989d' # red
                self.newLogSetNameLineEdit.setStyleSheet('QLineEdit { background-color: %s }' % color)
                
    def populateObject(self):
        logger.debug(">>populateObject()")
        if self.newLogSetRadioButton.isChecked():
            self._logSet.name = self.newLogSetNameLineEdit.text()
            self._logSet.existing = False
        else:
            self._logSet.name = self.existingLogSetComboBox.currentText()
            self._logSet.existing = True
        self._logService.analysis_by = self.analysisByLineEdit.text()
        self._logService.analysis_location = self.analysisLocationLineEdit.text()
        self._logService.default_rw = NumberUtils.parseStringToFloat(self.defaultRwLineEdit.text())
        self._logService.default_rwt = NumberUtils.parseStringToFloat(self.defaultRwtLineEdit.text())
        self._logService.z_measure_reference = self.loggingReferenceLineEdit.text()
        self._logService.null_value = NumberUtils.parseStringToFloat(self.nullValueLineEdit.text())
        self._logService.run_number = NumberUtils.stringToInt(self.runNumberLineEdit.text())
        self._logService.service_company = self.serviceCompanyLineEdit.text()
        self._logService.service_date = self.serviceDateLineEdit.text()
        self._logService.td_logger = NumberUtils.parseStringToFloat(self.tdLoggerLineEdit.text())
        self._logService.type_of_fluid_in_hole = self.typeOfFluidInHoleLineEdit.text()
        
        
        self._logDomain.log_start = NumberUtils.parseStringToFloat(self.logStartLineEdit.text())
        self._logDomain.log_step = NumberUtils.parseStringToFloat(self.logStepLineEdit.text())
        self._logDomain.log_stop = NumberUtils.parseStringToFloat(self.logStopLineEdit.text())
        self._logDomain.total_samples = NumberUtils.stringToInt(self.totalSamplesLineEdit.text())
        
        #TODO comboboxes
        ################## DUMMY DATA ##################################
        self._logDomain.z_measure_type_name = "MD"
        
        self._logService.z_measure_domain = "MD"

        
class Filter(QtCore.QObject):
    #see http://stackoverflow.com/questions/15066913/how-to-connect-qlineedit-focusoutevent
    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QtCore.QEvent.FocusOut:
            self.emit(SIGNAL("newLogSetNameLineEdit_exited"))
            logger.debug("--eventFilter() newLogSetNameLineEdit_exited")
            return False
        else:
            # we don't care about other events
            return False
        