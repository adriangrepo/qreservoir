
import logging

from db.windows.wellplot.logtrackdata.logtrackdata import LogTrackData
from globalvalues.constants.wellplotconstants import WellPlotConstants
from db.core.basedao import BaseDao
from globalvalues.constants.plottingconstants import PenLineStyles

logger = logging.getLogger('console')

class LogTrackDefaultsInitialiser(object):
    '''
    Persists default values in database
    '''


    def __init__(self, session, params=None):
        self._session = session
        self._initialiseLogTrackDefaults()

    def _initialiseLogTrackDefaults(self):
        trackData = LogTrackData()
        trackData.title_on = False
        #stored in mm
        trackData.track_width = WellPlotConstants.WELL_PLOT_TRACK_WIDTH_DEFAULT
        trackData.track_gap = WellPlotConstants.WELL_PLOT_TRACK_GAP_DEFAULT
        
        trackData.grid_rgb = "150,150,150"
        trackData.grid_alpha = "100"
        trackData.grid_line_style = PenLineStyles.solid.name
        trackData.grid_on = True
        trackData.grid_vertical_divisions = WellPlotConstants.WELL_PLOT_GRID_DIVISIONS_DEFAULT
        
        trackData.is_displayed = False
        trackData.is_preferences = True
        trackData.is_domain_track = False
        self._session.add(trackData)
        
        self._session.flush()
        return trackData.id
        
    
    