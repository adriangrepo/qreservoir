from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


import logging

from db.core.log.logdao import LogDao
from db.windows.wellplot.wellplotdata.wellplotdatadao import WellPlotDataDao
from db.windows.wellplot.logtrackdata.logtrackutility import LogTrackUtility

logger = logging.getLogger('console')

class LayoutHandler(object):
    '''
    classdocs
    '''


    def __init__(self, curveStyleWidget):
        self._curveStyleWidget = curveStyleWidget
        
    def changeLogTrack(self, item):
        logger.debug(">>changeLogTrack()")
        assert item != None
        
        row = item.row()
        col = item.column()
        logger.debug("--changeLogTrack() row:{0} col:{1}".format(row, col))
        log = item.data(Qt.UserRole)
        logger.debug("--changeLogTrack() log:{0}".format(log.name))
        allRows = self._curveStyleWidget.chkboxTableWidget.rowCount()
    
        logger.debug("--changeLogTrack() log name: {0} row: {1} col: {2}".format(log.name, row, col))
        if item.checkState() == QtCore.Qt.Checked:
            logger.debug("--changeLogTrack() Checked log name: {0}".format(log.name))
            addedToExistingSubPlot = False
            for subPlotData in self._curveStyleWidget._wellPlotData.getLogTrackDatas():
                logger.debug("--changeLogTrack() subplot.plot_index:{0}, col:{1}, log name:{2}, len(subplots):{3}".format(subPlotData.plot_index, col, log.name, len(self._curveStyleWidget._wellPlotData.getLogTrackDatas())))
                if subPlotData.plot_index == col:
                    logger.debug("--changeLogTrack() plot_index == col, adding log to subplot.plot_index:{0}, col:{1}, log name:{2}".format(subPlotData.plot_index, col, log.name))
                    subPlotData.addLog( log)
                    subPlotData.is_displayed = True
                    addedToExistingSubPlot = True
            if not addedToExistingSubPlot:
                #need to create a new subplot
                subPlotData = self.createSubPlotFromTable(col, allRows)
                subPlotData.is_displayed = True
                self._curveStyleWidget._wellPlotData.getLogTrackDatas().append(subPlotData)
            self.addColumnIfClickLast(col)
            #self.removeEmptyColumns(log)
            
        #test
        else:
            logger.debug("--changeLogTrack() Unchecked log name: {0}".format(log.name))
            if (col <= len(self._curveStyleWidget._wellPlotData.getLogTrackDatas())+1):
                for trackData in self._curveStyleWidget._wellPlotData.getLogTrackDatas():
                    logger.debug("--changeLogTrack() subplot.index:{0} column:{1} len(subplots):{2}".format(trackData.plot_index, col, len(self._curveStyleWidget._wellPlotData.getLogTrackDatas())))
                    if (trackData.plot_index == col):
                        trackData.is_displayed = False
                        trackData.removeLog(log)
                        logger.debug("--changeLogTrack() removed log:{0} from subplot {1},  len(subplots):{2}".format(log.name, trackData.plot_index, len(self._curveStyleWidget._wellPlotData.getLogTrackDatas())))
        #end test
                        
        self.removeEmptyColumns(log)
        self._curveStyleWidget.refreshPlotTrackCurve()
         
        
    def tickDisplayedLogs(self):
        logger.debug(">>tickDisplayedLogs()")
        if self._curveStyleWidget._wellPlotData != None:
            plotList = self._curveStyleWidget._wellPlotData.getLogTrackDatas()
            for row, log in enumerate(self._curveStyleWidget._logs):
                checkedBox = False
                for subPlotData in plotList:
                    for plotLog in subPlotData.getLogs():
                        if log.id == plotLog.id:
                            logger.debug("--tickDisplayedLogs() row:{0}, plot index:{1}, log id:{2}".format(row, subPlotData.plot_index, log.id))
                            self._curveStyleWidget.chkboxTableWidget.item(row, subPlotData.plot_index).setCheckState(QtCore.Qt.Checked)
                            widgetLog = self._curveStyleWidget.chkboxTableWidget.item(row, subPlotData.plot_index).data(Qt.UserRole)
                            assert log.id == widgetLog.id
                            self._curveStyleWidget.chkboxTableWidget.item(row, subPlotData.plot_index).setData(Qt.UserRole, "")
                            self._curveStyleWidget.chkboxTableWidget.item(row, subPlotData.plot_index).setData(Qt.UserRole, log)
                            checkedBox = True
                    if checkedBox:
                        subPlotData.is_displayed = True       
            

            
    #TODO needs testing and more work to iron out bugs   
    def removeEmptyColumns(self, log):
        logger.debug(">>removeEmptyColumns()")
        initialRows = self._curveStyleWidget.chkboxTableWidget.rowCount()
        initialColumns = self._curveStyleWidget.chkboxTableWidget.columnCount()
        i=1
        #start at one so don't include the name column
        #end at number columns-1 as last one will be unchecked
        for column in range(1, initialColumns):
            logger.debug("--removeEmptyColumns() count: "+str(i)+" total col count: "+str(initialColumns))
            i += 1
            checked = False
            for row in range(initialRows):
                tw = self._curveStyleWidget.chkboxTableWidget.item(row,column)
                if tw != None:
                    if (tw != None) and (tw.checkState() == QtCore.Qt.Checked):
                        checked = True
                        logger.debug("--removeEmptyColumns() row: {0}, col: {1} checked".format(row, column))
            if not checked and (column < initialColumns-1):
                logger.debug("--removeEmptyColumns() no logs checked in col:{0} column count:{1} ".format(column, initialColumns))
                self._curveStyleWidget.chkboxTableWidget.removeColumn(column) 
                logger.debug("--removeEmptyColumns() inital cols:{0} new cols:{1}".format(initialColumns, self._curveStyleWidget.chkboxTableWidget.columnCount()))
                self.shiftAllPlots(column, log)
                #either break out of for loop or store column numbers and delete all in one go
                break
        #if nothing selected, reset plot index for single empty column
        columnCount = self._curveStyleWidget.chkboxTableWidget.columnCount()
        plotList = self._curveStyleWidget._wellPlotData.getLogTrackDatas()
        logger.debug("--removeEmptyColumns() len (plotList):"+str(len(plotList)))
        if columnCount == 2:
            #add 1 to i so plot index starts at 1 not 0
            for i, subPlotData in enumerate(plotList):
                logger.debug("--removeEmptyColumns() resetting plot_index:{0} to {1}".format(subPlotData.plot_index, i+1))
                subPlotData.plot_index = i+1
                assert subPlotData.is_displayed == False
                
                
        self.headers = self._curveStyleWidget.getLayoutTableHeaders(len(self._curveStyleWidget._wellPlotData.getLogTrackDatas())+1)
        self._curveStyleWidget.chkboxTableWidget.setHorizontalHeaderLabels(self.headers)
    
    def getNumberOfDisplayedTracks(self):
        numDisplayedSubPlots = 0
        if self._curveStyleWidget._wellPlotData is not None:
            for trackData in self._curveStyleWidget._wellPlotData.getLogTrackDatas():
                if trackData.is_displayed:
                    numDisplayedSubPlots +=1
        return numDisplayedSubPlots
            
    def shiftAllPlots(self, deletedColumn, log):
        ''' subtract 1 from plotIndexes to right of the deleted column '''
        logger.debug(">>shiftAllPlots()")
        for i, subPlotData in enumerate(self._curveStyleWidget._wellPlotData.getLogTrackDatas()):
            if subPlotData.plot_index == deletedColumn:
                subPlotData.plot_index = -1
                subPlotData.removeLog(log)
            elif subPlotData.plot_index > deletedColumn:
                logger.debug("subPlotData.plot_index {0} changed to {1} deleted column {2}".format(subPlotData.plot_index, subPlotData.plot_index-1, deletedColumn))
                subPlotData.plot_index -= 1

        self.headers = self._curveStyleWidget.getLayoutTableHeaders(self.getNumberOfDisplayedTracks()+1)
        self._curveStyleWidget.chkboxTableWidget.setHorizontalHeaderLabels(self.headers)
        
    def getTickedPlotList(self, chkboxTableWidget):
        ''' returns list of ticked logs as plot list '''
        logger.debug(">>getTickedPlotList()")
        #pass in chkboxTableWidget so can unit test
        tickedPlotList = []
         
        allRows = self._curveStyleWidget.chkboxTableWidget.rowCount() 
        allColumns = self._curveStyleWidget.chkboxTableWidget.columnCount()
        #range([start], stop[, step])
        for col in range(1, allColumns):
            subPlotData = self.createSubPlotFromTable(col, allColumns)
            tickedPlotList.append(subPlotData)
        return tickedPlotList
              
    def createSubPlotFromTable(self, column, allRows):
        logger.debug(">>createSubPlotFromTable() col:{0}, allRows:{1}".format(column, allRows))

        subPlotData = LogTrackUtility.createNewTrack()
        subPlotData.plot_index = column
        for row in range(allRows):
            tw = self._curveStyleWidget.chkboxTableWidget.item(row,column)
            if (tw != None) and tw.checkState():
                log = tw.data(Qt.UserRole)
                subPlotData.getLogs().append(log)
        return subPlotData 
    
    def selectDefaultLogsClicked(self):
        ''' default logs from preferences '''
        logger.debug(">>selectDefaultLogsClicked()")
        #self._curveStyleWidget.chkboxTableWidget.blockSignals(True)
        
        try:
            logger.debug("--selectDefaultLogsClicked() disconnecting from changeLogTrack")
            self._curveStyleWidget.chkboxTableWidget.itemChanged.disconnect(self._curveStyleWidget.changeLogTrack)
            logger.debug("--selectDefaultLogsClicked() disconnected from changeLogTrack")
        except TypeError as ex:
            # will be disconnected on first run, log it and continue
            logger.debug(str(ex))
        
            
        #clear all checkboxes first
        self.clearAllCheckboxes()

        defaultLogIds = WellPlotDataDao.getLogIdsPreferences(self._curveStyleWidget._logs)
               
        allRows = self._curveStyleWidget.chkboxTableWidget.rowCount() 
        allColumns = self._curveStyleWidget.chkboxTableWidget.columnCount()
        col = 1
        for row in range(allRows):
            logger.debug("--selectDefaultLogsClicked() row: {0}, col: {1} ".format(row, col))
            tw = self._curveStyleWidget.chkboxTableWidget.item(row,col)
            if (tw != None):
                #log = tw.data(Qt.UserRole)[0]
                log = tw.data(Qt.UserRole)
                if (log.id != 0) and (log.id in defaultLogIds):
                    logger.debug("--selectDefaultLogsClicked() setting checked for row: {0}, col: {1} log id: {1} ".format(row, col, log.id))
                    tw.setCheckState(QtCore.Qt.Checked)
                    col += 1  
        self._curveStyleWidget.chkboxTableWidget.itemChanged.connect(self._curveStyleWidget.changeLogTrack)
        logger.debug("--selectDefaultLogsClicked() reconnected to changeLogTrack")
                          
    def selectActiveLogsClicked(self):
        ''' set checkboxes as checked diagonally down the layout matrix '''
        logger.debug(">>selectActiveLogsClicked()")
        #self._curveStyleWidget.chkboxTableWidget.blockSignals(True)
        
        try:
            logger.debug("--selectActiveLogsClicked() disconnecting from changeLogTrack")
            self._curveStyleWidget.chkboxTableWidget.itemChanged.disconnect(self._curveStyleWidget.changeLogTrack)
            logger.debug("--selectActiveLogsClicked() disconnecting from changeLogTrack")
        except TypeError as ex:
            # will be disconnected on first run, log it and continue 
            logger.debug(str(ex))
        
        #clear all checkboxes first
        self.clearAllCheckboxes()
        if (self._curveStyleWidget._logs != None) and (len(self._curveStyleWidget._logs) > 0):
            activeLogIds = LogDao.getActiveLogIds(self._curveStyleWidget._logs)
                   
            allRows = self._curveStyleWidget.chkboxTableWidget.rowCount() 
            allColumns = self._curveStyleWidget.chkboxTableWidget.columnCount()
            for row in range(allRows):
                tw = self._curveStyleWidget.chkboxTableWidget.item(row,0)
                logger.debug("--selectActiveLogsClicked() row: "+str(row))
                log = tw.data(Qt.UserRole)
                if (tw != None) and (log.id in activeLogIds):
                    tw.setCheckState(QtCore.Qt.Checked)
        else:
            logger.debug("<<selectActiveLogsClicked logs == None")

        self._curveStyleWidget.chkboxTableWidget.itemChanged.connect(self._curveStyleWidget.changeLogTrack)
        logger.debug("--selectActiveLogsClicked() reconnected to changeLogTrack")
                    
    def selectAllLogsClicked(self):
        ''' set checkboxes as checked diagonally down the layout matrix '''
        logger.debug(">>selectAllLogsClicked()")
        #self._curveStyleWidget.chkboxTableWidget.blockSignals(True)
        
        try:
            logger.debug("--selectAllLogsClicked() disconnecting from changeLogTrack")
            self._curveStyleWidget.chkboxTableWidget.itemChanged.disconnect(self._curveStyleWidget.changeLogTrack)
            logger.debug("--selectAllLogsClicked() disconnecting from changeLogTrack")
        except TypeError as ex:
            # will be disconnected on first run, log it and continue 
            logger.debug(str(ex))
        
        #clear all checkboxes first
        self.clearAllCheckboxes()
        
        allRows = self._curveStyleWidget.chkboxTableWidget.rowCount()
        allColumns = self._curveStyleWidget.chkboxTableWidget.columnCount()
        #deselect all widgets

        #can use zip (shortest list) or map to iterate over both counters
        for row, column in zip(range(allRows), range(1, allColumns)):
            tw = self._curveStyleWidget.chkboxTableWidget.item(row,column)
            logger.debug("--selectAllLogsClicked() row: "+str(row)+" col: "+str(column))
            if tw != None:
                tw.setCheckState(QtCore.Qt.Unchecked)
            tw.setCheckState(QtCore.Qt.Checked)
        #self._curveStyleWidget.chkboxTableWidget.blockSignals(True)
        self._curveStyleWidget.chkboxTableWidget.itemChanged.connect(self._curveStyleWidget.changeLogTrack)
        
    def clearAllCheckboxes(self):
        allRows = self._curveStyleWidget.chkboxTableWidget.rowCount()
        allColumns = self._curveStyleWidget.chkboxTableWidget.columnCount()
        #deselect all widgets
        for row in range(allRows):
            #start at one so don't include the name column
            for column in range(1, allColumns):
                tw = self._curveStyleWidget.chkboxTableWidget.item(row,column)
                logger.debug("--clearAllCheckboxes() row: "+str(row)+" col: "+str(column))
                if tw != None:
                    tw.setCheckState(QtCore.Qt.Unchecked)
            
    def addTrackButtonClicked(self):
        logger.debug(">>addTrackButtonClicked()")
        #check that we are not already in the changeingLogTrack loop
        if self._curveStyleWidget.changeingLogTrack == False:
            try:
                logger.debug("--addTrackButtonClicked() disconnecting from changeLogTrack")
                self._curveStyleWidget.chkboxTableWidget.itemChanged.disconnect(self.changeLogTrack)
                logger.debug("--addTrackButtonClicked() disconnected from changeLogTrack")
            except TypeError as ex:
                #will be disconnected on first run, log it and continue
                logger.debug(str(ex))
            
        allRows = self._curveStyleWidget.chkboxTableWidget.rowCount() 
        allColumns = self._curveStyleWidget.chkboxTableWidget.columnCount()    
        logger.debug("--addTrackButtonClicked() allColumns: "+str(allColumns))   
        self.headers.append(str(allColumns))
        self._curveStyleWidget.chkboxTableWidget.setColumnCount(allColumns+1)
        self._curveStyleWidget.chkboxTableWidget.setHorizontalHeaderLabels(self.headers)
               
        for row in range(allRows):
            tw = self._curveStyleWidget.chkboxTableWidget.item(row,0)
            if (tw != None) and (tw.data(Qt.UserRole) != None):
                log = tw.data(Qt.UserRole)
                chkBoxItem = QtGui.QTableWidgetItem()
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                selected = False
                chkBoxItem.setData(Qt.UserRole, log)  
                self._curveStyleWidget.chkboxTableWidget.setItem(row, allColumns, chkBoxItem)
        if self._curveStyleWidget.changeingLogTrack == False:
            self._curveStyleWidget.chkboxTableWidget.itemChanged.connect(self._curveStyleWidget.changeLogTrack)
            logger.debug("--addTrackButtonClicked() reconnected to changeLogTrack")
            
    def addColumnIfClickLast(self, column): 
        '''Add another column if click rightmost column '''
        logger.debug(">>addColumnIfClickLast()")
        columns = self._curveStyleWidget.chkboxTableWidget.columnCount()
        logger.debug("--addColumnIfClickLast col: {0} total cols: {1}".format(column, columns))
        if column == (columns -1):
            self.addTrackButtonClicked()
            
    def addColumnOfCheckboxes(self, numColumnsBeforeAdd):
        '''add empty column at end of table'''
        logger.debug(">>addColumnOfCheckboxes()")
        for row, log in enumerate(self._logs):
            chkBoxItem = self.createChkBoxItem(log)
            self._curveStyleWidget.chkboxTableWidget.setItem(row, numColumnsBeforeAdd, chkBoxItem) 
            
    def createChkBoxItem(self, log): 
        chkBoxItem = QtGui.QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked) 
        chkBoxItem.setData(Qt.UserRole, log)       
        return chkBoxItem