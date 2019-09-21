import sys
import logging
import unittest
import numpy as np
from qrutilities.numberutils import NumberUtils
from unittest.mock import Mock, patch
from inout.las.reader.orm.laspersister import LasPersister
from db.core.logdomain.logdomain import LogDomain
from inout.las.reader.lasreader import LasReader
from db.test.dummydbsetup import DummyDbSetup
from db.databasemanager import DM
from db.core.log.log import Log
from db.core.basedao import BaseDao
from db.core.logdomain.logdomaindao import LogDomainDao
from inout.las.reader.dialog.lasimportlogicmodel import LasImportLogicModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LasPersisterTest(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(LasPersisterTest, self).__init__(*args, **kwargs)
        self.dummyDbSetup = DummyDbSetup()


       
    
    @patch('sqlalchemy.orm.session.Session')
    def test_writeLogData(self, mock_class):
        logger.debug(">>test_writeLogData()")
        #self.dummyDbSetup = DummyDbSetup()
        self.dummyDbSetup.setupDatabase()
        
        session = DM.getSession()
        well = self.dummyDbSetup.createWell(session)
        logs = self.dummyDbSetup.create3Logs(well.id, session)
        data = BaseDao.convertJSONtoData(logs[0].log_data_str)
        logData = np.empty((len(logs), len(data)))
        for i, log in enumerate(logs):
            data = BaseDao.convertJSONtoData(log.log_data_str)
            for j, sample in enumerate(data):
                logData[i][j] = sample
            log.importLog = True
        dataTest = logData[1,:]

        lasPersister = LasPersister(session)
        lasReader = LasReader()
        lasReader.logList = logs
        lasReader._logs = logData
        
        lasPersister._logSetId = 1
        lasPersister._logServiceId = 1
        #TODO log domain needs to be created with dumy DB
        logDomain = LogDomainDao.getLogDomain(log.log_domain_id, session)
        lasPersister._logDomainId = logDomain.id
        lasReader.logDomain = logDomain
        
        lasPersister._lasReader = lasReader
        lasPersister._wellId = well.id
        lasPersister._lasModel = lasReader.lasModel
        lasRounding = 4
        lasPersister._lasImportLogicModel = LasImportLogicModel()
        lasPersister.writeLogData(lasPersister._lasModel, lasPersister._lasImportLogicModel, lasRounding)
        allLogs = session.query(Log).all()
        for log in allLogs:
            logger.debug("--test_writeLogData() post write log data id:{0}, name:{1}".format(log.id, log.name))
        session.close()
    

    @patch('sqlalchemy.orm.session.Session')
    def test_updateWellStartStop(self, mock_class):
        logger.debug(">>test_updateWellStartStop()")
        #self.dummyDbSetup = DummyDbSetup()
        self.dummyDbSetup.setupDatabase()
        
        session = DM.getSession()
        well = self.dummyDbSetup.createWell(session)
        logs = self.dummyDbSetup.create3Logs(well.id, session)
        data = BaseDao.convertJSONtoData(logs[0].log_data_str)
        logData = np.empty((len(logs), len(data)))
        domainId = 0
        for i, log in enumerate(logs):
            if i == 0:
                domainId = log.log_domain_id
            data = BaseDao.convertJSONtoData(log.log_data_str)
            for j, sample in enumerate(data):
                logData[i][j] = sample
            log.importLog = True
        dataTest = logData[1,:]

        lasPersister = LasPersister(session)
        lasReader = LasReader()
        lasReader.logList = logs
        lasReader._logs = logData
        
        lasPersister._logSetId = 1
        lasPersister._logServiceId = 1
        #TODO log domain needs to be created with dumy DB
        logDomain = LogDomainDao.getLogDomain( domainId, session)
        self.assertNotEqual(None, logDomain, "Sould not be None")
        lasPersister._logDomainId = logDomain.id
        lasReader.logDomain = logDomain
        logger.debug("well.mdstart:{0}, well.mdstop:{1}, logDomain.log_start:{2}, logDomain.log_stop:{3}".format(well.mdstart, well.mdstop, logDomain.log_start, logDomain.log_stop))
        
        lasPersister._lasReader = lasReader
        lasPersister._wellId = well.id
        lasPersister.writeLogData()
        allLogs = session.query(Log).all()
        for log in allLogs:
            logger.debug("--test_updateWellStartStop() post write log data id:{0}, name:{1}".format(log.id, log.name))
        session.close()

    @patch('sqlalchemy.orm.session.Session')
    def test_computeStepNp(self, mock_class):
        logger.debug(">>test_computeStepNp()")
        lasPersister = LasPersister(mock_class)
        data = []
        #constant = 0.1524
        for i in range(1000):
            if (i % 2 == 0):
                data.append(i-0.000001)
            else:
                data.append(i+0.000001)
        data.append(2.34)
        lasPersister.computeStepNp(data, 1.0, 4)
        logger.debug("consistent step: "+str(lasPersister._consistentStep))
        logger.debug("meanStepValue: "+str(lasPersister._meanStepValue))
        logger.debug("stepIndexes len: "+str(len(lasPersister._stepIndexes)))
        logger.debug("steps len: "+str(len(lasPersister._uniqueSteps)))
        
    @patch('sqlalchemy.orm.session.Session')
    def test_getRounding(self, mock_class):
        lasPersister = LasPersister(mock_class)
        rounding = lasPersister.getRounding(0.1524)
        logger.debug(" rounding: "+str(rounding))
        
    @patch('sqlalchemy.orm.session.Session')
    def test_calcSteppedDepth(self, mock_class):
        lasPersister = LasPersister(mock_class)
        data = []
        logDomain = LogDomain()
        logDomain.log_start = 1746.5088
        logDomain.log_stop = 2707.7904
        logDomain.log_step = 0.1524

        depth_data = lasPersister.calcSteppedDepth(logDomain,4, data_start=1746.8088, data_stop=2707.6904)
        
        self.assertEqual(6306, len(depth_data))
        #joinedStr = ', '.join(str(d) for d in depth_data)
        #logger.info(" joined depth data:"+joinedStr)

    @patch('sqlalchemy.orm.session.Session')
    def test_calcSteppedDepth1(self, mock_class):
        lasPersister = LasPersister(mock_class)
        data = []
        logDomain = LogDomain()
        logDomain.log_start = 1
        logDomain.log_stop = 10
        logDomain.log_step = 1

        depth_data = lasPersister.calcSteppedDepth(logDomain,4, data_start=1, data_stop=10)
        
        self.assertEqual(10, len(depth_data))
        joinedStr = ', '.join(str(d) for d in depth_data)
        logger.info(" joined depth data:"+joinedStr)
        
    '''
    deprecated 
    @patch('sqlalchemy.orm.session.Session')
    def test_computeStep(self, mock_class):
        lasPersister = LasPersister(mock_class)
        data = []
        #constant = 0.1524
        for i in range(1000):
            if (i % 2 == 0):
                data.append(i-0.000001)
            else:
                data.append(i+0.000001)
        data.append(2.34)
        lasPersister.computeStepNp(data, 1.0, 4)
        logger.debug("consistent step: "+str(lasPersister._consistentStep))
        logger.debug("meanStepValue: "+str(lasPersister._meanStepValue))
        logger.debug("stepIndexes len: "+str(len(lasPersister._stepIndexes)))
        logger.debug("steps len: "+str(len(lasPersister._uniqueSteps)))
        depthDiff=[]
        for i, item in enumerate(data):
                    if i>0:
                        depthDiff.append(item-data[i-1])
                    #NumberUtils.floatApproxEqual(data[0], item, tol=10e-4)
        depthDiffAry = np.asarray(depthDiff) 
        logger.debug("array equal: "+str(np.array_equal(depthDiffAry, lasPersister._npDepthDiff))) 
        for i, item in enumerate(lasPersister._npDepthDiff.tolist()): 
            logger.debug("!= i: "+str(i)+" py diff: "+str(depthDiff[i])+" np diff "+str(lasPersister._npDepthDiff[i])) 
            if item !=  lasPersister._npDepthDiff[i]:
                logger.debug("!= i: "+str(i)+" py diff: "+str(depthDiff[i])+" np diff "+str(lasPersister._npDepthDiff[i])) 
    '''