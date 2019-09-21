from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import QSize, Qt, pyqtSlot
from PyQt4.QtGui import QSplitter

import numpy as np
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import logging
from gui.util.wellplotutils import WellPlotUtils
from qrutilities.imageutils import ImageUtils
from globalvalues.constants.wellconstants import WellConstants
from qrutilities.systemutils import SystemUtils

from gui.signals.wellplotsignals import WellPlotSignals
from gui.wellplot.overview.overviewwidgethandler import OverviewWidgetHandler


logger = logging.getLogger('console')

class OverviewWidget(PlotWidget):
    '''
    Scale widget used as a slider and zoom, narrow track with a default log
    '''
    #TODO, calculate the required offset for font and screen dpi
    #-40 works ok for this screen and font
    TICK_TEXT_OFFSET = 0


    def __init__(self, wellPlotData, trackViewer, wellPlotPGSplitter, parent=None):
        super(OverviewWidget, self).__init__(parent)
        #used to update range of all plots
        #self.primaryDomainWidget = trackViewer.primaryDomainTrackWidget
        self.wellPlotPGSplitter = wellPlotPGSplitter
        self.trackViewer = trackViewer
        self.wellPlotSignals = WellPlotSignals()
        self._wellPlotData = wellPlotData
        self._region = None
        self._screenDPI = SystemUtils.getScreenDPI()
        logger.debug("--__init__() wellPlotData.well.getMdLength():{0}".format(wellPlotData.well.getMdLength()))
        #if wellPlotData.well.getMdLength() is None:

        #else:
        #self.mdLength = wellPlotData.well.getMdLength()
            

        #cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        

        
    def getXYDataWithinRange(self, log, yDataRange):
        min = yDataRange[0]
        max = yDataRange[1]
        yData = log.z_measure_data
           
        
    def generatePlot(self, logTrackData, log, xData, yData):

        #pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
        self.getAxis('left').setStyle(tickTextOffset = self.TICK_TEXT_OFFSET, showValues=True)
        self.getAxis('bottom').setStyle(showValues=False)
        #store data for header to retrieve
        self.setData(Qt.UserRole, logTrackData)
        #see http://stackoverflow.com/questions/5036700/how-can-you-dynamically-create-variables-in-python-via-a-while-loop

        self.show()
        
        firstLogId = logTrackData.getLogs()[0]
        log = logTrackData.getLogs()[0]

        #note PlotItem is coming from parent
        #hide the A button see https://groups.google.com/forum/#!topic/pyqtgraph/5cc0k6TG89k
        self.plotItem.hideButtons()
        self.plotItem.setRange(xRange=(log.log_plot_left,log.log_plot_right), padding=0, disableAutoRange = True)
        plt = self.plotItem.plot(y = yData, x = xData)
        #temp set alpga to semi tranparent
        rgbaColor = ImageUtils.rbgaToQColor(log.rgb, 100)
        plt.setPen(rgbaColor)
        
        self.invertY()
        pixelWidth = WellPlotUtils.convertmmToDPI(logTrackData.track_width)

        self.setFixedWidth(pixelWidth)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Expanding)
        #self.setLimits(yMin = 0, yMax=4000)

        
        #self.proxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoveEvent)
        #self.plotItem.sigRangeChanged.connect(self.updateRegion)
        
        #region
        self._region = pg.LinearRegionItem(orientation=pg.LinearRegionItem.Horizontal)
        #The Z value decides the stacking order of sibling (neighboring) items. High Z = on top
        self._region.setZValue(10)
        self.setInitialRange()
        self.plotItem.addItem(self._region)
        #send signal to slots that range has been set
        #if if remove finished signal need to enable this instead
        #self.updateOnRegionChange()
        self.updateOnRegionChangeFinished()
        self.connectSlots()

        
    def setInitialRange(self):
        overviewWidgetHandler = OverviewWidgetHandler()
        regionStart, regionStop = overviewWidgetHandler.calcMDRegionStartStop(self._wellPlotData.well.mdstart, self._wellPlotData.well.mdstop)
        self._region.setRegion([regionStart, regionStop])
        
        self._wellPlotData.overview_region_start = regionStart
        self._wellPlotData.overview_region_stop = regionStop
        
    '''
    def update():
        global data, curve, times, lr
        connect = np.ones(N*2, dtype=np.uint32)
        connect[1::2] = 0
        start, stop = lr.getRegion()
        connect[::2][times < start] = 0
        connect[::2][times > stop] = 0
        curve.setData(x=data[:,0], y=data[:,1], connect=connect)
    '''


    def updateOnRegionChange(self):
        logger.debug(">>updateOnRegionChangeFinished() self._wellPlotData.uid:{0}".format(self._wellPlotData))
        self.wellPlotSignals.overviewRegionChange.emit(self._wellPlotData, self._region)

                
    def updateOnRegionChangeFinished(self):
        logger.debug(">>updateOnRegionChangeFinished() self._wellPlotData.uid:{0}".format(self._wellPlotData))
        self.wellPlotSignals.overviewRegionChangeFinished.emit(self._wellPlotData, self._region)

    
    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self._region.setRegion(rgn)
          
    #self.wellPlotSignals.toolbarZoomInVertical
    @pyqtSlot()
    def zoomInVertical(self):
        logger.debug(">>zoomInVertical")
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomInMinMax(self._region)
        self._region.setRegion([zoomedMinY, zoomedMaxY])

    #self.wellPlotSignals.toolbarZoomInVertical
    @pyqtSlot()
    def zoomOutVertical(self):
        logger.debug(">>zoomOutVertical")
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomOutMinMax(self._region)
        self._region.setRegion([zoomedMinY, zoomedMaxY]) 
        
    '''
    #Revisit implementing at some stage
    @pyqtSlot()
    def panModeSelected(self):
        #connects up mouse listener - works out where mouse is relative to Y axis
        #as hold LMB and move mouse, updates the region
        #will need to connect to pointModeSelected and crossHairsModeSelected
        #just to turn off mouse listening
    '''

    def connectSlots(self):
        self._region.sigRegionChanged.connect(self.updateOnRegionChange)
        self._region.sigRegionChangeFinished.connect(self.updateOnRegionChangeFinished)
        self.wellPlotSignals.toolbarZoomInVertical.connect(self.zoomInVertical)
        self.wellPlotSignals.toolbarZoomOutVertical.connect(self.zoomOutVertical)

 