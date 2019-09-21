from __future__ import absolute_import

from PyQt4.QtGui import QToolBar
from PyQt4 import QtGui, QtCore 
from PyQt4.QtCore import QObject
from pyqtgraph import LinearRegionItem



import logging
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData
from db.core.well.well import Well
from gui.util.pymimedata import PyMimeData


logger = logging.getLogger('console')

__SOInstance = None

def SenderObject(*args, **kw):
    global __SOInstance
    if __SOInstance is None:
        __SOInstance = __SenderObject(*args, **kw)
    return __SOInstance


class __SenderObject(QObject):
    ''' general signal object '''

    core_event = QtCore.pyqtSignal()

    
    def __init__(self):
        QObject.__init__(self)
        

    
'''
class SenderObject(QtCore.QObject):
    
    core_event = QtCore.pyqtSignal()
    #emit signal when plot has been changed
    logPlotSettingsModified = QtCore.pyqtSignal()
'''

#__Instance = None


# EventObject Singleton
def EventObject(*args, **kw):
    global __Instance
    if __Instance is None:
        __Instance = __EventObject(*args, **kw)
    return __Instance


class __EventObject(QObject):
    ''' similar to actions class in ninja ide '''


    def __init__(self):
        QObject.__init__(self)
        
    def connectEvents(self, mainApp):
        """Install the shortcuts to the IDE."""
        self.mainApp = mainApp
        self.actionImportFile.triggered.connect(self.importFileAction)

    def importFileAction(self):
        pass