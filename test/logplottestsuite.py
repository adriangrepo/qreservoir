import unittest

from gui.wellplot.subplots.test.headerplottest import HeaderPlotTest
from inout.las.reader.test.lasreader_test import LasReaderTest
from inout.las.reader.orm.test.laspersister_test import LasPersisterTest
from gui.wellplot.subplots.test.wellplottest import WellPlotTest

class LogPlotTestSuite(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

def suite():

    suite = unittest.TestSuite()
    suite.addTest (WellPlotTest())
    suite.addTest (HeaderPlotTest())
    suite.addTest (LasReaderTest())
    suite.addTest (LasPersisterTest())

    return suite

 

 

if __name__ == '__main__':

    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run (test_suite)  