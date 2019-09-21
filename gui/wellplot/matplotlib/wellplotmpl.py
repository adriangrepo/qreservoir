from PyQt4 import QtGui, QtCore

from views.core import centraltabwidget
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData
from PyQt4.QtGui import QSplitter, QWidget, QScrollArea

from gui.wellplot.matplotlib.depthaxis import DepthAxis
from globalvalues.appsettings import AppSettings
from gui.wellplot.toolbar import logsettingstoolbar
from gui.signals.wellplotsignals import WellPlotSignals

from PyQt4.QtCore import pyqtSlot

import logging

from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess
from gui.wellplot.matplotlib.headerplotmpl import HeaderPlotMPL

from gui.wellplot.subplots.wellplotwidget import WellPlotWidget
from gui.wellplot.matplotlib.multilogcanvas import MultiLogCanvas
from gui.wellplot.matplotlib.mplutils import MplUtils
from gui.util.qt.widgetutils import WidgetUtils

logger = logging.getLogger('console')

class WellPlotMPL(QtCore.QObject):
    
    def __init__(self, logs, well, logSet = None, parent = None):
        super(WellPlotMPL, self).__init__(parent)

        self._well = well
        self._logSet = logSet
        self._logs = logs
        self.plots = [] 
        self.canvas = None
        self.depthPlot = None
        self.headerPlot = None
        centralWidget = centraltabwidget.CentralTabWidget()
        #id(self) returns the 'hash' of this object
        self.uid = (centralWidget.count(), id(self))
        self.wellPlotSignals = WellPlotSignals()
        
        self.setupUI()
        self.createTabView()
        self.connectSlots()
        self.plotMultiLogs()
        self.setSplitterStretch()
        self.createToolWidget()
        
    def setupUI(self):
        self.mainWidget = WellPlotWidget()
        vBox = QtGui.QVBoxLayout()
        self.mainWidget.setLayout(vBox)
        
        self.headerWidget = QWidget()
        self.headerLayout = QtGui.QHBoxLayout()
        self.headerWidget.setLayout(self.headerLayout)
        
        self.dataWidget = QWidget()
        self.dataLayout = QtGui.QHBoxLayout()
        self.dataWidget.setLayout(self.dataLayout)
        
        #if don't set a minimum, get matplotlib error when is very small
        self.dataWidget.setMinimumHeight(self.getMinimumVerticalHeight())

        self.splitter = QSplitter(QtCore.Qt.Vertical)
        
        self.headerScrollArea = QScrollArea()
        self.headerScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.headerScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.headerScrollArea.setWidgetResizable(False)
        self.headerScrollArea.setWidget(self.headerWidget)
        
        self.scrollArea = QScrollArea()  
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setWidget(self.dataWidget)
        #see http://stackoverflow.com/questions/29583927/pyqt-qscrollarea-within-qscrollarea/29584939#29584939
        self.scrollArea.horizontalScrollBar().valueChanged.connect(
            self.headerScrollArea.horizontalScrollBar().setValue)
        
        self.splitter.addWidget(self.headerScrollArea)
        self.splitter.addWidget(self.scrollArea)
        self.splitter.setStretchFactor(1, 10)

        vBox.addWidget(self.splitter)
        
        
    def getMinimumVerticalHeight(self):
        screenRect = QtGui.QDesktopWidget().screenGeometry()
        #need to set a minimum size otherwise get matplotlib error when rezizing to too small
        twentythOfScreen = int(round(screenRect.width()/20))
        return twentythOfScreen
    
    def plotMultiLogs(self):
        logPlotModelAccess = WellPlotModelAccess()
        logPlotData = logPlotModelAccess.createWellPlotData(self._logs)
        self.createCanvas(logPlotData)
        self.plotHeaderFields(logPlotData)
        
    def createCanvas(self, logPlotData):
        logger.debug(">>createCanvas()")
        #test
        for subPlotData in logPlotData.sub_plots:
            logger.debug("--createCanvas() plot_index:{0} track_width:{1} track_gap:{2}".format(subPlotData.plot_index, subPlotData.track_width, subPlotData.track_gap))
            for log in subPlotData._logs:
                logger.debug("--createCanvas id:{0}, name:{1}".format(log.id, log.name))
        #end test
        if len(logPlotData.sub_plots) > 0:
            WidgetUtils.removeWidgets(self.dataLayout)
            
            #test
            #time.sleep(1) # delays for 1 second
            #end test
            
            #There may be a better way to link plots with the toolbar
            self.mainWidget.setLogPlotData(logPlotData)

            self.depthPlot = DepthAxis(logPlotData, self.dataWidget)
            self.dataLayout.addWidget(self.depthPlot)  
                
            self.canvas = MultiLogCanvas(logPlotData, self.dataWidget)
            self.canvas.setAutoFillBackground(True)
            self.dataLayout.addWidget(self.canvas)
            
            spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.dataLayout.addItem(spacerItem)
        else:
            logger.error("--plotMultiLogs() Error: no logs to plot")
            if AppSettings.isDebugMode:
                raise ValueError
            

        
    def plotHeaderFields(self, logPlotData):
        logger.debug(">>plotMultiLogs()")
        WidgetUtils.removeWidgets(self.headerLayout)
        self.headerPlot = HeaderPlotMPL(depthPlot = self.depthPlot, mainPlot = self.canvas, logPlotData = logPlotData)
        self.headerLayout.addWidget(self.headerPlot)

    def setSplitterStretch(self):
        #Minimum size is required for the QScrollArea.setWidgetResizable(False) setting'''
        headerW = self.headerPlot.width()
        headerH = self.headerPlot.height()
        self.headerWidget.setMinimumSize(headerW, headerH)

        #test
        (totalW, dataH) = MplUtils.calcFigCanvasWidthHeight(self.canvas.figure)
        #end test
        dWidth, dHeight = self.canvas.figure.canvas.get_width_height()
        
        self.dataWidget.setMinimumSize(dWidth, dHeight)
        
        
    def connectSlots(self):
        logger.debug(">>connectSlots")
        self.wellPlotSignals.logPlotSettingsModified.connect(self.replotLogs)

    
    @pyqtSlot(WellPlotData)
    def replotLogs(self, logPlotData):
        logger.debug(">>replotLogs len(logPlotData.sub_plots): "+str(len(logPlotData.sub_plots)))
        #check uid's before accessing them, where uid is a (number widgets in central widget, id) tuple
        logger.debug("--replotLogs() len(self.uid):{0}, len(logPlotData.uid):{1}".format(len(self.uid), len(logPlotData.uid)))
        if (len(self.uid) == 2) and (len(logPlotData.uid) == 2):
            #ensure this object is associated with the plot object
            if self.uid[0] == logPlotData.uid[0] and self.uid[1] == logPlotData.uid[1]:
                logger.debug("--replotLogs() match found uid: "+str(self.uid[0]))

                self.createCanvas(logPlotData)
                self.plotHeaderFields(logPlotData)


    def spacePlots(self, bottomLayout):
        rightSpacer = QtGui.QWidget()
        rightSpacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #topLayout.addWidget(rightSpacer)
        bottomLayout.addWidget(rightSpacer)
        #self.topWidget.setLayout(topLayout)
        self.dataWidget.setLayout(bottomLayout)

    def createTabView(self):
        centralWidget = centraltabwidget.CentralTabWidget()
        self.mainWidget.setData(self.uid)
        #centralWidget.addTab(self.scrollArea, "Well plot "+str(self.uid[0]))
        centralWidget.addTab(self.mainWidget, "Well plot "+str(self.uid[0]))


    def createToolWidget(self):
        if len(self._logs) > 0:
            toolbar = logsettingstoolbar.LogSettingsToolbar()
            toolbar.setData(self._well, self._logSet, self.canvas, self.depthPlot, self.headerPlot)
            toolbar.emitShowToolbarSignal()
            logger.debug("<<createToolWidget() toolbar created")
            
    

    
    

      