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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class WellPlotTemplateInitializerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        logger.debug(">>__init__()")
        super(WellPlotTemplateInitializerTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()

        
    def test__initialiseWellTemplateDefaults(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)
        self.dummyDbSetup.setupDatabase()
        
        #WellPlotTemplateInitialiser is run in db setup so don't need to re-run it here
        templates = WellPlotTemplateDao.getAllWellPlotTemplates()
        self.assertEqual(9, len(templates))

        zAxisCounter = 0
        trackCounter = 0
        zAxis = ZAxis.NONE
        zAxisClassName = zAxis.__class__.__name__
        logType = LogType.GAMMA
        logTypeClassName = logType.__class__.__name__
        for template in templates:
            if template.uid == "triplecombo":
                #template.__init__()
                self.assertEqual(0, template._primary_z_track_index)
                self.assertEqual("", template._primary_z_track_name)
                self.assertEqual(ZAxis.MD.uid, template._primary_z_type)
                
                self.assertEqual(ReferenceLevelType.KB.uid, template._primary_z_reference)
                for zAxis in template.getZAxes():
                    if zAxisCounter == 0:
                        for zAxisKey, zAxisValue in zAxis.items():
                            if zAxisKey == WellPlotType.INDEX:
                                self.assertEqual(4, zAxisValue)
                            elif zAxisKey == WellPlotType.TRACKNAME:
                                self.assertEqual("", zAxisValue)
                            elif zAxisKey == zAxisClassName:
                                self.assertEqual(ZAxis.TVD.uid, zAxisValue)
                            elif zAxisKey == WellPlotType.ZAXISUNIT:
                                self.assertEqual(Unit.METER._symbol, zAxisValue)
                            elif zAxisKey == WellPlotType.ZAXISREFERENCELEVEL:
                                self.assertEqual(ReferenceLevelType.MSL.uid, zAxisValue)
                    zAxisCounter += 1
                for track in template._tracks:   
                    if trackCounter == 0:        
                        for trackKey, trackValue in track.items():
                            if trackKey == WellPlotType.INDEX:
                                self.assertEqual(1, trackValue)
                            elif trackKey == WellPlotType.TRACKNAME:
                                self.assertEqual("", trackValue)
                            elif trackKey == logTypeClassName:
                                logCount = 0
                                for log in trackValue:
                                    if logCount == 0:
                                        self.assertEqual(LogType.GAMMA.name, log)
                                    elif logCount == 1:
                                        self.assertEqual(LogType.CAL.name, log)
                                    elif logCount == 2:
                                        self.assertEqual(LogType.SP.name, log)
                                    logCount += 1
                    trackCounter += 1
