from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class HistorySetBase(Base):
    '''
    Store history sets
    '''
    __tablename__ = 'history_set'

    id = Column(Integer, primary_key=True, nullable = False)
    histories = relationship("History")
