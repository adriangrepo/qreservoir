


from db.core.basedao import BaseDao
from db.windows.wellplot.logtrackdata.logtrackdefaultsinitialiser import LogTrackDefaultsInitialiser
from db.windows.wellplot.zaxistrackdata.zaxisdefaultsinitialiser import ZAxisDefaultsInitialiser
from db.windows.wellplot.wellplotdata.wellplotdefaultsinitializer import WellPlotDefaultsInitialiser
from db.windows.logcurvepreferences.logcurvedefaultsinitialiser import LogCurveDefaultsInitialiser

import logging
from db.windows.wellplot.template.wellplottemplateinitializer import WellPlotTemplateInitialiser
logger = logging.getLogger('console')

class DefaultsInitialiser(BaseDao):
    '''
    Persists default values in database
    '''


    def __init__(self, params=None):
        session = self.getSession()
        
        initialiseLogTrackDefaults = LogTrackDefaultsInitialiser(session)
        initialiseDomainTrackDefaults = ZAxisDefaultsInitialiser(session)
        initialiseWellPlotDefaults = WellPlotDefaultsInitialiser(session)
        initialiseLogCurveDefaults = LogCurveDefaultsInitialiser(session)
        initialiseWellPlotTemplateDefaults = WellPlotTemplateInitialiser(session)

        self.commitSession(session)
        
    
    