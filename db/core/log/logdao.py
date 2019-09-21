from sqlalchemy.orm.exc import NoResultFound
from db.core.log.log import Log
from db.core.basedao import BaseDao

import logging
from db.databasemanager import DM
from statics.types.logtype import LogType
from globalvalues.appsettings import AppSettings
logger = logging.getLogger('console')

class LogDao(BaseDao):
    '''
    classdocs
    '''

    @classmethod
    def getWellLogsOptSession(self, well, logSet, session = None):
        ''' returns list of all logs in well, log set as an optional filter'''
        logger.debug(">>getWellLogs()")
        if well == None:
            logger.dedug("--getWellLogs() no well selected, returning none")
            return None
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        rs  = None
        if logSet == None:
            ''' returns all logs in well '''
            rs = session.query(Log).filter(Log.well_id == well.id)
        else:
            ''' only return logs in relevant log set in the well '''
            logger.debug("--getWellLogs() well.id:[0] logSet.id:{1}".format(well.id, logSet.id))
            rs = session.query(Log).filter(Log.well_id == well.id).filter(Log.log_set_id == logSet.id)
        resultset = []
        for log in rs:
            LogDao.populateLogData(log)
            resultset.append(log)
        if createdLocalSession:
            session.close()
        return resultset
            
    @classmethod
    def getWellLogs(cls, wellId, session = None):
        ''' gets all logs from given well from database '''
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        expandedLogs = []
        if isinstance(wellId, int):
            rs = session.query(Log).filter(Log.well_id == wellId)
            logs = []
            for log in rs:
                logger.debug("--getWellLogs() log id: "+str(wellId)+ " log: "+str(log.name))
                logs.append(log)
            expandedLogs = LogDao.expandLogs(logs, session)
        else:
            logger.error("--getWellLogs() wellId is wrong type:{0}".format(type(wellId)))
            if AppSettings.isDebugMode:
                raise TypeError

        if createdLocalSession:
            session.close()
        return expandedLogs
       
    @classmethod     
    def getLogSetLogs(cls, logSetId, session = None):
        ''' gets all logs from given log set from database '''
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        rs = session.query(Log).filter(Log.log_set_id == logSetId)
        logs = []
        for log in rs:
            logger.debug("--getLogSetLogs() log id:{0}, log name:{1}".format(logSetId, log.name))
            logs.append(log)
        expandedLogs = []
        expandedLogs = LogDao.expandLogs(logs, session)
        if createdLocalSession:
            session.close()
        return expandedLogs
    
    @classmethod     
    def getLogTypeLogs(cls, wellId, logTypeName, session = None):
        ''' gets all logs of specific type in well '''
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        rs = session.query(Log).filter(Log.well_id == wellId).filter(Log.log_type_name == logTypeName)
        logs = []
        for log in rs:
            logger.debug("--getLogTypeLogs() logTypeName:{0}, log name:{1}".format(logTypeName, log.name))
            logs.append(log)
        expandedLogs = []
        expandedLogs = LogDao.expandLogs(logs, session)
        if createdLocalSession:
            session.close()
        return expandedLogs
    
    @classmethod     
    def getLogTypeNamesInWell(cls, wellId,  session = None):
        ''' gets all log types  in well '''
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        rs = session.query(Log).filter(Log.well_id == wellId)
        logTypes = []
        for log in rs:
            logTypes.append(log.log_type_name)
        if createdLocalSession:
            session.close()
        return list(set(logTypes))
    
    @classmethod
    def expandLogs(cls, logs, session = None):
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        expandedLogs = []
        if len(logs)>0:
            expandedLogs = LogDao.extractLogData(logs, session)
        if createdLocalSession:
            session.close()
        return expandedLogs
    
    @classmethod
    def populateLogData(cls, log):
        log.log_data = LogDao.convertJSONtoData(log.log_data_str)
        data  = LogDao.convertJSONtoData(log.z_measure_data_str)
        log.z_measure_data = (data)
                         
    @classmethod 
    def extractLogData(cls, logs, session = None):
        ''' extracts depth data from JSON string, returns log list'''
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        logList = []
        if len(logs) > 0: 
            #session = DM.getSession()
            logIds = []
            for log in logs:
                logIds.append(log.id)
            try:
                rs = session.query(Log).filter(Log.id.in_(logIds))
                for log in rs:
                    #log = Log()
                    #log.id = (item.log_domain_id)
                    LogDao.populateLogData(log)
                    #log.depth_min = item.depth_min
                    #log.depth_max = item.depth_max
                    logList.append(log)
            except NoResultFound as e:
                logger.info("No result found "+str(e))
        else:
            logger.debug("<<extractLogData() No logs in input")
        if createdLocalSession:
            session.close()
        return logList 
    

    
    
    def getIdNameTupleFromLogList(self, logs):
        logNameDict = {}
        for log in logs:
            logNameDict[log.id] = log.name
            
    @classmethod
    def getActiveLogIds(cls, logs):
        activeLogIds = []
        if len(logs)>0:
            for log in logs: 
                if log.active:
                    activeLogIds.append(log.id)
        return activeLogIds


    @classmethod 
    def getLogsFromIds(cls, logIds, session = None):
        ''' returns expanded log list (extracts depth data from JSON string)'''
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        logList = []
        if len(logIds) > 0: 
            try:
                rs = session.query(Log).filter(Log.id.in_(logIds))
                for log in rs:
                    #log = Log()
                    #log.id = (item.log_domain_id)
                    LogDao.populateLogData(log)
                    #log.depth_min = item.depth_min
                    #log.depth_max = item.depth_max
                    logList.append(log)
            except NoResultFound as e:
                logger.info("No result found "+str(e))
        else:
            logger.debug("<<extractLogData() No logs in input")
        if createdLocalSession:
            session.close()
        return logList 
    
    @classmethod 
    def getLog(cls, logId, session = None):
        ''' returns expanded log (extracts depth data from JSON string)'''
        if not isinstance(logId, int) or (logId <= 0):
            logger.error("Id input is invalid:{0}".format(logId))
            if AppSettings.isDebugMode:
                raise ValueError
        
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
        selectedLog = None

        selectedLog = None
        try:
            rs = session.query(Log).filter(Log.id == logId)
            assert rs.count() == 1
            for log in rs:
                #log = Log()
                #log.id = (item.log_domain_id)
                LogDao.populateLogData(log)
                #log.depth_min = item.depth_min
                #log.depth_max = item.depth_max
                selectedLog = log
        except NoResultFound as e:
            logger.info("No result found "+str(e))

        if createdLocalSession:
            session.close()
        return selectedLog 
    
    @classmethod
    def getUnits(cls, log):
        units = ""
        logType = LogType.getLogType(log.log_type_name)
        if logType != None:
            units = logType.getStdUnits().name
        else:
            logType = LogType.UNKNOWN
            units = logType.getStdUnits().name
            logger.error("--getUnits() "+str(log.name)+" is of an unknown type returning unknown units: "+str(units))
            if AppSettings.isDebugMode:
                raise AttributeError
        return units
    
    @classmethod
    def getLogNamesCSV(cls, logs):
        logNames = []
        for log in logs:
            logNames.append(log.name)
        logCSV = ",".join(logNames)
        return logCSV
    
    @classmethod
    def getActiveLogsForWell(cls, wellId, session = None):
        ''' gets all active logs from given well from database '''
        createdLocalSession = False
        if session == None:
            session = LogDao.getSession()
            createdLocalSession = True
            
        rs = session.query(Log).filter(Log.well_id == wellId)
        logs = []
        for log in rs:
            logger.debug("--getWellLogs() log id: "+str(wellId)+ " log: "+str(log.name))
            if log.active:
                logs.append(log)

        expandedLogs = []
        expandedLogs = LogDao.expandLogs(logs, session)
        if createdLocalSession:
            session.close()
        return expandedLogs
