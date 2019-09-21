from db.databasemanager import DM
import logging
from db.core.logdomain.logdomain import LogDomain
from db.core.basedao import BaseDao

logger = logging.getLogger('console')

class LogDomainDao(BaseDao):
    '''
    classdocs
    '''


    @classmethod
    def getLogDomain(cls, id, session = None):
        ''' gets logset of given id from database '''
        createdLocalSession = False
        if id == None:
            return None
        if  session == None:
            session = LogDomainDao.getSession()
            createdLocalSession = True
        selectedLogDomain = None
        rs = session.query(LogDomain).filter(LogDomain.id == id)
        
        if rs is not None:
            assert rs.count() == 1
            for logDomain in rs:
                logger.debug("--getLogDomain() id: "+str(LogDomain.id))
                selectedLogDomain = logDomain 
        else:
            logger.debug("--getLogDomain() error query returned none")
        if createdLocalSession:
            session.close()
        return selectedLogDomain