from __future__ import unicode_literals

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import (Qt, SIGNAL)
from PyQt4.QtGui import (QComboBox, QDialog,  QTableWidgetItem, QTableWidget, QWizardPage, QMessageBox, QWidget)
#import lasio.pylasdev.las_reader
import logging
import totaldepth.PlotLogs
import inout.las.reader.ui.parametertablemodel as parametertablemodel

from db.core.parameterset.parameterset import ParameterSet
from inout.las.reader.ui.wizard.ui_parameterlaswizardpage import Ui_ParameterLasWizardPage
from inout.las.reader.lasreader import LasReader
from inout.las.reader.ui.notepad import Notepad
from statics.types.logtype import LogType
from statics.types.logunitstype import LogUnitsType
from globalvalues.constants.dataitemconstants import DataItemConstants
from db.core.parameter.parameter import Parameter


logger = logging.getLogger('console')

class ParameterLasWizardPage(QWizardPage, Ui_ParameterLasWizardPage):
    '''
    Parameter data wizard page, shows list of all parameter data that will be imported.
    '''

    def __init__(self, reader, parent=None):
        logger.debug(">>__init__() ")
        assert reader is not None
        super(ParameterLasWizardPage, self).__init__(parent)
        self._parent = parent
        self.setupUi(self)
        self._parameterSet = reader.parameterSet
        self._parameterList = reader.parameterList
        self.buildTableModel()
        self.populateTableWidget()
        self.setExistingParameterSetNames()
        self.connectSlots()
        self.setDefaultState()
        
    def buildTableModel(self):
        logger.debug(">>buildTableModel()")
        self._parameterTableModel = parametertablemodel.ParameterTableModel(self._parameterList)
            
    def populateTableWidget(self, selectedLog=None):
        logger.debug(">>populateTableWidget()")
        selected = None

        self.parametersTableWidget.clear()
        self.parametersTableWidget.setSortingEnabled(False)
        self.parametersTableWidget.setRowCount(len(self._parameterTableModel._parameters))
        self.parametersTableWidget.setColumnCount(len(self._parameterTableModel.HEADERS))
        self.parametersTableWidget.setHorizontalHeaderLabels(self._parameterTableModel.HEADERS)
        for row, parameter in enumerate(self._parameterTableModel._parameters):
            item = QTableWidgetItem(parameter.mnemonic)
            item.setData(Qt.UserRole, str(id(parameter)))
 
            self.parametersTableWidget.setItem(row, parametertablemodel.MNEMONIC, item)
            self.parametersTableWidget.setItem(row, parametertablemodel.VALUE,
                    QTableWidgetItem(parameter.value))
            self.parametersTableWidget.setItem(row, parametertablemodel.UNIT,
                    QTableWidgetItem(parameter.unit))
            self.parametersTableWidget.setItem(row, parametertablemodel.DESCRIPTION,
                    QTableWidgetItem(parameter.description))
        self.parametersTableWidget.setSortingEnabled(True)
        self.parametersTableWidget.resizeColumnsToContents()
        if selected is not None:
            selected.setSelected(True)
            self.parametersTableWidget.setCurrentItem(selected)
            
    def setValidators(self):
        pass
            
    def setExistingParameterSetNames(self):
        ''' Check existing Parameter set names in database and populate combobox '''
        if self._parent._wellExistsInDB:
            session = self._parent._session
            rs = session.query(ParameterSet, ParameterSet.name).all()
            for row in rs:
                self.existingParameterSetComboBox.addItem(row.name)
    
    def checkParameterSetName(self):
        logger.debug(">>checkParameterSetName()")
        if self._parent._wellExistsInDB:
            session = self._parent._session
            rs = session.query(ParameterSet, ParameterSet.name).all()
            for row in rs:
                if row.name == self.newParameterSetLineEdit.text():
                    logger.debug("Parameter set name exists")
                    self.newParameterSetLineEdit.setFocus()
                elif str(row.name).lower == str(self.newParameterSetLineEdit.text()).lower:
                    QMessageBox.warning(QWidget, 'Existing parameter set message', 'The parameter set name is similar to an existing set. It is recommended to import this data into the existing set: '+row.name, buttons=QMessageBox.Ok, defaultButton=QMessageBox.NoButton)
                    logger.warn('The parameter set name is similar to an existing set. It is recommended to import this data into the existing set: '+row.name)

    def connectSlots(self):
        logger.debug(">>connectSlots()")
        self.connect(self.newParameterSetLineEdit, SIGNAL("newParameterSetLineEdit_exited"),
                     self.checkParameterSetName)
        
    def setDefaultState(self):
        self.newParameterSetLineEdit.setText(DataItemConstants.DEFAULT_PARAMETERSET)
        self.setParameterSetRadioButtons()      
        if self._parent._importAllData:
            self.parametersTableWidget.setEnabled(True)
        else:
            self.parametersTableWidget.setEnabled(False)
            
    def setParameterSetRadioButtons(self):
        ''' runs prior to user entering any data '''
        if self._parent._wellExistsInDB:
            existingParameterSets = [self.existingParameterSetComboBox.itemText(i) for i in range(self.existingParameterSetComboBox.count())]
            if self.newParameterSetLineEdit.text() in existingParameterSets:
                index = self.existingParameterSetComboBox.findText(self.newParameterSetLineEdit.text())
                self.existingParameterSetComboBox.setCurrentIndex(index)
                self.newParameterSetRadioButton.setChecked(False)
                self.existingParameterSetRadioButton.setEnabled(True)
                self.existingParameterSetComboBox.setEnabled(True)
                self.existingParameterSetRadioButton.setChecked(True)
            else:
                #check if matches regardless of case and inform user
                existingParameterSetsLowerCase = [x.lower() for x in existingParameterSets]
                if str(self.newParameterSetLineEdit.text()).lower in existingParameterSetsLowerCase:
                    logger.warn("A parameter set with a similar name to: "+str(self.newParameterSetLineEdit.text())+" exists in the database")
        else:
                self.newParameterSetRadioButton.setChecked(True)
                self.existingParameterSetRadioButton.setChecked(False)
                self.existingParameterSetRadioButton.setEnabled(False)
                self.existingParameterSetComboBox.setEnabled(False)

    def populateObject(self):
        logger.debug(">>populateObject()")
        if self.newParameterSetRadioButton.isChecked():
            self._parameterSet.name = self.newParameterSetLineEdit.text()
            self._parameterSet.existing = False
        else:
            self._parameterSet.name = self.existingParameterSetComboBox.currentText()
            self._parameterSet.existing = True
        #Then just import all data already in object
        
class Filter(QtCore.QObject):
    #see http://stackoverflow.com/questions/15066913/how-to-connect-qlineedit-focusoutevent
    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QtCore.QEvent.FocusOut:
            self.emit(SIGNAL("newParameterSetLineEdit_exited"))
            # return False so that the widget will also handle the event
            # otherwise it won't focus out
            return False
        else:
            # we don't care about other events
            return False