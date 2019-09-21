from sqlalchemy.orm.exc import NoResultFound

from db.core.basedao import BaseDao

import logging
from db.core.history.history import History

logger = logging.getLogger('console')

class HistoryDao(BaseDao):
    '''
    classdocs
    '''

    @classmethod
    def getHistory(self, historyId, session = None):
        ''' returns specific history item'''
        logger.debug(">>getHistory()")
        assert historyId is not None
        
        createdLocalSession = False
        if session == None:
            session = HistoryDao.getSession()
            createdLocalSession = True
        try:
            rs  = None
            rs = session.query(History).filter(History.id == historyId)
            resultset = []
            for item in rs:
                resultset.append(item)
        except NoResultFound as e:
            logger.info("No result found "+str(e))
        if createdLocalSession:
            session.close()
        return resultset
