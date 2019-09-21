from __future__ import unicode_literals


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
from matplotlib.backends import qt4_compat
from db.windows.wellplot.zaxistrackdata.zaxisdata import ZAxisData
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
#if use_pyside:
#    from PySide import QtGui, QtCore
#else:


from PyQt4.QtGui import QSizePolicy


import logging

logger = logging.getLogger('console')

class DepthAxis(FigureCanvas):
    '''
    classdocs
    '''


    def __init__(self, wellPlotData=None, parentWidget=None):
        #self.parent = parent
        self.setupFirstPlot(wellPlotData, parentWidget)
        self.adjustFigure()

    def adjustFigure(self):
        #subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
        self.figure.subplots_adjust(left=0.85, bottom=0.001, right=.999, top=.999, wspace=0.0001, hspace=0.0001)
        #self.figure.subplots_adjust(left=.85, bottom=0.01, hspace=0)
        

        
    def setupFirstPlot(self, logPlotData, parentWidget):
        assert len(logPlotData.depth_sub_plots) >0
        depth1 = logPlotData.depth_sub_plots[0]
        self.figure = Figure(figsize=(depth1.depthAxisXWidth, logPlotData.widget_height), dpi=logPlotData.dpi)
        self.axes = self.figure.add_subplot(1, 1, 1)
        #self.axes.set_title(logPlotData.title)
        #self.axes.set_ylabel(logPlotData.yLabel)

        
        self.axes.invert_yaxis()
        if len(logPlotData.getLogTrackDatas())>0:
            #TODO handle variable log steps, sampling and depth extents
            plots = logPlotData.getLogTrackDatas()
            logsInFirstPlot = plots[0].getLogs()
            if (logsInFirstPlot != None ) and (len(logsInFirstPlot)>0):
                firstLog = logsInFirstPlot[0]
                #create zero array for x data
                xData = np.zeros(len(firstLog.z_measure_data))
                self.axes.plot(xData, firstLog.z_measure_data)
                #self.axes.set_xticklabels([])
                self.axes.get_xaxis().set_visible(False)
                self.axes.set_xlim(0, 0)
                self.axes.hold(logPlotData.hold)
                logger.debug("--setupFirstPlot() dto max: "+str(depth1.depthAxisPlotMax)+" min: "+str(depth1.depthAxisPlotMin))
                self.axes.set_ylim(depth1.depthAxisPlotMax, depth1.depthAxisPlotMin)
                #test
                ymin, ymax = self.axes.get_ylim()
                logger.debug("--setupFirstPlot() axes ymin: "+str(ymin)+" ymax: "+str(ymax))
                #end test
                self.step = 1 # axis units
                self.scale = 1e3 # conversion betweeen scrolling units and axis units
                #depthSubPlotData = ZAxisData()
                depth1.depthAxis = self.axes
                #logPlotData.getDepthSubPlots().append(depthSubPlotData)
        
        
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parentWidget)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)