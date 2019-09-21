import copy
import logging

from PyQt4 import QtGui
from PyQt4.QtGui import (QDialog, QVBoxLayout, QHBoxLayout)

from globalvalues.constants.plottingconstants import PlottingConstants
from qrutilities.numberutils import NumberUtils
from gui.signals.wellplotsignals import WellPlotSignals
from db.core.log.logdao import LogDao
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from globalvalues.appsettings import AppSettings
from gui.widgets.itemwidget import ItemWidget
from gui.widgets.rangewidget import RangeWidget

from gui.wellplot.settings.ui_templatesettingsdialog import Ui_Dialog

from gui.wellplot.settings.scale.primaryztypewidget import PrimaryZTypeWidget
from gui.wellplot.settings.scale.tracksscalewidget import TracksScaleWidget
from gui.wellplot.settings.layout.widgets.tracklayoutwidget import TrackLayoutWidget
from gui.wellplot.settings.layout.widgets.overviewlayoutwidget import OverviewLayoutWidget
from gui.wellplot.settings.style.wellplotstylewidget import WellPlotStyleWidget
from gui.wellplot.settings.style.trackstylewidget import TrackStyleWidget
from gui.wellplot.settings.style.curvestylewidget import CurveStyleWidget
from gui.wellplot.settings.style.trackstylehandler import TrackStyleHandler
from gui.wellplot.settings.layout.widgets.overviewlayouthandler import OverviewLayoutHandler
from gui.wellplot.settings.style.wellplotstylehandler import WellPlotStyleHandler
from gui.wellplot.settings.style.curvestylehander import CurveStyleHandler


logger = logging.getLogger('console')

class TemplateSettingsDialog(QDialog, Ui_Dialog):
    '''
    Well plot settings
    '''
    MAGIC_SCALE = 500
    MAGIC_VERTICAL_SPACING = 10
    MAGIC_VERTICAL_SPACING_UNITS = "cm/m"
    
    
    def __init__(self, wellPlotData, selectedWell, logSet = None, parent=None):
        super(TemplateSettingsDialog, self).__init__(parent)
        assert selectedWell is not None
        
        self.setWindowTitle(self.__str__())
        self._well = selectedWell
        self._logSet = logSet
        self._wellPlotData = wellPlotData
        self._template = None
        if self._wellPlotData is not None:
            self._initialPlotList = copy.deepcopy(wellPlotData.getLogTrackDatas())
        self._logs = LogDao.getWellLogsOptSession(self._well, self._logSet)

        self.wellPlotSignals = WellPlotSignals()

        self.isDirty = False
        #added this flag so don't disconnect from slot while in the slot
        self.changeingLogTrack = False
        
        #For now use what is working
        self.useCheckboxLayout = False
        
        self._overviewLayoutWidget = None
        self._trackLayoutWidget = None
        self._wellPlotStyleWidget = None
        self._trackStyleWidget = None
        self._curveStyleWidget = None
        self._itemWidget = None
        #scale tab widgets
        self._tracksScaleWidget = None
        self._primaryZTypeWidget = None
        self._overviewRangeWidget = None
        
        self.setupUi(self)
        self.setupTabs()
        self.setTemplate()
        #set details after template as requires template to setup
        self.setupDetailsTab()
        self.connectSlots()
        self.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.setContentsMargins(0, 0, 0, 0)

    def __str__( self ):
        return "Well plot template settings"
    
    def setupTabs(self):
        
        self.setupLayoutTab()
        self.setupStyleTab()
        self.setupScaleTab()
        
    def setupDetailsTab(self):
        self._itemWidget = ItemWidget(self._template)
        self.detailsTabLayout.addWidget(self._itemWidget)
        
    def setupLayoutTab(self):
        self._trackLayoutWidget = TrackLayoutWidget(self._wellPlotData)
        hBoxLayout = QHBoxLayout()
        self.tracksLayoutTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(self._trackLayoutWidget)
        
        self._overviewLayoutWidget = OverviewLayoutWidget(self._wellPlotData)
        hBoxLayout2 = QHBoxLayout()
        self.overviewLayoutTab.setLayout(hBoxLayout2)
        hBoxLayout2.addWidget(self._overviewLayoutWidget)
        
    def setupStyleTab(self):
        self._wellPlotStyleWidget = WellPlotStyleWidget(self._wellPlotData)
        hBoxLayout = QHBoxLayout()
        self.wellPlotStyleTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(self._wellPlotStyleWidget)
        
        self._trackStyleWidget = TrackStyleWidget(self._wellPlotData, self)
        hBoxLayout = QHBoxLayout()
        self.trackStyleTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(self._trackStyleWidget)
        
        self._curveStyleWidget = CurveStyleWidget(self._wellPlotData)
        hBoxLayout = QHBoxLayout()
        self.curveStyleTab.setLayout(hBoxLayout)
        hBoxLayout.addWidget(self._curveStyleWidget)
        
    def setupScaleTab(self):
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
        self._tracksScaleWidget = TracksScaleWidget(verticalSpacing, spacingUnits, scale, primaryZAxis)
        tracksLayout.addWidget(self._tracksScaleWidget)
        self.tracksGroupBox.setLayout(tracksLayout)
        
    def getVerticalSpacing(self):
        return self.MAGIC_VERTICAL_SPACING
    
    def getVerticalSpacingUnits(self):
        ''' in units per unit eg inches/second '''
        return self.MAGIC_VERTICAL_SPACING_UNITS
    
    def getScale(self):
        return self.MAGIC_SCALE
        
    def setTemplate(self):
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
    '''   
    def reject(self):
        logger.debug("reject")
        return True
    '''
        
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
        

 
    def getLogFromId(self, id):
        for log in self._logs:
            if log.id == id:
                return log
        return None
        
    def styleChanged(self):

        self.isDirty = True
        sender = self.sender()
        logger.debug("<<styleChanged() sender: "+str(sender))
        
    def applyButtonClicked(self):
        ''' get all checked logs and put in dto '''
        logger.debug(">>applyButtonClicked()")
        
        self.handleTrackStyleAllWidthChanged()
        if self.checkIsDirty():
            self.notifyOnPlotsChanged()
        else:
            self.noChangeInPlots()

    def checkIsDirty(self):
        #ugly - other option is set parent to dirty
        if self.isDirty:
            return True
        elif self._overviewLayoutWidget.isDirty:
            overviewLayoutHandler = OverviewLayoutHandler()
            overviewLayoutHandler.saveDataState(self._wellPlotData, self._overviewLayoutWidget)
            return True
        elif self._trackLayoutWidget.isDirty:
            return True
        elif self._wellPlotStyleWidget.isDirty:
            wellPlotStyleHandler = WellPlotStyleHandler()
            wellPlotStyleHandler.saveDataState(self._wellPlotData, self._wellPlotStyleWidget)
            return True
        elif self._trackStyleWidget.isDirty:
            trackStyleHandler = TrackStyleHandler()
            trackStyleHandler.saveDataState(self._wellPlotData, self._trackStyleWidget)
            return True
        elif self._curveStyleWidget.isDirty:
            curveStyleHandler = CurveStyleHandler()
            curveStyleHandler.saveDataState(self._wellPlotData, self._curveStyleWidget)
            return True
        elif self._itemWidget.isDirty:
            return True
        #TODO link up isDirty to events
        elif self._tracksScaleWidget.isDirty:
            return True
        elif self._primaryZTypeWidget.isDirty:
            return True
        #do we need to change anything wrt overview?
        #elif self._overviewRangeWidget.isDirty:
        #    return True
        else:
            return False
        
    def handleTrackStyleAllWidthChanged(self):
        if self._trackStyleWidget.trackApplyAllCheckBox.isChecked():
            width = NumberUtils.straightStringToFloat(self._trackStyleWidget.trackWidthLineEdit.text())
            gap = NumberUtils.straightStringToFloat(self._trackStyleWidget.trackGapLineEdit.text())
            plotList = self._wellPlotData.getLogTrackDatas()
            for trackData in plotList:
                trackData.track_width = width
                trackData.track_gap = gap
            self.isDirty = True


            
    def notifyOnPlotsChanged(self):
        #TODO properties may have changed
        #self._wellPlotData.sub_plots = tickedPlotList 
        #reset initial list so if change again is seen as different
        self._initialPlotList = copy.deepcopy(self._wellPlotData.getLogTrackDatas())
        logger.debug("--notifyOnPlotsChanged() fire senderObject emit signal")

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
        if self._template is not None and self._itemWidget is not None:
            self._itemWidget.nameLineEdit.setText(self._template.name)
            self._itemWidget.classLineEdit.setText(self._template.typeName)
        else:
            logger.error("Template or Details widget is None")
            if AppSettings.isDebugMode:
                raise ValueError
            
    
    def connectSlots(self):
        #connect apply button through button box
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.applyButtonClicked)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.applyButtonClicked)
        #QColorButton emits this signal on colour set method


    
            