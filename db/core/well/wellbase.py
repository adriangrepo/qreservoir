#!/usr/bin/env python
""" generated source for module WellBase """
# 
#  * To change this license header, choose License Headers in Project Properties.
#  * To change this template file, choose Tools | Templates
#  * and open the template in the editor.
#  
# package: com.qgs.qreservoir.jpa.data.model.entity

from sqlalchemy import Boolean, Column, Integer, String
#see http://docs.sqlalchemy.org/en/rel_0_9/core/type_basics.html#sql-standard-types
from sqlalchemy import REAL
#from sqlalchemy.sql.schema import CheckConstraint
#from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from db.base import Base
from sqlalchemy import ForeignKey


class WellBase(Base):
    """ Persisted WellBase data 
    For ease of import, all except essential, required data is stored as string and will need to be converted to double as required"""
        # Name of mapped database table.
    __tablename__ = 'well'
    qr_classname = "Well"
    
    id = Column(Integer, primary_key=True, nullable = False)
    #Child log_sets, one to many relationship
    log_sets = relationship("LogSet")
    parameter_sets = relationship("ParameterSet")
    #log_sets = relationship("LogSet", backref="well")
    #parameter_sets = relationship("ParameterSet", backref="well")

    #Required fields
    #depth_type is defined in wrapper - not persisted
    depth_reference = Column(String(255), nullable = False)
    elevation_of_depth_reference = Column(REAL, nullable = False)
    '''
    @validates('elevation_of_depth_reference')
    def validate_elevation_of_depth_reference(self, key, elevation_of_depth_reference):
        if elevation_of_depth_reference < -10 or elevation_of_depth_reference >10 :
            raise ValueError('elevation_of_depth_reference must be between -10 and 10.')
        return elevation_of_depth_reference
    '''
    #Non required data
    uwi = Column(String(255), nullable = True)
    api = Column(String(255), nullable = True)
        
    #  Permanent Datum eg MSL
    permanent_datum = Column(String(255), nullable = True)
    permanent_datum_elevation = Column(REAL, nullable = True)
    elevation_above_permanent_datum = Column(REAL, nullable = True)
        
    #  duplicated in zdata but well could change?
    drilling_reference = Column(String(255), nullable = True)
    df_elevation = Column(REAL, nullable = True)
    gl_elevation = Column(REAL, nullable = True)
    kb_elevation = Column(REAL, nullable = True)
    water_depth = Column(REAL, nullable = True)
    td_driller = Column(REAL, nullable = True)
    latitude = Column(String(255), nullable = True)
    longitude = Column(String(255), nullable = True)
    x_coordinate = Column(REAL, nullable = True)
    y_coordinate = Column(REAL, nullable = True)
    #akin to Petrel TD Measured Depth when can manually set in well settings
    #if not set can set to td_drill or at lead to mdstop
    td_md_kb = Column(REAL, nullable = True)
        
    #  Geodetic Datum use for both X,Y and Lat,Long
    geodetic_datum = Column(String(255), nullable = True)
    horizontal_coordinate_system = Column(String(255), nullable = True)
        
    #  need units?
    operator = Column(String(255), nullable = True)
    block = Column(String(255), nullable = True)
    area = Column(String(255), nullable = True)
    province = Column(String(255), nullable = True)
    license = Column(String(255), nullable = True)
    spud_date = Column(String(255), nullable = True)
    td_date = Column(String(255), nullable = True)
    rig_name = Column(String(255), nullable = True)
        
    #  The name of the drilling company that drilled the well. 
    drilling_contractor = Column(String(255), nullable = True)
    field = Column(String(255), nullable = True)
    country = Column(String(255), nullable = True)
    location = Column(String(255), nullable = True)
    company = Column(String(255), nullable = True)
    utm_zone = Column(String(255), nullable = True)
    completion_status = Column(String(255), nullable = True)
    state = Column(String(255), nullable = True)
    county = Column(String(255), nullable = True)
    note = Column(String(255), nullable = True)
    #file_depth_units = Column(String(255), nullable = True)
    file_depth_units = str()
        
    #  rest of fields are application fields, not from las
    #  WellBase Path related
    ahdtotvdkbconversion = Column(Integer, nullable=True)
    tvdsstotwtconversion = Column(Integer, nullable=True)
    mdstart = Column(REAL, nullable = True)
    mdstop = Column(REAL, nullable = True)
    #mdstep = Column(REAL, nullable = True)
    tvdkbstart = Column(REAL, nullable = True)
    tvdkbstop = Column(REAL, nullable = True)
    #tvdkbstep = Column(REAL, nullable = True)
    twtstart = Column(REAL, nullable = True)
    twtstop = Column(REAL, nullable = True)
    #twtstep = Column(REAL, nullable = True)
    calcmdstart = Column(REAL, nullable = True)
    calcmdstop = Column(REAL, nullable = True)
    calctvdkbstart = Column(REAL, nullable = True)
    calctvdkbstop = Column(REAL, nullable = True)
    calctwtstart = Column(REAL, nullable = True)
    calctwtstop = Column(REAL, nullable = True)
    useuserstartstop = Column(Boolean, nullable = True)
    applydepthchangetoallzsticks = Column(Boolean, nullable = True)
    pseudo_well = Column(Boolean, nullable = True)
        
    #  UI related
    rgb = Column(String(), nullable = True)
    alpha = Column(String(), nullable = True)
    symbol = Column(Integer, nullable=True)
    colorbardatabaseid = Column(Integer, nullable=True)
    displaymarkers = Column(Boolean, nullable = True)
    wellpathwidth = Column(REAL, nullable = True)
    wellpathstyle = Column(String(), nullable = True)
    displaypathinmap = Column(Boolean, nullable = True)
    displaysymbolatstart = Column(Boolean, nullable = True)
    displaylogtrackextents = Column(Boolean, nullable = True)
            
    #other
    source = Column(String(), nullable = True)
    
    history_set_id = Column(Integer, ForeignKey('history_set.id'))
    name = Column(String(), nullable = False)
    comments = Column(String(), nullable = True)
    
    def __init__(self):
        #Non persisted data
        self.z_measure_type_name = str()
        
        #  Permanent Datum eg MSL
        self.permanent_datum_elevation_unit = str()
        self.elevation_above_permanent_datum_unit = str()
        
        #  duplicated in zdata but well could change?
        self.elevation_of_depth_reference_unit = str()
        self.df_elevation_unit = str()
        self.gl_elevation_unit = str()
        self.kb_elevation_unit = str()
        self.water_depth_unit = str()
        self.td_driller_unit = str()
        
        #flag for is existing well 
        self.existing = bool()

