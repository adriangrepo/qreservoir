#!/usr/bin/env python
""" generated source for module LogSet """

from sqlalchemy import Boolean, Column, Integer, String

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

class LogSetBase(Base):
    """ generated source for class LogSet """
    __tablename__ = 'log_set'
    qr_classname = "Log set"
    
    id = Column(Integer, primary_key=True, nullable = False)
    #parent well
    well_id = Column(Integer, ForeignKey('well.id'))
    #child logs
    logs = relationship("Log")
    #logs = relationship("Log", backref="log_set")
    
    active = Column(Boolean)
    
    history_set_id = Column(Integer, ForeignKey('history_set.id'))
    name = Column(String(), nullable = True)
    comments = Column(String(), nullable = True)
    
    def __init__(self):
        #flag for is existing set 
        self.existing = bool()

    