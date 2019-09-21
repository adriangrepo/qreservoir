from __future__ import unicode_literals
import sys
import os
import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi

import pylab
import numpy as np


from PyQt4.QtGui import QSizePolicy
from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout
from globalvalues.constants.plottingconstants import PlottingConstants
import logging
from globalvalues.constants.wellplotconstants import WellPlotConstants

from qrutilities.imageutils import ImageUtils
from gui.util.wellplotutils import WellPlotUtils

from globalvalues.constants.wellconstants import WellConstants


logger = logging.getLogger('console')

class TrackCreator(object):
    #Plot with a shared y depth axis
    
    def __init__(self, well, parentWidget=None):
        #super(MultiLogCanvas, self).__init__(parentWidget)
        self.parentWidget = parentWidget
        #used for calculating widget height in pixels 1m=1 pixel
        if well.getMdLength() is None:
            self.mdLength = WellConstants.DEFAULT_MD_LENGTH
        else:
            self.mdLength = well.getMdLength()
        #self.setSeaborn()
        #self.generatePlot(logList, logPlotData)
        #self.setupSubplots(logList, logPlotData)
        #self.setFigureCanvas()
        #self.testaxes()
        #self.adjustFigure()
        
    def generatePlot(self, logTrackData, wellPlotData):

        pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
        pw.getAxis('left').setStyle(showValues=False)
        pw.getAxis('bottom').setStyle(showValues=False)
        #store data for header to retrieve
        pw.setData(Qt.UserRole, logTrackData)
        #see http://stackoverflow.com/questions/5036700/how-can-you-dynamically-create-variables-in-python-via-a-while-loop

        pw.show()
        
        logDict = {}
        axisDict = {}
        i = 0
        firstLogId = logTrackData.getLogs()[0]
        for log in logTrackData.getLogs():
            if i == 0:
                logDict[log.id] = pw.plotItem
                #hide the A button see https://groups.google.com/forum/#!topic/pyqtgraph/5cc0k6TG89k
                logDict[log.id].hideButtons()
                logDict[log.id].setRange(xRange=(log.log_plot_left,log.log_plot_right), padding=0, disableAutoRange = True)
                plt = logDict[log.id].plot(y = log.z_measure_data, x = log.log_data)
                rgbaColor = ImageUtils.rbgaToQColor(log.rgb, log.alpha)
                plt.setPen(rgbaColor)
            elif i == 1:
                logDict[log.id] = pg.ViewBox()
                logDict[log.id].setRange(xRange=(log.log_plot_left,log.log_plot_right), padding=0, disableAutoRange = True)
                logDict[firstLogId].scene().addItem(logDict[log.id])
                logDict[firstLogId].getAxis('left').linkToView(logDict[log.id])
                logDict[log.id].setXLink(logDict[firstLogId])
                
                plotCurveItem = pg.PlotCurveItem()
                plotCurveItem.setData(y = log.z_measure_data, x = log.log_data)
                rgbaColor = ImageUtils.rbgaToQColor(log.rgb, log.alpha)
                plotCurveItem.setPen(rgbaColor)
                logDict[log.id].addItem(plotCurveItem)
            else:
                logDict[log.id] = pg.ViewBox()
                logDict[log.id].setRange(xRange=(log.log_plot_left,log.log_plot_right), padding=0, disableAutoRange = True)
                axisDict[i]= pg.AxisItem('top')
                logDict[firstLogId].layout.addItem(axisDict[i])
                logDict[firstLogId].scene().addItem(logDict[log.id])
                axisDict[i].linkToView(logDict[log.id])
                logDict[log.id].setYLink(logDict[firstLogId])
                
                plotCurveItem = pg.PlotCurveItem()
                plotCurveItem.setData(y = log.z_measure_data, x = log.log_data)
                rgbaColor = ImageUtils.rbgaToQColor(log.rgb, log.alpha)
                plotCurveItem.setPen(rgbaColor)
                logDict[log.id].addItem(plotCurveItem)
            i += 1
            
        pw.invertY()
        pixelWidth = WellPlotUtils.convertmmToDPI(logTrackData.track_width)

        pw.setFixedWidth(pixelWidth)
        pw.setSizePolicy(QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Maximum)
        #pw.setLimits(yMin = 0, yMax=4000)
        logger.debug("-generatePlot() max min:{0}".format(self.mdLength))
        pw.setMaximumHeight(self.mdLength)
        pw.setMinimumHeight(self.mdLength)
        return pw
        

    def generateDomainPlot(self, domainTrackData, wellPlotData, domainStart, domainStop, domainStep):
        #self.cw = QtGui.QWidget()
        #l = QtGui.QVBoxLayout()
        #self.cw.setLayout(l)
        ## Switch to using white background and black foreground
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        ## giving the plots names allows us to link their axes together
        pw = pg.PlotWidget(name='Depth')  
        pw.setData(Qt.UserRole, domainTrackData)
        #l.addWidget(pw)
        '''
        ## Create an empty plot curve to be filled later, set its pen
        p1 = pw.plot()
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
        #pw.setLabel('left', wellPlotData.y_label, units='m')
        
        # get AxisItam, disable automatic SI prefix scaling on this axis.
        pw.getAxis('left').enableAutoSIPrefix(enable=False)
        pw.getAxis('bottom').setWidth(w=0.01)
        pw.getAxis('bottom').setStyle(showValues=False)

        pw.setRange(xRange=(0, 0),yRange=(0, domainStop), padding=0, disableAutoRange = True)
        #pw.setYRange(0, domainStop, padding=0, disableAutoRange = True)
        pw.invertY()
        pw.hideButtons()
        #return self.cw 
        pw.setFixedWidth(WellPlotConstants.WELL_PLOT_DOMAIN_TRACK_WIDTH)
        pw.setSizePolicy(QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Maximum)

        pw.setMaximumHeight(self.mdLength)
        pw.setMinimumHeight(self.mdLength)
        return pw
    
    
    def getWidget(self):
        return self.cw 
    

    
    '''        
    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(10, 10)

    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.p1.setXRange(minX, maxX, padding=0)    

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.p1.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < len(self.data1):
                self.label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), self.data1[index], self.data2[index]))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
    '''
    
## Create a subclass of GraphicsObject.
## The only required methods are paint() and boundingRect() 
## (see QGraphicsItem documentation)
class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()
    
    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())



#p1.scene().sigMouseMoved.connect(mouseMoved)


## Start Qt event loop unless running in interactive mode or using pyside.
#import sys
#if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#    app.exec_() 