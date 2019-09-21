
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import Boolean, Column, Integer, String, REAL, ForeignKey

from db.core.basedao import BaseDao
from db.base import Base
from db.core.log.logdao import LogDao
from db.databasemanager import DM
from globalvalues.appsettings import AppSettings


import logging

logger = logging.getLogger('console')

class LogTrackDataBase(Base):
    '''
    class for a track, stores track properties, plot dimensions and header properties
    here the model is combined with the dao
    '''

    __tablename__ = 'log_track_data'
    qr_classname = "Log track data"
    
    id = Column(Integer, primary_key=True, nullable = False)
    plot_index = Column(Integer, nullable = True)
    
    #unique id for use prior to persistence
    uid = Column(String(), nullable = True)
    
    #Default label not implemented
    title = Column(String(), nullable = True)
    title_on = Column(Boolean)
    log_ids = Column(String(), nullable = True)
    #log type(s) separated by a slash
    track_type = Column(String(), nullable = True)
    #track width in mm
    track_width = Column(REAL, nullable = False)
    #gap between tracks in mm
    track_gap = Column(REAL, nullable = False)
    #track can store domain as well as log tracks
    #domainZType = Column(String(), nullable = True)
    #unique to each track
    grid_on = Column(Boolean)
    grid_rgb = Column(String(), nullable = True)
    grid_alpha = Column(String(), nullable = True)
    grid_line_style = Column(String(), nullable = True)
    grid_vertical_divisions = Column(Integer(), nullable = True)
    
    is_displayed = Column(Boolean)
    #rater than duplicate all fields and have a separate preferences table just store the data here
    is_preferences = Column(Boolean)



    def __init__(self):
        #self.id = 0
        #zero relative index of plots in the parent LogPlot window
        #self.plot_index = None
        
        #Default label not implemented
        #self.title = None
        
        #store each log track in this plot in a list note we don't use set as storing logs not log id's
        #self.log_ids = None
        self._logs = []



        #track width in mm
        #self.track_width = None
        #gap between tracks
        #self.track_gap = None
        

        
    
        
