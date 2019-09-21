from sqlalchemy.orm.exc import NoResultFound

from db.core.basedao import BaseDao

import logging
from db.core.history.historyset import HistorySet

logger = logging.getLogger('console')

class HistorySetDao(BaseDao):
    '''
    classdocs
    '''

    @classmethod
    def getHistorySet(self, historySetId, session = None):
        ''' returns specific historySet item'''
        logger.debug(">>getHistorySet()")
        assert historySetId is not None
        
        createdLocalSession = False
        if session == None:
            session = HistorySetDao.getSession()
            createdLocalSession = True
        try:
            rs  = None
            rs = session.query(HistorySet).filter(HistorySet.id == historySetId)
            resultset = []
            for item in rs:
                resultset.append(item)
        except NoResultFound as e:
            logger.info("No result found "+str(e))
        if createdLocalSession:
            session.close()
        return resultset
