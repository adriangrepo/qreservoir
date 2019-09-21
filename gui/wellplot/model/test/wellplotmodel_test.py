
import unittest
import logging
from db.test.dummydbsetup import DummyDbSetup
from PyQt4.QtGui import QApplication
import sys
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from db.defaultsinitialiser import DefaultsInitialiser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('console')

class WellPlotModelTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(WellPlotModelTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()

        
    def test_createWellPlotData(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)
        self.dummyDbSetup.setupDatabase()

        well = self.dummyDbSetup.createWell()
        logs = self.dummyDbSetup.create3Logs(well.id)
        
        templateDao = WellPlotTemplateDao()
        logger.debug("--test_createWellPlotData() created WellPlotTemplateDao()")
        allTemplaes = templateDao.getAllWellPlotTemplates()
        logger.debug("--test_createWellPlotData() created templateDao.getAllWellPlotTemplates() len:{0}".format(len(allTemplaes)))
        template = allTemplaes[0]
        #need to run as properties are called inside init() method
        template.__init__()
        logger.debug("uid: {0}, name: {1}".format(template.uid, template.name))
        uid = 42
        wellPlotModelAccess = WellPlotModelAccess()
        logger.debug("--test_createWellPlotData() created WellPlotModelAccess() template[0].name:{0}".format(template.name))
        wellPlotData = wellPlotModelAccess.createWellPlotData(logs, uid, well, template)
        logger.debug("--test_createWellPlotData() created wellPlotModelAccess.createWellPlotData()")
        self.assertEquals(uid, wellPlotData.uid)
        logger.debug("TODO test all other properties")  
    
    
        
if __name__ == '__main__':
    unittest.main()
    