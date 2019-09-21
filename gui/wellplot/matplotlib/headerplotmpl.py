from __future__ import unicode_literals

from PyQt4 import QtGui, QtCore
from matplotlib.backends import qt4_compat
from PyQt4.QtGui import QWidget, QPainter,  QVBoxLayout, \
    QColor,  QPen

import numpy as np

from globalvalues.appsettings import AppSettings
from qrutilities.imageutils import ImageUtils


from qrutilities.numberutils import NumberUtils

from db.core.log.logdao import LogDao
from gui.wellplot.matplotlib.mplutils import MplUtils
from gui.util.qt.widgetutils import WidgetUtils

use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
#if use_pyside:
#    from PySide import QtGui, QtCore
#else:


from PyQt4.QtCore import QSize, QRect

import logging

logger = logging.getLogger('console')

class HeaderPlotMPL(QWidget):
    #Plot with a shared y depth axis
    
    def __init__(self, depthPlot, mainPlot, wellPlotData, parentWidget=None):
        QWidget.__init__( self, parentWidget )
        #super(MultiLogCanvas, self).__init__(parentWidget)
        
        self.logPlotData = wellPlotData
        self.parentWidget = parentWidget
        self.depthPlot = depthPlot
        self.mainPlot = mainPlot
        self.setSize()
        #self.testAxes()
        self.addWidgets()
             
    def calcHeaderHeight(self):
        '''Finds max number of logs per plot and bases height on a multiplier of this value '''  
        pass
        
        
    def setSize(self):
        depthFigure = self.depthPlot.figure
        mainFigure = self.mainPlot.figure
        dwidth, dheight = depthFigure.canvas.get_width_height()
        logger.debug("dwidth: "+str(dwidth)+" dheight: "+str(dheight))

        width, height = mainFigure.canvas.get_width_height()
        self.setGeometry( 0, 0, dwidth+width, dheight + height )
        

    
    def addWidgets(self):
        #self.header_layout = QHBoxLayout()
        depthSubPlots = self.logPlotData.getZAxisDatas()
        assert depthSubPlots!=None and len(depthSubPlots)>0
        dbox = self.createDepthHeader(self.logPlotData.getZAxisDatas()[0])
        dbox.move(0, 0)
        dbox.setParent(self)
        #self.header_layout.addWidget(dbox)
        figure = self.mainPlot.figure
        if len(figure.get_axes()) >0:
            assert len(figure.get_axes()) == len(self.logPlotData.getLogTrackDatas())
            for ax, subPlotData in zip(figure.get_axes(), self.logPlotData.getLogTrackDatas()):
            #for ax in self.mainPlot.get_axes():
                bbox = ax.get_position()   
                logger.debug("--addWidgets() ax.get_position(): "+str(bbox))
                (xpix, ypix) = MplUtils.getAxisLimits(ax)        
            #for subPlotData in self.logPlotData.getLogTrackDatas():
                vbox = self.createPlotHeader(subPlotData, xpix, self.logPlotData)
                logger.debug("--addWidgets() self.getDepthPlotWidth() : "+str(self.getDepthPlotWidth())+" xpix[0]: "+str(xpix[0])+" xpix[1]: "+str(xpix[1]))
                startPixel = self.getDepthPlotWidth() + xpix[0]
                vbox.move(startPixel, 0)
                vbox.setParent(self)

                #self.header_layout.addWidget(vbox)
            #rightSpacer = QtGui.QWidget()
            #rightSpacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            #self.header_layout.addWidget(rightSpacer)
            #self.setLayout(self.header_layout)
        
        
    def createDepthHeader(self, depthSubPlotData):
        layout = QVBoxLayout()
        vbox = QWidget()

        
        dfig = self.depthPlot.figure
        dwidth, dheight = dfig.canvas.get_width_height()
        layout.addWidget(self.getHeaderBox(dwidth))

        bottomSpacer = QtGui.QWidget()
        bottomSpacer.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        layout.addWidget(bottomSpacer)
        vbox.setLayout(layout)
        return vbox
        
    def createPlotHeader(self, subPlotData, xpix, logPlotData):
        logger.debug(">>createPlotHeader() ")
        vbox = QWidget()
        #logPlotPreferencesLogic = WellPlotPreferencesLogic()
        #logPlotDefaults = logPlotPreferencesLogic.getLogPlotPreferences()
        
        label_bg_rgb = self.logPlotData.label_background_rgb
        label_bg_alpha = self.logPlotData.label_background_alpha
        label_fg_rgb = self.logPlotData.label_foreground_rgb
        label_fg_alpha = self.logPlotData.label_foreground_alpha
        (fr, fg, fb, falpha) = ImageUtils.rbgaTointValues(label_fg_rgb, label_fg_alpha)
        (br, bg, bb, balpha) = ImageUtils.rbgaTointValues(label_bg_rgb, label_bg_alpha)
        '''
        labelProps.label_fg_color = QColor(fr, fg, fb, falpha)
        labelProps.label_bg_color = QColor(br, bg, bb, balpha)
        labelProps.subPlotData = subPlotData
        labelProps.xpix = xpix
        labelProps.expandedLabel = logPlotDefaults.expanded_header_labels
        '''
        if subPlotData != None and len(subPlotData.getLogs())>0:
            layout = QVBoxLayout()
            topSpacer = QtGui.QWidget()
            topSpacer.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
            layout.addWidget(topSpacer)
            for log in subPlotData.getLogs():

                canvasFig = self.mainPlot.figure
                #labelProps.canvas_width, labelProps.canvas_height = canvasFig.canvas.get_width_height()

                headerWidget = LogHeaderLabel(subPlotData, log, xpix, logPlotData)
                layout.addWidget(headerWidget)
        
            vbox.setLayout(layout)
        plot_width = xpix[1] - xpix[0]
        logger.debug("--createPlotHeader() xpix 1: "+str(xpix[1])+" xpix 0: "+str(xpix[0])+" plot_width "+str(plot_width))
        vbox.setFixedWidth(plot_width)
        return vbox
        
    
    def getDepthPlotWidth(self):
        dfig = self.depthPlot.figure
        dwidth, dheight = dfig.canvas.get_width_height()
        return dwidth

    def paintEvent( self, event ) :
        painter = QPainter()
        painter.begin( self )

        window_width  = self.width()
        window_height = self.height()

        #painter.drawText( 20, 20, "Window size is %dx%d "  %  \
        #                       ( window_width, window_height ) )
        
        dfig = self.depthPlot.figure
        dwidth, dheight = dfig.canvas.get_width_height()
        #top horizontal
        painter.drawLine( 0, 0, dwidth, 0 )
        #left vertical
        painter.drawLine( 0, 0, 0, window_height ) 
        
        painter.drawLine( dwidth, 0, dwidth, window_height )
        #why 4 pixels???
        xStart = dwidth + 4
        for ax in self.mainPlot.figure.get_axes():
            self.drawHeaderBox(ax, xStart, painter)   
        painter.end()

    def drawHeaderBox(self, paramAxis, xStart, painter):
        bbox = paramAxis.get_position()   
        
        (xpix, ypix) = MplUtils.getAxisLimits(paramAxis)        
        
        window_width  = self.width()
        window_height = self.height()

        #top horizontal
        painter.drawLine( xpix[0]+xStart, 0, xpix[1]+xStart, 0 )
        #left vertical
        painter.drawLine( xpix[0]+xStart, 0, xpix[0]+xStart, window_height ) 
        #right vertical
        painter.drawLine( xpix[1]+xStart, 0, xpix[1]+xStart, window_height ) 
        #return xpix[1]+xStart
                        
    def plotHeaders(self):
        xpix, ypix = self.getAxesLimits(self.depthPlot, self.mainPlot)
        


    def getAxesLimits(self, figure):
        dfig = self.depthPlot.figure
        dwidth, dheight = dfig.canvas.get_width_height()
        logger.debug("dwidth: "+str(dwidth)+" dheight: "+str(dheight))
            
        for ax in figure.get_axes():
                x = ax.get_xlim()
                y = ax.get_ylim()
                
                xy_pixels = ax.transData.transform(np.vstack([x,y]).T)
                xpix, ypix = xy_pixels.T
                
                # In matplotlib, 0,0 is the lower left corner, whereas it's usually the upper 
                # right for most image software, so we'll flip the y-coords...
                width, height = figure.canvas.get_width_height()
                ypix = height - ypix
                logger.debug("width: "+str(width)+" height: "+str(height))
                
                logger.debug( 'Coordinates of the points in pixel coordinates...')
                for xp in xpix:
                    logger.debug("xp: "+str(xp))
                for yp in ypix:
                    logger.debug("yp: "+str(yp))
      
    def minimumSizeHint(self):
        return QSize(10, 10)
        
    def getHeaderBox(self, width):
        logger.debug(">>getHeaderBox() width: "+str(width))

        headingText_widget = QtGui.QWidget()

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setMargin(0)
        '''
        logValLeft_label = QtGui.QLabel()
        logValLeft_label.setText(str(labelProperties.leftLogLimit))
        horizontalLayout.addWidget(logValLeft_label)
        
        spacerItem = QtGui.QSpacerItem(width/2, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem)
        
        logName_label = QtGui.QLabel()
        logName_label.setText(str(labelProperties.logName))
        horizontalLayout.addWidget(logName_label)
        
        spacerItem1 = QtGui.QSpacerItem(width/2, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem1)
        
        logValRight_label = QtGui.QLabel()
        logValRight_label.setText(str(labelProperties.rightLogLimit))
        horizontalLayout.addWidget(logValRight_label)
        '''

        headingText_widget.setLayout(horizontalLayout)
        headingText_widget.setFixedWidth(width)
        #as using QColor should'nt need this try block, can remove if working OK
        try:
            pal=QtGui.QPalette()
            role = QtGui.QPalette.Background
            backgroundQColor = ImageUtils.rgbToQColor(self.logPlotData.label_background_rgb)
            #colour = QtGui.QColor(labelProperties.backgroundColour)
            pal.setColor(role, backgroundQColor)
            role = QtGui.QPalette.Foreground
            foregroundQColor = ImageUtils.rgbToQColor(self.logPlotData.label_foreground_rgb)
            pal.setColor(role, foregroundQColor)
            headingText_widget.setPalette(pal)
        except AttributeError as ex:
            logger.error(str(ex))
            if AppSettings.isDebugMode:
                raise AttributeError
        return headingText_widget
    
    '''
    #deprecated
    def testAxes(self):
        figure = self.mainPlot.figure
        try:
            #figure.axes is a list of AxesSubplots
            for ax in figure.get_axes():
                
                
                bbox = ax.get_position()
                #Get the points of the bounding box directly as a numpy array
                #of the form: [[x0, y0], [x1, y1]].
                points = bbox.get_points().tolist()
                xvals = points[0]
                yvals = points[1]
                transformed = ax.transData.transform(xvals)
                b = ax.bbox
                b2 = b.transformed(ax.transData)
                pointsB = bbox.get_points().tolist()
                xvalsB = pointsB[0]
                yvalsB = pointsB[1]
                logger.debug("pointsB "+str(pointsB))
                logger.debug("b2 "+str(b2))
                
                
                logger.debug("x min: "+str(xvals[0])+" x trans "+str(transformed[0])+" max: "+str(xvals[1])+" x trans "+str(transformed[1]))
                logger.debug("y min: "+str(yvals[0])+" max: "+str(yvals[1]))
                
                
                pos1 = ax.get_position()
                pos2 = [pos1.x0 + 0.3, pos1.y0 + 0.3,  pos1.width / 2.0, pos1.height / 2.0] 
                #self.axes.set_position(pos2)
                
                bbox = ax.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
                width, height = bbox.width, bbox.height
                width *= figure.dpi
                height *= figure.dpi
                logger.debug("width: "+str(width)+" height: "+str(height))
                #see http://stackoverflow.com/questions/13662525/how-to-get-pixel-coordinates-for-matplotlib-generated-scatterplot
            
        except AttributeError as e:
            logger.debug("--testaxes() "+str(e))
            if AppSettings.isDebugMode:
                raise AttributeError
    '''
            
class LogHeaderLabel(QWidget):
    ''' Creates a log header label that can be positioned as needed '''
    
    def __init__(self, subPlotData, log, xpix, wellPlotData, parentWidget=None):
        QWidget.__init__( self, parentWidget)
        self.subPlotData = subPlotData
        self.logPlotData = wellPlotData
        self.xpix = xpix
        self.widget_width = xpix[1] - xpix[0]
        self.log = log
        self.setupUI()


    def setupUI(self):
        PREFFERED_SPACER_HEIGHT = 6
        
        if self.logPlotData.single_row_header_labels:
            logger.debug("--setupUI() expanded label")
            vBox = QtGui.QVBoxLayout()
            vBox.setMargin(0)
        
            hbox = QtGui.QHBoxLayout()
            hbox.setMargin(0)
            
            self.logName_label = QtGui.QLabel()
            self.logName_label.setText(self.log.name)
            logNameWidth = self.logName_label.geometry().width()

            if (self.widget_width - logNameWidth) >0:
                preferredSpace = (self.widget_width - logNameWidth)/2
            else:
                preferredSpace = (self.widget_width)/2
            
            labelLspacerItem = QtGui.QSpacerItem(preferredSpace, PREFFERED_SPACER_HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            
            hbox.addItem(labelLspacerItem)          
            hbox.addWidget(self.logName_label)
            
            labelRspacerItem = QtGui.QSpacerItem(preferredSpace, PREFFERED_SPACER_HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            hbox.addItem(labelRspacerItem)
            
            valHbox = QtGui.QHBoxLayout()
            valHbox.setMargin(0)
            
            self.logValLeft_label = QtGui.QLabel()
            self.logValLeft_label.setText(str(self.log.log_plot_left))
            
            units = self.getUnits(self.log)
            
            assert units != None
            
            self.logUnit_label = QtGui.QLabel()
            self.logUnit_label.setText(units)
            
            self.logValRight_label = QtGui.QLabel()
            self.logValRight_label.setText(str(self.log.log_plot_right))
            
            logValLeftWidth = self.logValLeft_label.geometry().width()
            logValRightWidth = self.logValRight_label.geometry().width()
            logUnitWidth = self.logUnit_label.geometry().width()
            labelWidths =  (logValLeftWidth + logValRightWidth + logUnitWidth)
            if (self.widget_width - labelWidths) >0:
                preferredSpace = (self.widget_width - labelWidths)/2
            else:
                preferredSpace = (self.widget_width)/2
            
            valueLSpacerItem = QtGui.QSpacerItem(preferredSpace, PREFFERED_SPACER_HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            valueRSpacerItem = QtGui.QSpacerItem(preferredSpace, PREFFERED_SPACER_HEIGHT, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            
            valHbox.addWidget(self.logValLeft_label)
            valHbox.addItem(valueLSpacerItem)
            valHbox.addWidget(self.logUnit_label)
            valHbox.addItem(labelRspacerItem)        
            valHbox.addWidget(self.logValRight_label)
            
            vBox.addLayout(hbox)
            vBox.addLayout(valHbox)
            
            self.setLayout(vBox)

        else:
            logger.debug("--setupUI() compressed label")
            hbox = QtGui.QHBoxLayout()
            hbox.setMargin(0)
            
            self.logValLeft_label = QtGui.QLabel()
            self.logValLeft_label.setText(str(self.log.log_plot_left))
            
            self.logName_label = QtGui.QLabel()
            units = LogDao.getUnits(self.log)
            if units != None:
                labelText = self.log.name + " (" + units +")"
            else:
                labelText = self.log.name
            self.logName_label.setText(labelText)
            
            self.logValRight_label = QtGui.QLabel()
            self.logValRight_label.setText(str(self.log.log_plot_right))
            
            logValLeftWidth = self.logValLeft_label.geometry().width()
            logValRightWidth = self.logValRight_label.geometry().width()
            logNameWidth = self.logName_label.geometry().width()
            
            labelWidths =  (logValLeftWidth + logValRightWidth + logNameWidth)
            if (self.widget_width - labelWidths) >0:
                preferredSpace = (self.widget_width - labelWidths)/2
            else:
                preferredSpace = (self.widget_width)/2
                
            labelLspacerItem = QtGui.QSpacerItem(preferredSpace, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            labelRspacerItem = QtGui.QSpacerItem(preferredSpace, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            
            hbox.addWidget(self.logValLeft_label)
            hbox.addItem(labelLspacerItem)
            hbox.addWidget(self.logName_label)
            hbox.addItem(labelRspacerItem)
            hbox.addWidget(self.logValRight_label)
            self.setLayout(hbox)

        self.setFixedWidth(self.widget_width)

        #set colours
        pal=QtGui.QPalette()
        role = QtGui.QPalette.Background
        backgroundQColor = ImageUtils.rgbToQColor(self.logPlotData.label_background_rgb)
        pal.setColor(role, backgroundQColor)
        role = QtGui.QPalette.Foreground
        foregroundQColor = ImageUtils.rgbToQColor(self.logPlotData.label_foreground_rgb)
        pal.setColor(role, foregroundQColor)
        self.setPalette(pal)
        

    def paintEvent( self, event ) :
        MARGIN_PIXELS = 4
        
        painter = QPainter()
        (r, g, b, alpha) = ImageUtils.rbgaTointValues(self.log.rgb, self.log.alpha)
        
        lineColour = QColor(r, g, b, alpha)
        
        assert lineColour != None 
        assert self.log.line_style != None
        
        lineStyle = WidgetUtils.getQtPenStyle(self.log.line_style)
        
        assert lineStyle != None 
        assert self.log.line_width != None
        
        lineWidth = NumberUtils.floatToIntDefault(self.log.line_width, 1)
        pen = QPen(lineColour, lineWidth, lineStyle)
        
        painter.begin(self)
        painter.setPen(pen)

        yLevel = self.logName_label.rect().bottomLeft().y()
        xStart = self.xpix[0]
        xStop = self.xpix[1]
        
        #horizontal line
        #logger.debug("--paintEvent() r: {0},  g: {1},  b: {2},  a: {3}, name{4}".format(r, g, b, alpha, self.log.name))
        #logger.debug("--paintEvent() xStart: {0},  yLevel: {1},  xStop: {2},  yLevel: {3}".format(xStart, yLevel, xStop, yLevel))
        painter.drawLine( xStart, yLevel, xStop, yLevel )
        
        painter.end()
    



class PenLine(QtGui.QWidget):

    def __init__(self, lineGeometry, position):
        super(PenLine, self).__init__()
        self.lineGeom = lineGeometry
        self.initUI(position)

    def initUI(self, position):

        self.setGeometry(position)
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(self.lineGeom[0], self.lineGeom[1], self.lineGeom[2], self.lineGeom[3])
        
    
  
                  
    #deprecated
    def getBbox(self, figure):
        bbox = None
        for ax in figure.get_axes():
            #locator = figuew.axes.xaxis.get_major_locator()
            locator = ax.xaxis.get_major_locator()
            bbox = locator.axis.axes.bbox
            x0, x1 = bbox.p0
            y0, y1 = bbox.p1
            logger.debug("--getBbox() x0: "+str(x0)+" x1: "+str(x1)+" y0: "+str(y0)+" y1: "+str(y1))
        return bbox
    
    
            
    

    '''  
    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)
    '''