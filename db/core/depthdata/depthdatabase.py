from db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import REAL
from sqlalchemy import ForeignKey


class DepthDataBase(Base):
    ''' Raw depth data, cannot store array in sqlite '''
    __tablename__ = 'depth_data'
    qr_classname = "Depth data"
        
    id = Column(Integer, primary_key=True, nullable = False)
    #Parent log_domain
    log_domain_id = Column(Integer, ForeignKey('log_domain.id'))
    #JSON string 
    data = Column(String(), nullable=True)