
from __future__ import absolute_import

from PyQt4.QtGui import QToolBar, QLabel, QPixmap, QApplication, QCursor
from PyQt4 import QtGui, QtCore 
from PyQt4.QtCore import pyqtSlot, Qt

from views.core import centraltabwidget


from gui.wellplot.subplots.wellplotwidget import WellPlotWidget
from globalvalues.appsettings import AppSettings
from gui.wellplot.settings.templatesettingsdialog import TemplateSettingsDialog
from gui.signals.wellplotsignals import WellPlotSignals


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

import logging

logger = logging.getLogger('console')

__Instance = None

class Communicator(QtCore.QObject):
    
    hideToolbar = QtCore.pyqtSignal() 
    showToolbar = QtCore.pyqtSignal() 

# LogSettingsToolbar Singleton
def LogSettingsToolbar(*args, **kw):
    global __Instance
    if __Instance is None:
        __Instance = __LogSettingsToolbar(*args, **kw)
    return __Instance


class __LogSettingsToolbar(QToolBar):

    def __init__(self, parent=None):
        super(QToolBar, self).__init__(parent)
        self.parent = parent
        self.toolbar = None
        self.wellPlotSignals = WellPlotSignals()
        self.communicator = Communicator()
        self.initUI()

        
    def initUI(self):
        #self.toolBarRHS = QtGui.QToolBar(self.parent)
        #self.setObjectName(_fromUtf8("toolBarRHS"))
        self.actionSettings = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"settings_eclipse.gif"), '&Settings', self.parent)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionSettings.setStatusTip('Settings')
        #self.actionZoomIn = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"zoom-in-5.png"), '&Zoom in', self.parent)
        #self.actionZoomIn.setObjectName(_fromUtf8("actionZoomIn"))
        #self.actionZoomIn.setStatusTip('Zoom in')
        #self.actionZoomOut = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"zoom-out-5.png"), '&Zoom out', self.parent)
        #self.actionZoomOut.setObjectName(_fromUtf8("actionZoomOut"))
        #self.actionZoomOut.setStatusTip('Zoom out')
        self.actionPoint = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"pointer_edit-select.png"), '&Point', self.parent)
        self.actionPoint.setObjectName(_fromUtf8("actionPoint"))
        self.actionPoint.setStatusTip('Point')
        #self.actionPan = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"hand-cursor-16.png"), '&Pan', self.parent)
        #self.actionPan.setObjectName(_fromUtf8("actionPan"))
        #self.actionPan.setStatusTip('Pan')
        self.actionZoomInVertical = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"zoom-in-5_vertical.png"), '&Vertical zoom in', self.parent)
        self.actionZoomInVertical.setObjectName(_fromUtf8("actionZoomInVertical"))
        self.actionZoomInVertical.setStatusTip('Zoom in vertically')
        self.actionZoomOutVertical = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"zoom-out-5_vertical.png"), '&Vertical zoom out', self.parent)
        self.actionZoomOutVertical.setObjectName(_fromUtf8("actionZoomOutVertical"))
        self.actionZoomOutVertical.setStatusTip('Zoom out vertically')
        
        #self.actionZoomBox = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"zoom-in-5_box2.png"), '&Box zoom', self.parent)
        #self.actionZoomBox.setObjectName(_fromUtf8("actionZoomBox"))
        #self.actionZoomBox.setStatusTip('Box zoom')
        self.actionLevelLine = QtGui.QAction(QtGui.QIcon(AppSettings.ACTIONS_ICON_PATH+"snap-orto_hx.png"), '&Level', self.parent)
        self.actionLevelLine.setObjectName(_fromUtf8("actionLevelLine"))
        self.actionLevelLine.setStatusTip('Level line')
        
        self.addAction(self.actionSettings)
        self.addSeparator()
        #self.addAction(self.actionZoomIn)
        #self.addAction(self.actionZoomOut)
        self.addAction(self.actionZoomInVertical)
        self.addAction(self.actionZoomOutVertical)
        #self.addAction(self.actionZoomBox)
        self.addSeparator()
        self.addAction(self.actionPoint)
        #self.addAction(self.actionPan)
        self.addAction(self.actionCrossHairs)

        self.actionSettings.triggered.connect(self.actionSettingsTriggered)
        #self.actionZoomIn.triggered.connect(self.actionZoomInTriggered)
        #self.actionZoomOut.triggered.connect(self.actionZoomOutTriggered)
        self.actionZoomInVertical.triggered.connect(self.actionZoomInVerticalTriggered)
        self.actionZoomOutVertical.triggered.connect(self.actionZoomOutVerticalTriggered)
        #self.actionZoomBox.triggered.connect(self.actionZoomBoxTriggered)
        self.actionPoint.triggered.connect(self.actionPointTriggered)
        #self.actionPan.triggered.connect(self.actionPanTriggered)
        self.actionLevelLine.triggered.connect(self.actionHzLineTriggered)
        self.wellPlotSignals.settingsOpenFired.connect(self.showSettingsSlot)
        logger.debug("--initUI() showToolbar.emit()")
        
        
    def emitShowToolbarSignal(self):
        logger.debug(">>emitShowToolbarSignal() ")
        self.communicator.showToolbar.emit()
        
    @pyqtSlot()
    def showSettingsSlot(self):
        '''RMB on well plot, select settings triggers a signal intercepted here'''
        self.actionSettingsTriggered()
        
    def actionSettingsTriggered(self):
        logger.debug(">>actionSettings()")
        centralWidget = centraltabwidget.CentralTabWidget()
        currentWidget = centralWidget.currentWidget()
        #for widget in centralWidget.children():
        if isinstance(currentWidget, WellPlotWidget):
            logger.debug("--actionSettingsTriggered "+str(currentWidget.data))
            logPlotData = currentWidget.logPlotData
            if self.well != None:
                if self.logSet == None:
                    dialog = TemplateSettingsDialog(logPlotData, self.well, parent = self)
                else:
                    dialog = TemplateSettingsDialog(logPlotData, self.well, self.logSet, parent = self)
                dialog.show()
        
    '''
    #Leave out for now, see TODO 4/7/15 for notes on options to connect up
    def actionZoomInTriggered(self):
        self.wellPlotSignals.toolbarZoomIn.emit()
        
    def actionZoomOutTriggered(self):
        self.wellPlotSignals.toolbarZoomOut.emit()
    '''
        
    def actionZoomInVerticalTriggered(self):
        self.wellPlotSignals.toolbarZoomInVertical.emit()

    def actionZoomOutVerticalTriggered(self):
        self.wellPlotSignals.toolbarZoomOutVertical.emit()
        
    '''
    #Box zoom is more for a single track plot - eg a log QC rather than multiple tracks
    #May want to add a test to initiation - if well plot, hide, if single track plot show
    def actionZoomBoxTriggered(self):
        logger.debug(">>actionZoomBox()")
        self.wellPlotSignals.toolbarZoomBox.emit()
    '''
        
    def actionPointTriggered(self):
        logger.debug(">>actionPoint()")
        self.wellPlotSignals.toolbarPoint.emit()

    '''
    #Leave out for now, not core functionality
    def actionPanTriggered(self):
        logger.debug(">>actionPan()")
        self.wellPlotSignals.toolbarPan.emit()
    '''
        
    def actionHzLineTriggered(self):
        logger.debug(">>actionHzLineTriggered()")
        self.wellPlotSignals.toolbarHzLine.emit()

