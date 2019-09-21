from __future__ import absolute_import

from PyQt4 import QtCore 
from PyQt4.QtCore import QObject
from pyqtgraph import LinearRegionItem


import logging
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData
from db.core.well.well import Well
from gui.util.pymimedata import PyMimeData


logger = logging.getLogger('console')

__WPSInstance = None

def WellPlotSignals(*args, **kw):
    global __WPSInstance
    if __WPSInstance is None:
        __WPSInstance = __WellPlotSignals(*args, **kw)
    return __WPSInstance


class __WellPlotSignals(QObject):
    ''' well plot signal object '''

    #emit signal when plot has been changed
    logPlotSettingsModified = QtCore.pyqtSignal(WellPlotData)
    logPlotCurveColourModified = QtCore.pyqtSignal()
    
    wellSelectionChanged = QtCore.pyqtSignal(Well)
    
    #settings
    settingsOpenFired = QtCore.pyqtSignal()
    settingsTrackLayoutItemDropped = QtCore.pyqtSignal(PyMimeData)
    
    #overview
    overviewRegionChange = QtCore.pyqtSignal(WellPlotData, LinearRegionItem)
    overviewRegionChangeFinished = QtCore.pyqtSignal(WellPlotData, LinearRegionItem)
    
    #toolbar signals
    #these need to connect to wellPlotPG as redrawing sizes
    toolbarZoomIn = QtCore.pyqtSignal()
    toolbarZoomOut = QtCore.pyqtSignal()
    toolbarZoomBox = QtCore.pyqtSignal()
    #can just connect to overview widget and change region
    toolbarZoomInVertical = QtCore.pyqtSignal()
    toolbarZoomOutVertical = QtCore.pyqtSignal()
    
    toolbarPoint = QtCore.pyqtSignal()
    toolbarPan = QtCore.pyqtSignal()
    toolbarHzLine = QtCore.pyqtSignal()
    
    
    def __init__(self):
        QObject.__init__(self)