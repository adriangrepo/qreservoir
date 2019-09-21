#!/usr/bin/env python
""" generated source for module ParameterEntity """

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class ParameterSetBase(Base):
    """ generated source for class ParameterEntity """
    __tablename__ = 'parameter_set'
    qr_classname = "Parameter set"
    
    id = Column(Integer, primary_key=True, nullable = False)
    #parent well
    well_id = Column(Integer, ForeignKey('well.id'))
    #child logs
    logs = relationship("Log")
    #logs = relationship("Log", backref="parameter_set")
    
    history_set_id = Column(Integer, ForeignKey('history_set.id'))
    name = Column(String(), nullable = True)
    comments = Column(String(), nullable = True)
    
    def __init__(self):
        #needs to be an object variable not a class one
        #self.parameter_list = []
        self.existing = bool()

