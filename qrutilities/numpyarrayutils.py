import numpy as np
import math

class NumpyArrayUtils(object):
    '''
    Utilities for numpy arrays
    '''
    @classmethod
    def findNearest(cls, array, paramValue):
        '''Find the nearest value in an array'''
        #see http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
        idx = (np.abs(array-paramValue)).argmin()
        return array[idx]
    
    @classmethod
    def findNearestInSortedArray(cls, array, paramValue):
        ''' If array is sorted and is very large, this is a much faster than findNearest'''
        #see web page as above
        idx = np.searchsorted(array, paramValue, side="left")
        if math.fabs(paramValue - array[idx-1]) < math.fabs(paramValue - array[idx]):
            return array[idx-1]
        else:
            return array[idx]
        
    @classmethod
    def findValueAfterInSortedArray(cls, array, paramValue):
        ''' Returns value after paramValue in sorted array'''
        idx = np.searchsorted(array, paramValue, side="left")
        return array[idx]
    
    @classmethod
    def findValueBeforeInSortedArray(cls, array, paramValue):
        ''' Returns value before paramValue in sorted array'''
        idx = np.searchsorted(array, paramValue, side="left")
        return array[idx-1]