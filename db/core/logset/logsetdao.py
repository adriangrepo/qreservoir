from db.databasemanager import DM
from db.core.well.well import Well
from db.core.log.log import Log
from db.core.logset.logset import LogSet
import logging
from db.core.basedao import BaseDao, QRDBValueError
from globalvalues.appsettings import AppSettings
from sqlalchemy import exc

logger = logging.getLogger('console')

class LogSetDao(BaseDao):
    '''
    classdocs
    '''


    @classmethod
    def getLogSets(cls, ids, session = None):
        ''' gets logset of given id from database '''
        createdLocalSession = False
        if len(ids) == 0:
            return None
        if  session == None:
            session = LogSetDao.getSession()
            createdLocalSession = True

        selectedLogSet = None
        rs = session.query(LogSet).filter(LogSet.id in ids)
        logSets = []
        for logSet in rs:
            logger.debug("--getLogSet() logSet name: "+str(logSet.name))
            logSets.append(logSet)
        if createdLocalSession:
            session.close()
        return logSets
    
    @classmethod
    def getLogSet(cls, id, session = None):
        ''' gets logset of given id from database '''
        if not isinstance(id, int) or (id <= 0):
            logger.error("Id input is invalid:{0}".format(id))
            if AppSettings.isDebugMode:
                raise ValueError
            
        createdLocalSession = False
        if  session == None:
            session = LogSetDao.getSession()
            createdLocalSession = True

        selectedLogSet = None
        try:
            rs = session.query(LogSet).filter(LogSet.id == id)
            if rs.count() == 0:
                raise QRDBValueError('No records found')
            if rs.count() > 1:
                raise QRDBValueError('More than 1 record found for one id')
            for logSet in rs:
                logger.debug("--getLogSet() logSet name: "+str(logSet.name))
                selectedLogSet = logSet 
        except QRDBValueError as e:
            logging.error(e)
            if AppSettings.isDebugMode:
                raise ValueError
        except exc.SQLAlchemyError as se:
            logging.exception('Database error')
            
        if createdLocalSession:
            session.close()
        return selectedLogSet