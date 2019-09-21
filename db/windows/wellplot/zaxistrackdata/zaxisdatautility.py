import logging

import copy
from db.windows.wellplot.zaxistrackdata.zaxisdatadao import ZAxisDataDao

logger = logging.getLogger('console')

class ZAxisDataUtility(object):
    '''
    Helper functions not included in ZAxisData to avoid circular dependencies
    '''


    @classmethod
    def createNewZAxis(cls):
        #create default ZAxis from preferences
        zAxisPrefs = ZAxisDataDao.getZMeasureTrackPreferences()
        zAxis = copy.deepcopy(zAxisPrefs)
        #manually call init as it is not called automatically here
        zAxis.__init__()
        zAxis.is_preferences = False
        #id to be assigned by SQLAlchemy when persisted
        zAxis.id = None
        #careful to set to True if primary
        zAxis.is_primary = False
        return zAxis
        