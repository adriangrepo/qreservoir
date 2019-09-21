
import logging


from globalvalues.constants.plottingconstants import PlottingConstants,\
    PenLineStyles


from db.core.basedao import BaseDao

from db.windows.wellplot.template.wellplottemplate import WellPlotTemplate
from statics.templates.wellplottype import WellPlotType



logger = logging.getLogger('console')



class WellPlotTemplateInitialiser(object):
    '''
    Persists default values in database
    '''

    def __init__(self, session, params=None):
        logger.debug(">>__init__()")
        self._session = session
        self._initialiseWellTemplateDefaults()
        
        
    
    def _initialiseWellTemplateDefaults(self):
        logger.debug(">>_initialiseWellTemplateDefaults()")
        #subPlotId = self._initialiseLogTrackDefaults()
        tempTemplate = WellPlotType.TRIPLECOMBO
        for key, value in tempTemplate.templateTypes.items():
            assert isinstance(value, WellPlotType)
            wellPlotTemplate = WellPlotTemplate()
            wellPlotTemplate.uid =  value.uid
            wellPlotTemplate.name = value.name
            #wellPlotTemplate.typeName = value.typeName
            wellPlotTemplate.track_data_str = BaseDao.convertDataToJSON(value.trackDataList)
            wellPlotTemplate.is_preferences = True
            
            if (value.uid == WellPlotType.ALLLOGS.uid) or (value.uid == WellPlotType.ACTIVELOGS.uid) or (value.uid == WellPlotType.EMPTY.uid) or (value.uid == WellPlotType.QUICKPLOT.uid):
                wellPlotTemplate.is_modifiable = False
            else:
                wellPlotTemplate.is_modifiable = True
            
            self._session.add(wellPlotTemplate)
        self._session.flush()
        