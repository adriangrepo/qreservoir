from sqlalchemy.orm.exc import NoResultFound
from db.core.basedao import BaseDao, QRDBValueError
import logging

from db.windows.wellplot.template.wellplottemplate import WellPlotTemplate
from statics.templates.wellplottype import WellPlotType
from globalvalues.appsettings import AppSettings
from sqlalchemy import exc
from statics.types.zaxis import ZAxis
from statics.types.logtype import LogType

logger = logging.getLogger('console')



class WellPlotTemplateDao(BaseDao):
    
    @classmethod 
    def getWellPlotTemplateFromId(cls, wellPlotTemplateId, session = None):
        ''' returns WellPlotTemplate'''
        assert isinstance(wellPlotTemplateId, int)
        createdLocalSession = False
        if session == None:
            session = WellPlotTemplateDao.getSession()
            createdLocalSession = True
        try:
            selectedTemplate = None
            rs = session.query(WellPlotTemplate).filter(WellPlotTemplate.id == wellPlotTemplateId)
            assert rs.count() == 1
            for wellTemplate in rs:
                selectedTemplate = WellPlotTemplateDao.populateTrackData(wellTemplate)
        except NoResultFound as e:
                logger.info("No result found "+str(e))
        else:
            logger.debug("--getWellPlotTemplateFromId() id list is empty")
        if createdLocalSession:
            session.close()
        return selectedTemplate   
    

    @classmethod 
    def getWellPlotTemplateFromUid(cls, wellPlotTemplateUid, session = None):
        ''' returns WellPlotTemplate'''

        if not isinstance(wellPlotTemplateUid, str) :
            logger.error("Uid input is invalid:{0}".format(id))
            if AppSettings.isDebugMode:
                raise ValueError
            
        createdLocalSession = False
        if  session == None:
            session = WellPlotTemplateDao.getSession()
            createdLocalSession = True
    
        selectedTemplate = None 
        try:
            rs = session.query(WellPlotTemplate).filter(WellPlotTemplate.uid == wellPlotTemplateUid)
            if rs.count() == 0:
                raise QRDBValueError('No records found')
            if rs.count() > 1:
                raise QRDBValueError('More than 1 record found for one id')
            for wellTemplate in rs:
                WellPlotTemplateDao.populateTrackData(wellTemplate)
                selectedTemplate = wellTemplate 
        except QRDBValueError as e:
            logging.error(e)
            if AppSettings.isDebugMode:
                raise ValueError
        except exc.SQLAlchemyError as se:
            logging.exception('Database error')
            
        if createdLocalSession:
            session.close()
        return selectedTemplate  
    
    @classmethod 
    def getAllWellPlotTemplates(cls, session = None):
        ''' returns all WellPlotTemplates'''
        createdLocalSession = False
        if session == None:
            session = WellPlotTemplateDao.getSession()
            createdLocalSession = True
        wellTemplateList = []
        try:
            rs = session.query(WellPlotTemplate)
            for wellTemplate in rs:
                WellPlotTemplateDao.populateTrackData(wellTemplate)
                wellTemplateList.append(wellTemplate)
        except NoResultFound as e:
                logger.info("No result found "+str(e))
        if len(wellTemplateList)==0:
            logger.debug("--getAllWellPlotTemplates() list is empty")
        if createdLocalSession:
            session.close()
        return wellTemplateList  
    
    @classmethod 
    def getWellPlotTemplatesFilterModifiable(cls, isModifiable, session = None):
        ''' returns all WellPlotTemplates filtered on isModifiable flag'''
        createdLocalSession = False
        if session == None:
            session = WellPlotTemplateDao.getSession()
            createdLocalSession = True
        wellTemplateList = []
        #added for testing only
        wellTemplateUids = []
        try:
            rs = session.query(WellPlotTemplate).filter(WellPlotTemplate.is_modifiable == isModifiable)
            for wellTemplate in rs:
                WellPlotTemplateDao.populateTrackData(wellTemplate)
                wellTemplateList.append(wellTemplate)
                #added for testing only
                wellTemplateUids.append(wellTemplate.uid)
        except NoResultFound as e:
                logger.info("No result found "+str(e))
        if len(wellTemplateList)==0:
            logger.error("wellTemplateList is empty")
            if AppSettings.isDebugMode:
                raise ValueError
        #added for testing only
        if len(wellTemplateUids)!=len(set(wellTemplateUids)):
            logger.error("Duplicates found in wellTemplateList uids")
            if AppSettings.isDebugMode:
                raise ValueError
        if createdLocalSession:
            session.close()
        return wellTemplateList
        
    @classmethod 
    def populateTrackData(cls, template):
        zAxis = ZAxis.NONE
        zAxisClassName = zAxis.__class__.__name__
        logType = LogType.GAMMA
        logTypeClassName = logType.__class__.__name__
        template.primaryZAxisDict = WellPlotTemplateDao.convertJSONtoData(template.track_data_str)
        for item in template.primaryZAxisDict:
            #logger.debug("item:{0}, type:{1}".format(item, type(item))) 
            for key, value in item.items():
                if key == WellPlotType.PRIMARYZAXIS:
                    for primaryZKey, primaryZValue in value.items():
                        if primaryZKey == WellPlotType.INDEX:
                            template._primary_z_track_index = primaryZValue
                        elif primaryZKey == WellPlotType.TRACKNAME:
                            template._primary_z_track_name = primaryZValue
                        elif primaryZKey == zAxisClassName:
                            template._primary_z_type = primaryZValue
                        elif primaryZKey == WellPlotType.ZAXISUNIT:
                            template._primary_z_unit = primaryZValue
                        elif primaryZKey == WellPlotType.ZAXISREFERENCELEVEL:
                            template._primary_z_reference = primaryZValue
                elif key == WellPlotType.ZAXES:
                    template._z_axes = value
                elif key == WellPlotType.TRACKS:
                    template._tracks = value
