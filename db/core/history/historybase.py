from sqlalchemy import Column, Integer, String

from db.base import Base
from sqlalchemy.sql.schema import ForeignKey

class HistoryBase(Base):
    '''
    Store history actions for relevant tables
    '''
    __tablename__ = 'history'
    #qr_classname = "History"
    
    id = Column(Integer, primary_key=True, nullable = False)
    history_set_id = Column(Integer, ForeignKey('history_set.id'))
    #store history values relevant to a particular class
    sub_id = Column(Integer, nullable = True)
    
    user = Column(String(), nullable=True)
    action = Column(String(), nullable=True)
    details = Column(String(), nullable=True)
    
    version = Column(String(), nullable=True)
    build_date = Column(String(), nullable=True)

        