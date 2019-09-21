import logging
import unittest
from qrutilities.numberutils import NumberUtils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NumberUtilsTest(unittest.TestCase):
    '''
    classdocs
    '''
    def test_parseStringToFloat0(self):
        stringToStrip = "-0.01.2"
        value = NumberUtils.parseStringToFloat(stringToStrip)
        self.assertTrue(-0.01==value, 'expected {0} actual {1}'.format(-0.01, value))  

    def test_parseStringToFloat1(self):
        stringToStrip = "w34"
        value = NumberUtils.parseStringToFloat(stringToStrip)
        self.assertTrue(0.0==value, 'expected {0} actual {1}'.format(0.0, value))  

    def test_parseStringToFloat2(self):
        stringToStrip = "9.33meters"
        value = NumberUtils.parseStringToFloat(stringToStrip)
        self.assertTrue(9.33==value, 'expected {0} actual {1}'.format(9.33, value)) 
        
    def test_parseStringToRoundedFloat(self):
        stringToStrip = "9.333333333meters"
        value = NumberUtils.parseStringToRoundedFloat(stringToStrip, 3)
        self.assertTrue(9.333==value, 'expected {0} actual {1}'.format(9.333, value)) 
  
    def test_roundToDecimal(self):
        resultDown = float(NumberUtils.roundToDecimal(8.3333333, 2))
        self.assertTrue(8.33==resultDown, 'expected value {0} actual value {1}'.format(8.33, resultDown))
        resultUp = float(NumberUtils.roundToDecimal(8.399999, 2))
        self.assertTrue(8.40==resultUp, 'expected {0} actual {1}'.format(8.40, resultUp))  
        
    def test_stringToInt1(self):
        stringForTest = "34"
        value = NumberUtils.stringToInt(stringForTest)
        self.assertTrue(34==value, 'expected {0} actual {1}'.format(34, value)) 
        
    def test_stringToInt0(self):
        stringForTest = "100.w"
        value = NumberUtils.stringToInt(stringForTest)
        self.assertTrue(0==value, 'expected {0} actual {1}'.format(0, value)) 
        
    def test_is_a_number(self):
        stringForTest = "1e2"
        value = NumberUtils.isaNumber(stringForTest)
        self.assertTrue(True==value, 'expected {0} actual {1}'.format(True, value)) 
        
    def test_is_a_number2(self):
        stringForTest = "EE"
        value = NumberUtils.isaNumber(stringForTest)
        self.assertTrue(False==value, 'expected {0} actual {1}'.format(False, value)) 

    def test_roundDown(self):
        logger.debug(">>test_roundDown")

        result = NumberUtils.roundDown(1345.23, 100)
        logger.debug("--round_down result:"+str(result))
        self.assertEquals(1300,result)
        
    def test_roundDown1(self):
        logger.debug(">>test_roundDown1")

        result = NumberUtils.roundDown(-1345.23, 100)
        logger.debug("--round_down1 result:"+str(result))
        self.assertEquals(-1400,result)
        
    def test_roundUp(self):
        logger.debug(">>test_round_up")

        result = NumberUtils.roundUp(1345.23, 100)
        logger.debug("--round_up result:"+str(result))
        self.assertEquals(1400,result)
        
    def test_round_up1(self):
        logger.debug(">>test_round_up1")

        result = NumberUtils.roundUp(-1345.23, 100)
        logger.debug("--round_up1 result:"+str(result))
        self.assertEquals(-1300,result)
        

