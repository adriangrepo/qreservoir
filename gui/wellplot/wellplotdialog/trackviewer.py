from PyQt4.QtGui import QSplitter, QWidget, QScrollArea
from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4 import QtGui, QtCore

import pyqtgraph as pg
from gui.wellplot.track.trackcreator import TrackCreator
from gui.util.qt.widgetutils import WidgetUtils
from globalvalues.appsettings import AppSettings
from qrutilities.systemutils import SystemUtils

import quantities as pq
import logging
from gui.util.wellplotutils import WellPlotUtils
from db.core.well.welldao import WellDao
from gui.wellplot.track.trackwidget import TrackWidget
from gui.wellplot.track.domaintrackwidget import DomainTrackWidget

logger = logging.getLogger('console')

class TrackViewer(QWidget):
    '''
    classdocs
    '''
    def __init__(self, wellPlotData, parent = None):
        super(TrackViewer, self).__init__(parent)
        self.wellPlotData = wellPlotData
        self.parent = parent
        self.allTracks = [] 
        #store primary index track so scale widget can be linked easily
        self.primaryDomainTrackWidget = None
        self.setupUI()
        self.createCanvas()
        #self.setWidgetHeight()
        
    def setupUI(self):
        self.dataLayout = QtGui.QHBoxLayout()
        self.setLayout(self.dataLayout)
        self.setMaximumSize(16777215, 16777215)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,
            QtGui.QSizePolicy.Preferred)

        
        #if don't set a minimum, get matplotlib error when is very small
        #self.setMinimumHeight(self.getMinimumVerticalHeight())
    '''
    def getMinimumVerticalHeight(self):
        screenRect = SystemUtils.getScreenGeometry()
        #need to set a minimum size otherwise get matplotlib error when resizing to too small
        twentythOfScreen = int(round(screenRect.width()/40))
        return twentythOfScreen
    '''
        
    def createCanvas(self):
        logger.debug(">>createCanvas()")
        
        if len(self.wellPlotData.getLogTrackDatas()) > 0:
            WidgetUtils.removeWidgets(self.dataLayout)
            tracks = self.createPyqtgraphTracks()  
            for track in tracks:
                self.allTracks.append(track)
                self.dataLayout.addWidget(track)
            #if using Preferred size policy for this class need to stretch (Maximum doesn't require it)
            self.dataLayout.addStretch(1)
        else:
            logger.debug("--plotMultiLogs() Error: no logs to plot")

        
    def createPyqtgraphTracks(self):
        logger.debug(">>createPyqtgraphTracks() TODO use WellPlotUtils.createPlotDict")
        
        tracks = [] 
        if len(self.wellPlotData.getLogTrackDatas()) > 0:
            trackCreator = TrackCreator(self.wellPlotData.well)
            domainStart, domainStop, domainStep= WellPlotUtils.calculateStartStopStep(self.wellPlotData.getLogTrackDatas())
            i = 0
            isPrimaryDomainTrack = False
            for domainTrackData in self.wellPlotData.getZAxisDatas():  
                if i == 0:
                    isPrimaryDomainTrack = True
                else:
                    isPrimaryDomainTrack = False
                domainTrackWidget = DomainTrackWidget(self.wellPlotData.well, isPrimaryDomainTrack)
                domainTrackWidget.generateDomainPlot(domainTrackData, self.wellPlotData, domainStart, domainStop, domainStep)
                tracks.append(domainTrackWidget)
                if isPrimaryDomainTrack:
                    self.primaryDomainTrackWidget = domainTrackWidget
                i += 1
            
            for logTrackData in self.wellPlotData.getLogTrackDatas():  
                #plot = trackCreator.generatePlot(logTrackData, self.wellPlotData)
                #plots.append(plot)  
                trackWidget = TrackWidget(self.wellPlotData.well, self.parent)
                trackWidget.generatePlot(logTrackData, self.wellPlotData)
                tracks.append(trackWidget)  
        self.linkPyqtgraphYAxes(tracks)
        return tracks
    
    def linkPyqtgraphYAxes(self, plots):
        if len(plots)>1:
            firstPlot = plots[0]
            for plot in plots:
                plot.setYLink(firstPlot)
                
    def getMinWidgetWidth(self):
        totalWidth = 0
        for plot in self.allTracks:
            minimumSize = plot.minimumSize()
            totalWidth += minimumSize.width()
        return totalWidth
    
    def createSignals(self):
        #plotwid = pg.GraphicsWindow()
        self.proxy = pg.SignalProxy(self.ui.plotwid.scene().sigMouseMoved, rateLimit=30, slot=self.crosshair)
    
