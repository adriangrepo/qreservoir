import logging
from PyQt4.QtGui import QWidget
from PyQt4 import QtCore

logger = logging.getLogger('console')

class WellPlotWidget(QWidget):
    def __init__(self, parent = None):
        super(WellPlotWidget, self).__init__(parent)
        self.installEventFilter(self)
        self.logPlotData = None
        self.data = None
        
    def setLogPlotData(self, wellPlotData):
        self.logPlotData = wellPlotData
        
    def setData(self, data):
        self.data = data

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            logger.debug( "widget window has gained focus ")
        elif event.type()== QtCore.QEvent.WindowDeactivate:
            logger.debug( "widget window has lost focus")
        elif event.type()== QtCore.QEvent.FocusIn:
            logger.debug( "widget has gained keyboard focus")
        elif event.type()== QtCore.QEvent.FocusOut:
            logger.debug( "widget has lost keyboard focus")

        return False