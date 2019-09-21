
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QDialog,  QTableWidgetItem)
from gui.wellplot.settings.ui_layout import Ui_Dialog

from globalvalues.constants.plottingconstants import PlottingConstants,\
    LineStyles

from qrutilities.numberutils import NumberUtils

from gui.signals.wellplotsignals import WellPlotSignals

import copy


from db.core.log.logdao import LogDao
from globalvalues.constants.wellplotconstants import LogPlotConstants
from gui.widgets.qcolorbutton import QColorButton
from qrutilities.imageutils import ImageUtils
from gui.util.qt.widgetutils import WidgetUtils
from statics.types.logunitstype import LogUnitsType
from statics.types.logtype import LogType
from inout.validation.realvalidator import RealValidator
from globalvalues.constants.colorconstants import ColorConstants

from gui.wellplot.settings.layouthandler import LayoutHandler
from gui.wellplot.settings.trackstylehandler import TrackStyleHandler
from gui.wellplot.settings.plotstylehandler import PlotStyleHandler
from gui.wellplot.settings.curvestylehander import CurveStyleHandler

import logging

logger = logging.getLogger('console')

class WellPlotSettingsDialog(QDialog, Ui_Dialog):
    '''
    Well plot settings
    '''
    def __init__(self, wellPlotData, selectedWell, logSet = None, parent=None):
        logger.debug(">>__init__() ")
        assert wellPlotData != None
        
        super(WellPlotSettingsDialog, self).__init__(parent)
        
        self.setWindowTitle(self.__str__())
        self._well = selectedWell
        self._logSet = logSet
        self._wellPlotData = wellPlotData
        self._initialPlotList = copy.deepcopy(wellPlotData.getLogTrackDatas())
        self._logs = LogDao.getWellLogsOptSession(self._well, self._logSet)
        self._layoutHandler = LayoutHandler(self)
        self._trackStyleHander = TrackStyleHandler(self)
        self._plotStyleHander = PlotStyleHandler(self)
        self._curveStyleHander = CurveStyleHandler(self)
        self.wellPlotSignals = WelPlotSignals()

        self.styleDirty = False
        #added this flag so don't disconnect from slot while in the slot
        self.changeingLogTrack = False
        self.setupUi(self)
        self.setWidgetProperties()
        self.populateCheckboxTable()
        self.refreshPlotTrackCurve()
        self.connectSlots()
        self.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.setContentsMargins(0, 0, 0, 0)
        self.dataSelectionTab.setContentsMargins(0, 0, 0, 0)
        self.chkboxTableWidget.setContentsMargins(0, 0, 0, 0)
        self.plotStyleTab.setContentsMargins(0, 0, 0, 0)
        self.trackStyleTab.setContentsMargins(0, 0, 0, 0)
        self.curveStyleTab.setContentsMargins(0, 0, 0, 0)
        #self.chkboxTableWidget.setItemDelegateForColumn(1, CheckBoxDelegate(self))
        
    def __str__( self ):
        return "Well plot settings"
        
    def setWidgetProperties(self):
        ''' sets initial ranges for sliders and combos '''
        for item in LineStyles:
            self.gridStyleComboBox.addItem(item.name)
        self.gridOpacitySpinBox.setMinimum(0)
        self.gridOpacitySpinBox.setMaximum(255)
        self.labelBackgroundOpacitySpinBox.setMinimum(0)
        self.labelBackgroundOpacitySpinBox.setMaximum(255)
        self.trackBackgroundOpacitySpinBox.setMinimum(0)
        self.trackBackgroundOpacitySpinBox.setMaximum(255)
        self.labelForegroundOpacitySpinBox.setMinimum(0)
        self.labelForegroundOpacitySpinBox.setMaximum(255)
        self.gridVerticalDivSpinBox.setMinimum(0)
        self.gridVerticalDivSpinBox.setMaximum(20)
        
        #lutCm = LogUnitsType.CM
        lutIn = LogUnitsType.INCH 
        #self.trackGapUnitsComboBox.addItem(lutCm.name)
        self.trackGapUnitsComboBox.addItem(lutIn.name)
        #self.trackWidthUnitsComboBox.addItem(lutCm.name)
        self.trackWidthUnitsComboBox.addItem(lutIn.name)  
        self.trackGapUnitsComboBox.setEnabled(False)
        self.trackWidthUnitsComboBox.setEnabled(False)
        self.trackGapLineEdit.setEnabled(False)
        self.trackWidthLineEdit.setEnabled(False)
               
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
                               
    def populatePlotTab(self):
        logger.debug(">>populatePlotTab()")
        
        
        titleOnCheckState = WidgetUtils.getQtCheckObject(self._wellPlotData.title_on)
        self.plotTitleOnCheckBox.setCheckState(titleOnCheckState)
        self.plotTitleOnCheckBox.stateChanged.connect(self.styleChanged)
        self.plotTitleLineEdit.setText(self._wellPlotData.title)
        self.plotTitleLineEdit.textChanged.connect(self.styleChanged)
        self.plotPrintDPILineEdit.setText(str(self._wellPlotData.dpi))
        self.plotPrintDPILineEdit.textChanged.connect(self.styleChanged)
        intValidator = QtGui.QIntValidator()
        self.plotPrintDPILineEdit.setValidator(intValidator)
        #not enabled for this version
        self.plotTitleOnCheckBox.setEnabled(False)
        self.plotTitleLineEdit.setEnabled(False)
        self.plotPrintDPILineEdit.setEnabled(False)
        
        trackBackButtonQColor = ImageUtils.rbgToQColor(self._wellPlotData.plot_background_rgb)
        trackBackColorButton = QColorButton()
        trackBackColorButton.setColor(trackBackColorButton)
        self.trackBackgroundColorPushButton = trackBackColorButton
        self.trackBackgroundColorPushButton.clicked.connect(self.styleChanged)
        plotBackgroundAlpha = NumberUtils.stringToInt(self._wellPlotData.plot_background_alpha)
        self.trackBackgroundOpacitySpinBox.setValue(plotBackgroundAlpha)
        self.trackBackgroundOpacitySpinBox.valueChanged.connect(self.styleChanged)
        
        gridOnCheckState = WidgetUtils.getQtCheckObject(self._wellPlotData.grid_on)
        self.gridOnCheckBox.setCheckState(gridOnCheckState)
        self.gridOnCheckBox.stateChanged.connect(self.styleChanged)

        buttonQColor = ImageUtils.rbgToQColor(self._wellPlotData.grid_rgb)
        qColorButton = QColorButton()
        qColorButton.setColor(buttonQColor)
        self.gridColorPushButton = qColorButton
        self.gridColorPushButton.clicked.connect(self.styleChanged)
        
        gridAlpha = NumberUtils.stringToInt(self._wellPlotData.grid_alpha)
        self.gridOpacitySpinBox.setValue(gridAlpha)
        self.gridOpacitySpinBox.valueChanged.connect(self.styleChanged)
        
        index = self.gridStyleComboBox.findText(self._wellPlotData.grid_line_style, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.gridStyleComboBox.setCurrentIndex(index)
        self.gridStyleComboBox.currentIndexChanged.connect(self.styleChanged)

        self.gridVerticalDivSpinBox.setValue(self._wellPlotData.grid_vertical_divisions)
        self.gridVerticalDivSpinBox.valueChanged.connect(self.styleChanged)
        
        expandedCheckState = WidgetUtils.getQtCheckObject(self._wellPlotData.single_row_header_labels)
        self.labelsExpandedCheckBox.setCheckState(expandedCheckState)
        self.labelsExpandedCheckBox.stateChanged.connect(self.styleChanged)
        
        labelBackButtonQColor = ImageUtils.rbgToQColor(self._wellPlotData.label_background_rgb)
        labelBackColorButton = QColorButton()
        labelBackColorButton.setColor(labelBackButtonQColor)
        self.labelBackgroundColorPushButton = labelBackColorButton
        self.labelBackgroundColorPushButton.clicked.connect(self.styleChanged)
        
        labelBackgroundAlpha = NumberUtils.stringToInt(self._wellPlotData.label_background_alpha)
        self.labelBackgroundOpacitySpinBox.setValue(labelBackgroundAlpha)
        self.labelBackgroundOpacitySpinBox.valueChanged.connect(self.styleChanged)
        
        labelForegroundRGB = NumberUtils.stringToInt(self._wellPlotData.label_foreground_rgb)
        labelForeButtonQColor = ImageUtils.rbgToQColor(labelForegroundRGB)
        labelForeColorButton = QColorButton()
        labelForeColorButton.setColor(labelForeButtonQColor)
        self.labelForegroundColorPushButton = labelForeColorButton
        self.labelForegroundColorPushButton.clicked.connect(self.styleChanged)
        
        labelForegroundAlpha = NumberUtils.stringToInt(self._wellPlotData.label_foreground_alpha)
        self.labelForegroundOpacitySpinBox.setValue(labelForegroundAlpha)
        self.labelForegroundOpacitySpinBox.valueChanged.connect(self.styleChanged)
       
    
    def populateTrackTab(self): 
        logger.debug(">>populateTrackTab()")
        try: 
            self.trackApplyAllCheckBox.stateChanged.disconnect(self.handleApplyAllChkClicked)
            self.trackWidthLineEdit.textChanged.disconnect(self.checkReqiredState)
            self.trackGapLineEdit.textChanged.disconnect(self.checkReqiredState)
        except TypeError as ex:
            # will be disconnected on first run, log it and continue
            logger.debug(str(ex))
  
        self.populateTrackTable()
        self.trackApplyAllCheckBox.setCheckState(QtCore.Qt.Unchecked)
        self.trackApplyAllCheckBox.stateChanged.connect(self.handleApplyAllChkClicked)
        widthValidator = RealValidator()
        widthValidator.setRange (LogPlotConstants.LOG_PLOT_TRACK_WIDTH_MIN, LogPlotConstants.LOG_PLOT_TRACK_WIDTH_MAX, LogPlotConstants.LOG_PLOT_TRACK_DECIMALS)
        self.trackWidthLineEdit.setValidator(widthValidator)
        self.trackWidthLineEdit.setText(str(LogPlotConstants.LOG_PLOT_TRACK_WIDTH_DEFAULT))
        self.trackWidthLineEdit.textChanged.connect(self.checkReqiredState)
        
        gapValidator = RealValidator()
        gapValidator.setRange (LogPlotConstants.LOG_PLOT_TRACK_GAP_MIN, LogPlotConstants.LOG_PLOT_TRACK_GAP_MAX, LogPlotConstants.LOG_PLOT_TRACK_DECIMALS)
        self.trackGapLineEdit.setValidator(gapValidator)
        self.trackGapLineEdit.setText(str(LogPlotConstants.LOG_PLOT_TRACK_GAP_DEFAULT))
        self.trackGapLineEdit.textChanged.connect(self.checkReqiredState)
        
    def populateTrackTable(self):
        logger.debug(">>populateTrackTable()")

        try: 
            self.trackTableWidget.itemChanged.disconnect(self.styleChanged)
        except TypeError as ex:
            logger.debug(str(ex))
        
        headers = LogPlotConstants.LOG_PLOT_TRACK_STYLE_HEADERS
        numberOfColumns = len(headers)
        self.trackTableWidget.clear()
        self.trackTableWidget.setSortingEnabled(False)
        tracks = self._layoutHandler.getDisplayedSubPlots()
        self.trackTableWidget.setRowCount(tracks)
        self.trackTableWidget.setColumnCount(numberOfColumns)
        self.trackTableWidget.setHorizontalHeaderLabels(headers)
        i = 0
        for plot in self._wellPlotData.getLogTrackDatas():
            logger.debug("--populateTrackTable() plot_index:{0}, is_displayed:{1} ".format(plot.plot_index, plot.is_displayed))
            if (plot.plot_index != -1) and plot.is_displayed:
                trackLineEdit = QtGui.QLineEdit(str(plot.plot_index))
                titleLineEdit = QtGui.QLineEdit(plot.title)
                logNames = LogDao.getLogNamesCSV(plot._logs)
                curvesLineEdit = QtGui.QLineEdit(logNames)
                widthLineEdit = QtGui.QLineEdit(str(plot.track_width))
                gapLineEdit = QtGui.QLineEdit(str(plot.track_gap))
                
                twItem0 = QtGui.QTableWidgetItem(trackLineEdit.text())
                twItem0.setData(Qt.UserRole, str(plot.plot_index))
                #make non editable
                twItem0.setFlags(QtCore.Qt.ItemIsEnabled)
                
                twItem1 = QtGui.QTableWidgetItem(titleLineEdit.text())
                twItem1.setData(Qt.UserRole, str(plot.plot_index))
                
                twItem2 = QtGui.QTableWidgetItem(curvesLineEdit.text())
                twItem2.setData(Qt.UserRole, str(plot.plot_index))
                #make non editable
                twItem2.setFlags(QtCore.Qt.ItemIsEnabled)
                
                twItem3 = QtGui.QTableWidgetItem(widthLineEdit.text())
                twItem3.setData(Qt.UserRole, str(plot.plot_index))
                
                twItem4 = QtGui.QTableWidgetItem(gapLineEdit.text())
                twItem4.setData(Qt.UserRole, str(plot.plot_index))
                #row, column
                self.trackTableWidget.setItem(i,0, twItem0)
                self.trackTableWidget.setItem(i,1,  twItem1)
                self.trackTableWidget.setItem(i,2,  twItem2)
                self.trackTableWidget.setItem(i,3,  twItem3)
                self.trackTableWidget.setItem(i,4,  twItem4)
                i += 1

        self.trackTableWidget.itemChanged.connect(self.trackStyleChanged)


    def trackStyleChanged(self, twItem):
        self._trackStyleHander.trackStyleChanged(twItem)
        
    def populateCurveTable(self):
        logger.debug(">>populateCurveTable()")
        try: 
            self.curveTableWidget.itemChanged.disconnect(self.styleChanged)
        except TypeError as ex:
            logger.debug(str(ex))
        
        headers = LogPlotConstants.LOG_PLOT_CURVE_STYLE_HEADERS
        numberOfColumns = len(headers)
        self.curveTableWidget.clear()
        self.curveTableWidget.setSortingEnabled(False)
        logCount = 0
        countIds = []
        for plot in self._wellPlotData.getLogTrackDatas():
            for log in  plot.getLogs():
                #only want unique curve attributes
                if log.id not in countIds:
                    logCount += 1
                    countIds.append(log.id) 
        self.curveTableWidget.setRowCount(logCount)
        self.curveTableWidget.setColumnCount(numberOfColumns)
        self.curveTableWidget.setHorizontalHeaderLabels(headers)
        #only want unique curve attributes
        ids = []
        for i, plot in enumerate(self._wellPlotData.getLogTrackDatas()):
            j = 0
            for log in  plot.getLogs():
                if log.id not in ids:
                    #add one so starts at 1 not zero?
                    nameLineEdit = QtGui.QLineEdit(log.name)
                    typeLineEdit = QtGui.QLineEdit(log.log_type_name)
                    logType = LogType.getLogType(log.log_type_name)
                    unit = logType.getUnit()
                    unitsLineEdit = QtGui.QLineEdit(unit.getName())
                    trackLineEdit = QtGui.QLineEdit(str(plot.plot_index))
                    leftScaleLineEdit = QtGui.QLineEdit(str(log.log_plot_left))
                    rightScaleLineEdit = QtGui.QLineEdit(str(log.log_plot_right))
                    
                    logarithmicCheckBox = QtGui.QTableWidgetItem()
                    logarithmicCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    logarithmicCheckBox.setCheckState(log.is_logarithmic)
                    logarithmicCheckBox.setData(Qt.UserRole, str(log.id))

                    buttonQColor = ImageUtils.rbgToQColor(log.rgb)
                    #logger.debug("--populateCurveTable() "+log.rgb+" converted rgb: "+str(buttonQColor.getRgb()))
                    qColorButton = QColorButton()
                    qColorButton.setColor(buttonQColor)
                    qColorButton.setData(Qt.UserRole, str(log.id))
                    
                    opacityLineEdit = QtGui.QLineEdit(log.alpha)
                    widthLineEdit = QtGui.QLineEdit(str(log.line_width))
                    styleLineEdit = QtGui.QLineEdit(log.line_style)
                    pointSizeLineEdit = QtGui.QLineEdit(str(log.point_size))
                    pointStyleLineEdit = QtGui.QLineEdit(log.point_style)
                    pointsOn = QtGui.QTableWidgetItem()
                    pointsOn.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    pointsOn.setCheckState(log.log_plot_points_on)
                    pointsOn.setData(Qt.UserRole, str(log.id))
    
                    twItem0 = QtGui.QTableWidgetItem(nameLineEdit.text())
                    twItem0.setData(Qt.UserRole, str(log.id))
                    twItem1 = QtGui.QTableWidgetItem(typeLineEdit.text())
                    twItem1.setData(Qt.UserRole, str(log.id))
                    twItem2 = QtGui.QTableWidgetItem(unitsLineEdit.text())
                    twItem2.setData(Qt.UserRole, str(log.id))
                    twItem3 = QtGui.QTableWidgetItem(trackLineEdit.text())
                    twItem3.setData(Qt.UserRole, str(log.id))
                    twItem4 = QtGui.QTableWidgetItem(leftScaleLineEdit.text())
                    twItem4.setData(Qt.UserRole, str(log.id))
                    twItem5 = QtGui.QTableWidgetItem(rightScaleLineEdit.text())
                    twItem5.setData(Qt.UserRole, str(log.id))

                    
                    twItem8 = QtGui.QTableWidgetItem(opacityLineEdit.text())
                    twItem8.setData(Qt.UserRole, str(log.id))
                    twItem9 = QtGui.QTableWidgetItem(widthLineEdit.text())
                    twItem9.setData(Qt.UserRole, str(log.id))
                    twItem10 = QtGui.QTableWidgetItem(styleLineEdit.text())
                    twItem10.setData(Qt.UserRole, str(log.id))
                    twItem11 = QtGui.QTableWidgetItem(pointSizeLineEdit.text())
                    twItem11.setData(Qt.UserRole, str(log.id))
                    twItem12 = QtGui.QTableWidgetItem(pointStyleLineEdit.text())
                    twItem12.setData(Qt.UserRole, str(log.id))

                    
                    #row, column
                    self.curveTableWidget.setItem(j+i,0,  twItem0)
                    self.curveTableWidget.setItem(j+i,1,  twItem1)
                    self.curveTableWidget.setItem(j+i,2, twItem2)
                    self.curveTableWidget.setItem(j+i,3, twItem3)
                    self.curveTableWidget.setItem(j+i,4,  twItem4)
                    self.curveTableWidget.setItem(j+i,5, twItem5)
                    self.curveTableWidget.setItem(j+i,6, logarithmicCheckBox)
                    self.curveTableWidget.setCellWidget(j+i,7, qColorButton)
                    self.curveTableWidget.setItem(j+i,8, twItem8)
                    self.curveTableWidget.setItem(j+i,9, twItem9)
                    self.curveTableWidget.setItem(j+i,10, twItem10)
                    self.curveTableWidget.setItem(j+i,11, twItem11)
                    self.curveTableWidget.setItem(j+i,12, twItem12)
                    self.curveTableWidget.setItem(j+i,13, pointsOn)
    
                    #logger.debug("--populateCurveTable() j: "+str(j)+" i: "+str(i)) 
                    ids.append(log.id)  
                    j+=1 
        self.curveTableWidget.itemChanged.connect(self.curveStyleChanged)

    def curveStyleChanged(self, twItem):
        self._curveStyleHander.curveStyleChanged(twItem)
        
    def getLogFromId(self, id):
        for log in self._logs:
            if log.id == id:
                return log
        return None
        
    def styleChanged(self):

        self.styleDirty = True
        sender = self.sender()
        logger.debug("<<styleChanged() sender: "+str(sender))
        
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
        
    def handleApplyAllChkClicked(self, state): 
        if state == QtCore.Qt.Checked:
            self.trackGapUnitsComboBox.setEnabled(True)
            self.trackWidthUnitsComboBox.setEnabled(True)
            self.trackGapLineEdit.setEnabled(True)
            self.trackWidthLineEdit.setEnabled(True)
        else:
            self.trackGapUnitsComboBox.setEnabled(False)
            self.trackWidthUnitsComboBox.setEnabled(False)
            self.trackGapLineEdit.setEnabled(False)
            self.trackWidthLineEdit.setEnabled(False)
        
    def applyButtonClicked(self):
        ''' get all checked logs and put in dto '''
        logger.debug(">>applyButtonClicked()")
        #self.removeEmptyColumns()
        tickedPlotList = self._layoutHandler.getTickedPlotList(self.chkboxTableWidget)
        #check if all widths/gaps set
        self.handleTrackStyleAllWidthChanged()
        if self.arePlotsChanged(tickedPlotList) or self.styleDirty:
            self.notifyOnPlotsChanged()
        else:
            self.noChangeInPlots()

       
    def handleTrackStyleAllWidthChanged(self):
        if self.trackApplyAllCheckBox.isChecked():
            width = NumberUtils.straightStringToFloat(self.trackWidthLineEdit.text())
            gap = NumberUtils.straightStringToFloat(self.trackGapLineEdit.text())
            plotList = self._wellPlotData.getLogTrackDatas()
            for trackData in plotList:
                trackData.track_width = width
                trackData.track_gap = gap
            self.styleDirty = True

             
    def arePlotsChanged(self, tickedPlotList):
        changedPlotList = False
        for plot in self._initialPlotList:
            changedPlotList = False
            for tickedPlot in tickedPlotList:
                #logger.debug("--applyButtonClicked() initial plots index: "+str(plot.plot_index)+" ticked plots index: "+str(tickedPlot.plot_index))
                if plot.compareLogs(tickedPlot): 
                    changedPlotList = True
                    logger.debug("--arePlotsChanged() changedPlotList = True")
                    return changedPlotList
        
        return changedPlotList
            
    def notifyOnPlotsChanged(self):
        #TODO properties may have changed
        #self._wellPlotData.sub_plots = tickedPlotList 
        #reset initial list so if change again is seen as different
        self._initialPlotList = copy.deepcopy(self._wellPlotData.getLogTrackDatas())
        logger.debug("--notifyOnPlotsChanged() fire senderObject emit signal")
        #test
        for subPlotData in self._wellPlotData.sub_plots:
            logger.debug("--notifyOnPlotsChanged() plot_index:{0} track_width:{1} track_gap:{2}".format(subPlotData.plot_index, subPlotData.track_width, subPlotData.track_gap))
            for log in subPlotData._logs:
                logger.debug("--createCanvas id:{0}, name:{1}".format(log.id, log.name))
        #end test
        
        self.wellPlotSignals.logPlotSettingsModified.emit(self._wellPlotData)
        
    def noChangeInPlots(self):
        #set to initial state in case apply/change cycle done a few times
        #TODO properties may have changed
        self._wellPlotData.sub_plots = self._initialPlotList
        logger.debug("<<noChangeInPlots()")
        
    def getLayoutTableHeaders(self, tickableColumns):     
        headers = [PlottingConstants.LOG_LAYOUT_HEADER_NAME]
        #create n+1 headers where n = number of logs
        for i in range(tickableColumns):
            #zero indexed, add one so start is at one
            headers.append(str(i+1)) 
        return headers
        
    def refreshPlotTrackCurve(self):
        #refresh tables 
        logger.debug(">>refreshPlotTrackCurve()")
        self.populatePlotTab()
        self.populateTrackTab()
        self.populateCurveTable()
    
    def connectSlots(self):
        self.selectDefaultRadioButton.clicked.connect(self.selectDefaultLogsClicked)
        self.selectAllRadioButton.clicked.connect(self.selectAllLogsClicked)
        self.selectActiveRadioButton.clicked.connect(self.selectActiveLogsClicked)
        self.selectNoneRadioButton.clicked.connect(self.clearAllCheckboxes)
        self.addTrackPushButton.clicked.connect(self.addTrackButtonClicked)
        #connect apply button through button box
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.applyButtonClicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.applyButtonClicked)
        #QColorButton emits this signal on colour set method
        self.wellPlotSignals.logPlotCurveColourModified.connect(self.styleChanged)
        
    
            