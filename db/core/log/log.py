
from qrutilities.numberutils import NumberUtils


import logging
from db.core.log.logbase import LogBase
logger = logging.getLogger('console')

class Log(LogBase):
    '''
    Logic layer wrapper for LogBase
    '''
    
    def getDepthRange(self, logList):
        '''finds max and min depth values for all log data supplied
        returns all logs depth min, max'''
        yMax = 0
        yMin = 0
        if len(logList) == 0:
            logger.debug("Log list length is zero cannot set log depth range")
            return yMin, yMax 
        
        elif len(logList[0].z_measure_data) == 0:
            logger.debug("Log depth data length is zero cannot set log depth range")
            return yMin, yMax 
        
        yMax = logList[0].z_measure_data[0]
        yMin = logList[0].z_measure_data[0]
        for item in logList:
            dMax = max(item.z_measure_data)
            if dMax>yMax:
                yMax = dMax
                
            dMin = max(item.z_measure_data)
            if dMin<yMin:
                yMin = dMin
            
        return yMin, yMax 
    
    def findLogWithLargestDepthRange(self, logList):
        '''returns longest (log with largest depth min, max difference)
        relies on z_measure_max and z_measure_min being set each time log is persisted'''
        if len(logList) == 0:
            logger.debug("Log list length is zero cannot find longest log")
            return None 

        difference = 0
        longestLog = None
        for item in logList:
            pMax = item.z_measure_max
            pMin = item.z_measure_min
            
            yDiff = pMax - pMin
            if yDiff>difference:
                difference = yDiff
                longestLog = item
                
        return longestLog

        
    def getDepthPlotRange(self, allDepthMin, allDepthMax):
        ''' rounds log depth range up or down to nearest round n^10 eg 140 to 200
        returns mix, max depth axis plot values'''
        intMaxValue = NumberUtils.floatToInt(allDepthMax)
        intMinValue = NumberUtils.floatToInt(allDepthMin)
        diff = intMaxValue-intMinValue
        numberDigits = NumberUtils.intNumDigits(diff)
        roundValue = pow(10, numberDigits-1)

        depthAxis1PlotMax = NumberUtils.roundUp(allDepthMax, roundValue)
        depthAxis1PlotMin = NumberUtils.roundDown(allDepthMin, roundValue)

        return depthAxis1PlotMin, depthAxis1PlotMax
    

    
