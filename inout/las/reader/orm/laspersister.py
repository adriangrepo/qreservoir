from sqlalchemy import exc

from db.core.depthdata.depthdata import DepthData

from preferences.inout.importexport import ImportExportPreferences
from qrutilities.numberutils import NumberUtils
from statics.types.logtype import LogType
from globalvalues.constants.inputdataconstants import InputDataConstants
import numpy as np
import statistics
import logging
from globalvalues.appsettings import AppSettings
from statics.types.zaxis import ZAxis

from db.core.basedao import BaseDao
from db.windows.logcurvepreferences.logcurvepreferencedao import LogCurvePreferencesDao
from db.core.history.history import History
from qrutilities.systemutils import SystemUtils
from db.core.history.historyset import HistorySet


logger = logging.getLogger('console')

class LasPersister(object):
    '''
    Persists data from wizard pages
    '''

    def __init__(self, session):
        self._historySetId = 0
        self._wellId = 0
        self._logSetId = 0
        self._logServiceId = 0
        self._stepIndexes=[]
        self._uniqueSteps=[]
        self._consistentStep = True
        self._meanStepValue = 1
        self._session = session
        #default 
        self._allDataFlag = ImportExportPreferences.IMPORT_ALL_LAS_DATA
        self._committedOK = False

    #keep as an outside class call for unit testing
    def dispatchDataWriters(self, lasReader, allDataFlag):
        ''' feeds writing to 4 stages, flag is False is writing essential data only '''
        self._allDataFlag = allDataFlag
        self._lasReader = lasReader
        self._las_rounding = self.getRounding(self._lasReader._step)
        #we dont even use the las dstart stop here - just use raw depth values - ultimate truth
        self.computeStepNp(self._lasReader._depthData, self._lasReader._step, self._las_rounding)
        
        self.writeHistory()
        self.writeWellData()
        self.writeLogSet()
        self.writeLogServiceData()
        self.writeLogDomainData()
        self.writeDepthData()
        if allDataFlag:
            self.writeParameterSetData()
            self.writeParameterListData()
        self.writeLogData()
        
        try:
            self._session.commit()
            self.committedOK = True
            logger.debug("--dispatchDataWriters() committed")
        except exc.SQLAlchemyError as e:
            logger.error("Cannot write data to database: "+str(e))
        
    def writeHistory(self):
        historySet = HistorySet()
        self._session.add(historySet)
        self._session.flush()
        self._historySetId = historySet.id

        history = History()
        history.history_set_id = self._historySetId
        history.user = SystemUtils.getCurrentUser()
        history.action = "Import"
        history.details = "Source: "+str(self._lasReader.fullFilePathName)
        history.build_date = AppSettings.buildDate
        history.version = AppSettings.softwareVersion
        self._session.add(history)
        self._session.flush()
        
        
    def writeWellData(self):
        well = self._lasReader.well
        well.source = self._lasReader.fullFilePathName
        self.updateWellStartStop(well)
        well.history_set_id = self._historySetId
        self._session.add(well)
        self._session.flush()
        self._wellId = well.id
        logger.debug("--writeWellData() well.id: "+str(self._wellId))

    
    def writeLogSet(self):
        logSet = self._lasReader.logSet
        logSet.well_id = self._wellId
        logSet.history_set_id = self._historySetId
        self._session.add(logSet)
        self._session.flush()
        self._logSetId = logSet.id
        logger.debug("--writelogSet() logSet.id: "+str(self._logSetId))
            
    def writeLogServiceData(self):
        ''' writes logService and depth data '''
        logService = self._lasReader.logService
        logService.well_id = self._wellId
        logService.history_set_id = self._historySetId
        self._session.add(logService)
        self._session.flush()
        self._logServiceId = logService.id
        logger.debug("--writelogServiceData() logService.id: "+str(self._logServiceId))
        
    #  for now domain is deprecated
    def writeLogDomainData(self):
        # writes logService and depth data 
        logDomain = self._lasReader.logDomain
        logDomain.well_id = self._wellId
        logDomain.z_measure_type_name = self._lasReader.well.z_measure_type_name
        
        self._session.add(logDomain)
        self._session.flush()
        self._logDomainId = logDomain.id
        logger.debug("--writeLogDomainData() logDomain.id: "+str(self._logDomainId))
        
    def updateWellStartStop(self, well):
        logger.debug(">>updateWellStartStop()")
        logDomain = self._lasReader.logDomain
        logDomain.well_id = self._wellId
        logDomain.z_measure_type_name = self._lasReader.well.z_measure_type_name
        
        if logDomain.z_measure_type_name == ZAxis.MD.getUid():
            md_start = well.mdstart
            md_stop = well.mdstop
            if (md_start is None):
                if (logDomain.log_start is not None):
                    well.mdstart = logDomain.log_start
            elif (logDomain.log_start is not None):
                if (md_start > logDomain.log_start):
                    well.mdstart = logDomain.log_start
                    
            if (md_stop is None):
                if (logDomain.log_stop is not None):
                    well.mdstop = logDomain.log_stop
            elif (logDomain.log_stop is not None):
                if (md_stop < logDomain.log_stop):
                    well.mdstop = logDomain.log_stop
                    
        elif logDomain.z_measure_type_name == ZAxis.TVD.getUid():
            tvd_start = well.tvdstart
            tvd_stop = well.tvdstop
            if (tvd_start is None):
                if (logDomain.log_start is not None):
                    well.tvdstart = logDomain.log_start
            elif (logDomain.log_start is not None):
                if (tvd_start > logDomain.log_start):
                    well.tvdstart = logDomain.log_start
                    
            if (tvd_stop is None):
                if (logDomain.log_stop is not None):
                    well.tvdstop = logDomain.log_stop
            elif (logDomain.log_stop is not None):
                if (tvd_stop < logDomain.log_stop):
                    well.tvdstop = logDomain.log_stop
                    
        elif logDomain.z_measure_type_name == ZAxis.TWT.getUid():
            twt_start = well.twtstart
            twt_stop = well.twtstop
            if (twt_start is None):
                if (logDomain.log_start is not None):
                    well.twtstart = logDomain.log_start
            elif (logDomain.log_start is not None):
                if (twt_start > logDomain.log_start):
                    well.twtstart = logDomain.log_start
                    
            if (twt_stop is None):
                if (logDomain.log_stop is not None):
                    well.twtstop = logDomain.log_stop
            elif (logDomain.log_stop is not None):
                if (twt_stop < logDomain.log_stop):
                    well.twtstop = logDomain.log_stop
        
    def writeDepthData(self):
        logger.debug(">>writeDepthData() ")
        if ImportExportPreferences.HONOUR_LAS_DEPTH_VALUES:
            depthList = self._lasReader._depthData
        else:
            depthList = self.calcSteppedDepth(self._lasReader.logDomain, self._las_rounding, self._lasReader._logs[0,:])
        jsonStr = BaseDao.convertDataToJSON(depthList)
        depth = DepthData()
        depth.data = jsonStr
        depth.log_domain_id = self._logDomainId
        self._session.add(depth)
        self._session.flush()
        logger.debug("--writeDepthData() ")
    
            
    def calcSteppedDepth(self, logDomain, rounding, data_start, data_stop):
        logger.debug(">>calcSteppedDepth() ")

        start = logDomain.log_start
        stop = logDomain.log_stop
        step = logDomain.log_step
        if not ImportExportPreferences.PAD_DATA_TO_LAS_LIMITS:
            if np.around(start, decimals=rounding) != np.around(data_start, decimals=rounding):
                start = data_start
                logger.info(".las file header z domain start value: "+str(start)+" != data z domain start value: "+str(data_start))
            if np.around(stop, decimals=rounding) != np.around(data_stop, decimals=rounding):
                stop = data_stop
                logger.info(".las file header z domain stop value: "+str(stop)+" != data z domain stop value: "+str(data_stop))
        else:
            #check data depth values and pad out
            if (start - data_start)> step/2:
                start_diff = data_start-start
                num_to_pad = round(np.float64(start_diff/step).item())+1
                #add these to each log data as null
                logger.debug("TODO pad out start n steps: "+str(num_to_pad))
            if (stop - data_stop)> step/2:
                stop_diff = stop-data_stop
                num_to_pad = round(np.float64(stop_diff/step).item())+1
                logger.debug("TODO pad out stop n steps: "+str(num_to_pad))
                #add these to each log data as null

        abs_step = 0
        abs_start = 0
        abs_stop = 0
        if step < 0:
            abs_step = step*-1
        else:
            abs_step = step;
        if start < 0 and stop < 0:
           abs_start = start*-1
           abs_stop = stop *-1
        elif start < 0 and stop >0 or start >0 and stop>0:
            #starting above sea level
            abs_start = start
            abs_stop = stop
        else:
            #+ve start, -ve stop
            abs_start = start*-1
            abs_stop = stop*-1
        abs_start = np.around(abs_start, decimals=rounding)
        abs_stop = np.around(abs_stop, decimals=rounding)
        roundedDepthDiff = np.around(abs_stop-abs_start, decimals=rounding)
        num_samples = round(np.float64(roundedDepthDiff/abs_step).item())+1
        depth_data = [None]*num_samples
        logger.debug(" start: "+str(abs_start)+" stop: "+str(abs_stop)+" step: "+str(abs_step))
        counting_depth = abs_start
        #start at one
        for i in range(0, num_samples):
            depth_data[i]=counting_depth
            counting_depth = counting_depth + abs_step
        depth_data[0]=abs_start
        if depth_data[len(depth_data)-1] != abs_stop:
            logger.debug("depth_data[len(depth_data)-1]: "+str(depth_data[len(depth_data)-1])+" != abs_stop: "+str(abs_stop))
            
        return depth_data
                 
    def writeParameterSetData(self):
        parameterSet = self._lasReader.parameterSet
        assert parameterSet.name is not None
        parameterSet.well_id = self._wellId
        parameterSet.history_set_id = self._historySetId
        self._session.add(parameterSet)
        self._session.flush()
        self._parameterSetId = parameterSet.id
        logger.debug("--writeParameterSetData() parameterSet.id: "+str(self._parameterSetId))
        
    def writeParameterListData(self):
        logger.debug(">>writeParameterListData()")
        parameterList = self._lasReader.parameterList
        logger.debug("--writeParameterListData() "+str(len(parameterList)))
        for parameter in parameterList:
            parameter.parameter_set_id = self._parameterSetId
            self._session.add(parameter)
        self._session.flush()
        logger.debug("<<writeParameterListData() ")
        
    def writeLogData(self):
        logger.debug(">>writeLogData()")
        logList = self._lasReader.logList
        assert len(self._lasReader.logList) == len(self._lasReader._logs)
        depthType = self._lasReader.well.z_measure_type_name
        for i, log in enumerate(logList):
            logger.debug("--writeLogData() log: "+str(log.name)+" import: "+str(log.importLog))
            if log.importLog:
                log.log_set_id = self._logSetId
                log.log_service_id = self._logServiceId
                log.log_domain_id = self._logDomainId
                log.well_id = self._wellId
                
                if ImportExportPreferences.HONOUR_LAS_DEPTH_VALUES:
                    depthList = self._lasReader._depthData
                    honour_las_depth_values = True
                else:
                    depthList = self.calcSteppedDepth(self._lasReader.logDomain, self._las_rounding, self._lasReader._logs[0,:])
                    honour_las_depth_values = False
                jsonStr = BaseDao.convertDataToJSON(depthList)
                log.z_measure_data_str = jsonStr
                logDomain = self._lasReader.logDomain
                log.z_measure_min = logDomain.log_start
                log.z_measure_max = logDomain.log_stop
                log.consistent_step = self._consistentStep
                #store the mean step anyway
                log.z_measure_step = self._meanStepValue

                log.null = self._lasReader.null_value

                logTypeUid = LogType.getUidFromName(log.log_type_name)
                logCurveDefaults = LogCurvePreferencesDao.getLogCurvePreferences(logTypeUid, self._session)
                if logCurveDefaults == None:
                    #no preferences set yet, use defaults
                    logCurveDefaults = LogCurvePreferencesDao.getLogCurveDefaults(logTypeUid, self._session)
                
                log.log_plot_left = logCurveDefaults.log_plot_left
                log.log_plot_right = logCurveDefaults.log_plot_right
                log.log_plot_default = logCurveDefaults.log_plot_default
                log.log_plot_points_on = logCurveDefaults.log_plot_points_on
                
                log.histogram_left = logCurveDefaults.histogram_left
                log.histogram_right = logCurveDefaults.histogram_right
                log.histogram_default = logCurveDefaults.histogram_default
                
                log.cross_plot_left = logCurveDefaults.cross_plot_left
                log.cross_plot_right = logCurveDefaults.cross_plot_right
                log.cross_plot_default = logCurveDefaults.cross_plot_default

                log.line_width = logCurveDefaults.line_width
                log.line_style = logCurveDefaults.line_style
                
                log.point_size = logCurveDefaults.point_size
                log.point_style = logCurveDefaults.point_style
                
                log.rgb = logCurveDefaults.rgb
                log.alpha = logCurveDefaults.alpha
                
                log.is_logarithmic = logCurveDefaults.is_logarithmic
                if log.is_logarithmic:
                    log.log_plot_log_cycles = logCurveDefaults.log_plot_log_cycles

                log.z_measure_type_name = depthType
                #duplication - but makes simpler if want to change log down track
                log.z_measure_reference = self._lasReader.logService.z_measure_reference
                try:
                    #see http://stackoverflow.com/questions/4455076/numpy-access-an-array-by-column
                    data = self._lasReader._logs[i,:]
                    log.honour_las_depth_values = honour_las_depth_values
                    log.value_min = NumberUtils.minimumExcludingNulls(data, log.null)
                    log.value_max = NumberUtils.maximumExcludingNulls(data, log.null)
                    jsonStr = BaseDao.convertDataToJSON(data.tolist())
                    log.log_data_str = jsonStr
                    #statistics
                    log.mean = statistics.mean(data)
                    log.median = statistics.median(data)
                    #standard deviation
                    log.stdev = statistics.pstdev(data)
                    
                except IndexError as ie:
                    logger.error("Error saving log data "+str(ie))
                    return
                if self._allDataFlag:
                    log.parameter_set_id = self._parameterSetId
                    
                log.source = self._lasReader.fullFilePathName
                logger.debug("--writeLogData() pre flush log.id: "+str(log.id)+" log_set_id "+str(log.log_set_id)+" log_service_id "+str(log.log_service_id)+" log_domain_id "+str(log.log_domain_id)+ " log.parameter_set_id "+str(log.parameter_set_id))
                logger.debug("--writeLogData() name: "+str(log.name)+" type: "+str(log.log_type_name)) #+" datas: "+str(log.log_datas))
                
                log.history_set_id = self._historySetId
                
                self._session.add(log)
                self._session.flush()
                logger.debug("--writeLogData() post flush log.id: "+str(log.id))
                

    
    def getRounding(self, readerStep):
        readerStepStr = str(readerStep)
        trailingString = readerStepStr.split(".",1)[1]

        precision = len(trailingString)
        logger.debug("precision "+str(precision)+" trail; "+trailingString)
        #surely 10 is sufficient - magic number though needs to be in constants
        if precision<=InputDataConstants.LAS_READER_Z_DOMAIN_MAXIMUM_EPSILON:
            rounding = precision
        else:
            rounding = InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES
        return rounding
    
             
    def computeStepNp(self, depthData, readerStep, rounding):
        """ check if las data has a consistent step value between all samples """
        #use depthData parameter so can unit test easily
        if len(depthData)>1:
            try:
                depthDiff = []
                for i, item in enumerate(depthData):
                    if i>0:
                        depthDiff.append(abs(item - depthData[i-1]))
                        
                roundedDepthDiff = np.around(depthDiff, decimals=rounding)

                #twice as fast as itemfreq
                uniqueDiffs, indexes, counts = np.unique(roundedDepthDiff, return_index = True, return_counts=True)

                if readerStep in uniqueDiffs:
                    readerStepInDiffs = True
                self._meanStepValue = NumberUtils.roundToDecimal(np.mean(roundedDepthDiff), rounding)

                if len(uniqueDiffs) ==1:
                    self._consistentStep = True
                else:
                    self._consistentStep = False
                    numberDiffSteps = len(counts.tolist())
                    nonReaderStepLocations = {}
                    #are we going to use these or not?
                    for i, item in enumerate(roundedDepthDiff.tolist()):
                        for dstep in uniqueDiffs:
                            if dstep == item and dstep != readerStep:
                                if dstep in nonReaderStepLocations:
                                    # append the new number to the existing array at this slot
                                    nonReaderStepLocations[dstep].append(i)
                                else:
                                    # create a new array in this slot
                                    nonReaderStepLocations[dstep] = [i]
                    joinedStr = ', '.join(str(s) for s in indexes.tolist())
                    diffSteps = []
                    for s in uniqueDiffs:
                        if s != readerStep:
                            diffSteps.append(str(s))
                    joinedNonReaderSteps = ', '.join(diffSteps)
                    logger.info(str(numberDiffSteps)+" different steps detected.")
                    if readerStepInDiffs:
                        logger.info("Non .las header specified steps ("+str(readerStep)+") are: "+str(joinedNonReaderSteps))
                        logger.debug("Non .las header specified step line indexes in file: "+str(nonReaderStepLocations.values()))

                        
            
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logger.debug(message)
        else:
            #  one or less data values
            self.consistentStep == True

        
    #see http://stackoverflow.com/questions/2390753/is-there-a-way-to-transparently-perform-validation-on-sqlalchemy-objects
    '''
    # uses sqlalchemy hooks to data model class specific validators before update and insert
    class ValidationExtension( sqlalchemy.orm.interfaces.MapperExtension ):
        def before_update(self, mapper, connection, instance):
            """not every instance here is actually updated to the db, see http://www.sqlalchemy.org/docs/reference/orm/interfaces.html?highlight=mapperextension#sqlalchemy.orm.interfaces.MapperExtension.before_update"""
            instance.validate()
            return sqlalchemy.orm.interfaces.MapperExtension.before_update(self, mapper, connection, instance)
        def before_insert(self, mapper, connection, instance):
            instance.validate()
            return sqlalchemy.orm.interfaces.MapperExtension.before_insert(self, mapper, connection, instance)
    
    
    sqlalchemy.orm.mapper( model, table, extension = ValidationExtension(), **mapper_args )
    '''