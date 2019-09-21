from __future__ import unicode_literals

from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as tic

from matplotlib.backends import qt4_compat
from globalvalues.appsettings import AppSettings
from qrutilities.arrayutils import ArrayUtils
from qrutilities.imageutils import ImageUtils
from globalvalues.constants.wellplotconstants import WellPlotConstants

#import seaborn as sns
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
#if use_pyside:
#    from PySide import QtGui, QtCore
#else:

from PyQt4.QtGui import QSizePolicy
from PyQt4.QtCore import QSize

import logging

logger = logging.getLogger('console')

class MultiLogCanvas(FigureCanvas):
    #Plot with a shared y depth axis
    
    def __init__(self, wellPlotData, parentWidget=None):
        assert wellPlotData != None
        #super(MultiLogCanvas, self).__init__(parentWidget)
        self.axes = None
        self.parentWidget = parentWidget
        #self.setSeaborn()
        self.logPlotData = wellPlotData
        self.createFigure(wellPlotData)
        self.createPlots(wellPlotData)
        self.setFigure()
        #self.testaxes(wellPlotData)
        self.adjustFigure()
        
    def createFigure(self, logPlotData):
        '''if xmin == xmax:
        xmax += np.finfo(type(xmax)).eps
        axes.set_xlim([xmin,xmax])
        '''
        logger.debug(">>createFigure")
        self.figure = Figure(figsize=(logPlotData.widget_width, logPlotData.widget_height), dpi=logPlotData.dpi)
        
    def createPlots(self, logPlotData):
        if (len(logPlotData.sub_plots) >0):
            firstPlotDTO = logPlotData.sub_plots[0]
            firstLog = ArrayUtils.getFirstItem(firstPlotDTO.getLogs())
            if (firstLog != None):
                self.setupFirstPlot(logPlotData)
                if len(logPlotData.sub_plots) > 1:
                    self.setupSubplots(logPlotData)
            else:
                logger.debug("--createPlots() firstLog == None")
        else:
            logger.debug("--createPlots() no logs to plot")
        
    def setupFirstPlot(self, logPlotData):
        logger.debug(">>setupFirstPlot")
        assert len(logPlotData.sub_plots) >0
        
        #1*n grid, 1st subplot
        #self.axes = self.figure.add_subplot(1, len(logList), 1, sharey = logPlotData.depthAxis)
        depthPlots = logPlotData.getZAxisDatas()
        firstDepthPlot = depthPlots[0]
        self.axes = self.figure.add_subplot(1, len(logPlotData.sub_plots), 1, sharey = firstDepthPlot.depthAxis)
        #self.axes.set_title(logPlotData.title)
        #self.axes.set_xlabel(logList[0].name)
        #self.axes.set_ylabel(logPlotData.yLabel)
        self.axes.xaxis.tick_top()
        #self.axes.xaxis.set_label_position('top') 
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        xTicks = tic.MaxNLocator(2)
        self.axes.xaxis.set_major_locator(xTicks)
        #test semi-transparent region
        #self.axes.axhspan(1500, 2000, facecolor='g', alpha=0.5)
        
        self.axes.invert_yaxis()
        subPlots = logPlotData.sub_plots
        firstPlotDTO = subPlots[0]
        logs = firstPlotDTO.getLogs()
        log = ArrayUtils.getFirstItem(logs)    
        mpl_rgba = ImageUtils.rgbaToMPLrgba(log.rgb, log.alpha)
        logger.debug("--setupFirstPlot() log.rgb:{0}".format(log.rgb))
        self.axes.plot(log.log_data, log.z_measure_data, color = mpl_rgba)
        self.axes.set_xlim([log.log_plot_left, log.log_plot_right])
        assert len(logPlotData.depth_sub_plots) > 0
        max = logPlotData.depth_sub_plots[0].depthAxisPlotMax
        min = logPlotData.depth_sub_plots[0].depthAxisPlotMin
        self.axes.set_ylim(max, min)
        if len(logs)>1:
            for i, log in enumerate(logs , start = 1):
                logger.debug("--setupFirstPlot() "+str(i)+" "+str(log.name))
                par = self.axes.twiny()
                mpl_rgba = ImageUtils.rgbaToMPLrgba(log.rgb, log.alpha)
                p = par.plot(log.log_data, log.z_measure_data, color = (mpl_rgba))
                par.set_xlim([log.log_plot_left, log.log_plot_right])
                par.get_xaxis().set_visible(False)
            
        if logPlotData.display_depth_axes == False:
            self.axes.get_yaxis().set_visible(False)
        #else:
        #doesn't do anything
        #self.figure.tight_layout()
            
        #turn on grid
        if logPlotData.grid_on:
            self.axes.xaxis.grid(True,'minor')
            self.axes.yaxis.grid(True,'minor')
            self.axes.xaxis.grid(True,'major',linewidth=2)
            self.axes.yaxis.grid(True,'major',linewidth=2)

        self.axes.hold(logPlotData.hold)
        
        self.step = 1 # axis units
        self.scale = 1e3 # conversion betweeen scrolling units and axis units
        
        
    def setupSubplots(self, logPlotData):
        assert len(logPlotData.sub_plots) >1
        assert len(logPlotData.depth_sub_plots) > 0
        
        firstPlotDTO = ArrayUtils.getFirstItem(logPlotData.sub_plots)
        firstLog = ArrayUtils.getFirstItem(firstPlotDTO.getLogs())
        #start at 2 as first plot already plotted

        for i, subPlotData in enumerate(logPlotData.sub_plots):
            #not best way to do this
            if i > 0:
                #(234) means "2x3 grid, 4th subplot".
                ax1 = self.figure.add_subplot(1, len(logPlotData.sub_plots), i+1, sharey=self.axes)
    
                for log in subPlotData.getLogs():
                    mpl_rgba = ImageUtils.rgbaToMPLrgba(log.rgb, log.alpha)
                    logger.debug("--setupSubplots() log.rgb:{0}".format(log.rgb))
                    ax1.plot(log.log_data, log.z_measure_data, color = mpl_rgba)
                    ax1.set_xlim([log.log_plot_left, log.log_plot_right])
                    
                #ax1.set_xlabel(logList[v].name)
                ax1.get_xaxis().set_visible(False)
                ax1.get_yaxis().set_visible(False)
                ax1.xaxis.tick_top()
                xTicks = tic.MaxNLocator(2)
                ax1.xaxis.set_major_locator(xTicks)
                
                max = logPlotData.depth_sub_plots[0].depthAxisPlotMax
                min = logPlotData.depth_sub_plots[0].depthAxisPlotMin
                #need to set this otherwide axis is different to main depth axis
                ax1.set_ylim(max, min)
                #turn on grid
                if logPlotData.grid_on:
                    ax1.xaxis.grid(True,'minor')
                    ax1.yaxis.grid(True,'minor')
                    ax1.xaxis.grid(True,'major',linewidth=2)
                    ax1.yaxis.grid(True,'major',linewidth=2)
                    #ax1.yaxis.grid(color= subPlotData.gridColor, linestyle= subPlotData.gridLineStyle)
                
                if logPlotData.display_depth_axes == False:
                    #turn off y axis labels
                    ax1.get_yaxis().set_visible(False)
                    #for label in ax1.get_yticklabels():
                    #    label.set_visible(False)
                    #ax1.yaxis.offsetText.set_visible(False)
                
                #ax1.xaxis.set_label_position('top') 
                #ax1.set_yticklabels([])
                #ax1.yaxis.set_major_locator(pylab.NullLocator())

    def setFigure(self):
        FigureCanvas.__init__(self, self.figure)
        #self.setParent(self.parentWidget)
        # prevent the canvas to shrink beyond a point
        # original size looks like a good minimum size
        #FigureCanvas.setMinimumSize(FigureCanvas.size())
        FigureCanvas.setSizePolicy(self, QSizePolicy.Fixed, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #self.figure.subplots_adjust(left = 0.00)
     
    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(10, 10)
        
    def set_slider(self, parent):
        # Slider only support integer ranges so use ms as base unit
        smin, smax = self.xmin*self.scale, self.xmax*self.scale

        self.slider = QtGui.QSlider(QtCore.Qt.Vertical, parent=parent)
        self.slider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.slider.setTickInterval((smax-smin)/10.)
        self.slider.setMinimum(smin)
        self.slider.setMaximum(smax-self.step*self.scale)
        self.slider.setSingleStep(self.step*self.scale/5.)
        self.slider.setPageStep(self.step*self.scale)
        self.slider.setValue(0)  # set the initial position
        self.slider.valueChanged.connect(self.xpos_changed)
        parent.addWidget(self.slider)
        
    def xpos_changed(self, pos):
        #pprint("Position (in scroll units) %f\n" %pos)
        #        self.pos = pos/self.scale
        pos /= self.scale
        self.set_xlim(pos, pos + self.step)
        self.draw_idle()



    def adjustFigure(self):
        #subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
        #self.figure.subplots_adjust(left=0.01, bottom=0.01, hspace=0.01)
        totalPlotWidth = 0
        for plot in self.logPlotData.sub_plots:
            totalPlotWidth += plot.track_width
            logger.debug("--adjustFigure() plot_index: "+str(plot.plot_index)+" plot.track_width: "+str(plot.track_width)+" plot.track_gap: "+str(plot.track_gap))
            totalPlotWidth += plot.track_gap
        self.logPlotData.widget_width = totalPlotWidth
        logger.debug("--adjustFigure() totalPlotWidth: "+str(totalPlotWidth))
        self.figure.set_size_inches(totalPlotWidth, 6)
        #self.figure.set_figwidth(totalPlotWidth)
        
        self.figure.subplots_adjust(left=WellPlotConstants.WELL_PLOT_FIGURE_LEFT, bottom=WellPlotConstants.WELL_PLOT_FIGURE_BOTTOM
                                    , right=WellPlotConstants.WELL_PLOT_FIGURE_RIGHT, top=WellPlotConstants.WELL_PLOT_FIGURE_TOP
                                    , wspace=WellPlotConstants.WELL_PLOT_FIGURE_WSPACE, hspace=WellPlotConstants.WELL_PLOT_FIGURE_HSPACE)
        #self.draw()
        

    