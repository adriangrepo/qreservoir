from db.base import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import REAL


class ZAxisDataBase(Base):
    __tablename__ = 'z_axis'
    qr_classname = "Z axis"
    
    id = Column(Integer, primary_key=True, nullable = False)
    plot_index = Column(Integer, nullable = True)
    #unique id for use prior to persistence
    uid = Column(String(), nullable = True)
    title = Column(String(), nullable = True)
    title_on = Column(Boolean)
    log_ids = Column(String(), nullable = True)
    #primary or secondary
    is_primary = Column(Boolean)
    #track width in mm
    track_width = Column(REAL, nullable = False)
    #gap between tracks in mm
    track_gap = Column(REAL, nullable = False)
    #track can store domain as well as log tracks
    z_axis_type = Column(String(), nullable = True)
    z_axis_display_units = Column(String(), nullable = True)
    z_axis_reference_level = Column(String(), nullable = True)
    #unit not required as is SI
    #z_axis_unit = Column(String(), nullable = True)

    is_displayed = Column(Boolean)
    #rater than duplicate all fields and have a separate preferences table just store the data here
    is_preferences = Column(Boolean)
    plotYmin = Column(REAL, nullable = True)
    plotYmax = Column(REAL, nullable = True)
    allLogDomainMax = Column(REAL, nullable = True)
    allLogDomainMin = Column(REAL, nullable = True)
    #rather than duplicate all fields and have a separate preferences table just store the data here
    #is_preferences = Column(Boolean)
    

        
    def __init__(self, params=None):
        pass
        
        