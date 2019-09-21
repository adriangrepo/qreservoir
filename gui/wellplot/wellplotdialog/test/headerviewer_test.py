
import unittest
import logging
from db.test.dummydbsetup import DummyDbSetup
from PyQt4.QtGui import QApplication, QWidget
import sys
from gui.wellplot.model.wellplotmodelaccess import WellPlotModelAccess
from gui.wellplot.wellplotdialog.headerviewer import LogHeaderLabel
from db.windows.wellplot.template.wellplottemplatedao import WellPlotTemplateDao
from statics.templates.wellplottype import WellPlotType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HeaderViewerTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(HeaderViewerTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()

        
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
    
    def test_LogHeaderLabel(self):
        #QWidget: Must construct a QApplication before a QPaintDevice
        app = QApplication(sys.argv)

        self.dummyDbSetup.setupDatabase()
        well = self.dummyDbSetup.createWell()
        logs = self.dummyDbSetup.create1Log(well.id)
        track = QWidget()
        track.setFixedWidth(180)
        wellPlotData = self.getWellPLotdata()
        self.assertIsNotNone(wellPlotData, "Is None")
        logHeaderLabel = LogHeaderLabel(logs[0], track, wellPlotData)
        boundWidth = logHeaderLabel.logName_label.fontMetrics().boundingRect(logHeaderLabel.logName_label.text()).width()
        self.assertEquals(track.geometry().width(), logHeaderLabel.geometry().width())
        self.assertEquals("SWIRR", logHeaderLabel.logName_label.text())
        logger.debug("--test_LogHeaderLabel() name bound width:{0} name width:{1}".format(boundWidth, logHeaderLabel.logName_label.geometry().width() ))
        logger.debug("--test_LogHeaderLabel() Lval x:{0} name x:{1} Rval x:{2}".format(logHeaderLabel.logValLeft_label.geometry().x(), logHeaderLabel.logName_label.geometry().x(), logHeaderLabel.logValRight_label.geometry().x() ))
        summedWidth = logHeaderLabel.logValLeft_label.geometry().width()+ logHeaderLabel.logName_label.geometry().width()+logHeaderLabel.logValRight_label.geometry().width()
        logger.debug("--test_LogHeaderLabel()summed width:{0}".format(summedWidth))
        
if __name__ == '__main__':
    unittest.main()
    