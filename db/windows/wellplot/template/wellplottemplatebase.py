
from sqlalchemy import Boolean, Column, Integer, String


import logging
from db.base import Base
from sqlalchemy.sql.schema import ForeignKey

logger = logging.getLogger('console')

class WellPlotTemplateBase(Base):
    '''
    data pertaining to a WellPlot template 
    stores axis tracks and tracks, 
    track data is not stored here
    '''
    __tablename__ = 'well_plot_template'
    qr_classname = "Well plot template"
    
    id = Column(Integer, primary_key=True, nullable = False)
    uid = Column(String(), nullable = True)
    #typeName = Column(String(), nullable = True)

    track_data_str = Column(String(), nullable = True)

    #all, active, empty, quickplot not modifiable
    is_modifiable = Column(Boolean)
    is_preferences = Column(Boolean)
    
    history = Column(Integer, ForeignKey('history.id'))
    name = Column(String(), nullable = False)
    comments = Column(String(), nullable = True)
    
    def __init__(self):
        #alternatively could store separate tables for zAxis, track templates
        self._primary_z_track_index = 0
        self._primary_z_track_name = ""
        self._primary_z_type = ""
        #deprecated as is SI and defined by type
        #self._primary_z_unit = ""
        self._primary_z_display_unit = ""
        self._primary_z_reference = ""
        self._z_axes = []
        self._tracks = []
