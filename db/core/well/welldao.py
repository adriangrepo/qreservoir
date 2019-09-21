from db.databasemanager import DM
from db.core.well.well import Well
from db.core.log.log import Log
from db.core.logset.logset import LogSet
import logging
from db.core.basedao import BaseDao, QRDBValueError
from globalvalues.appsettings import AppSettings
from sqlalchemy import exc

logger = logging.getLogger('console')

class WellDao(BaseDao):
    '''
    classdocs
    '''


    @classmethod
    def getWells(cls, ids, session = None):
        ''' gets wells of given ids from database '''
        logger.debug(">>getWells()")
        createdLocalSession = False
        if len(ids) == 0:
            return None
        if  session == None:
            session = WellDao.getSession()
            createdLocalSession = True
        if ids[0]<=0:
            logger.error("Invalid well id:{0}".format(ids[0]))
            if AppSettings.isDebugMode:
                raise ValueError
            return None
        selectedWell = None
        rs = session.query(Well).filter(Well.id in ids)
        wells = []
        for well in rs:    
            wells.append(well)
        logger.debug("--getWells() wells object:{0} ".format(wells))
        if createdLocalSession:
            session.close()
        return wells
    
    @classmethod
    def getWell(cls, id, session = None):
        ''' gets well of given id from database '''
        logger.debug(">>getWell()")
        if not isinstance(id, int) or (id <= 0):
            logger.error("Id input is invalid:{0}".format(id))
            if AppSettings.isDebugMode:
                raise ValueError
        
        createdLocalSession = False
        if session == None:
            session = WellDao.getSession()
            createdLocalSession = True

        selectedWell = None
        rs = session.query(Well).filter(Well.id == id)
        assert rs.count() == 1
        for well in rs:
            logger.debug("--getWell() well name: "+str(well.name))
            selectedWell = well 
        if createdLocalSession:
            session.close()
        return selectedWell
    
    @classmethod
    def getAllWells(cls, session = None):
        ''' gets all wells from database '''
        logger.debug(">>getAllWells()")

        createdLocalSession = False
        if session == None:
            session = WellDao.getSession()
            createdLocalSession = True
        wells = []
        try:
            rs = session.query(Well)
            for well in rs:
                wells.append(well) 
            if len(wells) == 0:
                logger.warn("No wells found")
        except exc.SQLAlchemyError as se:
            logging.exception('Database error')
            
        if createdLocalSession:
            session.close()
        return wells
    
        
        
    
    