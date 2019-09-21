
import unittest
import logging
from db.test.dummydbsetup import DummyDbSetup
from PyQt4.QtGui import QApplication, QWidget
import sys
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess

from db.core.well.welldao import WellDao
from db.databasemanager import DM
from db.core.well.well import Well
from db.core.log.log import Log

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LogTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(LogTest, self).__init__(*args, **kwargs)

    def test_findLogWithLargestDepthRange(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)

        self.dummyDbSetup = DummyDbSetup()
        self.dummyDbSetup.setupDatabase()
        
        session = DM.getSession()
        well = self.dummyDbSetup.createWell()
        logs = self.dummyDbSetup.create3VariableDepthLogs(well.id)
        log = Log()
        longestLog = log.findLogWithLargestDepthRange(logs)
        self.assertEqual("3SP", longestLog.name)
        
       
        
if __name__ == '__main__':
    unittest.main()
    