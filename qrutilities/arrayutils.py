import logging
from itertools import count
from globalvalues.appsettings import AppSettings

logger = logging.getLogger('console')

class ArrayUtils(object):
    '''
    List and dict related utilities
    '''
    

    @classmethod
    def arraycopy(cls, source, sourcepos, dest, destpos, numelem):
        ''' Python version of Java System.arraycopy()  '''
        dest[destpos:destpos+numelem] = source[sourcepos:sourcepos+numelem]
        
    @classmethod
    def checkListItemsEqualWhereMostlySame(cls, lst):
        ''' iterates through a list and checks that all elements are equal
        this is an order of magnitude quicker for mostly similar items than checkListItemsEqualWhereMostlyDifferent '''
        return lst.count(lst[0]) == len(lst)
    
    @classmethod
    def checkListItemsEqualWhereMostlyDifferent(cls, lst):
        ''' iterates through a list and checks that all elements are equal
        this is an order of magnitude quicker for mostly different items than checkListItemsEqualWhereMostlySame '''
        return lst[1:] == lst[:-1]
    
    @classmethod
    def dictDiff(cls, first, second):
        """ Return a dict of keys that differ with another config object.  If a value is
            not found in one fo the configs, it will be represented by KEYNOTFOUND.
            @param first:   Fist dictionary to diff.
            @param second:  Second dicationary to diff.
            @return diff:   Dict of Key => (first.val, second.val)
        """
        KEYNOTFOUND = '<KEYNOTFOUND>'       # KeyNotFound for dictDiff
        diff = {}
        try:
            # Check all keys in first dict
            for key in first.keys():
                if (not key in second):
                    diff[key] = (first[key], KEYNOTFOUND)
                elif (first[key] != second[key]):
                    diff[key] = (first[key], second[key])
            # Check all keys in second dict to find missing
            for key in second.keys():
                if (not key in first):
                    diff[key] = (KEYNOTFOUND, second[key])
        except AttributeError as e:
            logger.debug("--diffDict "+str(e))
            return None
        return diff

    @classmethod
    def getFirstItem(cls, some_list):
        ''' returns first item of a list
        Empty lists in Python evaluate to False in an if check
        '''
        # see http://stackoverflow.com/questions/363944/python-idiom-to-return-first-item-or-none '''
        
        if some_list:
            return some_list[0]
        else:
            return None
        
    @classmethod
    def checkSequentialDictKeys(self, paramDict):
        '''Check keys are sequentially increasing'''
        #In Python 3, dict.values() (along with dict.keys() and dict.items()) returns a view, rather than a list.
        keyValues = list(paramDict.keys())
        for rank in range(0, len(keyValues)-1):
            if keyValues[rank+1] - keyValues[rank] > 2:
                logger.error("--checkSequentialDictKeys() key order not sequential")
                if AppSettings.isDebugMode:
                    raise ValueError
                else:
                    return False
        return True
