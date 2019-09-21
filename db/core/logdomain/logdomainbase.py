from db.base import Base
from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy import REAL
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from db.core.log.log import Log

class LogDomainBase(Base):
    '''
    Data related to log domain properties - depth start/step/stop, number of samples
    '''
    __tablename__ = 'log_domain'
    qr_classname = "Log domain"

    id = Column(Integer, primary_key=True, nullable = False)
    #parent well
    well_id = Column(Integer, ForeignKey('well.id'))
    #Child logs
    logs = relationship("Log")
    logs = relationship("Log", backref="log_domain")

    
    z_measure_type_name = Column(String(), nullable = False)
    z_measure_data = []
    log_start = Column(REAL, nullable = False)
    log_step = Column(REAL, nullable = False)
    log_stop = Column(REAL, nullable = False)

    #  data with inconsistent step is imported as point data
    point_data = Column(Boolean, nullable=True)
    total_samples = Column(Integer, nullable=True)
    
    def __init__(self):
        #non persisted data
        self.log_start_unit = str()
        self.log_step_unit = str()
        self.log_stop_unit = str()