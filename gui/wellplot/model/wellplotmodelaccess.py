from db.core.log.log import Log

import copy

import logging

from db.core.well.well import Well
from statics.templates.wellplottype import WellPlotType
from db.windows.wellplot.template.wellplottemplate import WellPlotTemplate
from db.windows.wellplot.logtrackdata.logtrackdatadao import LogTrackDataDao
from db.windows.wellplot.wellplotdata.wellplotdatadao import WellPlotDataDao
from globalvalues.constants.wellplotconstants import WellPlotConstants
from globalvalues.appsettings import AppSettings
from gui.util.wellplotutils import WellPlotUtils
from db.windows.wellplot.zaxistrackdata.zaxisdata import ZAxisData
from db.windows.wellplot.zaxistrackdata.zaxisdatautility import ZAxisDataUtility
from db.windows.wellplot.logtrackdata.logtrackutility import LogTrackUtility

logger = logging.getLogger('console')

class WellPlotModelAccess(object):
    '''
    classdocs
    '''

    def createWellPlotData(self, logList, uid, well, template, logSet=None):
        '''populates the input wellPlotData with data '''
        assert isinstance(well, Well), "well is wrong type:{0}".format(type(well))
        assert isinstance(template, WellPlotTemplate), "template is wrong type:{0}".format(type(template))
        
        #copy all prefs over, issue with deepcopy so manually copying - TODO improve this
        prefsPlotData = WellPlotDataDao.getWellPlotPreferences(template.uid) 
        wellPlotData = copy.deepcopy(prefsPlotData)
        #manually call init as it is not called automatically here
        wellPlotData.__init__()

        wellPlotData.is_preferences = False
        wellPlotData.uid = uid
        #Preliminary width, is overwritten in Canvas
        wellPlotData.widget_width = len(logList)*2
        wellPlotData.well = well
        wellPlotData.well_id = well.id
        if logSet is not None:
            wellPlotData.log_set_id = logSet.id

        #for quick plots use z track prefs, for other templates use given Z
        if template.is_modifiable is False:
            self.handleQuickPlotType(well, wellPlotData, logList, template, logSet)
        else:
            self.handleTemplateType(well, wellPlotData, logList, template, logSet)
        return wellPlotData

                
    def handleQuickPlotType(self, well, wellPlotData, logList, template, logSet):
        assert well is not None
        assert wellPlotData is not None
        assert logList is not None
        assert template is not None
        
        '''Modifies wellPlotData parameter, uses ZMeasureTrackPreferences for zAxis priority'''
        if template.uid == WellPlotType.ALLLOGS.uid or template.uid == WellPlotType.ACTIVELOGS.uid:
            self.handleActiveOrAllTemplate(well, wellPlotData, logList, template, logSet)
        elif template.uid == WellPlotType.QUICKPLOT.uid:
            self.handleQuickPlotTemplate(well, wellPlotData, logList, template, logSet)
        elif template.uid == WellPlotType.EMPTY.uid:
            return 
        
    def handleQuickPlotTemplate(self, well, wellPlotData, logList, template, logSet): 
        assert well is not None
        assert wellPlotData is not None
        assert logList is not None
        assert template is not None
        
        filteredLogs, zMeasureReferenceStr, zMeasureTypeStr = self.filterLogsOnZAxisPriority(well, wellPlotData, logList, template, logSet)
        zAxisData = None
        if len(filteredLogs)>0:
            zAxisData = self.generateQuickPlotPrimaryZAxis(wellPlotData, filteredLogs, zMeasureReferenceStr, zMeasureTypeStr) 
            wellPlotData._z_axis_track_datas.append(zAxisData) 
            trackDatas = self.generateQuickPlotLogTracks(wellPlotData, filteredLogs)
            wellPlotData._log_track_datas = trackDatas
        else:
            self.generateLoggerMessageNoLogsOfZAxisType(well, logSet, wellPlotData)
            
    def handleActiveOrAllTemplate(self, well, wellPlotData, logList, template, logSet):
        assert well is not None
        assert wellPlotData is not None
        assert logList is not None
        assert template is not None
        
        logDataLogic = Log()

        
        zAxis = ZAxisDataUtility.createNewZAxis()
        #assign a uid that can be used on object before is persisted
        zAxis.uid = id(zAxis)
        domainTrackPriority = wellPlotData.getZAxisPriority()
        #use for iterating through ZMeasureType list and get list of logs with matching zAxisType 
        logsFilteredOnZAxis = []
        #just want to find first domainTrackPriority
        matched = False
        zAxisReferenceStr = ""
        zAxisTypeStr = ""
        for zAxisReference in domainTrackPriority:
            zAxisType, zReference = zAxisReference.split()
            for log in logList:
                if (log.z_measure_type_name == zAxisType) and (log.z_measure_reference == zReference):
                    matched = True
                    logsFilteredOnZAxis.append(log)
            if matched:
                zAxisReferenceStr = zReference
                zAxisTypeStr = zAxisType
                break
           
        if len(logsFilteredOnZAxis)>0:  

            #use primary ZMeasureType for min/max      
            yMin, yMax = logDataLogic.getDepthRange(logsFilteredOnZAxis)
            zAxis.allLogDepthMin = yMin
            zAxis.allLogDepthMax = yMax 
            plotYmin, plotYmax = logDataLogic.getDepthPlotRange(yMin, yMax)
            zAxis.plotMin = plotYmin
            zAxis.plotMax = plotYmax
            zAxis.z_axis_type = zAxisTypeStr
            zAxis.is_primary = True
            zAxis.z_axis_reference_level = zAxisReferenceStr
            #ensure we don't use same plot indexes if already allocated
            plotDict = WellPlotUtils.createPlotDict(wellPlotData)
            if plotDict is not None:
                zAxis.plot_index = len(plotDict)
            else:
                zAxis.plot_index = 0
                
            wellPlotData._z_axis_track_datas.append(zAxis)
            
            wellPlotData._log_track_datas = self.generateActiveAllEmptyLogTracks(wellPlotData, logsFilteredOnZAxis, paramTemplate=template)

        else:
            self.generateLoggerMessageNoLogsOfZAxisType(well, logSet, domainTrackPriority)
            
        if len(wellPlotData.getLogTrackDatas()) == 0:
            self.noLogTrackDataMessages(template, logSet, well)
            
    def handleTemplateType(self, well, wellPlotData, logList, template, logSet):
        '''Modifies wellPlotData parameter, uses template for zAxis settings'''
        assert well is not None
        assert wellPlotData is not None
        assert logList is not None
        assert template is not None
        

        primaryZAxis = ZAxisDataUtility.createNewZAxis()
        
        #assign a uid that can be used on object before is persisted
        primaryZAxis.uid = id(primaryZAxis)
        
        #populate the ZAxis object using template
        primaryZAxis.is_primary = True
        primaryZAxis.plot_index = template._primary_z_track_index
        primaryZAxis.title = template._primary_z_track_name
        primaryZAxis.z_axis_type = template._primary_z_type
        primaryZAxis.z_axis_display_units = template._primary_z_display_unit
        primaryZAxis.z_axis_reference_level = template._primary_z_reference
        
        
        secondaryZAxes = template.getZAxes()
        
        tracks = template._tracks

    def generateQuickPlotPrimaryZAxis(self, wellPlotData, logsFilteredOnZMeasure, zMeasureReferenceStr, zMeasureTypeStr):
        '''Generates ZAxisData'''
        assert wellPlotData is not None
        assert logsFilteredOnZMeasure is not None
        assert zMeasureReferenceStr is not None
        assert zMeasureTypeStr is not None
        
        logDataLogic = Log()
        zAxisData = ZAxisDataUtility.createNewZAxis()
        #assign a uid that can be used on object before is persisted
        zAxisData.uid = id(zAxisData)
        
        #use primary ZMeasureType for min/max      
        yMin, yMax = logDataLogic.getDepthRange(logsFilteredOnZMeasure)
        zAxisData.allLogDepthMin = yMin
        zAxisData.allLogDepthMax = yMax 
        plotYmin, plotYmax = logDataLogic.getDepthPlotRange(yMin, yMax)
        zAxisData.plotMin = plotYmin
        zAxisData.plotMax = plotYmax
        zAxisData.z_axis_type = zMeasureTypeStr
        #zAxisData.z_axis_display_units = zDisplayUnitStr
        zAxisData.z_axis_reference_level = zMeasureReferenceStr
        zAxisData.is_primary = True
        
        #ensure we don't use same plot indexes if already allocated
        plotDict = WellPlotUtils.createPlotDict(wellPlotData)
        if plotDict is not None:
            #as are creating quickplot from nothing should be no zaxis already, if exists ensure only 1 primary axis
            for item in plotDict.values():
                if isinstance(item, ZAxisData):
                    logger.error("Existing ZAxis found during quickplot set-up")
                    item.is_primary = False
            zAxisData.plot_index = len(plotDict)
        else:
            zAxisData.plot_index = 0
        return zAxisData
    
    def filterLogsOnZAxisPriority(self, well, wellPlotData, logList, template, logSet):
        assert well is not None
        assert wellPlotData is not None
        assert logList is not None
        assert template is not None
        
        domainTrackPriority = wellPlotData.getZAxisPriority()
        #use for iterating through ZMeasureType list and get list of logs with matching zMeasureType 
        logsFilteredOnZMeasure = []
        #just want to find first domainTrackPriority
        matched = False
        zMeasureReferenceStr = ""
        zMeasureTypeStr = ""
        zDisplayUnitStr = ""
        for zMeasureReference in domainTrackPriority:
            zMeasureType, zReference = zMeasureReference.split()
            for log in logList:
                if (log.z_measure_type_name == zMeasureType) and (log.z_measure_reference == zReference):
                    matched = True
                    logsFilteredOnZMeasure.append(log)
            if matched:
                zMeasureReferenceStr = zReference
                zMeasureTypeStr = zMeasureType
                break
        return logsFilteredOnZMeasure, zMeasureReferenceStr, zMeasureTypeStr
       
    def generateTemplateLogTracks(self, logList):
        #create plots with a single track per plot
        i = 1
        logTracks = []

        logTrackData = LogTrackDataDao.getLogTrackPreferences() 

        for log in logList:
            if log.log_type_name == logTypeInTrack:
                plotLogs.append(log)
        #decode template
        #find matching logs
        #populate log tracks objects



    def generateActiveAllEmptyLogTracks(self, wellPlotData, logList, paramTemplate):
        logger.debug("--getPlotLogs() paramTemplate: {0}".format(paramTemplate))
        assert isinstance(paramTemplate, WellPlotTemplate)
        assert wellPlotData is not None
        assert logList is not None
        
        quickPlotLogs = []
        logTracks = None
        if paramTemplate is not None:
            if paramTemplate.uid == WellPlotType.ACTIVELOGS.uid:
                i=0
                for log in logList:
                    if log.active:
                        if i < WellPlotConstants.WELL_PLOT_MAX_TRACK_NUMBER:
                            quickPlotLogs.append(log)
                        i+=1
                if len(logList) > WellPlotConstants.WELL_PLOT_MAX_TRACK_NUMBER:
                    logger.info("Limited number of tracks to: {0}".format(WellPlotConstants.WELL_PLOT_MAX_TRACK_NUMBER))
            elif paramTemplate.uid == WellPlotType.ALLLOGS.uid:
                logger.debug("--getPlotLogs() all")
                if len(logList) > WellPlotConstants.WELL_PLOT_MAX_TRACK_NUMBER:
                    logger.info("Limited number of tracks to: {0}".format(WellPlotConstants.WELL_PLOT_MAX_TRACK_NUMBER))
                quickPlotLogs = list(logList[0 : WellPlotConstants.WELL_PLOT_MAX_TRACK_NUMBER])
            elif paramTemplate.uid == WellPlotType.EMPTY.uid:
                logger.debug("--getPlotLogs() empty")

            logTracks = self.generateQuickPlotLogTracks(wellPlotData, quickPlotLogs)             
        return logTracks
    
    
    def generateQuickPlotLogTracks(self, wellPlotData, quickPlotLogs):
        assert wellPlotData is not None
        assert quickPlotLogs is not None
        
        #create plots with a single track per plot
        
        logTracks = []

        #ensure we don't use same plot indexes if already allocated
        plotDict = WellPlotUtils.createPlotDict(wellPlotData)
        #zero based indexing for everything
        i = 0

        for log in quickPlotLogs:
            trackData = LogTrackUtility.createNewTrack()
            
            #store a hash that can be used prior to persistence
            trackData.uid = id(trackData)
            trackData.is_displayed = True
            #logTrackData = SubPlotData()
            if plotDict is not None:
                trackData.plot_index = len(plotDict)+i
            else:
                trackData.plot_index = i
            trackData.addLog(log)
            logTracks.append(trackData)
            i += 1
        return logTracks
    
    def generateLoggerMessageNoLogsOfZAxisType(self, well, logSet, wellPlotData):
        assert well is not None
        assert logSet is not None
        assert wellPlotData is not None
        
        
        domainTrackPriority = wellPlotData.getZAxisPriority()
        zMeasures = []
        for zAxisReference in domainTrackPriority:
            zMeasures.append(zAxisReference)
        concatenatedZMeasures = ",".join(zMeasures)
        if logSet is None:
            logger.info("No logs in well: {0} with Z measurement type(s): {1}".format(well.name, concatenatedZMeasures))
        else:
            logger.info("No logs in well: {0} log set: {1} with Z measurement type(s): {2}".format(well.name, logSet.name, concatenatedZMeasures))
            
    def noLogTrackDataMessages(self, template, logSet, well):
        assert well is not None
        
        activeLogs = WellPlotType.ACTIVELOGS
        allLogs = WellPlotType.ALLLOGS
        
        message = ""
        if template is None:
            logger.error("template is None")
            if AppSettings.isDebugMode:
                raise ValueError
        else:
            if template.uid == activeLogs.uid:
                if logSet is None:
                    message = "No active logs to plot in well: {0}".format(well.name)
                else:
                    message = "No active logs to plot in well: {0} log set: {1}".format(well.name, logSet.name)
            if template.uid == allLogs.uid:
                if logSet is None:
                    message = "No logs to plot in well: {0}".format(well.name)
                else:
                    message = "No logs to plot in well: {0} log set: {1}".format(well.name, logSet.name)
            else:
                if logSet is None:
                     message = "No logs to plot of types in template: {0} in well: {1}".format(template.name, well.name)
                else:
                    message = "No logs to plot of types in template: {0} in well: {1} log set: {1}".format(template.name, well.name, logSet.name)
            logger.info(message)