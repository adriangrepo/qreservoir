
from globalvalues.appsettings import AppSettings

from PyQt4.QtGui import QApplication
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import unittest



#import logging
import logging.config
from gui.wellplot.overview.overviewwidgethandler import OverviewWidgetHandler



logging.config.fileConfig(AppSettings.getLoggingConfig())
# create logger
logger = logging.getLogger('console')

class OverviewWidgetHandlerTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(OverviewWidgetHandlerTest, self).__init__(*args, **kwargs)
    
    def test_calcZoomWhenMinMaxSameSign(self):
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomWhenMinMaxSameSign(0, 1000, zoomIn=True)
        self.assertEqual(200.0, zoomedMinY)
        self.assertEqual(800.0, zoomedMaxY)
        
    
    def test_calcZoomWhenMinMaxSameSign1(self):
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomWhenMinMaxSameSign(200, 1200, zoomIn=True)
        self.assertEqual(400.0, zoomedMinY)
        self.assertEqual(1000.0, zoomedMaxY)
    
      
    
    def test_calcZoomWhenMinMaxSameSign2(self):
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomWhenMinMaxSameSign(-1200, -200, zoomIn=True)
        self.assertEqual(-1000.0, zoomedMinY)
        self.assertEqual(-400.0, zoomedMaxY)
    
        
    def test_calcZoomInMinMax0(self):
        app = QtGui.QApplication([])
        win = pg.GraphicsWindow()
        p1 = win.addPlot(row=1, col=0)
        region = pg.LinearRegionItem()
        
        region.setRegion([0, 1000])
        
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomInMinMax(region)
        self.assertEqual(200.0, zoomedMinY)
        self.assertEqual(800.0, zoomedMaxY)
    
    def test_calcZoomInMinMax1(self):
        app = QtGui.QApplication([])
        win = pg.GraphicsWindow()
        p1 = win.addPlot(row=1, col=0)
        region = pg.LinearRegionItem()
        
        region.setRegion([-100, 900])
        
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomInMinMax(region)
        self.assertEqual(100.0, zoomedMinY)
        self.assertEqual(700.0, zoomedMaxY)
    
    def test_calcZoomInMinMax2(self):
        app = QtGui.QApplication([])
        win = pg.GraphicsWindow()
        p1 = win.addPlot(row=1, col=0)
        region = pg.LinearRegionItem()
        
        region.setRegion([-1100, -100])
        
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomInMinMax(region)
        self.assertEqual(-900.0, zoomedMinY)
        self.assertEqual(-300.0, zoomedMaxY)
    
    def test_calcZoomInMinMax3(self):
        app = QtGui.QApplication([])
        win = pg.GraphicsWindow()
        p1 = win.addPlot(row=1, col=0)
        region = pg.LinearRegionItem()
        
        region.setRegion([100, 1100])
        
        overviewWidgetHandler = OverviewWidgetHandler()
        zoomedMinY, zoomedMaxY = overviewWidgetHandler.calcZoomInMinMax(region)
        self.assertEqual(300.0, zoomedMinY)
        self.assertEqual(900.0, zoomedMaxY)
    
        
if __name__ == '__main__':
    unittest.main()