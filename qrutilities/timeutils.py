import time

class TimeUtils(object):
    '''
    classdocs
    '''

    @classmethod
    def getTimeInMilliSecs(cls):
        currentMilliTime = lambda: int(round(time.time() * 1000))
        return currentMilliTime