import decimal, math
import logging
from globalvalues.appsettings import AppSettings
from math import floor, log10, ceil
from re import search

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NumberUtils(object):
    ''' Number input / output related  '''
    
    @classmethod
    def stringToBoolean(cls, valueToConvert):
        if valueToConvert != None:
            if valueToConvert.lower() == "true":
                return True
            elif valueToConvert.lower() == "false":
                return False
        logger.debug("--stringToBoolean() value is not a string representation of a boolean: {0}".format(valueToConvert))
        if AppSettings.isDebugMode:
            raise ValueError
    
    @classmethod
    def stringToInt(cls, valueToConvert):
        ''' converts string to int, returns zero if can't convert '''
        converted = 0
        if valueToConvert != None:
            try:
               converted = int(valueToConvert)
            except ValueError:
                logger.error("Error converting "+str(valueToConvert)+" to int")
        else:
            logger.error("--stringToInt() valueToConvert is None")    
        return converted 
    
    @classmethod
    def straightStringToFloat(cls, x):
        ''' straight conversion to float, returns 0.0 if fails '''
        try:
            f = float(x)
            return f
        except ValueError:
            return 0.0  
        
    @classmethod  
    def parseStringToFloat(cls, field, null=0.0):
        '''strips any non number from end of a string eg -0.01.2 returns -0.01; w34 returns 0.0; 9.33meters returns 9.33
        Default 'null' is 0.0 in cases where not using las'''
        characters = []
        dotCount = 0
        index = 0
        for char in field:
            if char == "-":
                if index == 0:
                    characters.append(str(char))
            elif char == ".":
                if dotCount == 0:
                    characters.append(str(char))
                else:
                    break
                dotCount += 1
            else:
                try:
                    if char.isdigit():
                        characters.append(str(char))

                    #remove else below if want numbers from anywhere in string
                    #eg w34 would return 34, as is returns 0.0
                    else:
                        break
                except ValueError:
                    logger.debug("Character is not part of a number")
                    break
            index += 1
        try:
            parsedFloat = float("".join(characters)) 
            return parsedFloat
        except ValueError:
            logger.error("Error parsing: "+str(field)+" to float")
            return null
        
    @classmethod  
    def parseStringToRoundedFloat(cls, stringToFormat, rounding):
        value = cls.parseStringToFloat(stringToFormat)
        roundedValue = cls.roundToDecimal(value, rounding)
        return roundedValue
    
    @classmethod   
    def roundToDecimal(cls, numberToRound, rounding):
        try:
            decNumber = decimal.Decimal(numberToRound)
            return float(round(decNumber, rounding))
        except ValueError:
            logger.error("Error converting "+str(numberToRound)+" to float")
            return 0.0
        
        
        
    
    @classmethod 
    def floatToInt(cls, floatValue):
        try:
            return int(round(floatValue))
        except ValueError:
            logger.error("Error converting "+str(floatValue)+" to int")
            return 0
        
    @classmethod 
    def floatToIntDefault(cls, floatValue, default):
        try:
            return int(round(floatValue))
        except ValueError:
            logger.error("Error converting "+str(floatValue)+" to int")
            return default
    
    @classmethod
    def isaNumber(cls, x):
        try:
            float(x)
            return True
        except ValueError:
            return False
        
    @classmethod
    def intNumDigits(cls, n):
        '''this will give correct answers for integers only'''
        try:
            return math.floor(math.log10(n))+1
        except ValueError:
            return 0
        
    @classmethod
    def averageExcludingNulls(cls, list, null):
        sum = 0
        counter = 0
        for elm in list:
            if elm != null:
                sum += elm
                counter = counter+1
        #We do this to make sure the counter, an integer is turned into a double
        return(sum/(counter*1.0))
        
    @classmethod
    def minimumExcludingNulls(cls, list, null):
        min = list[0]
        for elm in list[1:]:
            if elm != null:
                if elm < min:              
                    min = elm                  
        return min     
    
    @classmethod
    def maximumExcludingNulls(cls, list, null):     
        max = list[0]          
        for elm in list[1:]:  
            if elm != null:       
                if elm > max:
                    max = elm

        return max
    
    @classmethod
    def roundDown(cls, num, divisor):
        ''' Rounds down to nearest divisor, works on positive and negative integers and floats'''
        return num - (num%divisor)
    
    @classmethod
    def roundUp(cls, num, divisor):
        ''' Rounds up to nearest divisor, works on positive and negative integers and floats'''
        realDivisor = float(divisor)
        return int(math.ceil(num / realDivisor)) * divisor
    
    @classmethod
    def floatApproxEqual(cls, x, y, tol=1e-18, rel=1e-7):
        ''' from http://code.activestate.com/recipes/577124-approximately-equal/ '''
        if tol is rel is None:
            raise TypeError('cannot specify both absolute and relative errors are None')
        tests = []
        if tol is not None: tests.append(tol)
        if rel is not None: tests.append(rel*abs(x))
        assert tests
        return abs(x - y) <= max(tests)
    
    @classmethod
    def almostEqual(cls, a, b, digits):
        try:
            epsilon = 10 ** -digits
            result = abs(a/b - 1) < epsilon
            return result
        except Exception as ex:
            template = "--almostEqual() An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.debug(message)
            return 0.0
        
    @classmethod
    def floatEqualWithEpsilon(cls, a, b, max_relative_error=1e-12, max_absolute_error=1e-12):
        a = float(a)
        b = float(b)
        # if the numbers are close enough (absolutely), then they are equal
        if abs(a-b) < max_absolute_error:
            return True
        # if not, they can still be equal if their relative error is small
        if abs(b) > abs(a):
            relative_error = abs((a-b)/b)
        else:
            relative_error = abs((a-b)/a)
        return relative_error <= max_relative_error 