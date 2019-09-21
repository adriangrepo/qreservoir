import logging
import unittest
from timeit import default_timer as timer
import random
from qrutilities.arrayutils import ArrayUtils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ArrayUtilsTest(unittest.TestCase):
    '''
    classdocs
    '''


    def test_checkListItemsEqualMostlySame(self):


        lst = [1.002]*5000
        
        start = timer()
        ArrayUtils.checkListItemsEqualWhereMostlySame(lst)
        end = timer()
        logger.debug(" checkListItemsEqualWhereMostlySame "+str(end - start))
        
    def test_checkListItemsEqualMostlyDifferent(self):


        lst = [1.002]*5000
        
        start = timer()
        ArrayUtils.checkListItemsEqualWhereMostlyDifferent(lst)
        end = timer()
        logger.debug(" checkListItemsEqualWhereMostlyDifferent "+str(end - start))
        
    def test_checkListItemsEqualMostlySame_random(self):


        lst = [int(1000*random.random()) for i in range(10000)]
        
        start = timer()
        ArrayUtils.checkListItemsEqualWhereMostlySame(lst)
        end = timer()
        logger.debug(" checkListItemsEqualWhereMostlySame random "+str(end - start))
        
    def test_checkListItemsEqualMostlyDifferent_random(self):


        lst = [int(1000*random.random()) for i in range(10000)]
        
        start = timer()
        ArrayUtils.checkListItemsEqualWhereMostlyDifferent(lst)
        end = timer()
        logger.debug(" checkListItemsEqualWhereMostlyDifferent random "+str(end - start))
        
    def test_getFirstItem(self):
        some_list = [0]
        result = ArrayUtils.getFirstItem(some_list)
        self.assertEquals(0, result)
        
        some_list = [2, 3]
        result = ArrayUtils.getFirstItem(some_list)
        self.assertEquals(2, result)
        
        some_list = []
        result = ArrayUtils.getFirstItem(some_list)
        self.assertEquals(None, result)
        
