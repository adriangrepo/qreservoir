#!/usr/bin/env python
""" generated source for module LogServiceDTO """
# package: com.qgs.qreservoir.io.las.reader.dto


#from com.qgs.qreservoir.global_.constants.well.wellsettingsconstants import WellSettingsConstants

#import com.qgs.qreservoir.io.las.reader.dto.list_.LogListDTO
import datetime


# see http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
class LogServiceDTO(object):
    """ Log service information holder """
    
    def __init__(self):
        self.id = int()
        self.z_measure_type_name = str()
        self.z_measure_data = []
        self.log_start = float()
        self.log_step = float()
        self.log_stop = float()

        #  data with inconsistent step is imported as point data
        self.point_data = bool()
        self.total_samples = int()

        #  logging company
        self.service_company = str()

        #  logging date
        self.service_date = str()
        self.analysis_by = str()
        self.analysis_location = str()
        self.type_of_fluid_in_hole = str()

        #  if not specified, use well depth reference
        self.z_measure_reference = str()
        self.td_logger = float()
        self.null_value = float()
        self.default_rw = float()
        self.default_rwt = float()

        #  either OWT, TWT, depth or elapsed time? (units always SI)
        self.z_measure_domain = str()
        self.description = str()
        #self.history = str()
        self.create_date = datetime.datetime.now()
        self.update_date = datetime.datetime.now()

        # 
        #      * Units for numeric fields, not in the persistence object-use to convert all to SI
        #      
        self.log_start_unit = str()
        self.log_step_unit = str()
        self.log_stop_unit = str()
        self.td_logger_unit = str()
        self.default_rw_unit = str()
        self.default_rwt_unit = str()
        self.run_number = int()

    