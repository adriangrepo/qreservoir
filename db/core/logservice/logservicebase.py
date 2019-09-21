#!/usr/bin/env python
""" generated source for module LogServiceBase """

from sqlalchemy import Column, Integer, String
from sqlalchemy import REAL
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class LogServiceBase(Base):
    """ Container for data pertaining to logging service. Not a child of log set
    as could be across several sets.
    NB depth data is in its own class
    All data is stored as string - and will need to be converted to double as required"""
    __tablename__ = 'log_service'
    qr_classname = "Log service"

    id = Column(Integer, primary_key=True, nullable = False)
    #parent well
    well_id = Column(Integer, ForeignKey('well.id'))
    #Child logs
    logs = relationship("Log")
    #logs = relationship("Log", backref="log_service")

    
    #  logging company
    service_company = Column(String(), nullable = True)

    #  logging date
    service_date = Column(String(), nullable = True)
    analysis_by = Column(String(), nullable = True)
    analysis_location = Column(String(), nullable = True)
    type_of_fluid_in_hole = Column(String(), nullable = True)

    #  if not specified, use well depth reference
    z_measure_reference = Column(String(), nullable = True)
    td_logger = Column(REAL, nullable = True)
    null_value = Column(REAL, nullable = True)
    default_rw = Column(REAL, nullable = True)
    default_rwt = Column(REAL, nullable = True)

    #  either OWT, TWT, depth or elapsed time? (units always SI)
    z_measure_domain = Column(String(), nullable = False)
    run_number = Column(Integer, nullable=True)
    
    
    history_set_id = Column(Integer, ForeignKey('history_set.id'))
    name = Column(String(), nullable = True)
    comments = Column(String(), nullable = True)
    