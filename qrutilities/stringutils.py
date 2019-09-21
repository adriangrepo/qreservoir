
import logging
import decimal
from builtins import str

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StringUtils(object):
    '''
    Utility functions for parsing input strings 
    '''

    @classmethod
    def stripTrailingWordsIgnoreCase(cls, stringNeedingStrip, trailingWords):
        ''' params string to parse, trailing word list 
        eg trailingWords = ["f","ft","feet","m","meters"] 
        NB this ignores case '''
        lowerInput = str(stringNeedingStrip).lower()
        for item in trailingWords: 
            lowerItem = item.lower()            
            if lowerInput.endswith(lowerItem):
                return stringNeedingStrip[:-len(item)]
        return stringNeedingStrip
        

    @classmethod
    def strToBool(cls, value):
        ''' in most cases just use distutils.util.strtobool(some_string) '''
        valid = {'true': True, 't': True, '1': True,
                 'false': False, 'f': False, '0': False,
                 }   
    
        if isinstance(value, bool):
            return value
    
        if not isinstance(value, str):
            raise ValueError('invalid literal for boolean. Not a string.')
    
        lower_value = value.lower()
        if lower_value in valid:
            return valid[lower_value]
        else:
            raise ValueError('invalid literal for boolean: "%s"' % value)