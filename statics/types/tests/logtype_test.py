


import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from statics.types.logtype import LogType

class LogTypeTest(unittest.TestCase):
    
    """ generated source for class LogTypeTest """
    def test_findFromMnemonic0(self):
        """ generated source for method getLogTypeFromString0_Test """
        log = "RHOB"
        logType = LogType.findLogTypeFromMnemonic(log)
        self.assertTrue(logType.RHO.__str__().lower() == logType.__str__().lower())

    def test_findFromMnemonic1(self):
        logger.debug(">>test_findFromMnemonic1")
        logType = LogType.findLogTypeFromMnemonic("VQtz")
        self.assertTrue("Volume fraction" == logType.name)
        
    def test_getIndex(self):
        logger.debug(">>test_getIndex")
        logType = LogType.findLogTypeFromMnemonic("Time")
        index = logType.getIndex()
        self.assertTrue(5 == index)
        
    def test_getCurveMnemonic(self):
        logger.debug(">>test_getCurveMnemonic()")
        type = LogType
        logType = type.DT
        mnem = logType.getCurveMnemonic()
        self.assertTrue("Sonic DT DTL SON DTPM DTCO"==mnem)
        
    def test_getLogTypes(self):
        ''' prints out all types if uncomment '''
        logger.debug(">>test_getLogTypes()")
        logType = LogType
        types = logType.getLogTypes()
        #logger.debug("--test_getAllLogTypes() "+type(types))
        #for key in types:
        #    logger.debug(str(key))
        
    def test___str__(self):
        logger.debug(">>test___str__()")
        type = LogType
        logType = type.DT
        name = logType.__str__()
        self.assertTrue("Dt (Sonic-P)" == name)

    def test_getLogUnitsForType(self):
        logger.debug(">>getLogUnitsForType()")
        type = LogType
        logType = type.VP
        units = logType.getLogUnitsForType(logType)
        expected = ["m/s", "ft/s","km/s","kft/s"]
        for i in range(len(units)):
            self.assertTrue(expected[i] == str(units[i]))
            


