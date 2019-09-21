
from db.core.basedao import BaseDao
import logging

from db.windows.logcurvepreferences.logcurvepreferences import LogCurvePreferences
from pyparsing import basestring


logger = logging.getLogger('console')

class LogCurvePreferencesDao(BaseDao):
    
    @classmethod
    def getLogCurvePreferences(cls, logTypeUid, session = None):
        assert isinstance(logTypeUid, str)
        createdLocalSession = False
        if session == None:
            session = LogCurvePreferencesDao.getSession()
            createdLocalSession = True

        #Specify a sort on the right column so first() will be the last record.
        logPlotPreferences = session.query(LogCurvePreferences).filter_by(is_preferences = True).filter_by(log_type_uid=logTypeUid).order_by(LogCurvePreferences.id.desc()).first()
        if createdLocalSession:
            session.close()
        return logPlotPreferences       
    
    @classmethod
    def getAllLogCurvePreferences(cls, session = None):

        createdLocalSession = False
        if session == None:
            session = LogCurvePreferencesDao.getSession()
            createdLocalSession = True

        #Specify a sort on the right column so first() will be the last record.
        logPlotPreferences = session.query(LogCurvePreferences).filter_by(is_preferences = True).order_by(LogCurvePreferences.id.desc()).first()
        if createdLocalSession:
            session.close()
        return logPlotPreferences
    
    @classmethod
    def getLogCurveDefaults(cls, logTypeUid, session = None):

        assert isinstance(logTypeUid, str)
        createdLocalSession = False
        if session == None:
            session = LogCurvePreferencesDao.getSession()
            createdLocalSession = True
        #Specify a sort on the right column so first() will be the last record.
        logCurveDefaults = None
        try:
            logCurveDefaults = session.query(LogCurvePreferences).filter_by(is_preferences = False).filter_by(log_type_uid=logTypeUid).order_by(LogCurvePreferences.id.desc()).first()
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.debug(message)
            
        if logCurveDefaults == None:
            logger.debug("--getLogCurveDefaults() nothing returned for log type: "+str(logTypeUid))
        if createdLocalSession:
            session.close()
        return logCurveDefaults 
    
