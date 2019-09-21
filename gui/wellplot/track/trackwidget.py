from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import QSize, Qt
import numpy as np
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import logging
from gui.util.wellplotutils import WellPlotUtils
from qrutilities.imageutils import ImageUtils
from globalvalues.constants.wellconstants import WellConstants
from gui.wellplot.wellplotdialog.wellplotviewbox import WellPlotViewBox
logger = logging.getLogger('console')

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class TrackWidget(PlotWidget):
    '''
    classdocs
    '''

    def __init__(self, well, parent=None):
        self.vb = WellPlotViewBox()
        super(TrackWidget, self).__init__(parent, viewBox=self.vb)
        #self.vb = self.plotItem.vb
        #self.vb = WellPlotViewBox()
        self.parent = parent
        self.yData = []
        self.plotItemDict = {}
        
        if well.getMdLength() is None:
            self.mdLength = WellConstants.DEFAULT_MD_LENGTH
        else:
            self.mdLength = well.getMdLength()
        
        #self.mdLength = well.mdstop
        #cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)

        
    def generatePlot(self, logTrackData, wellPlotData):

        #pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
        self.getAxis('left').setStyle(showValues=False)
        self.getAxis('bottom').setStyle(showValues=False)
        #store data for header to retrieve
        self.setData(Qt.UserRole, logTrackData)
        #see http://stackoverflow.com/questions/5036700/how-can-you-dynamically-create-variables-in-python-via-a-while-loop

        self.show()
        #Reset the dict to empty
        self.plotItemDict = {}
        axisDict = {}
        i = 0
        firstLogId = logTrackData.getLogs()[0]
        for log in logTrackData.getLogs():
            if i == 0:
                self.yData = log.z_measure_data
                self.plotItemDict[log.id] = self.plotItem
                #hide the A button see https://groups.google.com/forum/#!topic/pyqtgraph/5cc0k6TG89k
                self.plotItemDict[log.id].hideButtons()
                self.plotItemDict[log.id].setRange(xRange=(log.log_plot_left,log.log_plot_right), padding=0, disableAutoRange = True)
                plt = self.plotItemDict[log.id].plot(y = log.z_measure_data, x = log.log_data)
                rgbaColor = ImageUtils.rbgaToQColor(log.rgb, log.alpha)
                plt.setPen(rgbaColor)
            elif i == 1:
                self.plotItemDict[log.id] = pg.ViewBox()
                self.plotItemDict[log.id].setRange(xRange=(log.log_plot_left,log.log_plot_right), padding=0, disableAutoRange = True)
                self.plotItemDict[firstLogId].scene().addItem(self.plotItemDict[log.id])
                self.plotItemDict[firstLogId].getAxis('left').linkToView(self.plotItemDict[log.id])
                self.plotItemDict[log.id].setXLink(self.plotItemDict[firstLogId])
                
                plotCurveItem = pg.PlotCurveItem()
                plotCurveItem.setData(y = log.z_measure_data, x = log.log_data)
                rgbaColor = ImageUtils.rbgaToQColor(log.rgb, log.alpha)
                plotCurveItem.setPen(rgbaColor)
                self.plotItemDict[log.id].addItem(plotCurveItem)
            else:
                self.plotItemDict[log.id] = pg.ViewBox()
                self.plotItemDict[log.id].setRange(xRange=(log.log_plot_left,log.log_plot_right), padding=0, disableAutoRange = True)
                axisDict[i]= pg.AxisItem('top')
                self.plotItemDict[firstLogId].layout.addItem(axisDict[i])
                self.plotItemDict[firstLogId].scene().addItem(self.plotItemDict[log.id])
                axisDict[i].linkToView(self.plotItemDict[log.id])
                self.plotItemDict[log.id].setYLink(self.plotItemDict[firstLogId])
                
                plotCurveItem = pg.PlotCurveItem()
                plotCurveItem.setData(y = log.z_measure_data, x = log.log_data)
                rgbaColor = ImageUtils.rbgaToQColor(log.rgb, log.alpha)
                plotCurveItem.setPen(rgbaColor)
                self.plotItemDict[log.id].addItem(plotCurveItem)
            i += 1
            
        self.invertY()
        pixelWidth = WellPlotUtils.convertmmToDPI(logTrackData.track_width)

        self.setFixedWidth(pixelWidth)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Expanding)
        #self.setLimits(yMin = 0, yMax=4000)
        

    
    def mouseMoveEvent(self, ev):
    #def mouseMoved(self, evt):
        #logger.debug(">>mouseMoved() {0}".format(ev))
        
        #pos = ev[0]
        #scenePos()
        if self.sceneBoundingRect().contains(ev.pos()):
            mousePoint = self.vb.mapSceneToView(ev.pos())
            index = int(mousePoint.y())
            if index > 0 and index < len(self.yData):
                #logger.debug("x:{0}, y:{1}".format(mousePoint.x(), self.yData[index]))
                pass
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
        
            
    def wheelEvent(self, ev):
        #logger.debug(">>wheelEvent()")
        self.parent.wheelEvent(ev)

    '''
    def mousePressEvent(self, ev):
        logger.debug(">>mousePressEvent()")
        QtGui.QGraphicsView.mousePressEvent(self, ev)

    def mouseReleaseEvent(self, ev):
        logger.debug(">>mouseReleaseEvent()")
        QtGui.QGraphicsView.mouseReleaseEvent(self, ev)
    '''
    