from sqlalchemy.orm.exc import NoResultFound
from db.core.basedao import BaseDao, QRDBValueError
import logging
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData
from statics.types.logtype import LogType
from sqlalchemy import exc


logger = logging.getLogger('console')

class WellPlotDataDao(BaseDao):
    
    @classmethod 
    def getWellPlotDatasFromId(cls, wellPlotId, session = None):
        ''' returns WellPlotData item'''
        assert isinstance(wellPlotId, int)
        createdLocalSession = False
        if session == None:
            session = WellPlotDataDao.getSession()
            createdLocalSession = True
        if wellPlotId > 0: 
            try:
                wellPlotData = session.query(WellPlotData).filter(WellPlotData.id == wellPlotId)
                if wellPlotData.count() == 0:
                    raise QRDBValueError('No records found')
                WellPlotDataDao.populateDomainPriority(wellPlotData)
            except QRDBValueError as e:
                #if no results found, is a problem
                logging.error(e)
        else:
            logger.debug("--getWellPlotDatasFromIds() id is 0 or less")

        if createdLocalSession:
            session.close()
        return wellPlotData 
    
    
    @classmethod 
    def getWellPlotDatasFromIds(cls, wellPlotIds, session = None):
        ''' returns WellPlotData list'''
        assert isinstance(wellPlotIds, list)
        createdLocalSession = False
        if session == None:
            session = WellPlotDataDao.getSession()
            createdLocalSession = True
        wellPlotList = []
        if len(wellPlotIds) > 0: 
            try:
                rs = session.query(WellPlotData).filter(WellPlotData.id.in_(wellPlotIds))
                if rs.count() == 0:
                    raise QRDBValueError('No records found')
                for wellPlotData in rs:
                    WellPlotDataDao.populateDomainPriority(wellPlotData)
                    wellPlotList.append(wellPlotData)
            except QRDBValueError as e:
                #if no results found, is a problem
                logging.error(e)
        else:
            logger.debug("--getWellPlotDatasFromIds() id list is empty")

        if createdLocalSession:
            session.close()
        return wellPlotList 
    
    @classmethod
    def populateDomainPriority(cls, wellPlotData):
        assert isinstance(wellPlotData, WellPlotData)
        wellPlotData.domain_track_priority = WellPlotDataDao.convertJSONtoData(wellPlotData.z_axis_priority_str)
        
    @classmethod
    def getWellPlotPreferences(self, templateUid = None, session = None):
        createdLocalSession = False
        if session == None:
            session = WellPlotDataDao.getSession()
            createdLocalSession = True
        if templateUid is not None:
            assert isinstance(templateUid, str)
            logPlotPreferences = session.query(WellPlotData).filter_by(is_preferences = True).filter_by(template_uid = templateUid).order_by(WellPlotData.id.desc()).first()
        else:
            #Specify a sort on the right column so first() will be the last record.
            logPlotPreferences = session.query(WellPlotData).filter_by(is_preferences = True).order_by(WellPlotData.id.desc()).first()
        if createdLocalSession:
            session.close()
        return logPlotPreferences 
    
    @classmethod
    def getAllDynamicWellPlots(self, session = None):
        '''Returns all non preference WellPlots '''
        createdLocalSession = False
        if session == None:
            session = WellPlotDataDao.getSession()
            createdLocalSession = True
        wellPlots = []
        try:
            #Specify a sort on the right column so first() will be the last record.
            rs =  session.query(WellPlotData).filter_by(is_preferences = False).order_by(WellPlotData.id.desc()).first()
            if (rs is None) or (rs.count() == 0):
                raise QRDBValueError('No records found')
            for wellPlot in rs:
                wellPlots.append(wellPlot)
        except QRDBValueError as e:
            #OK if no results found, don't need to logger.info it
            logging.debug(e)
        except exc.SQLAlchemyError as se:
            logging.exception('Database error')
        if createdLocalSession:
            session.close()
        return wellPlots 
    
    @classmethod
    def getAllDynamicWellPlotsOfTemplateType(self, templateUid, session = None):
        '''Returns all non preference WellPlots of Template type'''
        createdLocalSession = False
        if session == None:
            session = WellPlotDataDao.getSession()
            createdLocalSession = True
            
        assert isinstance(templateUid, str)
        logPlotPreferences = session.query(WellPlotData).filter_by(is_preferences = False).filter_by(template_uid = templateUid).order_by(WellPlotData.id.desc()).first()
        if createdLocalSession:
            session.close()
        return logPlotPreferences 
    
    def getLogIdsPreferences(self, logs):
        assert isinstance(logs, list)
        # returns list of default log ids 
        logIdsPrefs = []
        logTypeNamesPrefs = self.getLogTypeNamesPreferences()
        for i, log in enumerate(logs): 
            if log.log_type_name in logTypeNamesPrefs:
                logIdsPrefs.append(log.id)
        return logIdsPrefs
    
    def getLogsPreferences(self, logs):
        assert isinstance(logs, list)
        # returns list of default log objects 
        logsPrefs = []
        logTypeNamesPreferences = self.getLogTypeNamesPreferences()
        for i, log in enumerate(logs): 
            if log.log_type_name in logTypeNamesPreferences:
                logsPrefs.append(log)
        return logsPrefs
    
    
    def getLogTypeNamesPreferences(self):
        logPlotPreferences = WellPlotDataDao.getWellPlotPreferences()
        logTypeNamesPreferences = []
        if logPlotPreferences != None:
            
            logUids = logPlotPreferences.default_log_plots
            logger.debug("--getWellPlotPreferences() logUids: "+logUids)
            defaultList = logUids.split()
            for uid in defaultList:
                logger.debug("--getWellPlotPreferences() uid: "+str(uid)+" type: "+LogType.getLogTypeFromUid(uid).getName())
                logTypeNamesPreferences.append(LogType.getLogTypeFromUid(uid).getName())
        else:
            logger.error("No log plot defaults exist in the database")
        return logTypeNamesPreferences 


    