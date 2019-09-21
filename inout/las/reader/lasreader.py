#!/usr/bin/env python

import os
import numpy

#import os.access
#import os.R_OK
import logging
import unittest
import re
from itertools import islice

#from inout.las.reader.dto.list.parameter import Parameter
#from inout.las.reader.dto.parameterdto import ParameterDTO
#from db.core.parameter.parameter import Parameter
from db.core.parameterset.parameterset import ParameterSet
#from db.model.dto.parameterlist import ParameterList
from db.core.well.well import Well
from db.core.logservice.logservice import LogService
from db.core.logdomain.logdomain import LogDomain
from db.core.logset.logset import LogSet

from db.core.log.log import Log
from db.core.parameter.parameter import Parameter
from qrutilities.numberutils import NumberUtils
from inout.las.reader.dto.domainunitsetter import DomainUnitSetter
from statics.types.logtype import LogType
from statics.types.logunitstype import LogUnitsType
from qrutilities.namingutils import NamingUtils
from qrutilities.arrayutils import ArrayUtils
from qrutilities.stringutils import StringUtils
from globalvalues.constants.inputdataconstants import InputDataConstants
#from inout.las.reader.dto.list.logList import LogListDTO
# 
#  * Reads LAS-formatted files containing wells and log curves. double values such
#  * as KB, step are checked for validity and stored as double
#  

logger = logging.getLogger('console')



class LasReader(object):
    """ generated source for class LasReader """
    # 
    #      * Enumeration of the available delimiters that specify how the data records
    #      * are separated in an LAS file.
    #      
    class Delimiter:
        """ generated source for enum Delimiter """
        SPACE = u'SPACE'
        COMMA = u'COMMA'
        TAB = u'TAB'
        INVALID = u'INVALID'
        UNSPECIFIED = u'UNSPECIFIED'

    #  Column of the "Mnemonic" in the header. 
    MNEM = 0
    #  Column of the "Unit" in the header. 
    UNIT = 1
    #  Column of the "Value" in the header. 
    VALUE = 2
    #  Column of the "Description" in the header. 
    DESC = 3
    #  Column of the for "Format" in the header. 
    FORMAT = 4
    #  Column of the "Association" in the header. 
    ASSOC = 5
    #  Default null if file null value id not a double 
    NULL_VALUE = -999.25



    def __init__(self):
        """ generated source for method __init__ """
        #  use this for job process update
        #  could break into more parts is requred
        self.part1_completed = False
        self.part2_completed = False
        self.part3_completed = False
    
        #  mandatory
        self._VersionBlockInFile = bool()
        self._WellInformationBlockInFile = bool()
        self._CurveInformationBlockInFile = bool()
    
        #  optional
        self._ParameterInformationBlockInFile = bool()
        self._OtherInformationBlockInFile = bool()
        self._dataBlockInFile = bool()
        self._containsData = bool()
        
        self.null_value = self.NULL_VALUE
        
        #  Default to assuming the data is space delimited. 
        self._delimiter = self.Delimiter.SPACE
        self._versionOfLAS = ""
    
        #  If true each measurement is on multiple lines in the file. 
        self._wrapped = False
    
        #  double values 
        #  The raw log data.
        #ndarray 
        self._logs = []
    
        #  Start/stop/step depth of log records. 
        self._start = 0.0
        self._stop = 0.0
        self._step = 0.0
        #actual data start and stop
        self._data_start = 0.0
        self._data_stop = 0.0
    
        #  Strings 
        #  The description of the curve units of the logs in the LAS file. 
        self._unitMap = {}
    
        #  The comments for each of the logs. 
        self._commentsMap = {}
    
        #  The parameter name and units 
        self._parameterUnitMap = {}
    
        #  The values (as string) of the parameters. 
        self._parameterValueMap = {}
    
        #  The description of the parameters. 
        self._parameterDescriptionMap = {}
        self._wellDepthUnits = ""
        
        self.fullFilePathName = ""
        self.validatedRecords = []
        self.jobData = []
    
        #  store depths in an array to be used for calculating step later
        self._depthData = []
        
        self.logList = []
        self.parameterSet = ParameterSet()
        self.parameterList = []
        self.logService = LogService()
        self.logDomain = LogDomain()
        self.well = Well()
        #not used by reader but stored here for convenience
        self.logSet = LogSet()
   
    def readJobPart1(self, filePathName):
        """ checks header for file path string"""

        assert isinstance(filePathName, str)
        
        if os.access(filePathName, os.R_OK):
            self.fullFilePathName = filePathName
            logger.debug("LasReader() file name: " + self.fullFilePathName)
            try:
                tf = open(filePathName, 'r')
                if self.recordsValid(tf):
                    assert len(self.validatedRecords)
                    #  Parse the header records.
                    self.parseHeader(self.validatedRecords)
                    if self.isValidLasFile():
                        self.part1_completed = True
                    else:
                        logger.error("File " + filePathName + " is not a valid las file")
                        return False
                else:
                    logger.error("File " + filePathName + " contains no readable data")
                    return False
            except IOError:
                logger.error("Cannot open the file: " + filePathName)
            finally:
                tf.close()
                
        else:
            #  TODO Alpha B show message dialog with error
            logger.error("Cannot open the file: " + filePathName)
            return False
        return True

    def readJobPart2(self):
        """ generated source for method readJobPart2 """
        if self.part1_completed == True:
            assert len(self.validatedRecords)
            self.parseJobLasData(self.validatedRecords)
            self.part2_completed = True
            return True
        return False

    def readJobPart3(self):
        """ generated source for method readJobPart3 """
        if self.part2_completed == True:
            if self.parseJobRecordListArray():
                self.part3_completed = True
                return True
            logger.info("File contains no log data")
        return False

    def recordsValid(self, recordList):
        """ checks each record in list is not empty """
        validRecords = []
        #  Validate and store each of the records that are
        #  greater than zero in length.
        for record in recordList:
            if len(record.strip()) > 0:
                validRecords.append(record.strip())
        self.validatedRecords = list(validRecords)
        validRecords = None
        if len(self.validatedRecords):
            return True
        return False

    def isValidLasFile(self):
        """ Valid Las File must contain version block, well info block and curve info block"""
        validLasFile = self._VersionBlockInFile and self._WellInformationBlockInFile and self._CurveInformationBlockInFile
        if validLasFile:
            return True
        return False

    # 
    #      * Loads the contents of an LAS file that has been parsed into a collection
    #      * of strings.
    #      * 
    #      * @param recordList
    #      *            the collection of records.
    #      
    def load(self, recordList):
        """ adds each record to a list if record contains anything """
        validRecords = []
        #  Validate and store each of the records that are
        #  greater than zero in length.
        for record in recordList:
            if len(record.strip) > 0:
                validRecords.append(record.strip())
        records = validRecords
        validRecords = None
        #  Parse the header records.
        self.parseHeader(records)
        #  Parse the data records.
        self.parseLasData(records)

    # 
    #      * Parse the header records.
    #      
    def parseHeader(self, records):
        """ generated source for method parseHeader """
        logger.debug(">>parseHeader() records: "+str(len(records)))
        #  Loop thru each of the records.
        #for i in range(len(records)):
        #    logger.debug(str(records[i]))

        for i in range(len(records)):
            if records[i].startswith("~V"):
                logger.debug("~V "+str(records[i]))
                self.parseVersionBlock(records, i)
                self._VersionBlockInFile = True
            elif records[i].startswith("~W"):
                logger.debug("~W "+str(records[i]))
                self.parseWellInformationBlock(records, i)
                self._WellInformationBlockInFile = True
            elif records[i].startswith("~C"):
                logger.debug("~C "+str(records[i]))
                self.parseCurveInformationBlock(records, i)
                self._CurveInformationBlockInFile = True
            elif records[i].startswith("~P"):
                logger.debug("~P "+str(records[i]))
                self.parseParameterInformationBlock(records, i)
                self._ParameterInformationBlockInFile = True
                continue 
            elif records[i].startswith("~O"):
                logger.debug("~O "+str(records[i]))
                self.parseOtherInformationBlock(records, i)
                self._OtherInformationBlockInFile = True
                continue 
            elif records[i].startswith("~A"):
                logger.debug("~A "+str(records[i]))
                self._dataBlockInFile = True
                break


    def parseVersionBlock(self, records, start):
        """ generated source for method parseVersionBlock """
        logger.debug(">>parseVersionBlock()")
        index = start+1
        tempIndex = index
        tempIndex += 1
        if tempIndex < len(records):
            inBounds = True
        if inBounds:
            
            while not records[index].startswith("~"):
                if not records[index].startswith("#"):
                    data = self.splitHeaderRecord(records[index]);
                    
                    if data[self.MNEM].lower() == "VERS".lower():
                        self._versionOfLAS = data[self.VALUE]
                    elif data[self.MNEM].lower() == "WRAP".lower():
                        if data[self.VALUE].lower() == "YES".lower():
                            self._wrapped = True
                        else:
                            self._wrapped = False
                    elif data[self.MNEM] == "DLM":
                        if data[self.VALUE].lower() == "COMMA".lower():
                            self._delimiter = self.Delimiter.COMMA
                        elif data[self.VALUE].lower() == "TAB".lower():
                            self._delimiter = self.Delimiter.TAB
                        elif data[self.VALUE].lower() == "SPACE".lower():
                            self._delimiter = self.Delimiter.SPACE
                        else:
                            self._delimiter = self.Delimiter.INVALID
                index += 1
        else:
            logger.error("Version block invalid")

    def parseWellInformationBlock(self, records, startIndex):
        """ generated source for method parseWellInformationBlock """
        logger.debug(">>parseWellInformationBlock()")
        index = startIndex + 1
        recordRaw = ""
        index += 1
        while not recordRaw.startswith("~"):
            tempIndex = index
            tempIndex += 1
            if tempIndex < len(records):
                inBounds = True
            if inBounds:
                index += 1
                recordRaw = records[index]
                #Note that the test below is not needed in Java
                if recordRaw.startswith("~"):
                    break
                if not recordRaw.startswith("#"):
                    cols = self.splitHeaderRecord(recordRaw)
                    value = cols[self.VALUE].strip();
                    unit = cols[self.UNIT].strip();
                    description = cols[self.DESC].strip();
                    record = recordRaw;
                    
                    #stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
                    #regex remove non alphanumeric
                    recordList = re.findall(r"\w+",record) 
                    if recordList:
                        record = recordList[0]
                    if record == "STRT":       
                        self._start = self.stripAndRoundToDouble(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.logDomain.log_start = self._start
                        self.logDomain.log_start_unit = unit
                    elif record == "STOP":
                        self._stop = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.logDomain.log_stop = self._stop
                        self.logDomain.log_step_unit = unit
                    elif record == "STEP":
                        self._step = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.logDomain.log_step = self._step
                        self.logDomain.log_step_unit = unit
                    elif record == "NULL":
                        try:
                            nullInFile = float(value)
                        except ValueError:
                            nullInFile = self.null_value
                        self.logService.null_value = nullInFile
                    elif record == "SRVC":
                        self.logService.service_company = value
                    elif record == "DATE":
                        self.logService.service_date = value
                    elif record == "LGMEA":
                        self.logService.z_measure_reference = value
                    elif record == "LMF":
                        self.logService.z_measure_reference = value
                    elif record == "TDL":
                        self.logService.td_logger = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.logService.td_logger_unit = unit
                    elif record == "RWS":
                        self.logService.default_rw = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.logService.default_rw_unit = unit
                    elif record == "WST":
                        self.logService.default_rwt = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.logService.default_rwt_unit = unit
                    elif record == "RUN":
                        self.logService.run_number = NumberUtils.stringToInt(value)
                    elif record == "LOCA":
                        self.logService.analysis_location = value
                    elif record == "PET":
                        self.logService.analysis_by = value
                    elif record == "DFLD":
                        self.logService.type_of_fluid_in_hole = value
                    elif record == "WELL":
                        self.well.name = value
                    elif record == "COMP":
                        self.well.company = value
                    elif record == "OPER":
                        self.well.operator = value
                    elif record == "FLD":
                        self.well.field = value
                    elif record == "LOC":
                        self.well.location = value
                    elif record == "CTRY":
                        self.well.country = value
                    elif record == "AREA":
                        self.well.area = value
                    elif record == "BLCK":
                        self.well.block = value
                    elif record == "SPUD":
                        self.well.spud_date = value
                    elif record == "TDAT":
                        self.well.td_date = value
                    elif record == "CMPL":
                        self.well.completion_status = value
                    elif record == "RIG":
                        self.well.rig_name = value
                    elif record == "DRLC":
                        self.well.drilling_contractor = value
                    elif record == "GDAT":
                        self.well.geodetic_datum = value
                    elif record == "ZONE":
                        self.well.utm_zone = value
                    elif record == "UNIT":
                        self.well.file_depth_units = value
                        self._wellDepthUnits = value
                    elif record == "PDAT":
                        self.well.permanent_datum = value
                    elif record == "HZCS":
                        self.well.horizontal_coordinate_system = value
                    elif record == "DREF":
                        self.well.depth_reference = value
                        self.logService.z_measure_reference = value
                    elif record == "DRMEA":
                        self.well.drilling_reference = value
                    elif record == "DMF":
                        self.well.drilling_reference = value
                    elif record == "STAT":
                        self.well.state = value
                    elif record == "CNTY":
                        self.well.county = value
                    elif record == "API":
                        self.well.well_api = value
                    elif record == "PROV":
                        self.well.province = value
                    elif record == "LIC":
                        self.well.license = value
                    elif record == "UWI":
                        self.well.well_uwi = value
                    elif record == "UTMZ":
                        self.well.utm_zone = value
                    elif record == "LATI":
                        self.well.latitude = value
                    elif record == "LAT":
                        self.well.latitude = value
                    elif record == "LONG":
                        self.well.longitude = value
                    elif record == "X":
                        self.well.x_coordinate = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.GEOGRAPHIC_SIGNIFICANT_PLACES)
                    elif record == "Y":
                        self.well.y_coordinate = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.GEOGRAPHIC_SIGNIFICANT_PLACES)
                    elif record == "EPDAT":
                        self.well.permanent_datum_elevation = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.permanent_datum_elevation_unit = unit
                    elif record == "EREF":
                        self.well.elevation_of_depth_reference = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.elevation_of_depth_reference_unit = unit
                    elif record == "APDAT":
                        self.well.elevation_above_permanent_datum = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.elevation_above_permanent_datum_unit = unit
                    elif record == "EKB":
                        self.well.kb_elevation = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.kb_elevation_unit = unit
                    elif record == "KB":
                        self.well.kb_elevation = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.kb_elevation_unit = unit
                    elif record == "EDF":
                        self.well.df_elevation = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.df_elevation_unit = unit
                    elif record == "DF":
                        self.well.df_elevation = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.df_elevation_unit = unit
                    elif record == "EGL":
                        self.well.gl_elevation = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.gl_elevation_unit = unit
                    elif record == "GL":
                        self.well.gl_elevation = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.gl_elevation_unit = unit
                    elif record == "WTRD":
                        self.well.water_depth = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.water_depth_unit = unit
                    elif record == "TDD":
                        self.well.td_driller = NumberUtils.parseStringToRoundedFloat(value, InputDataConstants.Z_DOMAIN_SIGNIFICANT_PLACES)
                        self.well.td_driller_unit = unit
            else:
                logger.error("Invalid information block")
                break
        self.setDTOunits()

    def setDTOunits(self):
        """ generated source for method setDTOunits """
        
        dus = DomainUnitSetter()
        logType = LogType
        depthUnitMatch = dus.findDepthUnitsMatch(str(self.well.file_depth_units), logType.DEPTH)
        if not depthUnitMatch:
            dus.populateWellDepthUnits(self.well, self.logDomain)
        

    def parseParameterInformationBlock(self, records, startIndex):
        """ generated source for method parseParameterInformationBlock """
        logger.debug(">>parseParameterInformationBlock()")
        if startIndex >= len(records):
            logger.info("Parameter information block is empty")
            return
        for item in islice(records, startIndex+1, None):
            #logger.debug("--parseParameterInformationBlock() "+str(item))
            if item.startswith("~"):
                break
            if not item.startswith("#"):
                self.parseParameterRecord(item)


    def parseOtherInformationBlock(self, records, startIndex):
        """ generated source for method parseParameterInformationBlock """
        logger.debug(">>parseOtherInformationBlock()")
        record = ""
        mnemonicName = ""
        value = ""
        unit = ""
        cols = []
        if startIndex >= len(records):
            logger.info("Other information block is empty")
            return
        for item in islice(records, startIndex+1, None):
            if item.startswith("~"):
                break
            if not item.startswith("#"):
                cols = self.splitHeaderRecord(record)
                mnemonicName = cols[self.MNEM].strip()
                value = cols[self.VALUE].strip()
                unit = cols[self.UNIT].strip()
                
    def parseCurveInformationBlock(self, records, startIndex):
        """ generated source for method parseCurveInformationBlock """
        logger.debug(">>parseCurveInformationBlock()")
        if startIndex >= len(records):
            logger.info("Curve information block is empty")
            return
        #eg islice('ABCDEFG', 2, None) --> C D E F G
        for item in islice(records, startIndex+1, None):
            if item.startswith("~"):
                break
            if not item.startswith("#"):
                #logger.debug("record: "+str(item))
                self.parseUnitRecord(item)

    def parseUnitRecord(self, record):
        """ generated source for method parseUnitRecord """
        data = self.splitHeaderRecord(record)
        mnem = NamingUtils.createUniqueMnemonic(data[self.MNEM].strip(), self._unitMap)
        
        logItem = Log()
        logItem.fileMnemonic = mnem
        logItem.name = mnem
        logItem.type = self.convertType(mnem)
        logItem.fileUnit = data[self.UNIT].strip()
        logItem.unit = self.convertUnit(data[self.UNIT].strip())
        logItem.fileDescription = data[self.DESC].strip()
        
        
        self._unitMap[mnem] = data[self.UNIT].strip()
        #logger.debug("--parseUnitRecord() mnem: "+str(mnem)+" _unitMap[mnem]: "+str(self._unitMap[mnem]))
        self._commentsMap[mnem] = data[self.DESC].strip()
        self.logList.append(logItem)

    def convertType(self, fileMnemonic):
        """ generated source for method convertType """
        type_ = LogType.findLogTypeFromMnemonic(fileMnemonic).__str__()
        return type_

    def convertUnit(self, fileUnit):
        """ generated source for method convertUnit """
        logUnitsType = LogUnitsType.getLogUnitsType(fileUnit)
        return logUnitsType.__str__()

    def parseParameterRecord(self, record):
        """ generated source for method parseParameterRecord """
        #logger.debug(">>parseParameterRecord()")
        data = self.splitHeaderRecord(record)
        parameter = Parameter()
        mnem = NamingUtils.createUniqueMnemonic(data[self.MNEM].strip(), self._parameterUnitMap)
        parameter.mnemonic = mnem
        self._parameterUnitMap[mnem] = data[self.UNIT].strip()
        parameter.unit = data[self.UNIT].strip()
        self._parameterValueMap[mnem] = data[self.VALUE].strip()
        parameter.value = data[self.VALUE].strip()
        self._parameterDescriptionMap[mnem] = data[self.DESC].strip()
        parameter.description = data[self.DESC].strip()
        self.parameterList.append(parameter)

    #for createUniqueMnemonic see namingUtils

        
    def parseLasData(self, records):
        """ generated source for method parseLasData """
        data = None
        mnems = self.getMnemonicNames()
        if self._wrapped:
            for i in range(len(records)):
                if records[i].startswith("~A"):
                    data = self.parseWrappedDataRecords(records, len(mnems), i + 1, self._delimiter, self.null_value)
                    break
        else:
            for i in range(len(records)):
                if records[i].startswith("~A"):
                    data = self.parseNonWrappedDataRecords(records, len(mnems), i + 1, self._delimiter, self.null_value)
        if data != None and not data.isEmpty():
            self._containsData = True  
            self._logs = self.parseRecordListArray(data, len(mnems))
            depth_data = self._logs[0,:]
            self._data_start = depth_data[0]
            self._data_stop = depth_data[len(depth_data)-1]

    def parseJobLasData(self, records):
        """ generated source for method parseJobLasData """
        self.jobData = None
        mnems = self.getMnemonicNames()
        if self._wrapped:
            for i in range(len(records)):
                if records[i].startswith("~A"):
                    self.jobData = self.parseWrappedDataRecords(records, len(mnems), i + 1, self._delimiter, self.null_value )
                    break
                
        else:
            for i in range(len(records)):
                if records[i].startswith("~A"):
                    self.jobData = self.parseNonWrappedDataRecords(records, len(mnems), i + 1, self._delimiter, self.null_value )


    def parseJobRecordListArray(self):
        """ generated source for method parseJobRecordListArray """
        if self.jobData:
            self._containsData = True
            logger.debug("--parseJobRecordListArray() len mnem names: "+str(len(self.getMnemonicNames())))
            for item in self.getMnemonicNames():
                logger.debug(str(item))
            self._logs = self.parseRecordListArray(self.jobData, len(self.getMnemonicNames()))
            return True
        return False

    def parseNonWrappedDataRecords(self, records, numTraces, firstDataRecord, delimiter, nullValue):
        """ generated source for method parseNonWrappedDataRecords """
        list_ = []
        data = None
        i = firstDataRecord
        for item in islice(records, firstDataRecord, None):
            if delimiter == self.Delimiter.SPACE or delimiter == self.Delimiter.UNSPECIFIED or delimiter == self.Delimiter.INVALID:
                data = self.parseDataRecordsBySpaces(records[i])
            elif delimiter == self.Delimiter.TAB:
                data = self.parseDataRecordsByRegex(records[i], numTraces, "\\t", nullValue)
            elif delimiter == self.Delimiter.COMMA:
                data = self.parseDataRecordsByRegex(records[i], numTraces, ",", nullValue)
            list_.append(data)
            i += 1
        return list_

    def parseRecordListArray(self, data, numTraces):
        """ generated source for method parseRecordListArray """
        assert data != None
        logs = numpy.empty((numTraces, len(data)))
        logger.debug("--parseRecordListArray() created "+str(numTraces)+" by "+str(len(data))+" matrix ")
        logger.debug("--parseRecordListArray() numTraces: "+str(numTraces)+" len(data): "+str(len(data)))
        self._depthData = [None]*len(data)
        numberOfNonNumerics = 0

        for i in range(len(data)):
            record = data[i]
            for col in range(numTraces):
                #logger.debug("col: "+str(col)+" record: "+str(record[col])+" len record: "+str(len(record)))
                if col >= len(record):
                    logger.error("--parseRecordListArray() loop iterator length is invalid columns: "+str(col)+" records: "+str(len(record)))
                    assert col < len(record)
                    
                if NumberUtils.isaNumber(record[col]):
                    value = float(record[col])
                    #logger.debug(" col: "+str(col)+" i: "+str(i))
                    logs[col][i] = value
                else:
                    logs[col][i] = LasReader.NULL_VALUE
                    numberOfNonNumerics += 1
                if 0 == col:
                    self._depthData[i] = logs[col][i]
        if numberOfNonNumerics > 0:
            logger.warn(numberOfNonNumerics + " non numeric data values were detected and have been converted to null values")
        return logs
    
    def parseWrappedDataRecords(self, records, numTraces, firstDataRecord, delimiter, nullValue):
        #result = numpy.empty((numTraces, len(data)))
        #strings = []
        result = []
        #List<String[]> result = new ArrayList<String[]>();
        i = firstDataRecord;

        while (i < len(records)):
            record = [numTraces]

            #record[0] given records[i] value then i is increased
            record[0] = records[i].strip()
            i += 1
            data = []

            col = 1
            while col < numTraces:
                if (delimiter == self.Delimiter.SPACE or delimiter == self.Delimiter.UNSPECIFIED
                        or delimiter == self.Delimiter.INVALID):
                    data = self.parseDataRecordsBySpaces(records[i])
                elif (delimiter == self.Delimiter.TAB):
                    data = self.parseDataRecordsByRegex(records[i], numTraces, "\t", nullValue)
                elif (delimiter == self.Delimiter.COMMA):
                    data = self.parseDataRecordsByRegex(records[i], numTraces, ",", nullValue)
                else:
                    logger.error("No delimiter found in file.")
                    logData = ""
                i += 1

                ArrayUtils.arraycopy(data, 0, record, col, len(data))
                col += len(data)
            result.append(record)
        return result
    


    
    '''
    def parseWrappedDataRecords(self, records, numTraces, firstDataRecord, delimiter, nullValue):
        # turns wrapped data into a list 
        result = []
        if numTraces>0:
            firstItem = True
            for value in records[firstDataRecord:firstDataRecord+numTraces]:
                data = []
                logData = []
                data.append(value.strip())
                col = 1
                while col < numTraces:
                    if delimiter == self.Delimiter.SPACE or delimiter == self.Delimiter.UNSPECIFIED or delimiter == self.Delimiter.INVALID:
                        logData = self.parseDataRecordsBySpaces(value)
                    elif delimiter == self.Delimiter.TAB:
                        logData = self.parseDataRecordsByRegex(value, len(value), "\\t", nullValue)
                    elif delimiter == self.Delimiter.COMMA:
                        logData = self.parseDataRecordsByRegex(value, len(value), ",", nullValue)
                    else:
                        logger.error("No delimiter found in file.")
                        logData = ""
                    
                    for item in logData:
                        data.append(item)
                    col += data.length

                result.append(data)
        return result
    '''
    
    '''
    def parseWrappedDataRecords(self, records, numTraces, firstDataRecord, delimiter, nullValue):
        """ generated source for method parseWrappedDataRecords """
        result = []
        i = firstDataRecord
        record = [None]*numTraces
        logger.debug("--parseWrappedDataRecords() inital record length: "+str(len(record)))
        data = []
        while i < len(records):
            record[0] = str(records[i]).strip()
            i += 1      #I suspect this should be 
            col = 1
            while col < numTraces:
                if i < len(records):
                    #logger.debug("--parseWrappedDataRecords() i: "+str(i)+" col: "+str(col)+" len rec: "+str(len(records)))
                    if delimiter == self.Delimiter.SPACE or delimiter == self.Delimiter.UNSPECIFIED or delimiter == self.Delimiter.INVALID:
                        data = self.parseDataRecordsBySpaces(records[i], numTraces)
                        i += 1
                    elif delimiter == self.Delimiter.TAB:
                        data = self.parseDataRecordsByRegex(records[i], numTraces, "\\t", nullValue)
                        i += 1
                    elif delimiter == self.Delimiter.COMMA:
                        data = self.parseDataRecordsByRegex(records[i], numTraces, ",", nullValue)
                        i += 1
                    else:
                        logger.error("No delimiter found in file.")
                        return None
                    record[col:len(data)] = data[0:len(data)]
                    logger.debug("--parseWrappedDataRecords() record length: "+str(len(record))+" i: "+str(i)+" col: "+str(col))
                    col += len(data)
                else:
                    break
            logger.debug("--parseWrappedDataRecords() result length pre append: "+str(len(result))+" i: "+str(i)+" col: "+str(col))
            result.append(record)
            logger.debug("--parseWrappedDataRecords() result length post append: "+str(len(result))+" i: "+str(i)+" col: "+str(col))
        return result
    '''
                    
    @classmethod
    def parseDataRecordsBySpaces(cls, record):
        """ input is a space separated string, returns a list of strings  """
        return record.strip().split()

    #TODO check this method
    @classmethod
    def parseDataRecordsByRegex(cls, record, numTraces, delimiter, nullValue):
        """ generated source for method parseDataRecordsByRegex """
        result = [None]*numTraces
        remainder = record
        end = 0
        i = 0
        while i < numTraces:
            try:
                end = remainder.index(delimiter)
                result[i] = remainder[:end]
            except ValueError as e:
                logger.debug("--parseDataRecordsByRegex "+str(e))
                result[i] = remainder
            if 0 == len(result[i]):
                result[i] = "" + nullValue
            remainder = remainder[end + 1:]
            i += 1
        return result

    @classmethod
    def splitHeaderRecord(cls, record):
        """ Splits a header record. """
        #logger.debug(">>splitHeaderRecord() "+str(record))
        periodIndex = record.index(".")
        colonIndex = record.index(":")
        #If the . or : are missing then give up on this record.
        if periodIndex == -1 or colonIndex == -1:
            return ["", "", "", "", ""]
        #Extract the mnemonic (log type).
        name = record[0:periodIndex].strip()
        #Extract the unit. 
        #don't trim yet in case unit is blank
        remains = record[periodIndex + 1:]
        endOfUnit = remains.index(" ")
        unit = remains[0:endOfUnit]
        #Extract the type or code.
        remains = remains[endOfUnit:].strip()
        colonIndex = remains.index(":")
        code = remains[0:colonIndex].strip()
        #Extract the description.
        description = remains[colonIndex + 1:].strip()
        return [name, unit, code, description]

    def stripAndRoundToDouble(self, value, significantPlaces):
        trailingWords = ["f","ft","feet","m","meters"] 
        numberWithoutTrailingUints = StringUtils.stripTrailingWordsIgnoreCase(value, trailingWords)
        priorToRounding = NumberUtils.parseStringToFloat(numberWithoutTrailingUints, self.null_value)
        if priorToRounding == self.null_value:
            return priorToRounding
        else:
            rounded = NumberUtils.roundToDecimal(priorToRounding, significantPlaces);
            return rounded;

    def getMnemonicNames(self):
        """ generated source for method getMenmonicNames """
        #logger.debug(">>menmonicNames() "+str(len(self._unitMap)))
        #for item in self._unitMap.keys():
        #    logger.debug(str(item))
        return list(self._unitMap.keys())

    @property
    def parameterMenmonicNames(self):
        """ generated source for method getParameterMenmonicNames """
        return list(self._parameterUnitMap.keys())

    @property
    def getExpectedNumberOfSamples(self):
        """ generated source for method getExpectedNumberOfSamples """
        numSamples = int((1 + round((self._stop - self._start) / self._step)))
        return numSamples

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    unittest.main()
