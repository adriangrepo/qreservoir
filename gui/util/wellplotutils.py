from qrutilities.systemutils import SystemUtils
from globalvalues.constants.wellplotconstants import WellPlotConstants
import logging
from globalvalues.appsettings import AppSettings
from qrutilities.arrayutils import ArrayUtils
import collections

logger = logging.getLogger('console')

class WellPlotUtils(object):
    '''
    Dimension calculations used by tracks and headers
    '''
    
    @classmethod
    def calculateStartStopStep(cls, logTrackDataList, padData=True):
        #see openelectrophy viewers.tools.find_best_start_stop
        DEFAULT_START = 0
        DEFAULT_STOP = 1000
        DEAFULT_STEP = 0.1524
        
        start = DEFAULT_START
        stop = DEFAULT_STOP
        step = DEAFULT_STEP
        firstItem = True
        if len(logTrackDataList)>0:
            for logTrackData in logTrackDataList:
                #WellPlotUtils.getStartStopStepFromLogs(logTrackData.getLogs())
                for log in logTrackData.getLogs():
                    if firstItem:
                        start = log.z_measure_min
                        stop = log.z_measure_max
                        step = log.z_measure_step
                        firstItem = False
                    logger.debug("start:{0}, stop:{1}, step:{2}".format(start, stop, step))
                    if (log.z_measure_step != None) and (log.z_measure_min != None) and (log.z_measure_max != None):
                        start, max = WellPlotUtils.getMinMax(log.z_measure_min, start)
                        min, stop = WellPlotUtils.getMinMax(log.z_measure_max, stop)
                        step, max = WellPlotUtils.getMinMax(log.z_measure_step, step)
                    else:
                        return DEFAULT_START, DEFAULT_STOP, DEAFULT_STEP
            padding = (stop-start)/200.
            logger.debug("--calculateStartStopStep() start:{0}, stop:{1}, step:{2}, padding:{3}".format(start, stop, step, padding))
        else:
           logger.debug("--calculateStartStopStep() logTrackDataList is empty")
           if AppSettings.isDebugMode:
               raise ValueError 
        if padData:
            start-=padding
            stop+=padding
        return start, stop, step
    
    @classmethod
    def getStartStopStepFromLogs(cls, logList):
        start = True
        for log in logList:
            if start:
                step = log.z_measure_step
                start = log.z_measure_min
                stop = log.z_measure_max
                start = False
            logger.debug("step:{0}, start:{1}, stop:{2}".format(step, start, stop))
            if (step != None) and (start != None) and (stop != None):
                step, max = WellPlotUtils.getMinMax(log.z_measure_step, step)
                start, max = WellPlotUtils.getMinMax(log.z_measure_min, start)
                min, stop = WellPlotUtils.getMinMax(log.z_measure_max, stop)
            else:
                return 0, 0, 0
            
    @classmethod
    def getMinMax(cls, x, y):
        min, max = (x, y) if x < y else (y, x)
        return min, max

    def calcTrackMinHeight(self, log, lenDepth):
        depthCoverage = abs(log.z_measure_data[lenDepth-1] - log.z_measure_data[0])
        if depthCoverage> WellPlotConstants.WELL_PLOT_DEFAULT_ZOOM:
            rect = SystemUtils.getScreenGeometry()
            screenHeight = rect.height()
            hRatio = depthCoverage/WellPlotConstants.WELL_PLOT_DEFAULT_ZOOM
            widgetHeight = hRatio*(screenHeight/2)
        else:
            widgetHeight = screenHeight/2
        return int(widgetHeight)
    
    def calcTrackMinWidth(self, trackData):
        screendpmmX, screendpmmY = SystemUtils.getScreenDPMM()
        return int(trackData.track_width*screendpmmX)
    
    @classmethod
    def convertmmToDPI(cls, mmSize):
        if (isinstance(mmSize, int)) or (isinstance(mmSize, float)):
            xDpmm, yDpmm = SystemUtils.getScreenDPMM()
            result = float(mmSize)*float(xDpmm)
            return int(result)
        else:
            logger.error("--convertmmToDPI() input data wrong type "+str(type(mmSize)))
            if AppSettings.isDebugMode:
                raise ValueError
            return 0
        
    @classmethod
    def createPlotDict(cls, wellPlotData):
        '''Create plot dict where keys are the plot indexes, values are ZAxis or Track items'''
        assert wellPlotData is not None
        
        zAxes = wellPlotData.getZAxisDatas()
        tracks = wellPlotData.getLogTrackDatas()
        plotDict = {}
        #put all plot data in a dict so can easily lay out
        for zAxis in zAxes:
            assert zAxis.plot_index is not None
            plotDict[zAxis.plot_index] = zAxis
        for track in tracks:
            assert track.plot_index is not None
            if track.plot_index in plotDict:
                logger.error("--createPlotDict() duplicate key assignment")
                if AppSettings.isDebugMode:
                    raise ValueError
            else:
                plotDict[track.plot_index] = track
        
        if plotDict is not None:
            sortedDict = sorted(plotDict.items())
            orderedDict = collections.OrderedDict(sortedDict)
            #check that no gaps exist in track layout
            if ArrayUtils.checkSequentialDictKeys(orderedDict):
                return orderedDict
        else:
            logger.debug("--createPlotDict() no axes or tracks")
        return None
        