import logging
import unittest
from db.databasemanager import DM
from db.core.well.well import Well
from db.defaultsinitialiser import DefaultsInitialiser
from db.core.log.log import Log
from statics.types.logtype import LogType
from db.core.basedao import BaseDao
from db.windows.logcurvepreferences.logcurvepreferencedao import LogCurvePreferencesDao
from db.core.logdomain.logdomain import LogDomain
from db.core.well.welldao import WellDao
from qrutilities.timeutils import TimeUtils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('console')

class DummyDbSetup(object):
    
    def setupDatabase(self):
        ''' re-create database for each test method '''
        logger.debug(">>setupDatabase() ")
        DM.init_db()
        #need to create defaults as required by plotting - this hard codes all as default, TODO make it flexible
        defaultsInitialiser = DefaultsInitialiser()
        
    def create1Log(self, wellId, session = None):
        logger.debug(">>create3Logs() well id: "+str(wellId))
        localSession = False
        if session == None:
            session = DM.getSession()
            localSession = True
        
        log1 = Log()
        log1.name = "SWIRR"
        log1.log_type_name = LogType.SATURATION.name
        log1.z_measure_type_name = "MD"
        log1.z_measure_min = 0.0
        log1.z_measure_max = 2000.0
        log1.z_measure_step = 0.1524
        log1.log_data_str = BaseDao.convertDataToJSON([0.378425, 0.381605, 0.397528])
        log1.z_measure_data_str = BaseDao.convertDataToJSON([102, 103, 104])
        log1.well_id = wellId
        
        self.setPreferences( log1, session)
        session.add(log1)
        session.commit()
        dummyLog = session.query(Log).filter(Log.name == 'SWIRR').one()
        assert "SWIRR" == dummyLog.name
        assert wellId == dummyLog.well_id
        allLogs = session.query(Log).all()
        if localSession:
            session.close()
        return allLogs
    
    def create3Logs(self, wellId, session = None):
        logger.debug(">>create3Logs() well id: "+str(wellId))
        localSession = False
        if session == None:
            session = DM.getSession()
            localSession = True
        
        logDomain = LogDomain()
        logDomain.z_measure_type_name = "MD"

        logDomain.log_start = 0.0
        logDomain.log_step = 0.1524
        logDomain.log_stop = 1000.0
        
        session.add(logDomain)
        session.flush()
        logDomainId = logDomain.id
        
        log1 = Log()
        log1.name = "LWD_GR"
        log1.log_type_name = LogType.GAMMA.name
        log1.z_measure_type_name = "MD"
        log1.z_measure_min = 0.0
        log1.z_measure_max = 1000.0
        log1.z_measure_step = 0.1524
        log1.log_data_str = BaseDao.convertDataToJSON([0.378425, 0.381605, 0.397528])
        log1.z_measure_data_str = BaseDao.convertDataToJSON([102, 103, 104])
        #log1.rgb="100,100,100"
        #log1.alpha="255"
        #log1.log_plot_points_on = False
        log1.well_id = wellId
        log1.log_domain_id = logDomainId
        
        log2 = Log()
        log2.name = "2DT"
        log2.log_type_name = LogType.DT.name
        log2.z_measure_type_name = "MD"
        log2.z_measure_min = 0.0
        log2.z_measure_max = 1000.0
        log2.z_measure_step = 0.1524
        log2.log_data_str = BaseDao.convertDataToJSON([0.378425, 0.381605, 0.397528])
        log2.z_measure_data_str = BaseDao.convertDataToJSON([102, 103, 104])
        #log2.rgb="100,100,100"
        #log2.alpha="255"
        #log2.log_plot_points_on = False
        log2.well_id = wellId
        log2.log_domain_id = logDomainId
        
        log3 = Log()
        log3.name = "3SP"
        log3.log_type_name = LogType.SP.name
        log3.z_measure_type_name = "MD"
        log3.z_measure_min = 0.0
        log3.z_measure_max = 1000.0
        log3.z_measure_step = 0.1524
        log3.log_data_str = BaseDao.convertDataToJSON([0.378425, 0.381605, 0.397528])
        log3.z_measure_data_str = BaseDao.convertDataToJSON([102, 103, 104])
        #log3.rgb="100,100,100"
        #log3.alpha="255"
        #log3.log_plot_points_on = False
        log3.well_id = wellId
        log3.log_domain_id = logDomainId
        
        self.setPreferences(log1, session)
        self.setPreferences(log2, session)
        self.setPreferences(log3, session)
        
        
        session.add(log1)
        session.add(log2)
        session.add(log3)
        session.commit()
        dummyLog = session.query(Log).filter(Log.name == 'LWD_GR').one()
        assert "LWD_GR" == dummyLog.name
        assert wellId == dummyLog.well_id
        allLogs = session.query(Log).all()
        if localSession:
            session.close()
        return allLogs
    
    def create3VariableDepthLogs(self, wellId, session = None):
        logger.debug(">>create3Logs() well id: "+str(wellId))
        localSession = False
        if session == None:
            session = DM.getSession()
            localSession = True
        
        log1 = Log()
        log1.name = "LWD_GR"
        log1.log_type_name = LogType.GAMMA.name
        log1.z_measure_type_name = "MD"
        log1.z_measure_min = 200.0
        log1.z_measure_max = 1000.0
        log1.z_measure_step = 1
        
        log1.log_data_str = BaseDao.convertDataToJSON([0.378425, 0.381605, 0.397528])
        log1.z_measure_data_str = BaseDao.convertDataToJSON([102, 103, 104])
        #log1.rgb="100,100,100"
        #log1.alpha="255"
        #log1.log_plot_points_on = False
        log1.well_id = wellId
        
        log2 = Log()
        log2.name = "2DT"
        log2.log_type_name = LogType.DT.name
        log2.z_measure_type_name = "MD"
        log2.z_measure_min = 0.0
        log2.z_measure_max = 2000.0
        log2.z_measure_step = 1
        log2.log_data_str = BaseDao.convertDataToJSON([0.378425, 0.381605, 0.397528])
        log2.z_measure_data_str = BaseDao.convertDataToJSON([102, 103, 104])
        #log2.rgb="100,100,100"
        #log2.alpha="255"
        #log2.log_plot_points_on = False
        log2.well_id = wellId
        
        log3 = Log()
        log3.name = "3SP"
        log3.log_type_name = LogType.SP.name
        log3.z_measure_type_name = "MD"
        log3.z_measure_min = 500.0
        log3.z_measure_max = 2500.1
        log3.z_measure_step = 1
        log3.log_data_str = BaseDao.convertDataToJSON([0.378425, 0.381605, 0.397528])
        log3.z_measure_data_str = BaseDao.convertDataToJSON([102, 103, 104])
        #log3.rgb="100,100,100"
        #log3.alpha="255"
        #log3.log_plot_points_on = False
        log3.well_id = wellId
        
        self.setPreferences(log1, session)
        self.setPreferences(log2, session)
        self.setPreferences(log3, session)
        
        session.add(log1)
        session.add(log2)
        session.add(log3)
        session.commit()
        dummyLog = session.query(Log).filter(Log.name == 'LWD_GR').one()
        assert "LWD_GR" == dummyLog.name
        assert wellId == dummyLog.well_id
        allLogs = session.query(Log).all()
        if localSession:
            session.close()
        return allLogs
    
    def setPreferences(self, log, session = None):
        localSession = False
        if session == None:
            session = DM.getSession()
            localSession = True
        logType = LogType.getLogType(log.log_type_name)
        log_type_uid = logType.getUid()
        logCurveDefaults = LogCurvePreferencesDao.getLogCurvePreferences(log_type_uid, session)
        if logCurveDefaults == None:
            #no preferences set yet, use defaults
            logCurveDefaults = LogCurvePreferencesDao.getLogCurveDefaults(log_type_uid, session)
        assert logCurveDefaults is not None
        log.log_plot_left = logCurveDefaults.log_plot_left
        log.log_plot_right = logCurveDefaults.log_plot_right
        log.log_plot_default = logCurveDefaults.log_plot_default
        log.log_plot_points_on = logCurveDefaults.log_plot_points_on
        
        log.histogram_left = logCurveDefaults.histogram_left
        log.histogram_right = logCurveDefaults.histogram_right
        log.histogram_default = logCurveDefaults.histogram_default
        
        log.cross_plot_left = logCurveDefaults.cross_plot_left
        log.cross_plot_right = logCurveDefaults.cross_plot_right
        log.cross_plot_default = logCurveDefaults.cross_plot_default

        log.line_width = logCurveDefaults.line_width
        log.line_style = logCurveDefaults.line_style
        
        log.point_size = logCurveDefaults.point_size
        log.point_style = logCurveDefaults.point_style
        
        log.rgb = logCurveDefaults.rgb
        log.alpha = logCurveDefaults.alpha
        
        log.is_logarithmic = logCurveDefaults.is_logarithmic
        if logCurveDefaults.is_logarithmic:
            log.log_plot_log_cycles = logCurveDefaults.log_plot_log_cycles

        log.z_measure_type_name = "MD"
        #duplication - but makes simpler if want to change log down track
        log.z_measure_reference = "KB"
        if localSession:
            session.close()
    
    def createWell(self, session = None):
        logger.debug(">>createWell() ")
        localSession = False
        if session == None:
            session = DM.getSession()
            localSession = True
        wells = WellDao.getAllWells(session)
        if len(wells) > 0:
            for well in wells:
                logger.debug("existing wells:{0}".format(well.name))
        assert 0 == len(wells)
        #timeStamp = TimeUtils.getTimeInMilliSecs()
        well = Well()
        well.name = "test_well"
        well.depth_reference = "MDKB"
        well.elevation_of_depth_reference = "24.0"
        session.add(well)
        session.commit()
        dummyWell = session.query(Well).filter(Well.name == 'test_well').one()
        assert "test_well" == dummyWell.name
        if localSession:
            session.close()
        return dummyWell