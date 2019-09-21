
from db.core.basedao import BaseDao

from sqlalchemy.orm.exc import NoResultFound
import logging
from db.windows.wellplot.zaxistrackdata.zaxisdata import ZAxisData




logger = logging.getLogger('console')

class ZAxisDataDao(BaseDao):
    '''
    classdocs
    '''

    
    @classmethod
    def getDomainTrackDatasFromIds(cls, trackIds,  session = None):
        ''' returns DepthAxes list'''
        createdLocalSession = False
        if session == None:
            session = ZAxisDataDao.getSession()
            createdLocalSession = True
        domainTrackList = []
        if len(trackIds) > 0: 
            try:

                rs = session.query(ZAxisData).filter(ZAxisData.id.in_(trackIds))
                for domainTrackData in rs:
                    domainTrackList.append(domainTrackData)
            except NoResultFound as e:
                logger.info("No result found "+str(e))
        else:
            logger.debug("--getDomainTrackDatasFromIds() id list is empty")
        if createdLocalSession:
            session.close()
        return domainTrackList
    
    @classmethod
    def getZMeasureTrackPreferences(cls,  session = None):
        createdLocalSession = False
        if session == None:
            session = ZAxisDataDao.getSession()
            createdLocalSession = True
        #Specify a sort on the right column so first() will be the last record.
        zMeasureTrackPreferences = session.query(ZAxisData).filter_by(is_preferences = True).order_by(ZAxisData.id.desc()).first()
        if createdLocalSession:
            session.close()
        return zMeasureTrackPreferences 
        