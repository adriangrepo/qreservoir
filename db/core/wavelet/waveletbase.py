#!/usr/bin/env python

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import REAL
from sqlalchemy import ForeignKey
from db.base import Base


class WaveletBase(Base):
    """ Wavelet table """
    __tablename__ = 'wavelet'
    qr_classname = "Wavelet"
    
    id = Column(Integer, primary_key=True, nullable = False)
    #parent well
    well_id = Column(Integer, ForeignKey('well.id'))

    
    active = Column(Boolean)
    lag = Column(Integer, nullable = True)
    phase = Column(Integer, nullable = True)
    samples = Column(Integer, nullable = True)
    sample_interval = Column(REAL, nullable = True)
    data = Column(String(), nullable = False)
    phase_error_top = Column(String(), nullable = False)
    phase_error_bottom = Column(String(), nullable = False)
    amplitude_error_top = Column(String(), nullable = False)
    amplitude_error_bottom = Column(String(), nullable = False)
    scale = Column(String(), nullable = False)
    
    history = Column(Integer, ForeignKey('history.id'))
    name = Column(String(), nullable = False)
    comments = Column(String(), nullable = True)






