
from globalvalues.appsettings import AppSettings
from globalvalues import appsettings
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData
import json
import sys

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt, pyqtSlot
#from gui.wellplot.subplots.wellplot import WellPlotMPL
from db.core.log.log import Log

import unittest
from db.databasemanager import DM
from db.core.well.well import Well
from db.defaultsinitialiser import DefaultsInitialiser
from gui.wellplot.settings.wellplotsettingsdialog import WellPlotSettingsDialog
from PyQt4 import QtCore
from unittest.mock import MagicMock
from db.core.log.logdao import LogDao
from statics.types.logtype import LogType
from preferences.plotting.renderersettings import PlotRenderer
from globalvalues.constants.plottingconstants import LineStyles

#import logging
import logging.config, os, sys
from gui.util.qt.widgetutils import WidgetUtils
from db.core.basedao import BaseDao
from db.test.dummydbsetup import DummyDbSetup
from gui.wellplot.pyqtgraph.wellplotpg import WellPlotPG

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

class WellPlotSettingsDialogTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(WellPlotSettingsDialogTest, self).__init__(*args, **kwargs)
        #QWidget: Must construct a QApplication before a QPaintDevice
        #self.app = QApplication(sys.argv)
        self.dummyDbSetup = DummyDbSetup()

        
    
    def test_tickDisplayedLogs(self):
        #test that all input logs are automatically checked in the table
        logger.debug("=================================================================")
        logger.debug(">>test_tickDisplayedLogs() ")
        app = QApplication(sys.argv)
        
        well, logPlotData = self.generateLogPlotData()
        
        layoutDialog = WellPlotSettingsDialog(logPlotData, well)
        rows = layoutDialog.chkboxTableWidget.rowCount()
        cols = layoutDialog.chkboxTableWidget.columnCount()

        logs = LogDao.getWellLogsOptSession(well, logSet=None)
        self.assertEquals(3, len(logs))
        #number of logs=3 + Log name column plus extra column
        self.assertEquals(5, cols)
        chkBoxItem = layoutDialog.chkboxTableWidget.item(0,0)
        self.assertIsNotNone(chkBoxItem)
        plotList = layoutDialog._wellPlotData.sub_plots
        self.assertEquals(3, len(plotList))

        for row, log in enumerate(logs):
            for subPlotData in plotList:
                for plotLog in subPlotData.getLogs():
                    if log.id == plotLog.id:
                        logger.debug("--test_tickDisplayedLogs() match found id: {0}".format(log.id))
                        chkState = layoutDialog.chkboxTableWidget.item(row, subPlotData.plot_index).checkState()
                        self.assertEquals(QtCore.Qt.Checked, chkState)
        logger.debug("=================================================================")
    
      
    
    def test_changeLogTrack(self):
        #test that on column removal all indexes are set correctly 
        logger.debug("=================================================================")
        logger.debug(">>test_changeLogTrack() ")
        app = QApplication(sys.argv)
        
        well, logPlotData = self.generateLogPlotData()
        layoutDialog = WellPlotSettingsDialog(logPlotData, well)
        
        plotLogs = self.getCurrentlyPlottedLogs(logPlotData)
        self.assertEquals(3, len(plotLogs))
        
        subPlotList = layoutDialog._wellPlotData.sub_plots
        self.assertEquals(1, subPlotList[0].plot_index)
        self.assertEquals(2, subPlotList[1].plot_index)
        self.assertEquals(3, subPlotList[2].plot_index)
        self.assertEquals("LWD_GR", subPlotList[0]._logs[0].name)
        self.assertEquals("2DT", subPlotList[1]._logs[0].name)
        self.assertEquals("3SP", subPlotList[2]._logs[0].name)
        self.assertEquals(3, len(subPlotList))
                
        chkBoxItem = layoutDialog.chkboxTableWidget.item(0,1)
        logger.debug("--test_changeLogTrack() unchecking first cell")
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        
        subPlotList = layoutDialog._wellPlotData.sub_plots
        
        self.assertEquals(-1, subPlotList[0].plot_index)
        #log has been removed
        self.assertEquals(0, len(subPlotList[0]._logs))
        self.assertEquals("2DT", subPlotList[1]._logs[0].name)
        self.assertEquals("3SP", subPlotList[2]._logs[0].name)
        self.assertEquals(1, subPlotList[1].plot_index)
        self.assertEquals(2, subPlotList[2].plot_index)
        
        self.assertEquals(3, len(subPlotList))

    
        logger.debug("=================================================================")
    
    
    def test_removeEmptyColumns(self):
        #test that on column removal all indexes are set correctly 
        logger.debug("=================================================================")
        logger.debug(">>test_removeEmptyColumns() ")
        app = QApplication(sys.argv)
        well, logPlotData = self.generateLogPlotData()
        layoutDialog = WellPlotSettingsDialog(logPlotData, well)
        
        plotLogs = self.getCurrentlyPlottedLogs(logPlotData)
        self.assertEquals(3, len(plotLogs))
        logs = LogDao.getLogNamesCSV(plotLogs)
        logger.debug("--test_removeEmptyColumns() initial logs: "+logs)
                
        allRows = layoutDialog.chkboxTableWidget.rowCount()
        allColumns = layoutDialog.chkboxTableWidget.columnCount()
        self.assertEquals(3, allRows)
        self.assertEquals(5, allColumns)
        #unselect first log
        chkBoxItem = layoutDialog.chkboxTableWidget.item(0,1)
        log = chkBoxItem.data(Qt.UserRole)
        logger.debug("--test_removeEmptyColumns() unchecking first cell log name: "+str(log.name))
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        newPlotLogs = self.getCurrentlyPlottedLogs(logPlotData)
        newLogs = LogDao.getLogNamesCSV(newPlotLogs)
        self.assertEquals("2DT,3SP", newLogs)
        
        self.getCheckbxTableStatus(layoutDialog)
        allRows = layoutDialog.chkboxTableWidget.rowCount()
        allColumns = layoutDialog.chkboxTableWidget.columnCount()
        self.assertEquals(3, allRows)
        self.assertEquals(4, allColumns)
        
        chkBoxItem = layoutDialog.chkboxTableWidget.item(1,1)
        log = chkBoxItem.data(Qt.UserRole)
        logger.debug("--test_removeEmptyColumns() unchecking second cell log name: "+str(log.name))
        #unselect another log
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)

        newPlotLogs = self.getCurrentlyPlottedLogs(logPlotData)
        newLogs = LogDao.getLogNamesCSV(newPlotLogs)
        allRows = layoutDialog.chkboxTableWidget.rowCount()
        allColumns = layoutDialog.chkboxTableWidget.columnCount()

        self.assertEquals(3, allRows)
        self.assertEquals(3, allColumns)
        self.assertEquals("3SP", newLogs)
        self.getCheckbxTableStatus(layoutDialog)

        plotList = logPlotData.sub_plots
        #self.assertEquals(2, len(plotList))
        
        firstPlot = plotList[0]
        firstPlotLogs = []
        for log in firstPlot.getLogs():
                firstPlotLogs.append(log)
        #self.assertEquals(1, len(firstPlotLogs))  
        #self.assertEquals("2DT", firstPlotLogs[0].name)  
        
        secondPlot = plotList[1]
        secondPlotLogs = []
        for log in secondPlot.getLogs():
                secondPlotLogs.append(log)
        #self.assertEquals(1, len(secondPlotLogs))  
        #self.assertEquals("3PEF", secondPlotLogs[1].name) 
        
    
        logger.debug("=================================================================")
    
    def getCheckbxTableStatus(self, layoutDialog):
        allRows = layoutDialog.chkboxTableWidget.rowCount()
        allColumns = layoutDialog.chkboxTableWidget.columnCount()

        #start at one so don't include the name column
        #end at number columns-1 as last one will be unchecked
        for column in range(1, allColumns-1):
            checked = False
            for row in range(allRows):
                tw = layoutDialog.chkboxTableWidget.item(row,column)
                if tw != None:
                    if (tw != None) and (tw.checkState() == QtCore.Qt.Checked):
                        checked = True
                        logger.debug("--getCheckbxTableStatus() row: {0}, col: {1} checked, text {2}".format(row, column, tw.text))
            if not checked:
                logger.debug("--getCheckbxTableStatus() no logs checked in col: "+str(column))
            
        
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
        wellPlot = WellPlotPG(logs, well)
        logPlotData = wellPlot.createWellPlotData(logs)
        plotList = logPlotData.sub_plots
        self.assertEquals(3, len(plotList))
        return well, logPlotData
 

    

    
        '''
    def test_getTickedLogs(self):
        logger.debug(">>test_getTickedLogs() ")
        self.setupDatabase()
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)
        well = self.createWell()
        logs = self.createLogs(well.id)
        wellPlot = WellPlotMPL(logs, well)
        plotList = wellPlot.generateSubPlotDatas(logs)
        logPlotData = self.createWellPlotData()
        logPlotData.logList = logs
        logPlotData.sub_plots = plotList
        
        mockLayoutLogic = LogDao()
        mockLayoutLogic.getWellLogs = MagicMock(return_value = logs)
        
        layoutDialog = WellPlotSettingsDialog(logPlotData, well)
        logger.debug("--test_getTickedLogs() WellPlotSettingsDialog created")
        rows = layoutDialog.chkboxTableWidget.rowCount()
        cols = layoutDialog.chkboxTableWidget.columnCount()
        logger.debug("--test_getTickedLogs() rows: "+str(rows)+" cols: "+str(cols))
        logs = LogDao.getWellLogsOptSession(well, logSet=None)
        self.assertEquals(3, len(logs))
        #number of logs=3 + Log name column plus extra column
        self.assertEquals(5, cols)
        chkBoxItem = layoutDialog.chkboxTableWidget.item(0,0)
        self.assertIsNotNone(chkBoxItem)
        plotList = layoutDialog._wellPlotData.sub_plots
        self.assertEquals(3, len(plotList))
        for subPlotData in plotList:
            for plotLog in subPlotData.getLogs():
                logger.debug("test_getTickedLogs() log name: {0} plot index:{1}".format(plotLog.name, subPlotData.plot_index))
        self.assertEquals(True, WidgetUtils.getBoolFromQtCheck(chkBoxItem.checkState()))
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        logger.debug("--------------------------------------")
        #layoutDialog.chkboxTableWidget.item(1, 1).setCheckState(QtCore.Qt.Checked)
    '''
        
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
    