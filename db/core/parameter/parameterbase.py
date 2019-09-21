#!/usr/bin/env python
""" generated source for module Parameter """
from db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey



    
class ParameterBase(Base):
    """ generated source for class Parameter """
    __tablename__ = 'parameter'
    qr_classname = "Parameter"
    
    id = Column(Integer, primary_key=True, nullable = False)
    #Parent
    parameter_set_id = Column(Integer, ForeignKey('parameter_set.id'))
    
    validated_mnemonic = Column(String(), nullable = True)
    mnemonic = Column(String(), nullable = True)
    value = Column(String(), nullable = True)
    unit = Column(String(), nullable = True)
    description = Column(String(), nullable = True)
    #history = Column(String(), nullable = True)

    