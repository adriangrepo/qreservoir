
import unittest
import logging
from db.test.dummydbsetup import DummyDbSetup
from PyQt4.QtGui import QApplication, QWidget
import sys
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess

from db.core.well.welldao import WellDao
from db.databasemanager import DM
from db.core.well.well import Well

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class WellDaoTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(WellDaoTest, self).__init__(*args, **kwargs)
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
    
    def test_getMdLength(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)

        self.dummyDbSetup.setupDatabase()
        well = self.createWell(-200, -1200, 'first')
        #logs = self.dummyDbSetup.create1Log(well.id)
        mdLength = well.getMdLength()
        logger.debug("--test_getMdLength() mdLength:{0}".format(mdLength))
        self.assertEqual(1000, mdLength)
        
        well = self.createWell(-200, -100, 'second')
        #logs = self.dummyDbSetup.create1Log(well.id)
        mdLength = well.getMdLength()
        logger.debug("--test_getMdLength() mdLength:{0}".format(mdLength))
        self.assertEqual(100, mdLength)
        
        well = self.createWell(200, -1200, 'third')
        #logs = self.dummyDbSetup.create1Log(well.id)
        mdLength = well.getMdLength()
        logger.debug("--test_getMdLength() mdLength:{0}".format(mdLength))
        self.assertEqual(1400, mdLength, "start: 200 stop: -1200")
        
        well = self.createWell(200, 1200, 'fourth')
        #logs = self.dummyDbSetup.create1Log(well.id)
        mdLength = well.getMdLength()
        logger.debug("--test_getMdLength() mdLength:{0}".format(mdLength))
        self.assertEqual(1000, mdLength)
        
        well = self.createWell(200, 100, 'fifth')
        #logs = self.dummyDbSetup.create1Log(well.id)
        mdLength = well.getMdLength()
        logger.debug("--test_getMdLength() mdLength:{0}".format(mdLength))
        self.assertEqual(100, mdLength)
        
        well = self.createWell(-200, 1200, 'sixth')
        #logs = self.dummyDbSetup.create1Log(well.id)
        mdLength = well.getMdLength()
        logger.debug("--test_getMdLength() mdLength:{0}".format(mdLength))
        self.assertEqual(1400, mdLength)
        
if __name__ == '__main__':
    unittest.main()
    