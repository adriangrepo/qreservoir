import logging
import unittest
from timeit import default_timer as timer
import random
from qrutilities.arrayutils import ArrayUtils
from qrutilities.numpyarrayutils import NumpyArrayUtils
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NumpyArrayUtilsTest(unittest.TestCase):
    '''
    classdocs
    '''

    def dataFunction(self, i):
        return i+.5
    
    def test_findNearestInSortedArray(self):
        lst = [1.002]*5000
        myArray = np.zeros(1000)
        for i in range(1000):
            #for 1D array
            myArray[i] = self.dataFunction(i)
        start = timer()
        value = NumpyArrayUtils.findNearestInSortedArray(myArray, 500)
        end = timer()
        logger.debug("--test_findNearestInSortedArray time:{0}, value:{1}".format(end - start, value))
        
    def test_findNearest(self):
        lst = [1.002]*5000
        myArray = np.zeros(1000)
        for i in range(1000):
            #for 1D array
            myArray[i] = self.dataFunction(i)
        start = timer()
        value = NumpyArrayUtils.findNearest(myArray, 500)
        end = timer()
        logger.debug("--test_findNearest time:{0}, value:{1}".format(end - start, value))
        
    
    def test_findValueAfterInSortedArray(self):
            lst = [1.002]*5000
            myArray = np.zeros(1000)
            for i in range(1000):
                #for 1D array
                myArray[i] = self.dataFunction(i)
            start = timer()
            value = NumpyArrayUtils.findValueAfterInSortedArray(myArray, 500)
            end = timer()
            logger.debug("--test_findValueAfterInSortedArray time:{0}, value:{1}".format(end - start, value))

    def test_findValueBeforeInSortedArray(self):
                lst = [1.002]*5000
                myArray = np.zeros(1000)
                for i in range(1000):
                    #for 1D array
                    myArray[i] = self.dataFunction(i)
                start = timer()
                value = NumpyArrayUtils.findValueBeforeInSortedArray(myArray, 500)
                end = timer()
                logger.debug("--test_findValueBeforeInSortedArray time:{0}, value:{1}".format(end - start, value))
