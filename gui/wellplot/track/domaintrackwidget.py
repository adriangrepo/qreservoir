from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import QSize, Qt, pyqtSlot
import numpy as np
import pyqtgraph as pg
from pyqtgraph import PlotWidget, LinearRegionItem
import logging
from gui.util.wellplotutils import WellPlotUtils
from qrutilities.imageutils import ImageUtils
from globalvalues.constants.wellconstants import WellConstants
from gui.wellplot.wellplotdialog.wellplotviewbox import WellPlotViewBox
from globalvalues.constants.wellplotconstants import WellPlotConstants
from gui.signals.wellplotsignals import WellPlotSignals
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData

logger = logging.getLogger('console')

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class DomainTrackWidget(PlotWidget):
    '''
    classdocs
    '''

    def __init__(self, well, isPrimaryDomainTrack, parent=None):
        self.vb = WellPlotViewBox()
        super(DomainTrackWidget, self).__init__(parent, viewBox=self.vb)
        #self.vb = self.plotItem.vb
        #self.vb = WellPlotViewBox()
        self.yData = []
        self.isPrimaryDomainTrack = isPrimaryDomainTrack
        self.wellPlotSignals = WellPlotSignals()
        self._wellPlotData = None
        if well.getMdLength() is None:
            self.mdLength = WellConstants.DEFAULT_MD_LENGTH
        else:
            self.mdLength = well.getMdLength()
        
        #self.mdLength = well.mdstop
        self.connectSlots()

        
    def generateDomainPlot(self, domainTrackData, wellPlotData, domainStart, domainStop, domainStep):
        #self.cw = QtGui.QWidget()
        #l = QtGui.QVBoxLayout()
        #self.cw.setLayout(l)

        ## giving the plots names allows us to link their axes together
        self.setData(Qt.UserRole, domainTrackData)
        self._wellPlotData = wellPlotData
        #l.addWidget(pw)
        '''
        ## Create an empty plot curve to be filled later, set its pen
        p1 = self.plot()
        stopToStart = domainStop-domainStart
        numSamples = stopToStart/domainStep
        pseudoYData = []
        pseudoYData.append(domainStart)
        newValue = domainStart
        for i in range(numSamples):
            newValue +=domainStep
            pseudoYData.append(newValue)
            
        xData = [0]*numSamples
        assert len(pseudoYData)==len(xData)
        p1.setData(y = pseudoYData, x = xData)
        '''
        #self.setLabel('left', wellPlotData.y_label, units='m')
        
        # get AxisItam, disable automatic SI prefix scaling on this axis.
        self.getAxis('left').enableAutoSIPrefix(enable=False)
        self.getAxis('bottom').setWidth(w=0.01)
        self.getAxis('bottom').setStyle(showValues=False)

        #see https://groups.google.com/forum/#!msg/pyqtgraph/TxIj3mc49HE/jFVV2mLcNt4J
        #to override setrange so can set self.setXRange and Y range individually
        #self.setRange(xRange=(0, 0),yRange=(0, domainStop), padding=0, disableAutoRange = True)
        self.disableAutoRange('y')
        self.disableAutoRange('x')
        self.setXRange(0, 0, padding=0)
        self.setYRange(0, domainStop, padding=0)
        self.invertY()
        self.hideButtons()
        #return self.cw 
        self.setFixedWidth(WellPlotConstants.WELL_PLOT_DOMAIN_TRACK_WIDTH)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Expanding)



    def mouseMoveEvent(self, ev):
        pass
    
          
    def wheelEvent(self, ev):
        logger.debug(">>wheelEvent()")
        
        QtGui.QGraphicsView.wheelEvent(self, ev)
        if not self.mouseEnabled:
            return
        sc = 1.001 ** ev.delta()
        #self.scale *= sc
        #self.updateMatrix()
        self.scale(sc, sc)
        
        
    def mousePressEvent(self, ev):
        logger.debug(">>mousePressEvent()")
        QtGui.QGraphicsView.mousePressEvent(self, ev)

    def mouseReleaseEvent(self, ev):
        logger.debug(">>mouseReleaseEvent()")
        QtGui.QGraphicsView.mouseReleaseEvent(self, ev)
        
    @pyqtSlot(WellPlotData, LinearRegionItem)
    def regionUpdated(self, wellPlotData, region):
        #test first for signal settings preferences?
        assert self._wellPlotData is not None
        self.fitRangeToRegion(wellPlotData, region)
        
    #For the moment have left in - on slower machines may want to just enable this signal?
    @pyqtSlot(WellPlotData, LinearRegionItem)
    def regionUpdateFinished(self, wellPlotData, region):
        assert self._wellPlotData is not None
        self.fitRangeToRegion(wellPlotData, region)
        
    def fitRangeToRegion(self, wellPlotData, region):
        #ensure the region changed event was for this widget instance
        if (len(self._wellPlotData.uid) == 2) and (len(wellPlotData.uid) == 2):
            #ensure this object is associated with the plot object
            if self._wellPlotData.uid[0] == wellPlotData.uid[0] and self._wellPlotData.uid[1] == wellPlotData.uid[1]:
                if self.isPrimaryDomainTrack:
                    minY, maxY = region.getRegion()
                    self._wellPlotData.overview_region_start = minY
                    self._wellPlotData.overview_region_stop = maxY
                    self.setYRange(minY, maxY, padding=0)  
                    
    def connectSlots(self):
        self.wellPlotSignals.overviewRegionChangeFinished.connect(self.regionUpdateFinished)
        self.wellPlotSignals.overviewRegionChange.connect(self.regionUpdated)