import logging
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

logger = logging.getLogger('console')

class Base(object):
    ''' Base declarative_base includes id, create_date, update_date and __tablename__
    NB pyDev issue with @declared_attr, doesn't recognise as classmethod '''
    
    @declared_attr
    def __tablename__(cls):
        logger.debug(">>__tablename__() "+str(cls.__name__))
        return str(cls.__name__)
    update_date = Column(DateTime, nullable=True)
    create_date = Column(DateTime, default=func.now()) 
    
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(cls=Base)
