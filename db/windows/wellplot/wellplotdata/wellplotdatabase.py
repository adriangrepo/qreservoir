
from db.base import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import REAL

import logging

logger = logging.getLogger('console')

class WellPlotDataBase(Base):
    '''
    data pertaining to the WellPlot window 
    all depth/time axis data is stored here as common to all sub-plots
    '''
    __tablename__ = 'well_plot_data'
    qr_classname = "Well plot data"
    
    id = Column(Integer, primary_key=True, nullable = False)
    uid = Column(String(), nullable = True)
    #set to true for preferences
    well_id = Column(Integer, nullable = True)
    log_set_id = Column(Integer, nullable = True)
    
    title = Column(String(), nullable = True)
    title_on = Column(Boolean)
    
    widget_width = Column(REAL, nullable = True)
    widget_height = Column(REAL, nullable = True)

    y_label = Column(String(), nullable = True)
    y_limit = Column(String(), nullable = True)
    y_data_string = Column(String(), nullable = True)
    y_scale = Column(String(), nullable = True)

    log_ids = Column(String(), nullable = True)
        
    #TODO store these when saving the well plot
    #access these through getZMeasureTrackDatas()
    _z_axis_track_ids = Column(String(), nullable = True)

    #JSON string containing domain priority eg ZType.MD DisplayUnit.m ReferenceType.WB, ZType.TVDSS DisplayUnit.ft ReferenceType.MSL, ZTYPE.TWT DisplayUnit.ms ReferemceType.SRD
    z_axis_priority_str = Column(String(), nullable = True)
    #TODO store these when saving the well plot
    #use getLogTrackDatas() to access
    _log_track_ids = Column(String(), nullable = True)

    plot_background_rgb = Column(String(), nullable = True)
    plot_background_alpha = Column(String(), nullable = True)
    label_background_rgb = Column(String(), nullable = True)
    label_background_alpha = Column(String(), nullable = True)
    label_foreground_rgb = Column(String(), nullable = True)
    label_foreground_alpha = Column(String(), nullable = True)
    
    #DUG type vs HRS type labels 
    single_row_header_labels = Column(Boolean)
    
    #String name of template type, can be a user define name stored in preferences
    template_uid = Column(String(), nullable = True)
    track_header_titles_on = Column(Boolean)
    #preferences/defaults related
    
    #what to plot on starting plot - eg default, active, all
    start_plots_group = Column(String(), nullable = True)
    #DataStartToDataStop, ZeroToDataStop, Manual
    overview_range_type = Column(Integer, nullable = True)
    overview_start = Column(REAL, nullable = True)
    overview_stop = Column(REAL, nullable = True)
    
    overview_region_start = Column(REAL, nullable = True)
    overview_region_stop = Column(REAL, nullable = True)
    #see OverviewLayoutSelection class
    overview_layout_selection = Column(String(), nullable = True)
    #Log, Seismic
    overview_layout_data_class = Column(String(), nullable = True)
    #LogType.Gamma
    #overview_layout_data_type = Column(String(), nullable = True)
    #specific log
    overview_layout_log_id = Column(Integer, nullable = True)
    
    tracks_range_type = Column(Integer, nullable = True)
    tracks_range_start = Column(REAL, nullable = True)
    tracks_range_stop = Column(REAL, nullable = True)
    #SI units - convert to/from if different
    tracks_vertical_spacing = Column(REAL, nullable = True)
    tracks_vertical_spacing_display_units = Column(String(), nullable = True)
    tracks_scale = Column(REAL, nullable = True)
    
    is_preferences = Column(Boolean)

    def __init__(self):
        logger.debug(">>__init__() ")
        
        self.y_data = []
        #access these through getZMeasureTrackDatas()
        self._z_axis_track_datas = []
        #protected, use getLogTrackDatas() to access
        self._log_track_datas = []
        '''Used for defining what sort of logs to polt eg MD first, TVDSSS second etc'''
        self.z_axis_track_priority = []

    
    
