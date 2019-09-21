from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot

from views.core import centraltabwidget
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData
from gui.wellplot.toolbar import logsettingstoolbar
from gui.signals.wellplotsignals import WellPlotSignals
from gui.wellplot.wellplotdialog.uiwellplotpg import UIWellPlotPG
from gui.wellplot.wellplotdialog.headerviewer import HeaderViewer
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess

import logging
from gui.wellplot.wellplotdialog.trackviewer import TrackViewer

from gui.wellplot.overview.overviewwidget import OverviewWidget
from gui.util.qt.widgetutils import WidgetUtils

logger = logging.getLogger('console')

class WellPlotPG(UIWellPlotPG):
    '''Main well plot class, extends  UIWellPlotPG'''
    
    def __init__(self, logs, well, template, wellPlotData = None, logSet = None, parent = None):
        '''Logs are a selected logs that are plotting
        All logs can be accessed via '''
        super(WellPlotPG, self).__init__(parent)
        if (logs is not None) and (well is not None) and (template is not None):

            self._well = well
            self._logSet = logSet
            self._logs = logs
            self._template = template
            self.trackViewer = None
            self.headerViewer = None
            self.overviewWidget = None
            self.canvas = None
            self.depthPlot = None
            self.headerPlot = None
            self.centralWidget = centraltabwidget.CentralTabWidget()
            #id(self) returns the 'hash' of this object
            self.uid = (self.centralWidget.count(), id(self))      
            self.wellPlotSignals = WellPlotSignals()
            self.setupUI()
            self.createTabView()
            self.connectSlots()
            if wellPlotData is None:
                self.wellPlotData = self.generateInitialData()
            else:
                self.wellPlotData = wellPlotData
            
            self.plotMultiLogs(self.wellPlotData)
          
            
            self.createToolWidget()
        else:
            logger.error("Can't open well plot, input data is None: logs:{0}, well:{1}, template:{2}".format(logs, well, template))
         
    def generateInitialData(self):
        wellPlotModelAccess = WellPlotModelAccess()
        wellPlotData = wellPlotModelAccess.createWellPlotData(self._logs, self.uid, self._well, self._template, self._logSet)
        return wellPlotData
        
    def plotMultiLogs(self, wellPlotData):
        if (wellPlotData != None):
            self.clearWidgets(wellPlotData)
            
            self.mainWidget.setLogPlotData(wellPlotData)
            self.trackViewer = TrackViewer(wellPlotData, parent = self.scrollArea)
            self.scrollArea.setWidget(self.trackViewer)
            self.headerViewer = HeaderViewer(wellPlotData = wellPlotData, logTracks = self.trackViewer.allTracks)
            self.headerScrollArea.setWidget(self.headerViewer)
        
            self.setSplitterStretch()
            #create overview here so is recreated on redraw signal
            self.createOverviewWidget()
            
    def clearWidgets(self, wellPlotData):
        '''delete everything if existing'''
        if self.trackViewer is not None:
            WidgetUtils.removeWidgets(self.scrollArea.layout())        
            self.trackViewer = None
            self.wellPlotData = wellPlotData
            
        if self.headerViewer is not None:
            WidgetUtils.removeWidgets(self.headerScrollArea.layout())
            self.headerViewer = None

        if (self.overviewWidget is not None) and (self.scaleWidgetLayout is not None):
            WidgetUtils.removeWidgets(self.scaleWidgetLayout)
            self.overviewWidget = None
        
    def setSplitterStretch(self):
        #totalWidth = self.trackViewer.getMinWidgetWidth()
        trackHeight = self.trackViewer.geometry().height()
        headerHeight = self.headerViewer.geometry().height()
        #self.trackViewer.setMinimumSize(totalWidth, trackHeight)
        if headerHeight > 0:
            ratio = int((trackHeight+headerHeight)/headerHeight)
        else:
            ratio = 10
        logger.debug("trackHeight:{0} headerHeight:{1} ratio:{2}".format(trackHeight,headerHeight, ratio))
        self.splitter.setStretchFactor(1, ratio)
        
        
    def connectSlots(self):
        logger.debug(">>connectSlots")
        self.wellPlotSignals.logPlotSettingsModified.connect(self.replotLogs)
    
    @pyqtSlot(WellPlotData)
    def replotLogs(self, wellPlotData):
        #check uid's before accessing them, where uid is a (number widgets in central widget, id) tuple
        logger.debug("--replotLogs() len(self.uid):{0}, len(logPlotData.uid):{1}".format(len(self.uid), len(wellPlotData.uid)))
        if (len(self.uid) == 2) and (len(wellPlotData.uid) == 2):
            #ensure this object is associated with the plot object
            if self.uid[0] == wellPlotData.uid[0] and self.uid[1] == wellPlotData.uid[1]:
                logger.debug("--replotLogs() match found uid: "+str(self.uid[0]))
                self.plotMultiLogs(wellPlotData)

    def spacePlots(self, bottomLayout):
        rightSpacer = QtGui.QWidget()
        rightSpacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #topLayout.addWidget(rightSpacer)
        bottomLayout.addWidget(rightSpacer)
        #self.topWidget.setLayout(topLayout)
        self.dataWidget.setLayout(bottomLayout)

    def createTabView(self):
        self.mainWidget.setData(self.uid)
        self.centralWidget.addTab(self.mainWidget, "Well plot "+str(self.uid[0]))

    def createToolWidget(self):
        logger.debug(">>createToolWidget()")
        if len(self._logs) > 0:
            toolbar = logsettingstoolbar.LogSettingsToolbar()
            #toolbar.setData(self._well, self._logSet, self.canvas, self.depthPlot, self.headerPlot)
            toolbar.emitShowToolbarSignal()
            logger.debug("<<createToolWidget() toolbar created")
            

    def createOverviewWidget(self):
        #TODO find longest GR track and use as default
        #for logTrackData in self.wellPlotData.log_track_datas:
        #   logTrackData.getLogs()
        #also for Active logs raises index error
        logTrackDatas= self.wellPlotData.getLogTrackDatas()
        if len(logTrackDatas) > 0:
            logTrackData = logTrackDatas[0]  
            logger.debug("--createOverviewWidget() self.wellPlotData.uid:{0}".format(self.wellPlotData.uid))
            self.overviewWidget = OverviewWidget(self.wellPlotData, self.trackViewer, wellPlotPGSplitter = self.splitter)
            #revise these 3 lines to log want to plot and data range
            log = logTrackData.getLogs()[0]
            yData = log.z_measure_data
            xData = log.log_data
            
            self.overviewWidget.generatePlot(logTrackData, log, xData, yData)
            self.scaleWidgetLayout.addWidget(self.overviewWidget)
            #scaleWidget.primaryDomainWidget = self.trackViewer.primaryDomainTrackWidget
        else:
            logger.debug("No log track data, cannot create scale widget, ")

            
    

    
    

      