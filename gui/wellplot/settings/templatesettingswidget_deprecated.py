import copy
import logging

from PyQt4 import QtGui
from PyQt4.QtGui import (QDialog, QVBoxLayout, QHBoxLayout, QWidget)

from globalvalues.constants.plottingconstants import PlottingConstants
from qrutilities.numberutils import NumberUtils
from gui.signals.wellplotsignals import WellPlotSignals
from db.core.log.logdao import LogDao
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from globalvalues.appsettings import AppSettings

from gui.widgets.rangewidget import RangeWidget



from gui.wellplot.settings.style.trackstylehandler import TrackStyleHandler
from gui.wellplot.settings.style.plotstylehandler import PlotStyleHandler
from gui.wellplot.settings.style.curvestylehander import CurveStyleHandler
from gui.wellplot.settings.scale.primaryztypewidget import PrimaryZTypeWidget
from gui.wellplot.settings.scale.scalewidget import TracksScaleWidget
from gui.wellplot.settings.layout.widgets.tracklayoutwidget import TrackLayoutWidget
from gui.wellplot.settings.layout.widgets.overviewlayoutwidget import OverviewLayoutWidget
from gui.wellplot.settings.style.wellplotstylewidget import WellPlotStyleWidget
from gui.wellplot.settings.style.trackstylewidget import TrackStyleWidget
from gui.wellplot.settings.style.curvestylewidget import CurveStyleWidget
from gui.wellplot.settings.ui_templatesettingswidget import Ui_TemplateSettingsWidget
from PyQt4.QtCore import Qt
from gui.wellplot.settings.layout.widgets.checkboxtable.layouthandler import LayoutHandler
from gui.widgets.itemwidget import ItemWidget

logger = logging.getLogger('console')

class TemplateSettingsWidget(QWidget, Ui_TemplateSettingsWidget):
    '''
    Well plot settings
    '''
    def __init__(self, wellPlotData, selectedWell, logSet = None, parent=None):
        super(TemplateSettingsWidget, self).__init__(parent)
        assert selectedWell is not None
        #see http://stackoverflow.com/questions/12280815/pyqt-window-focus
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.__str__())
        self._well = selectedWell
        self._logSet = logSet
        self._wellPlotData = wellPlotData
        self._template = None
        if self._wellPlotData is not None:
            self._initialPlotList = copy.deepcopy(wellPlotData.getLogTrackDatas())
        self._logs = LogDao.getWellLogsOptSession(self._well, self._logSet)
        self.layoutHandler = LayoutHandler(self)


        self._overviewRangeWidget = None
        self._trackRangeWidget = None
        self._primaryZTypeWidget = None
        self.wellPlotSignals = WellPlotSignals()

        self.styleDirty = False
        #added this flag so don't disconnect from slot while in the slot
        self.changeingLogTrack = False
        self.setupUi(self)
        self.setupTabs()
        self.setTemplate()
        self.connectSlots()
        self.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.setContentsMargins(0, 0, 0, 0)

    def __str__( self ):
        return "Well plot template settings"
    
    def setupTabs(self):
        self.setupDetailsTab()
        self.setupLayoutTab()
        self.setupStyleTab()
        self.setupScaleTab()
        
    def setupDetailsTab(self):
        self._detailsWidget = ItemWidget()
        self.detailsTabLayout.addWidget(self._detailsWidget)
        
    def setupLayoutTab(self):
        trackLayoutWidget = TrackLayoutWidget(self._wellPlotData)
        hBoxLayout = QHBoxLayout()
        self.tracksLayoutTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(trackLayoutWidget)
        
        overviewLayoutWidget = OverviewLayoutWidget(self._wellPlotData)
        hBoxLayout2 = QHBoxLayout()
        self.overviewLayoutTab.setLayout(hBoxLayout2)
        hBoxLayout2.addWidget(overviewLayoutWidget)
        
    def setupStyleTab(self):
        wellPlotStyleWidget = WellPlotStyleWidget(self._wellPlotData)
        hBoxLayout = QHBoxLayout()
        self.wellPlotStyleTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(wellPlotStyleWidget)
        
        trackStyleWidget = TrackStyleWidget(self._wellPlotData, self)
        hBoxLayout = QHBoxLayout()
        self.trackStyleTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(trackStyleWidget)
        
        curveStyleWidget = CurveStyleWidget(self._wellPlotData)
        hBoxLayout = QHBoxLayout()
        self.curveStyleTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(curveStyleWidget)
        
    def setupScaleTab(self):
        if self._wellPlotData is not None:
            zAxisDatas = self._wellPlotData.getZAxisDatas()
            primaryZAxis = None
            if zAxisDatas is None:
                logger.error("No Z Axis track in well plot data id:{0}".format(self._wellPlotData.uid))
                if AppSettings.isDebugMode:
                    raise ValueError
            else:
                for item in zAxisDatas:
                    if item.is_primary:
                        primaryZAxis = item
                        
            if primaryZAxis is None:
                logger.error("No Primary Z Axis track in well plot data id:{0}".format(self._wellPlotData.uid))
                if AppSettings.isDebugMode:
                    raise ValueError
                       
            self._primaryZTypeWidget = PrimaryZTypeWidget(primaryZAxis.z_axis_type, primaryZAxis.z_axis_reference_level)
            rangeType = self._wellPlotData.tracks_range_type
            
            primaryZLayout = QVBoxLayout()
            primaryZLayout.addWidget(self._primaryZTypeWidget)
            self.tracksRangePlaceholderWidget.setLayout(primaryZLayout)
    
            overviewLayout = QVBoxLayout()
            self._overviewRangeWidget = RangeWidget(rangeType, primaryZAxis, self._well, self.scaleTab)
            overviewLayout.addWidget(self._overviewRangeWidget)
            self.overviewGroupBox.setLayout(overviewLayout)
            
            tracksLayout = QVBoxLayout()
            verticalSpacing = self.getVerticalSpacing()
            spacingUnits = self.getVerticalSpacingUnits()
            scale = self.getScale()
            self._scaleWidget = TracksScaleWidget(verticalSpacing, spacingUnits, scale, primaryZAxis)
            tracksLayout.addWidget(self._scaleWidget)
            self.tracksGroupBox.setLayout(tracksLayout)
        
    def getVerticalSpacing(self):
        return 10
    
    def getVerticalSpacingUnits(self):
        ''' in units per unit eg inches/second '''
        return "cm/m"
    
    def getScale(self):
        return 500
        
    def setTemplate(self):
        if self._wellPlotData is not None:
            template_uid = self._wellPlotData.template_uid
            self._template = WellPlotTemplateDao.getWellPlotTemplateFromUid(template_uid)
        
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
                               
    def accept(self):
        logger.debug(">>accept()")
        self.close()
        
    def reject(self):
        logger.debug("reject")
        
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
        
    '''
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
    '''
    



        
    

        
    def getLogFromId(self, id):
        for log in self._logs:
            if log.id == id:
                return log
        return None
        
    def styleChanged(self):

        self.styleDirty = True
        sender = self.sender()
        logger.debug("<<styleChanged() sender: "+str(sender))
        

        

        
    def applyButtonClicked(self):
        ''' get all checked logs and put in dto '''
        logger.debug(">>applyButtonClicked()")
        
        self.handleTrackStyleAllWidthChanged()
        if self.styleDirty:
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
        

        
    def populateDetailsTab(self):
        if self._template is not None and self._detailsWidget is not None:
            self._detailsWidget.nameLineEdit.setText(self._template.name)
            self._detailsWidget.classLineEdit.setText(self._template.typeName)
        else:
            logger.error("Template or Details widget is None")
            if AppSettings.isDebugMode:
                raise ValueError
            
    '''
    def populateScaleTracksTab(self):
        if self._template is not None:
            if self._trackRangeWidget is not None:
                domainTrackPriority = self._wellPlotData.getZMeasureTrackPriority()
                self._trackRangeWidget.setMeasurementTypeData(domainTrackPriority)
                self._trackRangeWidget.setRadioButtons(self._wellPlotData.tracks_range_type)
                self._trackRangeWidget.setIntialRangeValues(self._wellPlotData.tracks_range_type)
            else:
                logger.debug("TrackRangeWidget is None")
                if AppSettings.isDebugMode:
                    raise ValueError
        else:
            logger.debug("Template is None")
            if AppSettings.isDebugMode:
                raise ValueError
            

    def populateScaleOverviewTab(self):
        if self._template is not None:
            if self._overviewRangeWidget is not None:
                domainTrackPriority = self._wellPlotData.getZMeasureTrackPriority()
                self._overviewRangeWidget.setMeasurementTypeData(domainTrackPriority)
                self._overviewRangeWidget.setRadioButtons(self._wellPlotData.overview_range_type)
                self._overviewRangeWidget.setIntialRangeValues(self._wellPlotData.overview_range_type)
            else:
                logger.debug("OverviewRangeWidget is None")
                if AppSettings.isDebugMode:
                    raise ValueError
        else:
            logger.debug("Template is None")
            if AppSettings.isDebugMode:
                raise ValueError
    '''
    
    def connectSlots(self):
        #connect apply button through button box
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.applyButtonClicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.applyButtonClicked)
        #QColorButton emits this signal on colour set method
        self.wellPlotSignals.logPlotCurveColourModified.connect(self.styleChanged)

    
            