'''
Created on 21 Dec 2014

@author: a
'''
import unittest
import logging

from inout.las.reader.dto.domainunitsetter import DomainUnitSetter
from statics.types.logtype import LogType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DomainUnitSetterTest(unittest.TestCase):
    """ generated source for class DomainUnitSetterTest """
    def test_findDepthUnitsMatchTest(self):
        """ generated source for method findDepthUnitsMatchTest """

        logger.debug(">>test_findDepthUnitsMatchTest()")
        dus = DomainUnitSetter()
        match = str()
        
        match = dus.findDepthUnitsMatch("m", LogType.DEPTH)
        self.assertEquals("m", match)
        match = dus.findDepthUnitsMatch("meters", LogType.DEPTH)
        self.assertEquals("meters", match)
        match = dus.findDepthUnitsMatch("ft", LogType.DEPTH)
        self.assertEquals("ft", match)
        match = dus.findDepthUnitsMatch("feet", LogType.DEPTH)
        self.assertEquals("feet", match)
        match = dus.findDepthUnitsMatch("ms", LogType.TIME)
        self.assertEquals("ms", match)
        match = dus.findDepthUnitsMatch("s", LogType.TIME)
        self.assertEquals("s", match)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()