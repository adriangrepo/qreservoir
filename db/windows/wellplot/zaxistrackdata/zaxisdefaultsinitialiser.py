from sqlalchemy import exc
import logging

from globalvalues.constants.wellplotconstants import WellPlotConstants
from globalvalues.constants.siconversionconstants import SIConversionConstants
from db.windows.wellplot.zaxistrackdata.zaxisdata import ZAxisData
from statics.types.zaxis import ZAxis





logger = logging.getLogger('console')

class ZAxisDefaultsInitialiser(object):
    '''
    Persists default values in database
    '''

    def __init__(self, session, params=None):
        self._session = session
        self._initialiseZAxisDefaults()

    def _initialiseZAxisDefaults(self):
        domainTrackData = ZAxisData()
        domainTrackData.title_on = False
        #stored in mm
        domainTrackData.track_width = 0.8*SIConversionConstants.MM_PER_INCH
        domainTrackData.track_gap = WellPlotConstants.WELL_PLOT_TRACK_GAP_DEFAULT
        domainTrackData.z_axis_type = WellPlotConstants.WELL_PLOT_DEFAULT_Z_MEASURE_TYPE_UID
        zAxis = ZAxis.MD.getZAxisFromUID(WellPlotConstants.WELL_PLOT_DEFAULT_Z_MEASURE_TYPE_UID)
        domainTrackData.z_axis_display_units = zAxis.getDisplayUnits().getName()
        domainTrackData.z_axis_reference_level = WellPlotConstants.WELL_PLOT_DEFAULT_Z_MEASURE_REFERENCE_UID
        
        domainTrackData.is_displayed = True
        domainTrackData.is_preferences = True
        domainTrackData.is_domain_track = True
        self._session.add(domainTrackData)
        
        self._session.flush()
        return domainTrackData.id
    

    