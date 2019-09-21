
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import REAL
from sqlalchemy import ForeignKey
from db.base import Base


class LogBase(Base):
    """ generated source for class LogBase """
    __tablename__ = 'log'
    qr_classname = "Log"
    
    id = Column(Integer, primary_key=True, nullable = False)
    #Parents
    log_set_id = Column(Integer, ForeignKey('log_set.id'))
    log_domain_id = Column(Integer, ForeignKey('log_domain.id'))
    log_service_id = Column(Integer, ForeignKey('log_service.id'))
    parameter_set_id = Column(Integer, ForeignKey('parameter_set.id'))

    well_id = Column(Integer, ForeignKey('well.id'))

    #LogType.name property
    #TODO change this to store log_type_uid
    log_type_name = Column(String(), nullable=False)
    #ZType
    #TODO change this to store z_measure_type_uid
    z_measure_type_name = Column(String(), nullable = False)
    #stored in log service
    z_measure_reference = Column(String(), nullable = True)
    #JSON string 
    log_data_str = Column(String(), nullable=True)
    #JSON string 
    z_measure_data_str = Column(String(), nullable=True)
    consistent_step = Column(Boolean)
    #depth calculated as per header start/stop/step
    honour_las_depth_values = Column(Boolean)
    z_measure_min = Column(REAL, nullable = False)
    z_measure_max = Column(REAL, nullable = False)
    z_measure_step = Column(REAL, nullable = True)
    total_samples = Column(Integer, nullable=True)
    #  even though run number is in logService, could be multiple runs stored in the las file (eg las v3.0)
    run_number = Column(Integer, nullable=True)
    
    value_min = Column(REAL, nullable = True)
    value_max = Column(REAL, nullable = True)
    is_logarithmic = Column(Boolean)
    #instead of a global null store it per log?
    null = Column(REAL, nullable = True)
    
    #statistics
    mean = Column(REAL, nullable = True)
    median = Column(REAL, nullable = True)
    stdev = Column(REAL, nullable = True)
    

    #  rest are for display purposes
    blocked = Column(Boolean)
    active = Column(Boolean)
    pseudo_well_log = Column(Boolean)
    '''
    plot_min = Column(REAL, nullable = True)
    plot_max = Column(REAL, nullable = True)
    rgba = Column(String(), nullable = True)
    trace_width = Column(REAL, nullable = True)
    trace_style = Column(String(), nullable = True)
    '''
    log_plot_left = Column(REAL, nullable = True)
    log_plot_right = Column(REAL, nullable = True)
    log_plot_default = Column(REAL, nullable = True)
    #if a logarithmic plot
    log_plot_log_cycles = Column(Integer, nullable=True)
    log_plot_points_on = Column(Boolean)
    histogram_left = Column(REAL, nullable = True)
    histogram_right = Column(REAL, nullable = True)
    histogram_default = Column(REAL, nullable = True)
    cross_plot_left = Column(REAL, nullable = True)
    cross_plot_right = Column(REAL, nullable = True)
    cross_plot_default = Column(REAL, nullable = True)
    #MPL uses float width, Qt uses int so need to convert using NumberUtils
    line_width = Column(REAL, nullable = True)
    line_style = Column(String(), nullable = True)
    point_size = Column(REAL, nullable = True)
    point_style = Column(String(), nullable = True)
    #hexcode
    rgb = Column(String(), nullable = True)
    alpha = Column(String(), nullable = True)

    source = Column(String(), nullable = True)
    
    history_set_id = Column(Integer, ForeignKey('history_set.id'))
    name = Column(String(), nullable = False)
    comments = Column(String(), nullable = True)
    
    def __init__(self):
        self.importLog = bool()
        #convert to SI
        self.unit = str()
        self.validName = bool()
        self.isDuplicate = bool()
        self.fileMnemonic = str()
        self.fileUnit = str()
        self.fileDescription = str()
        self.rowIndex = int()
        #Real list
        self.log_data = []
        #Real list
        self.z_measure_data = []

    

