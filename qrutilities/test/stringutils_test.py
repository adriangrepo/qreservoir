'''
Created on 21 Dec 2014

@author: a
'''
import unittest
import logging

from qrutilities.stringutils import StringUtils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Test(unittest.TestCase):
    stringutils = StringUtils()



    def test_stripTrailingWordsIgnoreCase(self):
        trailingWords = ["f","ft","feet","m","meters"]
        stringToStrip = "400.0meters"
        stripped = self.stringutils.stripTrailingWordsIgnoreCase(stringToStrip, trailingWords)
        self.assertTrue("400.0"==stripped, 'expected {0} actual {1}'.format("400.0", stripped))  
           
    

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()