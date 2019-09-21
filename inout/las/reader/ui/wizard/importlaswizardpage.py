from __future__ import unicode_literals

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QComboBox, QDialog,  QTableWidgetItem, QTableWidget, QWizardPage)
#import lasio.pylasdev.las_reader
import logging
import totaldepth.PlotLogs
import inout.las.reader.ui.logtablemodel as logtablemodel

from inout.las.reader.ui.wizard.ui_importlaswizardpage import Ui_ImportLasWizardPage
from inout.las.reader.lasreader import LasReader
from inout.las.reader.ui.notepad import Notepad
from statics.types.logtype import LogType
from statics.types.logunitstype import LogUnitsType


logger = logging.getLogger('console')

class ImportLasWizardPage(QWizardPage, Ui_ImportLasWizardPage):
    #Dialog for setting which logs to import from .las file

    def __init__(self, logList, parent=None):
        logger.debug(">>__init__() ")
        assert logList is not None
        super(ImportLasWizardPage, self).__init__(parent)
        self.setupUi(self)
        self._logList = logList
        self._logTableModel = None
        self._parent = parent
        self.buildTableModel()
        self.populateTableWidget()
        self.connectSlots()
        #default state
        self.selectalldefinedRadioButton.setChecked(True)
        self.selectAllDefinedClicked()

    def buildTableModel(self):
        logger.debug(">>buildTableModel()")
        self._logTableModel = logtablemodel.LogTableModel(self._logList)
        logger.debug("<<buildTableModel()")
        
    def populateTableWidget(self, selectedLog=None):
        logger.debug(">>populateTableWidget()")
        selected = None
        self.logsTableWidget.clear()
        self.logsTableWidget.setSortingEnabled(False)
        self.logsTableWidget.setRowCount(len(self._logTableModel.logs))
        self.logsTableWidget.setColumnCount(len(self._logTableModel.HEADERS))
        self.logsTableWidget.setHorizontalHeaderLabels(self._logTableModel.HEADERS)
        for row, log in enumerate(self._logTableModel.logs):
            item = QTableWidgetItem(log.name)
            item.setData(Qt.UserRole, str(id(log)))
            localLogType = LogType.findLogTypeFromMnemonic(log.fileMnemonic)
            if selectedLog is not None and selectedLog == id(log):
                selected = item
            chkBoxItem = QtGui.QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            #is this needed?
            chkBoxItem.setData(Qt.UserRole, str(id(log)))
            
            self.logsTableWidget.setItem(row, logtablemodel.IMPORT, chkBoxItem)   
            self.logsTableWidget.setItem(row, logtablemodel.NAME, item)
            self.logsTableWidget.setCellWidget(row, logtablemodel.TYPE,
                    self.getPreparedTypesCombo(log.fileMnemonic))          
            self.logsTableWidget.setCellWidget(row, logtablemodel.UNIT,
                    self.populateUnitsCombo(localLogType, log.fileUnit))
            self.logsTableWidget.setItem(row, logtablemodel.FILE_MNEMONIC,
                    QTableWidgetItem(log.fileMnemonic))
            self.logsTableWidget.setItem(row, logtablemodel.FILE_UNIT,
                    QTableWidgetItem(log.fileUnit))
            self.logsTableWidget.setItem(row, logtablemodel.FILE_DESCRIPTION,
                    QTableWidgetItem(log.fileDescription))
        self.logsTableWidget.setSortingEnabled(True)
        self.logsTableWidget.resizeColumnsToContents()
        
        
        if selected is not None:
            selected.setSelected(True)
            self.logsTableWidget.setCurrentItem(selected)
            
    def handleItemClicked(self, item):
        #disable uncheck on depth log
        if item.row() == 0:
            item.setCheckState(QtCore.Qt.Checked)
            return
        log = self._logTableModel.getLogFromIndex(item.row())
        if item.checkState() == QtCore.Qt.Checked:
            log.importLog = True
            logger.debug("--handleItemClicked() checked name: "+str(log.name)+" importLog: "+str(log.importLog))
        else:
            log.importLog = False
            logger.debug("--handleItemClicked() unchecked")
    
    def generateTypesCombo(self):
        typesComboBox = QtGui.QComboBox()
        logTypes = LogType.getAllLogTypesStringList()
        typesComboBox.addItems(sorted(logTypes))
        typesComboBox.setEditable(False)
        return typesComboBox
    
    def getPreparedTypesCombo(self, logMnemonic):
        typesComboBox = self.generateTypesCombo()
        localLogType = LogType.findLogTypeFromMnemonic(logMnemonic)
        
        if typesComboBox.findData(localLogType.name):
            index = typesComboBox.findText(localLogType.name)
            logger.debug("--getPreparedTypesCombo() matched name in combo - index: "+str(index)+" name: "+str(localLogType.name)+" mnem: "+str(logMnemonic))
            typesComboBox.setCurrentIndex(index)
        else:
            type = LogType
            logType = type.UNKNOWN
            index = typesComboBox.findText(logType.name)
            logger.debug("--getPreparedTypesCombo() not matched - index: "+str(index)+" name: "+str(logType.name)+" mnem: "+str(logMnemonic))
            typesComboBox.setCurrentIndex(index)
        return typesComboBox
        
    def populateUnitsListForType(self, logType):
        unitTypes = LogType.getLogUnitsForType(logType)
        unitsList = []
        for item in unitTypes:
            #logger.debug("--populateUnitsListForType() log type: "+str(logType)+" unit type: "+str(item))
            unitsList.append(item.name)
        return unitsList
            
    def populateUnitsCombo(self, logType, fileUnit):
        unitList = self.populateUnitsListForType(logType)
        #debug
        if len(unitList) == 0:
            logger.debug("--populateUnitsCombo() no units found for log type: "+str(logType.name))
        #end debug
        match = str()
        type = LogType
        unknownLogType = type.UNKNOWN
        for item in unitList:
            #logger.debug("--populateUnitsCombo() log type: "+str(logType)+" unit type: "+str(item)+" file unit: "+str(fileUnit))
            if str(fileUnit).lower() == item.lower():
                match = item
        
        unitsComboBox = QtGui.QComboBox()
        unitsComboBox.addItems(sorted(unitList))
        unitsComboBox.setEditable(False)
        if match:
            index = unitsComboBox.findText(match)
            unitsComboBox.setCurrentIndex(index)
        elif logType == unknownLogType:
            unitsType = LogUnitsType
            unknownLogType = unitsType.UNKNOWN         
            index = unitsComboBox.findText(unknownLogType.name)
            unitsComboBox.setCurrentIndex(index)
        else:
            unitsComboBox.setCurrentIndex(0)
        #do we need an else?
        return unitsComboBox
           
    def connectSlots(self):
        logger.debug(">>connectSlots()")
        self.viewfilePushButton.clicked.connect(self.viewfileclicked)
        self.logsTableWidget.itemChanged.connect(self.tableItemChanged)
        self.selectalldefinedRadioButton.clicked.connect(self.selectAllDefinedClicked)
        self.selectallRadioButton.clicked.connect(self.selectAllClicked)
        self.selectnoneRadioButton.clicked.connect(self.selectNoneClicked)
        self.logsTableWidget.itemClicked.connect(self.handleItemClicked)
        #self.nextPushButton.clicked.connect(self.nextPushButtonClicked)
        
    def viewfileclicked(self):
        #http://www.rkblog.rk.edu.pl/w/p/simple-text-editor-pyqt4/
        logger.debug("file viewer")
        
    def tableItemChanged(self, item):
        logger.debug(">>tableItemChanged()")
        log = self.currentTableLog()
        if log is None:
            logger.debug("--tableItemChanged() log is None")
            return
        column = self.logsTableWidget.currentColumn()
        row = self.logsTableWidget.currentRow()
        logger.debug("--tableItemChanged() column: "+str(column)+" IMPORT: "+str(logtablemodel.IMPORT))
        #if column == logtablemodel.IMPORT:
        #    log.importLog = item.text().strip()
        #    changedLog = self._logTableModel.getLogFromIndex(row)
        #    logger.debug("--tableItemChanged() IMPORT "+str(item.text())+" log name: "+str(changedLog.name))
        if column == logtablemodel.NAME:
            log.name = item.text().strip()
            logger.debug("--tableItemChanged() NAME "+str(log.name))
        elif column == logtablemodel.TYPE:
            log.type = item.text().strip()
            logger.debug("--tableItemChanged() TYPE "+str(log.type))
        elif column == logtablemodel.UNIT:
            log.unit = item.text().strip()
            logger.debug("--tableItemChanged() UNIT "+str(log.unit))
        self._logTableModel.dirty = True
        
    def currentTableLog(self):
        #self.table.selectionModel().selectedRows()
        #selectedItems = self.logsTableWidget.selectedItems()
        item = self.logsTableWidget.item(self.logsTableWidget.currentRow(), 0)
        logger.debug("--currentTableLog() columnCount: "+str(self.logsTableWidget.columnCount())+" row count: "+str(self.logsTableWidget.rowCount()))
        logger.debug("--currentTableLog() row: "+str(self.logsTableWidget.currentRow()))
        logger.debug("--currentTableLog() column: "+str(self.logsTableWidget.currentColumn()))
        logger.debug("--currentTableLog() item type: "+str(type(item)))
        if item is None:
            return None
        '''
        if len(selectedItems) is 0:
            return None
        elif len(selectedItems) is 1:
            return selectedItems[0]
        else:
            return None
        '''
        #logger.debug("--currentTableLog() item data type: "+str(type(item.data(Qt.UserRole)))+" role: "+str(Qt.UserRole)+" data n role: "+str(item.data(Qt.UserRole).toLongLong()))
        #logger.debug("--currentTableLog() data: "+str(item.data(Qt.UserRole).toLongLong()[0]))
        return self._logTableModel.getLogFromIndex(self.logsTableWidget.currentRow())

    def selectAllDefinedClicked(self):
        ''' 
        Checks if log type is not Unknown and sets import checked if so
        Note use of cellWidget for combobox and item for checkbox
        '''
        allRows = self.logsTableWidget.rowCount()
        importColumn = logtablemodel.IMPORT
        typeColumn = logtablemodel.TYPE
        type = LogType
        unknownLogType = type.UNKNOWN
        for row in range(0,allRows):
            tableCell = self.logsTableWidget.cellWidget(row,typeColumn)
            if str(tableCell.currentText()) != unknownLogType.name:
                self.logsTableWidget.item(row,importColumn).setCheckState(Qt.Checked)
            else:
               self.logsTableWidget.item(row,importColumn).setCheckState(Qt.Unchecked) 

    
    def selectAllClicked(self):
        allRows = self.logsTableWidget.rowCount()
        importColumn = logtablemodel.IMPORT
        for row in range(0,allRows):
            self.logsTableWidget.item(row,importColumn).setCheckState(Qt.Checked)
    
    def selectNoneClicked(self):
        allRows = self.logsTableWidget.rowCount()
        importColumn = logtablemodel.IMPORT
        for row in range(0,allRows):
            self.logsTableWidget.item(row,importColumn).setCheckState(Qt.Unchecked)
            
    def nextButtonClicked(self):
        logger.debug(">>nextButtonClicked()")
            

    def populateObject(self):
        logger.debug(">>populateObject()")
        
        allRows = self.logsTableWidget.rowCount()
        allColumns = self.logsTableWidget.columnCount()
        
        for row in range(0,allRows):
            importItem = self.logsTableWidget.item(row,0)
            #don't want to import the Depth log
            if row == 0:
                self._logList[row].importLog = False
            elif importItem.checkState():
                self._logList[row].importLog = True
                #logger.debug("--populateObject() import: "+str(self._logList[row].importLog)+" name: "+str(self._logList[row].name))
                
                for column in range(1, allColumns):
                    if column == logtablemodel.NAME:
                        self._logList[row].name = self.logsTableWidget.item(row,column).text()
                        #logger.debug("--populateObject() name: "+str(self._logList[row].name))
                    elif column == logtablemodel.TYPE:
                        #note we use cellWidget to return a QWidget instead of a QTableWidgetItem
                        self._logList[row].log_type_name = self.logsTableWidget.cellWidget(row,column).currentText()
                        #logger.debug("--populateObject() type: "+str(self._logList[row].log_type))
                    #non persisted data
                    elif column == logtablemodel.UNIT:
                        self._logList[row].unit = self.logsTableWidget.cellWidget(row,column).currentText()
                        #logger.debug("--populateObject() unit: "+str(self._logList[row].unit))
                    elif column == logtablemodel.FILE_MNEMONIC:
                        self._logList[row].fileMnemonic = self.logsTableWidget.item(row,column).text()
                    elif column == logtablemodel.FILE_UNIT:
                        self._logList[row].fileUnit = self.logsTableWidget.item(row,column).text()
                    elif column == logtablemodel.FILE_DESCRIPTION:
                        self._logList[row].fileDescription = self.logsTableWidget.item(row,column).text()
                
            else:
                self._logList[row].importLog = False


               
        '''
        for row in range(0,allRows):
            for column in range(0, allColumns):
                if column == logtablemodel.IMPORT:
                    #importCell = self.logsTableWidget.cellWidget(row,importColumn)
                    importItem = self.logsTableWidget.item(row,column)
                    #don't want to import the Depth log
                    if row == 0:
                        self._logList[row].importLog = False
                    elif importItem.checkState():
                        self._logList[row].importLog = True
                        logger.debug("--populateObject() import: "+str(self._logList[row].importLog)+" name: "+str(self._logList[row].name))
                    else:
                        self._logList[row].importLog = False
                #NAME
                elif column == logtablemodel.NAME:
                    self._logList[row].name = self.logsTableWidget.item(row,column).text()
                    logger.debug("--populateObject() name: "+str(self._logList[row].name))
                elif column == logtablemodel.TYPE:
                    #note we use cellWidget to return a QWidget instead of a QTableWidgetItem
                    self._logList[row].type = self.logsTableWidget.cellWidget(row,column).currentText()
                    logger.debug("--populateObject() type: "+str(self._logList[row].type))
                #non persisted data
                elif column == logtablemodel.UNIT:
                    self._logList[row].unit = self.logsTableWidget.cellWidget(row,column).currentText()
                    logger.debug("--populateObject() unit: "+str(self._logList[row].unit))
                elif column == logtablemodel.FILE_MNEMONIC:
                    self._logList[row].unit = self.logsTableWidget.item(row,column).text()
                elif column == logtablemodel.FILE_UNIT:
                    self._logList[row].unit = self.logsTableWidget.item(row,column).text()
                elif column == logtablemodel.FILE_DESCRIPTION:
                    self._logList[row].unit = self.logsTableWidget.item(row,column).text()
        '''
                    
        

        