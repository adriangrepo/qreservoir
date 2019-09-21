from db.windows.wellplot.logtrackdata.logtrackdatadao import LogTrackDataDao

import logging

import copy

logger = logging.getLogger('console')

class LogTrackUtility(object):
    '''
    Helper functions not included in LogTrackData to avoid circular dependencies
    '''


    @classmethod
    def createNewTrack(cls):
        trackPrefs = LogTrackDataDao.getLogTrackPreferences()
        track = copy.deepcopy(trackPrefs)
        #manually call init as it is not called automatically here
        track.__init__()
        track.is_preferences = False
        #will be set when persisted
        track.id = None
        return track