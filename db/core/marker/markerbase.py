

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import REAL
from sqlalchemy import ForeignKey
from db.base import Base


class MarkerBase(Base):
    """ generated source for class MarkerBase """
    __tablename__ = 'marker'
    qr_classname = "Marker"
    
    id = Column(Integer, primary_key=True, nullable = False)
    well_id = Column(Integer, ForeignKey('well.id'))

    markertype = Column(String(), nullable = False)
    rgb = Column(String(), nullable = True)
    alpha = Column(String(), nullable = True)

    depth = Column(REAL, nullable = False)
    ztype = Column(String(), nullable = True)
    active = Column(Boolean, nullable = True)
    description = Column(String(), nullable = True)
    stratid = Column(String(), nullable = True)
    stratlevel = Column(String(), nullable = True)

    history = Column(Integer, ForeignKey('history.id'))
    name = Column(String(), nullable = False)
    comments = Column(String(), nullable = True)

    

