


from db.core.basedao import BaseDao
from globalvalues.appsettings import AppSettings
from db.core.marker.marker import Marker

import logging
logger = logging.getLogger('console')

class MarkerDao(BaseDao):

    @classmethod
    def getMarker(cls, id, session = None):
        ''' gets well of given id from database '''
        createdLocalSession = False
        if  session == None:
            session = MarkerDao.getSession()
            createdLocalSession = True
        if id <= 0:
            logger.error("Invalid well id:{0}".format(id))
            if AppSettings.isDebugMode:
                raise ValueError
            return None
        selectedMarker = None
        rs = session.query(Marker).filter(Marker.id == id)
        assert rs.count() == 1
        for marker in rs:
            logger.debug("--getMarker() marker name: "+str(marker.name))
            selectedMarker = marker 
        if createdLocalSession:
            session.close()
        return selectedMarker
    
    