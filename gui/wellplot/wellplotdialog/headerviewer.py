from __future__ import unicode_literals

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget, QPainter, QVBoxLayout, \
    QColor, QPen, QFrame

from qrutilities.imageutils import ImageUtils
from qrutilities.numberutils import NumberUtils
from db.core.log.logdao import LogDao
from gui.util.qt.widgetutils import WidgetUtils

from qrutilities.systemutils import SystemUtils

import logging
from db.windows.wellplot.zaxistrackdata.zaxisdata import ZAxisData
from PyQt4.Qt import Qt
from db.windows.wellplot.logtrackdata.logtrackdata import LogTrackData

logger = logging.getLogger('console')

class HeaderViewer(QWidget):
    #Plot with a shared y depth axis
    
    def __init__(self, wellPlotData, logTracks, parentWidget=None):
        QWidget.__init__( self, parentWidget )
        self.wellPlotData = wellPlotData
        self.logTracks = logTracks
        self.allTracks = [] 
        self.dataLayout = None
        self.setupUI()
        self.createHeaderTracks()

    def setupUI(self):
        #self.dataWidget = QWidget()
        self.dataLayout = QtGui.QHBoxLayout()
        self.setLayout(self.dataLayout)
        self.setMinimumHeight(self.getMinimumVerticalHeight())
        
    def getMinimumVerticalHeight(self):
        screenRect = SystemUtils.getScreenGeometry()
        #need to set a minimum size otherwise get matplotlib error when resizing to too small
        twentythOfScreen = int(round(screenRect.width()/40))
        return twentythOfScreen
        
    def calcHeaderHeight(self):
        '''Finds max number of logs per plot and bases height on a multiplier of this value '''  
        pass
        
    
    def createHeaderTracks(self):
        if len(self.logTracks) > 0:
            WidgetUtils.removeWidgets(self.dataLayout)
            for track in self.logTracks:
                data = track.data(Qt.UserRole)
                if isinstance(data, ZAxisData):
                    logger.debug("--createHeaderTracks() domainZType: {0} domainZReference: {1}".format(data.z_axis_type, data.z_axis_reference_level))
                    depthHeader = self.createDepthHeader(track, self.wellPlotData)
                    depthHeader.setFixedWidth(track.geometry().width())
                    self.dataLayout.addWidget(depthHeader)
                elif isinstance(data, LogTrackData):
                    plotHeader = self.createPlotHeader(track, self.wellPlotData)
                    plotHeader.setFixedWidth(track.geometry().width())
                    self.dataLayout.addWidget(plotHeader)
                    for log in data.getLogs():
                        logger.debug("--createHeaderTracks() log name: {0} ".format(log.name))
                else:
                    logger.debug("--createHeaderTracks() unrecognized data type:{0} ".format(type(data)))
            self.dataLayout.addStretch(1)
        else:
            logger.debug("--createHeaderTracks() Error: no logs to plot")

        
    
    def createDepthHeader(self, track, wellPlotData):
        layout = QVBoxLayout()
        depthHeaderFrame = QFrame()
        
        layout = QVBoxLayout()
        headerWidget = DomainHeaderLabel(track, wellPlotData)

        layout.addWidget(headerWidget)
        depthHeaderFrame.setLayout(layout)
        bottomSpacer = QtGui.QWidget()
        bottomSpacer.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        layout.addWidget(bottomSpacer)
        depthHeaderFrame.setLayout(layout)
        depthHeaderFrame.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Raised)
        trackGeom = track.geometry()
        depthHeaderFrame.setMinimumWidth(trackGeom.width())
        depthHeaderFrame.setGeometry(trackGeom.x(), trackGeom.y(), trackGeom.width(), headerWidget.geometry().height())
        #depthHeaderFrame.setStyleSheet("QFrame { background-color: %s }" % "Blue")  
        logger.debug("--createDepthHeader() x:{0} y:{1} width:{2} height:{3}".format(trackGeom.x(), trackGeom.y(), trackGeom.width(), headerWidget.geometry().height()))
        return depthHeaderFrame
            
    def createPlotHeader(self, track, wellPlotData):
        logger.debug(">>createPlotHeader() ")
        assert track != None
        assert wellPlotData != None
        
        logTrackData = track.data(Qt.UserRole)
        titleFrame = QFrame()
        vLayout = QVBoxLayout()
        vbox = QWidget()
        
        label_bg_rgb = self.wellPlotData.label_background_rgb
        label_bg_alpha = self.wellPlotData.label_background_alpha
        label_fg_rgb = self.wellPlotData.label_foreground_rgb
        label_fg_alpha = self.wellPlotData.label_foreground_alpha
        (fr, fg, fb, falpha) = ImageUtils.rbgaTointValues(label_fg_rgb, label_fg_alpha)
        (br, bg, bb, balpha) = ImageUtils.rbgaTointValues(label_bg_rgb, label_bg_alpha)
       
        #in case logs=0, as we reference .geometry()
        headerWidget = QWidget()
        if len(logTrackData.getLogs())>0:
            layout = QVBoxLayout()
            for log in logTrackData.getLogs():
                headerWidget = LogHeaderLabel(log, track, wellPlotData)
                layout.addWidget(headerWidget)
            topSpacer = QtGui.QWidget()
            topSpacer.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
            layout.addWidget(topSpacer)
            vbox.setLayout(layout)
        
        vLayout.addWidget(vbox)
        titleFrame.setLayout(vLayout)
        titleFrame.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Raised)
        trackGeom = track.geometry()
        titleFrame.setMinimumWidth(trackGeom.width())
        titleFrame.setGeometry(trackGeom.x(), trackGeom.y(), trackGeom.width(), headerWidget.geometry().height())
        logger.debug("--createPlotHeader() trackGeom.width(): {0} headerWidget.geometry().height(): {1}".format(trackGeom.width(), headerWidget.geometry().height()))
        logger.debug("--createPlotHeader() titleFrame.width(): {0} titleFrame.geometry().height(): {1}".format(titleFrame.width(), titleFrame.geometry().height()))
        return titleFrame
        
    
    def addWidgets(self):
        #self.header_layout = QHBoxLayout()
        depthSubPlots = self.logPlotData.getZAxisDatas()
        assert depthSubPlots!=None and len(depthSubPlots)>0
        dbox = self.createDepthHeader(self.logPlotData.getZAxisDatas()[0])
        dbox.move(0, 0)
        dbox.setParent(self)
        
    
            
class DomainHeaderLabel(QWidget):
    def __init__(self, track, wellPlotData, parentWidget=None):
        QWidget.__init__( self, parentWidget)
        self.track = track
        self.domainTrackData = track.data(Qt.UserRole)
        self.wellPlotData = wellPlotData
        self.setupUI()
        
    def setupUI(self):
        vbox = QtGui.QVBoxLayout()
        vbox.setMargin(0)

        logName_label = QtGui.QLabel()
        logName_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        logName_label.setText(self.domainTrackData.getTypeDisplayUnitReferenceTitle())
        #logNameWidth = logName_label.geometry().width()
        #logNameLabelHeight = logName_label.geometry().height()

        vbox.addWidget(logName_label)
        vbox.addStretch(1)
        self.setLayout(vbox)

        #self.setFixedWidth(self.widget_width)

        #set colours
        pal=QtGui.QPalette()
        role = QtGui.QPalette.Background
        backgroundQColor = ImageUtils.rgbToQColor(self.wellPlotData.label_background_rgb)
        #self.setStyleSheet("QFrame { background-color: %s }" % "Red")  

        role = QtGui.QPalette.Foreground
        foregroundQColor = ImageUtils.rgbToQColor(self.wellPlotData.label_foreground_rgb)
        pal.setColor(role, foregroundQColor)
        self.setPalette(pal)
    
class LogHeaderLabel(QWidget):
    ''' Creates a log header label that can be positioned as needed '''

    #20% for values as 10 was cutting off
    VALUE_PADDING = 5
    NAME_PADDING = 10
    PREFFERED_SPACER_WIDTH = 2
    PREFFERED_SPACER_HEIGHT = 2
    
    def __init__(self, log, track, wellPlotData, parentWidget=None):
        QWidget.__init__( self, parentWidget)
        self.log = log
        self.track = track
        self.wellPlotData = wellPlotData
        self.logName_label = None
        self.logValRight_label = None
        self.logValLeft_label = None
        self.setupUI()

    def setupUI(self):
        if self.wellPlotData.single_row_header_labels:
            hbox = self.createSingleRowLabelBox()
            self.setLayout(hbox)
        else:
            vbox = self.createDoubleRowLabelBox()
            self.setLayout(vbox)
        self.setFixedWidth(self.track.geometry().width())
        
        #set colours
        pal=QtGui.QPalette()
        role = QtGui.QPalette.Background
        backgroundQColor = ImageUtils.rgbToQColor(self.wellPlotData.label_background_rgb)
        pal.setColor(role, backgroundQColor)
        role = QtGui.QPalette.Foreground
        foregroundQColor = ImageUtils.rgbToQColor(self.wellPlotData.label_foreground_rgb)
        pal.setColor(role, foregroundQColor)
        self.setPalette(pal)
        
    def createSingleRowLabelBox(self):
        logger.debug("--setupUI() single row label")
        self.logValLeft_label = QtGui.QLabel()
        self.logValLeft_label.setText(str(self.log.log_plot_left))
        logValLeftWidth = self.logValLeft_label.fontMetrics().boundingRect(self.logValLeft_label.text()).width()
        
        #see http://stackoverflow.com/questions/8633433/qt-get-the-pixel-length-of-a-string-in-a-qlabel
        #add 10% padding as bounding rect may not give exact width
        paddedLeftWidth = int(logValLeftWidth + logValLeftWidth/self.VALUE_PADDING)
        self.logValLeft_label.setFixedWidth(paddedLeftWidth)
        assert self.log.log_plot_left != None
        assert self.log.log_plot_left != ""
        
        self.logName_label = QtGui.QLabel()
        units = LogDao.getUnits(self.log)
        assert units != None
        if units != None:
            labelText = self.log.name.strip() + " (" + units.strip() +")"
        else:
            labelText = self.log.name.strip()
        self.logName_label.setText(labelText)
        logNameWidth = self.logName_label.fontMetrics().boundingRect(self.logName_label.text()).width()
        paddedNameWidth = int(logNameWidth + logNameWidth/self.NAME_PADDING)

        self.logValRight_label = QtGui.QLabel()
        self.logValRight_label.setText(str(self.log.log_plot_right))
        logValRightWidth = self.logValRight_label.fontMetrics().boundingRect(self.logValRight_label.text()).width()
        paddedRightWidth = int(logValRightWidth + logValRightWidth/self.VALUE_PADDING)
        self.logValRight_label.setFixedWidth(paddedRightWidth)
        assert self.log.log_plot_right != None
        assert self.log.log_plot_right != ""

        fullLabelWidths =  (paddedLeftWidth + paddedNameWidth + paddedRightWidth)
        labelList = []
        #drop units if doesn't fit
        if self.track.geometry().width() < fullLabelWidths:
            self.logName_label.setText(self.log.name)
            logNameWidthNoUnit = self.logName_label.fontMetrics().boundingRect(self.logName_label.text()).width()
            paddedNameWidthNoUnit = int(logNameWidthNoUnit + logNameWidthNoUnit/10)
            labelWidths =  (paddedLeftWidth + paddedNameWidthNoUnit + paddedRightWidth)
            #drop l and R vals if still doesn't fit
            if self.track.geometry().width() < labelWidths:
                self.logName_label.setFixedWidth(paddedNameWidthNoUnit)
                labelList.append(self.logName_label)

            else:
                self.logName_label.setFixedWidth(paddedNameWidthNoUnit)
                labelList.append(self.logValLeft_label)
                labelList.append(self.logName_label)
                labelList.append(self.logValRight_label)
        else:
            self.logName_label.setFixedWidth(paddedNameWidth)
            labelList.append(self.logValLeft_label)
            labelList.append(self.logName_label)
            labelList.append(self.logValRight_label)
            
        hbox = self.createHBoxWithLabels(labelList, True)
        return hbox
    
    def createDoubleRowLabelBox(self):
        logger.debug("--setupUI() two row header labels")
        vBox = QtGui.QVBoxLayout()
        vBox.setMargin(0)
        
        self.logName_label = QtGui.QLabel()
        self.logName_label.setText(self.log.name)
        hbox = self.createBoxWithCentredLabel(self.logName_label)
        
        self.logValLeft_label = QtGui.QLabel()
        self.logValLeft_label.setText(str(self.log.log_plot_left))
        assert self.log.log_plot_left != None
        assert self.log.log_plot_left != ""
        
        units = LogDao.getUnits(self.log)
        logUnit_label = QtGui.QLabel()
        logUnit_label.setText(units)
        
        self.logValRight_label = QtGui.QLabel()
        self.logValRight_label.setText(str(self.log.log_plot_right))
        assert self.log.log_plot_right != None
        assert self.log.log_plot_right != ""

        lowerRowLables = []
        lowerRowLables.append(self.logValLeft_label)
        lowerRowLables.append(logUnit_label)
        lowerRowLables.append(self.logValRight_label)
        valHbox = self.createHBoxWithLabels(lowerRowLables)
        
        vBox.addLayout(hbox)
        vBox.addLayout(valHbox)
        return vBox
        
    def createBoxWithCentredLabel(self, label):
        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addStretch(1)
        hbox.addWidget(label)
        hbox.addStretch(1)
        return hbox
    
    def createHBoxWithLabels(self, labels, addStretch=True):
        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        for label in labels:
            hbox.addWidget(label)
            if addStretch:
                hbox.addStretch(1)
        return hbox

    
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
        labelMargin = self.logName_label.margin()
        yLevel = self.logName_label.rect().bottomLeft().y()
        xStart = labelMargin
        xStop = self.track.geometry().width() - labelMargin
        #line is relative to widget not screen
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