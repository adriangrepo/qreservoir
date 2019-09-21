from globalvalues.appsettings import AppSettings
from db.databasemanager import DM
from sqlalchemy import exc
import json

import logging

logger = logging.getLogger('console')

class QRDBValueError(ValueError):
    '''Raise when return value from database is incorrect'''
    #see http://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
    def __init__(self, message, foo=None, *args):
        self.message = message # without this you may get DeprecationWarning
        # Special attribute you desire with your Error, 
        # perhaps the value that caused the error?:
        self.foo = foo         
        # allow users initialize misc. arguments as any other builtin Error
        super(QRDBValueError, self).__init__(message, foo, *args) 

class BaseDao(object):
    '''
    classdocs
    '''

    @classmethod 
    def convertJSONtoData(cls, jasonStr):
        ''' returns empty string if fails '''
        data = ""
        try:
            if jasonStr != None:
                data = json.loads(jasonStr)
            else:
                logger.error("--convertJSONtoData() Input data is None")
        except (TypeError, ValueError) as e:
            logger.error("Error loading data "+str(jasonStr)+" "+str(e))
            if AppSettings.isDebugMode:
                assert True == False
        return data 
    
    @classmethod 
    def convertDataToJSON(cls, data):
        jsonStr = ""
        try:
            jsonStr = json.dumps(data)
        except TypeError as te:
            logger.error("Error converting data "+str(te))
        return jsonStr
    
    @classmethod
    def getSession(cls):
        session = DM.getSession()
        return session
    
    @classmethod
    def commitSession(self, session):
        try:
            session.commit()
            logger.debug("Session committed OK")
        except exc.SQLAlchemyError as e:
            logger.error("Cannot write data to database: "+str(e))