     
import logging
import unittest
from qrutilities.namingutils import NamingUtils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NamingUtilsTest(unittest.TestCase):
    '''
    classdocs
    '''


    def test_createUniqueMnemonic(self):
        logger.debug(">>test_createUniqueMnemonic")

        unitMap = {'GR':'gamma', 'GR_1':'sonic', 'DTS':'shear'}
        mnem = "GR"
        result = NamingUtils.createUniqueMnemonic(mnem, unitMap)
        self.assertEquals("GR_2",(str(result)))