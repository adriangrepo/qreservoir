import logging
import unittest
from db.test.dummydbsetup import DummyDbSetup
from PyQt4.QtGui import QApplication
import sys
from db.windows.wellplot.template.wellplottemplateinitializer import WellPlotTemplateInitialiser
from db.core.basedao import BaseDao
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from statics.types.zaxis import ZAxis
from statics.types.unit import Unit
from statics.types.referenceleveltype import ReferenceLevelType
from statics.templates.wellplottype import WellPlotType
from statics.types.logtype import LogType
from db.windows.wellplot.wellplotdata.wellplotdatadao import WellPlotDataDao

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("console")


class WellPlotDefaultsInitializerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        logger.debug(">>__init__()")
        super(WellPlotDefaultsInitializerTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()

        
    def test___initialiseWellPlotDefaults(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)
        self.dummyDbSetup.setupDatabase()
        
        #WellPlotTemplateInitialiser is run in db setup so don't need to re-run it here
        wellPlotPrefs = WellPlotDataDao.getWellPlotPreferences()



        logger.debug("uid: {0} well_id: {1}".format(wellPlotPrefs.uid, wellPlotPrefs.well_id))
