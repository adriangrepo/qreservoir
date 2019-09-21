from PyQt4.QtCore import QModelIndex, Qt
from PyQt4.Qt import QComboBox
from PyQt4.QtGui import QApplication, QItemSelectionModel, \
                        QPushButton, QStandardItem, \
                        QStandardItemModel, QTreeView, QTableWidgetItem

import logging
import copy

from PyQt4 import QtCore
from gui.wellplot.settings.layout.widgets.checkboxtable.ui_tracklayouttablewidget import Ui_TrackLayoutTableWidget
from gui.wellplot.settings.layout.widgets.checkboxtable.layouthandler import LayoutHandler
from globalvalues.constants.plottingconstants import PlottingConstants

logger = logging.getLogger('console')


class TrackLayoutTableWidget(QTreeView, Ui_TrackLayoutTableWidget):
    '''
    TrackLayoutTableWidget for well plot settings
    '''
    
    def __init__(self, wellPlotData, logs, parent=None):
        super(TrackLayoutTableWidget, self).__init__(parent)
        self._wellPlotData = wellPlotData
        self._initialPlotList = copy.deepcopy(wellPlotData.getLogTrackDatas())
        self._logs = logs
        self.setupUi(self)
        self._layoutHandler = LayoutHandler(self)
        self.populateCheckboxTable()
        

    def populateCheckboxTable(self):
        ''' populate QTableWidget manually with log names and checkboxes 
        simpler than using a QTableView and a dedicated model such as
        tableModel = LogLayoutTableModel(self, logList = self._logs, logHeaders = headers)
        self.tableView.setModel(tableModel)
        ''' 
        logger.debug(">>populateCheckboxTable()")
        selected = None

        initialTracks = len(self._logs)
        if len(self._initialPlotList) > initialTracks:
            initialTracks = len(self._initialPlotList)
            
        #add an extra log name column and a blank end column
        totalNumColumns = initialTracks+2
        logger.debug("--populateCheckboxTable() totalNumColumns:{0}".format(totalNumColumns))
        if (self._logs != None) and (len(self._logs)>0):
            self.headers = self.getLayoutTableHeaders(initialTracks+1)

            self.chkboxTableWidget.clear()
            self.chkboxTableWidget.setSortingEnabled(False)
            self.chkboxTableWidget.setRowCount(len(self._logs))
            self.chkboxTableWidget.setColumnCount(len(self.headers))
            self.chkboxTableWidget.setHorizontalHeaderLabels(self.headers)
    
            for row, log in enumerate(self._logs):
                item = QTableWidgetItem(log.name)
                #looks like can set an object as data
                item.setData(Qt.UserRole, log)
                self.chkboxTableWidget.setItem(row, 0, item)  
                for i in range(1, totalNumColumns):
                    chkBoxItem = self._layoutHandler.createChkBoxItem(log)
                    self.chkboxTableWidget.setItem(row, i, chkBoxItem)                       
    
            self.chkboxTableWidget.resizeColumnsToContents()
            self._layoutHandler.tickDisplayedLogs()
            self.chkboxTableWidget.itemChanged.connect(self.changeLogTrack)
        else:
            logger.debug("--populateCheckboxTable() _logs==None: {0}, _logs length: {1}".format((self._logs == None), (len(self._logs))))
    
    def changeLogTrack(self, item):
        if self.changeingLogTrack == False:
            self.changeingLogTrack = True
            self._layoutHandler.changeLogTrack(item)
        self.changeingLogTrack = False 
      
    def selectDefaultLogsClicked(self):
        ''' default logs from preferences '''
        logger.debug(">>selectDefaultLogsClicked()")
        self._layoutHandler.selectDefaultLogsClicked()
                          
    def selectActiveLogsClicked(self):
        ''' set checkboxes as checked diagonally down the layout matrix '''
        logger.debug(">>selectActiveLogsClicked()")
        
        self._layoutHandler.selectActiveLogsClicked()
                    
    def selectAllLogsClicked(self):
        ''' set checkboxes as checked diagonally down the layout matrix '''
        logger.debug(">>selectAllLogsClicked()")
        
        self._layoutHandler.selectAllLogsClicked()

     
    def clearAllCheckboxes(self):
        self._layoutHandler.clearAllCheckboxes()
            
    def addTrackButtonClicked(self):
        logger.debug(">>addTrackButtonClicked()")
        self._layoutHandler.addTrackButtonClicked()
    
    def getLayoutTableHeaders(self, tickableColumns):     
        headers = [PlottingConstants.LOG_LAYOUT_HEADER_NAME]
        #create n+1 headers where n = number of logs
        for i in range(tickableColumns):
            #zero indexed, add one so start is at one
            headers.append(str(i+1)) 
        return headers
    
    def connectSlots(self):
        self.selectDefaultRadioButton.clicked.connect(self.selectDefaultLogsClicked)
        self.selectAllRadioButton.clicked.connect(self.selectAllLogsClicked)
        self.selectActiveRadioButton.clicked.connect(self.selectActiveLogsClicked)
        self.selectNoneRadioButton.clicked.connect(self.clearAllCheckboxes)
        self.addTrackPushButton.clicked.connect(self.addTrackButtonClicked)
