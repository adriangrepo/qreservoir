#!/usr/bin/env python
""" generated source for module LasReaderTest """
# package: com.qgs.qreservoir.io.las.reader


#import statics.project.TestSettings

#import io.las.reader.LasReader


#from inout.las.reader.dto.logservicedto import LogServiceDTO
#from inout.las.reader.dto.welldto import WellDTO
#from db.core.parameterset.parameterset import ParameterEntity
#from inout.las.reader.lasreader import LasReader
import os
import sys
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#  TODO see tests at bottom
class LasReaderTest(unittest.TestCase):
    """ generated source for class LasReaderTest """
    
    a1las = os.environ.get("A1LAS")
    wrappedPath = os.environ.get("WRAPPED_PATH")
    cWrappedFile = os.environ.get("CWRAPPEDFILE")
    e1las = os.environ.get("E1LAS")
    
    def _makeOne(self, clear=False):
        ''' ensures that the module is re-created each time '''
        if clear:
            try:
                del sys.modules['inout.las.reader.lasreader']
            except KeyError:
                pass
        from inout.las.reader.lasreader import LasReader
        return LasReader()
    '''    
    def test_readJobPart1(self):
        logger.debug("\n >>test_readJobPart1")
        reader = self._makeOne(clear=True)
        a1las = os.environ.get("A1LAS")
        part1OK = reader.readJobPart1(a1las)
    
        
    def test_readJobPart2(self):
        logger.debug("\n >>test_readJobPart2")
        reader = self._makeOne(clear=True)
        las = os.environ.get("A1LAS")
        ok = reader.readJobPart1(las)
        ok = reader.readJobPart2()
    '''    

    def test_logDomain(self):
        logger.debug("\n >>test_logDomain")
        reader = self._makeOne(clear=True)
        las = os.environ.get("A1LAS")
        ok = reader.readJobPart1(las)
        ok = reader.readJobPart2()
        ok = reader.readJobPart3()
        logDomain = reader.logDomain
        self.assertEquals(0.1524, logDomain.log_step)
        self.assertEquals(2707.6908, logDomain.log_stop)
        self.assertEquals(1746.6564, logDomain.log_start)
        
    def test_logDomain_1(self):
        logger.debug("\n >>test_logDomain_1")
        reader = self._makeOne(clear=True)
        ok = reader.readJobPart1(self.wrappedPath)
        ok = reader.readJobPart2()
        ok = reader.readJobPart3()
        logDomain = reader.logDomain
        self.assertEquals(-0.1250, logDomain.log_step)
        self.assertEquals(901.0, logDomain.log_stop)
        self.assertEquals(910.0, logDomain.log_start)
        
    def test_expectedNumberOfSamples11(self):
        reader = self._makeOne(clear=True)
        reader._stop = 10
        reader._start = 0
        reader._step = 1
        numSamples = reader.getExpectedNumberOfSamples
        self.assertEqual(11, numSamples)
        
    def test_expectedNumberOfSamples100(self):
        reader = self._makeOne(clear=True)
        reader._stop = 100
        reader._start = 1
        reader._step = 1
        numSamples = reader.getExpectedNumberOfSamples
        self.assertEqual(100, numSamples)
     
    '''    
    def test_well(self):
        logger.debug("\n >>test_wellDTO")
        reader = self._makeOne(clear=True)
        las = os.environ.get("A1LAS")
        ok = reader.readJobPart1(las)
        ok = reader.readJobPart2()
        ok = reader.readJobPart3()
        well = reader.well
        self.assertEquals("ANTELOPE-1", well.name)
    
    
    def test_well_wrapped(self):
        logger.debug(">>test_wellDTO_wrapped()");
        reader = self._makeOne(clear=True)

        reader.readJobPart1(self.cWrappedFile)
        reader.readJobPart2()
        reader.readJobPart3()
        well = reader.well
        self.assertEquals("C-1", well.name)
  
    def test_parameterDTO(self):
        logger.debug("\n >>test_parameterDTO")
        reader = self._makeOne(clear=True)
        las = os.environ.get("A1LAS")
        ok = reader.readJobPart1(las)
        ok = reader.readJobPart2()
        ok = reader.readJobPart3()
        parameterSet = reader.parameterSet
        #for item in parameterSet.parameter_list:
        #    logger.debug(str(item.mnemonic))
        self.assertEquals(77, len(parameterSet.parameter_list))
        
    
    def test_parseParameterInformationBlock(self):
            logger.debug("\n >>test_parseParameterInformationBlock")
            input = ["~Parameter Information Block","ELEVATIO.m  25.00000 : TLOG Constant - 4 - ELEVATION", "RMC .ohmm 0.08720 : TLOG Constant - 5 - RMC", "RM  .ohmm 0.06780 : TLOG Constant - 7 - RM"]
            reader = self._makeOne(clear=True)
            #should be empty
            paramListStart = reader.parameterSet.parameter_list
            logger.debug("--test_parseParameterInformationBlock() param set name: "+str(reader.parameterSet.name)+" len: "+str(len(paramListStart)))
            for item in paramListStart:
                logger.debug()
            self.assertEqual(0, len(paramListStart))
                
            reader.parseParameterInformationBlock(input, 0)
            paramList = reader.parameterSet.parameter_list
            
            self.assertEqual("RM", str(paramList[2].mnemonic), 'expected value {0} actual value {1}'.format("BLI", str(paramList[2].mnemonic)))
            self.assertEqual("ohmm", str(paramList[2].unit))
            self.assertEqual("0.06780", str(paramList[2].value))
            self.assertEqual("TLOG Constant - 7 - RM", str(paramList[2].description))
        
    def test_parseWrappedDataRecords(self):
        logger.debug("->>parseWrappedDataRecords() ");
        records = [None]*12
        records[0]="1862.1727"
        records[1]="-1.01 -999.25000 -999.25000 -999.25000 -10.02"
        records[2]="-2.01 -999.25000 -999.25000 -999.25000 -20.02"
        records[3]="-3.01 30.14080 -999.25000 -999.25000 -30.02"
        records[4]="-4.01 -999.25000 -999.25000 -999.25000 -40.02"
        records[5]="-5.01 -999.25000 -999.25000 -999.25000 -50.02"
        records[6]="-6.01 -999.25000 -999.25000 -999.25000 -60.02"
        records[7]="-7.01 -999.25000 -999.25000 -999.25000 -70.02"
        records[8]="-8.01 -999.25000 -999.25000 -999.25000 -80.02"
        records[9]="-9.01 -999.25000 -999.25000 -999.25000 -90.02"
        records[10]="-10.01 -999.25000 -999.25000 -999.25000 -100.02"
        records[11]="-11.01"
        
        reader = self._makeOne(clear=True)
        numTraces = 52
        firstDataRecord =0
        
        from inout.las.reader.lasreader import LasReader
        delimiter = LasReader.Delimiter.SPACE
        nullValue = -999.25
        result = reader.parseWrappedDataRecords(records, numTraces, firstDataRecord, delimiter, nullValue)
        self.assertEquals("1862.1727", (result[0])[0])
        self.assertEquals(1, len(result))
        self.assertEquals(52, len(result[0]))

    def test_parseDataRecordsByRegex(self):
        logger.debug(">>test_parseDataRecordsByRegex()");
        reader = self._makeOne(clear=True)
        record = "0.0000\t0.2125\t16564.1445"
        delimiter = "\t"
        numTraces = 3
        nullValue = -999.25
        result = reader.parseDataRecordsByRegex(record, numTraces, delimiter, nullValue)
        self.assertEquals("0.0000", result[0])
        self.assertEquals("0.2125", result[1])
        self.assertEquals("16564.1445", result[2])
        
    def test_parseDataRecordsByRegex0(self):
        logger.debug(">>test_parseDataRecordsByRegex()");
        reader = self._makeOne(clear=True)
        record = "0.0000,0.2125,16564.1445"
        delimiter = ","
        numTraces = 3
        nullValue = -999.25
        result = reader.parseDataRecordsByRegex(record, numTraces, delimiter, nullValue)
        self.assertEquals("0.0000", result[0])
        self.assertEquals("0.2125", result[1])
        self.assertEquals("16564.1445", result[2])


    def test_splitHeaderRecord(self):
        logger.debug(">>test_splitHeaderRecord()");
        reader = self._makeOne(clear=True)

        reader.readJobPart1(self.cWrappedFile)
        reader.readJobPart2()
        data = "STRT.M 1862.17273 :START DEPTH"
        output = reader.splitHeaderRecord(data)
        self.assertEquals("STRT", output[0])
        self.assertEquals("M", output[1])
        self.assertEquals("1862.17273", output[2])
        self.assertEquals("START DEPTH", output[3])

    def test_getMnemonicNames(self):
        logger.debug("\n >>test_getMnemonicNames")
        reader = self._makeOne(clear=True)

        ok = reader.readJobPart1(self.cWrappedFile)
        ok = reader.readJobPart2()
        names = reader.getMnemonicNames()
        self.assertEquals(52, len(names))

    def test_parameterMenmonicNames(self):
        logger.debug("\n >>test_parameterMenmonicNames")
        reader = self._makeOne(clear=True)

        ok = reader.readJobPart1(self.cWrappedFile)
        ok = reader.readJobPart2()
        names = reader.parameterMenmonicNames
        self.assertEquals(42, len(names))




        
    #TODO
    def test_parseRecordListArray(self):
        pass
    
    def test_parseOtherInformationBlock(self):
        pass
                
    def test_parseCurveInformationBlock(self):
        pass

    def test_parseUnitRecord(self):
        pass

    def test_convertType(self):
        pass

    def test_convertUnit(self):
        pass

    def test_parseParameterRecord(self):
        pass
   
    def test_parseLasData(self):
        pass

    def test_parseJobLasData(self):
        pass

    def test_parseJobRecordListArray(self):
        pass

    def test_parseNonWrappedDataRecords(self):
        pass
    
    def test_recordsValid(self):
        pass
    
    def test_isValidLasFile(self):
        pass
        
    def test_parseHeader(self):
        pass
        
    def test_parseVersionBlock(self):
        pass

    def test_parseWellInformationBlock(self):
        pass
            
    def test_setDTOunits(self):
        pass        
    '''