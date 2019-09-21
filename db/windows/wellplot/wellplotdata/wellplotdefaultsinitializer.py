
import logging

from globalvalues.constants.plottingconstants import PlottingConstants,\
    PenLineStyles

from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData

from db.core.basedao import BaseDao

from statics.templates.wellplottype import WellPlotType

from globalvalues.constants.wellplotconstants import WellPlotConstants
from statics.types import screenunitstype
from statics.types.screenunitstype import ScreenUnitsType
from statics.types.wellplotrangetype import WellPlotRangeType

from db.core.log.log import Log
from statics.types.logtype import LogType
#from statics.templates.wellplottemplate import WellPlotTemplate

logger = logging.getLogger('console')

class WellPlotDefaultsInitialiser(object):
    '''
    Persists default values in database
    '''

    def __init__(self, session, params=None):
        self._session = session
        self._initialiseWellPlotDefaults()
        
    def _initialiseWellPlotDefaults(self):
        logger.debug(">>_initialiseWellPlotDefaults()")
        #subPlotId = self._initialiseLogTrackDefaults()
        template = WellPlotType.TRIPLECOMBO
        for key, value in template.templateTypes.items():
            assert isinstance(value, WellPlotType)
            wellPlotData = WellPlotData()
            self.setGenericDefaults(wellPlotData)
            wellPlotData.template_uid = value.uid
            wellPlotData.is_preferences = True
            self._session.add(wellPlotData)
        self._session.flush()
        logger.debug("--_initialiseLogPlotDefaults() logplotdefaults.id: "+str(wellPlotData.id))
      
    def setGenericDefaults(self, wellPlotData):
        #hack compromise with having preferences in a data table
        wellPlotData.well_id = 0
        
        wellPlotData.title=''
        
        wellPlotData.widget_width=None
        wellPlotData.widget_height= 6
        wellPlotData.y_label= WellPlotConstants.WELL_PLOT_DEFAULT_Z_MEASURE_TYPE_UID
        wellPlotData.y_limit=None
        
        wellPlotData.y_scale='linear'
        
        wellPlotData.y_data_string = ""
        wellPlotData.y_data = []

        #store plots in a list
        wellPlotData._z_axis_track_ids = ""
        #wellPlotData.z_axis_track_datas = []
        
        wellPlotData._log_track_ids = ""
        #wellPlotData.log_track_datas = []
        
        domainPriority = WellPlotConstants.WELL_PLOT_DOMAIN_PRIORITY
        domainTrackPriority = BaseDao.convertDataToJSON(domainPriority)
        wellPlotData.z_axis_priority_str = domainTrackPriority

        wellPlotData.display_depth_axes = False
        
        wellPlotData.title_on = False
        
        #wellPlotData.start_plots_group = PlotStartDefaults.template.name
        #ivory
        wellPlotData.plot_background_rgb = "255, 255, 240"
        wellPlotData.plot_background_alpha = "255"
        wellPlotData.label_background_rgb = "255, 255, 240"
        wellPlotData.label_background_alpha = "255"
        wellPlotData.label_foreground_rgb = "0,0,0"
        wellPlotData.label_foreground_alpha = "255"
        #wellPlotData.track_header_titles= "General Logs, Lithology, MRI, Porosity, Pore Volume, Resistivity, Saturation, Wellbore"

        wellPlotData.single_row_header_labels = False
        
        wellPlotData.track_header_titles_on = False
        wellPlotData.overview_range_type = WellPlotRangeType.DATASTARTSTOP.name
        wellPlotData.overview_layout_selection = WellPlotConstants.OVERVIEW_LONGEST_GR_LOG
        wellPlotData.overview_layout_data_class = str(type(Log()))
        #the following need to be set on populating widget
        #wellPlotData.overview_layout_data_type
        #wellPlotData.overview_layout_data
        wellPlotData.tracks_range_type = WellPlotRangeType.DATASTARTSTOP.name
        #5cm per 100m
        wellPlotData.tracks_vertical_spacing = 5
        wellPlotData.tracks_vertical_spacing_display_units = ScreenUnitsType.CMpHM.name
        
