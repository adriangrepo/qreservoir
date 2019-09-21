from PyQt4 import QtCore as QC

from views.core.test.senderobject import SenderObject
from views.core.test.roimanager import ROIManager
from views.core.test import logsettingstoolbar

import logging

logger = logging.getLogger(__name__)   
        
class WellPlotTest(QC.QObject):
    def __init__(self, parent = None):
        super(WellPlotTest, self).__init__(parent)
        logger.debug("--__init__()")
        self.wellPlotSignals = WellPlotSignals()
        self.roimanager = ROIManager()
        self.createToolWidget()
        self.connectSlots()
        self.createToolWidget()
        
    def connectSlots(self):
        logger.debug(">>connectSlots")
        self.wellPlotSignals.logPlotSettingsModified.connect(self.replotLogs)
        #self.roimanager.add_snaproi()
        
    def replotLogs(self):
        logger.debug(">>replotLogs")
        
    def createToolWidget(self):
        logger.debug(">>createToolWidget()")
        toolbar = logsettingstoolbar.LogSettingsToolbar()
        toolbar.emitShowToolbarSignal()
        logger.debug("<<createToolWidget() toolbar created")