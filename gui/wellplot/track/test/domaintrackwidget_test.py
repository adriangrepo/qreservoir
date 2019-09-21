
import unittest
import logging

from PyQt4.QtGui import QApplication, QWidget
from PyQt4.QtTest import QTest
import sys

from db.test.dummydbsetup import DummyDbSetup
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess

from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from statics.templates.wellplottype import WellPlotType

from gui.util.wellplotutils import WellPlotUtils
from gui.wellplot.track.domaintrackwidget import DomainTrackWidget

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DomainTrackWidgetTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(DomainTrackWidgetTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()
        self.app = QApplication(sys.argv)


        
    def getWellPLotdata(self):

        self.dummyDbSetup.setupDatabase()
        well = self.dummyDbSetup.createWell()
        logs = self.dummyDbSetup.create3Logs(well.id)
        wellPlotModelAccess = WellPlotModelAccess()
        uid = 42
        templateDao = WellPlotTemplateDao()
        allTemplates = templateDao.getAllWellPlotTemplates()
        template = None
        for item in allTemplates:
            if item.uid == WellPlotType.ALLLOGS.uid:
                template = item
        wellPlotData = wellPlotModelAccess.createWellPlotData(logs, uid, well, template)
        return wellPlotData
    
    def test_generateDomainPlot(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)

        self.dummyDbSetup.setupDatabase()
        well = self.dummyDbSetup.createWell()
        logs = self.dummyDbSetup.create1Log(well.id)
        track = QWidget()
        track.setFixedWidth(180)
        wellPlotData = self.getWellPLotdata()
        self.assertIsNotNone(wellPlotData, "wellPlotData is None")
        
        domainStart, domainStop, domainStep= WellPlotUtils.calculateStartStopStep(wellPlotData.getLogTrackDatas())
        plots = []
        i = 0
        for domainTrackData in wellPlotData.getZAxisDatas(): 
            if i == 0:           
                domainTrackWidget = DomainTrackWidget(well, isPrimaryDomainTrack = True)
            else:
                domainTrackWidget = DomainTrackWidget(well, isPrimaryDomainTrack = False)
            domainTrackWidget.generateDomainPlot(domainTrackData, wellPlotData, domainStart, domainStop, domainStep)
            plots.append(domainTrackWidget)
        self.assertEqual(1, len(plots), "length incorrect")
                
if __name__ == '__main__':
    unittest.main()
    