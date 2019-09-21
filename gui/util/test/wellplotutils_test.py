
import unittest
import logging
from db.test.dummydbsetup import DummyDbSetup
from PyQt4.QtGui import QApplication, QWidget
import sys
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess

from gui.util.wellplotutils import WellPlotUtils
from db.core.log.logdao import LogDao
from db.defaultsinitialiser import DefaultsInitialiser
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class WellPlotUtilsTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(WellPlotUtilsTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()

    
    def getWellPlotdata(self):

        self.dummyDbSetup.setupDatabase()
        templates = WellPlotTemplateDao.getAllWellPlotTemplates()
        assert 9 == len(templates), "Incorrect template number: {0}".format(len(templates))

        templates = WellPlotTemplateDao.getAllWellPlotTemplates()
        
        well = self.dummyDbSetup.createWell()
        self.dummyDbSetup.create1Log(well.id)
        logs = LogDao.getWellLogs(well.id)
        wellPlotModelAccess = WellPlotModelAccess()
        uid = 42
        templateDao = WellPlotTemplateDao()
        #allTemplates = templateDao.getAllWellPlotTemplates()
        template = templateDao.getWellPlotTemplateFromUid("alllogs")
        #template = allTemplates[0]
        template.__init__()
        wellPlotData = wellPlotModelAccess.createWellPlotData(logs, uid, well, template)
        return wellPlotData
    
    
    def test_calculateStartStopStep(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)

        wellPlotData = self.getWellPlotdata()
        self.assertIsNotNone(wellPlotData, "Is None")
        
        start, stop, step = WellPlotUtils.calculateStartStopStep(wellPlotData.getLogTrackDatas())
        logger.debug("--test_calculateStartStopStep() start:{0} stop:{1} step:{2}".format(start, stop, step))
                
if __name__ == '__main__':
    unittest.main()