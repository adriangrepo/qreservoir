
from db.core.basedao import BaseDao

from sqlalchemy.orm.exc import NoResultFound
import logging
from db.windows.wellplot.logtrackdata.logtrackdata import LogTrackData

logger = logging.getLogger('console')

class LogTrackDataDao(BaseDao):
    '''
    classdocs
    '''

    @classmethod 
    def getLogTrackDatasFromIds(cls, trackIds, session = None):
        ''' returns LogTrackData list'''
        assert isinstance(trackIds, list)
        createdLocalSession = False
        if session == None:
            session = LogTrackDataDao.getSession()
            createdLocalSession = True
        logTrackDatas = []
        if len(trackIds) > 0: 
            try:
                rs = session.query(LogTrackData).filter(LogTrackData.id.in_(trackIds))
                for trackData in rs:
                    logTrackDatas.append(trackData)
            except NoResultFound as e:
                logger.info("No result found "+str(e))
        else:
            logger.debug("--getLogTrackDatasFromIds() id list is empty")
        if createdLocalSession:
            session.close()
        return logTrackDatas 
    
    @classmethod 
    def getLogTrackPreferences(self, session = None):

        createdLocalSession = False
        if session == None:
            session = LogTrackDataDao.getSession()
            createdLocalSession = True
        #Specify a sort on the right column so first() will be the last record.
        trackPreferences = session.query(LogTrackData).filter_by(is_preferences = True).order_by(LogTrackData.id.desc()).first()
        if createdLocalSession:
            session.close()
        return trackPreferences 
        