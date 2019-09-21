from __future__ import unicode_literals

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QComboBox, QDialog,  QTableWidgetItem, QTableWidget, QWizard)
#import lasio.pylasdev.las_reader
import logging
import sqlite3

import totaldepth.PlotLogs
import inout.las.reader.ui.logtablemodel as logtablemodel

from db.databasemanager import DM
from db.core.well.well import Well
from inout.las.reader.lasreader import LasReader
from inout.las.reader.ui.notepad import Notepad
from statics.types.logtype import LogType
from statics.types.logunitstype import LogUnitsType
from inout.las.reader.ui.wizard.ui_importlaswizard import Ui_Wizard
from inout.las.reader.ui.wizard.importlaswizardpage import ImportLasWizardPage
from inout.las.reader.ui.wizard.welllaswizardpage import WellLasWizardPage
from inout.las.reader.ui.wizard.logservicewizardpage import LogServiceWizardPage
from inout.las.reader.ui.wizard.parameterlaswizardpage import ParameterLasWizardPage
from inout.las.reader.orm.laspersister import LasPersister


logger = logging.getLogger('console')

class ImportLasWizard(QWizard, Ui_Wizard):
    '''Wizard for importing logs from .las file'''
    _wellExistsInDB = bool()
    
    def __init__(self, fileName, parent=None):
        logger.debug("__init__() "+str(fileName))
        super(ImportLasWizard, self).__init__(parent)
        self.setObjectName("importLasWizard")
        #default wizard anyway
        #self.setupUi(self)
        #holder for radio button selection state -instead of registerField
        self._importAllData = False
        self._wellExistsInDB = False
        #if error saving an object quit wizard 
        self._errorOnSave = False
        self._reader = LasReader()
        self._fileName = fileName
        self._session = DM.getSession()
        self.checkIfWellExistsInDB()
        self.setWindowTitle("Import .las data wizard")
        self.resize(640,480)
        
        #slot handling the next button, but disconnect the default slot first
        #see http://stackoverflow.com/questions/11155494/handling-cancellation-on-a-wizard-page
        #self.disconnect(self.button(QWizard.NextButton), QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('next()'))
        

        
        if fileName is not None:
            #plotter=totaldepth.PlotLogs
            #plotter.mockPlot()
            self.readFile()
            #las_info = lasio.pylasdev.las_reader.read_las_file(str(fileName))
            if len(self._reader.logList) == 0: 
                self.NextButton.setEnabled(False)
                self.BackButton.setEnabled(False)
                logger.info("Cannot populate dialog, log list is empty")
            else:
                self.addPage(ImportLasWizardPage(self._reader.logList, self))
                self.addPage(WellLasWizardPage(self._reader.well, self))
                self.addPage(LogServiceWizardPage(self._reader, self))
                self.addPage(ParameterLasWizardPage(self._reader, self))      
        else:
            logger.info("Cannot populate dialog, filename is empty")
        
        self.connectSlots()
            
    def readFile(self):
        logger.debug(">>readFile()")
        #start main ui progress bar to busy
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        ok = self._reader.readJobPart1(self._fileName)
        ok = self._reader.readJobPart2()
        ok = self._reader.readJobPart3()
        QtGui.QApplication.restoreOverrideCursor()
        #set main ui progress bar to finished then zero
        #test
        #logList = self._reader.logList
        #for log in logList:
        #    logger.debug("--readFile(): "+str(log.name)+" "+str(log.type_)+" "+str(log.unit)+" "+str(log.fileUnit))
        #logger.debug("--readFile(): "+str(self._fileName)+" well name: "+str(wellDTO.well_name))
        #end test
        
    def connectSlots(self):
        logger.debug(">>connectSlots()")
        self.button(QWizard.NextButton).clicked.connect(self.saveOnNext)
        self.button(QWizard.FinishButton).clicked.connect(self.finishClicked)
      
    def initializePage(self, i):
        logger.debug( "Initializing page..." + str(i) )
        
    def saveOnNext(self):
        logger.debug( ">>saveOnNext()")
        try:
            #currentId has already been incremented when here
            page = self.page(self.currentId()-1)
            logger.debug(str("--saveOnNext() name: "+page.objectName()))
            page.populateObject()
        except:
            logger.error( "Could not save page "+str(self.currentId()-1))
            self._errorOnSave = True

        
    def finishClicked(self):
        logger.debug(">>finishClicked()")
        #Save the finish page (Parameters atm)
        try:
            #Note that Id has not been incremented unlike Next
            page = self.page(self.currentId())
            logger.debug(str("--saveOnNext() name: "+page.objectName()))
            page.populateObject()
            #TODO start main ui progress bar to busy
            lasPersister = LasPersister(self._session)
            lasPersister.dispatchDataWriters(self._reader, True)
            if lasPersister.committedOK:
                #send signal for tree update
                 DM.databaseModified()
            
            self._session.close()
        except:
            logger.error( "Could not save page "+str(self.currentId()))
            self._errorOnSave = True
        finally:
            self._session.close()
            
    def checkIfWellExistsInDB(self):
        ''' Need a well object in database before can query against child tables '''
        try:
            rs = self._session.query(Well, Well.id).all()
            if rs:
                self._wellExistsInDB = True
        except sqlite3.OperationalError as e:
            logger.error(str(e))
        