import unittest
from PyQt4 import QtCore
from gui.signals.wellplotsignals import WellPlotSignals
import logging

logger = logging.getLogger('console')

class WellPlotSignalObject(QtCore.QObject):
    
    def __init__(self, parent = None):
        super(WellPlotSignalObject, self).__init__(parent)
        #test
        self.testSignal()
        #end test
        
    #test
    def testSignal(self):
        self.wellPlotSignals = WellPlotSignals()
        self.wellPlotSignals.logPlotSettingsModified.connect(self.testSignalLogger)
        #self.wellPlotSignals.core_event.connect(self.testSignalEventLogger)
        
    def testSignalLogger(self):
        logger.debug(">>testSignalLogger logPlotIndexesModified intercepted")
        
    
    
class WellPlotSignalsTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(WellPlotSignalsTest, self).__init__(*args, **kwargs)
    
   
    def test_signal(self):
        wps = WellPlotSignalObject()