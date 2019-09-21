'''
Created on 29 Dec 2014

@author: a
'''
import unittest
import logging


from qrutilities.systemutils import SystemUtils
from globalvalues.appsettings import AppSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('console')

class SystemUtilsTest(unittest.TestCase):


    #fails as returns too much info
    '''
    def test_getProcessorDetails(self):
        logger.debug(">>test_getProcessorDetails()")
        processorName = AppSettings.getProcessorDetails()
        self.assertTrue("Pentium"==processorName, 'expected value {0} actual value {1}'.format("Pentium", str(processorName))) 
    '''

    def test_availableCpuCount(self):
        logger.debug(">>test_availableCpuCount()")
        availableCpuCount = SystemUtils.availableCpuCount()
        self.assertTrue(8==availableCpuCount, 'expected value {0} actual value {1}'.format("Pentium", str(availableCpuCount))) 
        
    def test_getProcessorName(self):
        logger.debug(">>test_getProcessorName()")
        processorName = AppSettings.processorName
        logger.debug(processorName)
        self.assertTrue("x86_64"==processorName, 'expected value {0} actual value {1}'.format("x86_64", str(processorName)))     
        
    #fails due to string formatting
    '''
    def test_pythonRuntimeVersion(self):
        logger.debug(">>test_pythonRuntimeVersion()")
        pythonRuntimeVersion = AppSettings.pythonRuntimeVersion
        self.assertTrue("sys.version_info(major=3, minor=4, micro=0, releaselevel='final', serial=0)"==pythonRuntimeVersion, 'expected value {0} actual value {1}'.format("sys.version_info(major=3, minor=4, micro=0, releaselevel='final', serial=0)", str(pythonRuntimeVersion)))   
    '''
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()