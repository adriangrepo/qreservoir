from db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import REAL
from sqlalchemy.sql.sqltypes import Boolean

class LogCurvePreferencesBase(Base):
    ''' curve plotting preferences for each log type '''
    __tablename__ = 'log_curve_data'
    qr_classname = "Log curve data"
    
    id = Column(Integer, primary_key=True, nullable = False)

    log_type_uid = Column(String(), nullable = False)
    #better to just use uid and look up name?
    log_type_name = Column(String(), nullable = True)
    log_plot_left = Column(REAL, nullable = True)
    log_plot_right = Column(REAL, nullable = True)
    log_plot_default = Column(REAL, nullable = True)
    log_plot_log_cycles = Column(Integer, nullable = True)
    log_plot_points_on = Column(Boolean)
    histogram_left = Column(REAL, nullable = True)
    histogram_right = Column(REAL, nullable = True)
    histogram_default = Column(REAL, nullable = True)
    cross_plot_left = Column(REAL, nullable = True)
    cross_plot_right = Column(REAL, nullable = True)
    cross_plot_default = Column(REAL, nullable = True)
    
    line_width = Column(REAL, nullable = True)
    line_style = Column(String(), nullable = True)
    point_size = Column(REAL, nullable = True)
    point_style = Column(String(), nullable = True)
    log_types = Column(String(), nullable = True)
    is_logarithmic = Column(Boolean)
    rgb = Column(String(), nullable = True)
    alpha = Column(String(), nullable = True)
    #is either default (False) or preferences
    is_preferences = Column(Boolean)
    