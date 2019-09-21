from db.databasemanager import DM
from db.core.well.well import Well
from db.core.log.log import Log

import logging
from db.core.basedao import BaseDao, QRDBValueError
from globalvalues.appsettings import AppSettings
from sqlalchemy import exc
from db.core.logservice.logservice import LogService

logger = logging.getLogger('console')

class LogServiceDao(BaseDao):
    '''
    classdocs
    '''


    @classmethod
    def getLogServices(cls, ids, session = None):
        ''' gets logsets of given ids from database '''
        createdLocalSession = False
        if len(ids) == 0:
            return None
        if  session == None:
            session = LogServiceDao.getSession()
            createdLocalSession = True

        selectedLogService = None
        rs = session.query(LogService).filter(LogService.id in ids)
        logServices = []
        for logService in rs:
            logger.debug("--getLogService() logService name: "+str(logService.name))
            logServices.append(logService)
        if createdLocalSession:
            session.close()
        return logServices
    
    
    @classmethod
    def getLogService(cls, id, session = None):
        ''' gets logset of given id from database '''
        if not isinstance(id, int) or (id <= 0):
            logger.error("Id input is invalid:{0}".format(id))
            if AppSettings.isDebugMode:
                raise ValueError
            
        createdLocalSession = False
        if  session == None:
            session = LogServiceDao.getSession()
            createdLocalSession = True

        selectedLogService = None
        try:
            rs = session.query(LogService).filter(LogService.id == id)
            if rs.count() == 0:
                raise QRDBValueError('No records found')
            if rs.count() > 1:
                raise QRDBValueError('More than 1 record found for one id')
            for logService in rs:
                logger.debug("--getLogService() logService name: "+str(logService.name))
                selectedLogService = logService 
        except QRDBValueError as e:
            logging.error(e)
            if AppSettings.isDebugMode:
                raise ValueError
        except exc.SQLAlchemyError as se:
            logging.exception('Database error')
            
        if createdLocalSession:
            session.close()
        return selectedLogService
    
    @classmethod
    def getAllLogServicesForWell(cls, wellId, session = None):
        ''' gets all log services for well from database '''
        logger.debug(">>getAllLogServicesForWell()")

        createdLocalSession = False
        if wellId == None or (not isinstance(wellId, int)):
            return None
        if  session == None:
            session = LogServiceDao.getSession()
            createdLocalSession = True

        selectedLogService = None
        rs = session.query(LogService).filter(LogService.well_id == wellId)
        logServices = []
        for logService in rs:
            logger.debug("--getAllLogServicesForWell() logService name: "+str(logService.name))
            logServices.append(logService)
        if createdLocalSession:
            session.close()
        return logServices