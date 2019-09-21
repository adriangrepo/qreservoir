
import unittest
import logging
from db.test.dummydbsetup import DummyDbSetup
from PyQt4.QtGui import QApplication, QWidget
import sys
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess

from db.core.well.welldao import WellDao
from db.databasemanager import DM
from db.core.well.well import Well
from db.core.logservice.logservicedao import LogServiceDao

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LogServiceDaoTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(LogServiceDaoTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()

    def createWell(self, mdstart, mdstop, wellName):
        logger.debug(">>createWell() ")
        session = DM.getSession()
        well = Well()
        well.name = wellName
        well.depth_reference = "MDKB"
        well.elevation_of_depth_reference = "24.0"
        well.mdstart = mdstart
        well.mdstop = mdstop
        session.add(well)
        session.commit()
        dummyWell = session.query(Well).filter(Well.name == wellName).one()
        assert wellName == dummyWell.name
        session.close()
        return dummyWell
    
    def test_getAllLogServicesForWell(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)

        self.dummyDbSetup.setupDatabase()
        well = self.dummyDbSetup.createWell()
        logs = self.dummyDbSetup.create3VariableDepthLogs(well.id)
        logServices = LogServiceDao.getAllLogServicesForWell(well.id)
        
if __name__ == '__main__':
    unittest.main()
    