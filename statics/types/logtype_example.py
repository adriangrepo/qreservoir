#!/usr/bin/env python

import logging
from statics.types.rangetype import RangeType

from statics.types.logunitstype import LogUnitsType
from statics.types.domain import Domain
from statics.types.unit import Unit


#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('console')

try:
    dict.iteritems
except AttributeError:
    # Python 3
    def itervalues(d):
        return iter(d.values())
    def iteritems(d):
        return iter(d.items())
else:
    # Python 2
    def itervalues(d):
        return d.itervalues()
    def iteritems(d):
        return d.iteritems()

class LogType(object):
    uid = str()
    #  simplified name, should be unique
    name = str()
    curveMnemonic = str()
    index = int()
    colour = ""  #RGB()
    alpha = "" #transparency
    defaultValue = float()
    maxIndex = 0
    logtypes = {}
    logTypeUids = {}

    def __init__(self, uid, name, logunitstype, domain, unit, d1, d2, defaultValue, curveMnemonic):
        """ generated source for method __init__ """
        #logger.debug("__init__() "+s+" type: "+logunitstype.__str__()+" domain: "+str(domain)+" unit: "+str(unit))
        self.uid = uid
        #instantiate LogUnitsType then can reference internals
        lut = LogUnitsType
        self.displayUnits = lut.UNKNOWN
        self.domain = domain
        self.unit = unit
        self.colour = "40, 40, 40"
        self.alpha = "255"
        self.name = name
        self.stdUnits = logunitstype
        self.logPlotRange = RangeType(d1, d2)
        self.defaultValue = defaultValue
        self.curveMnemonic = curveMnemonic
        self.index = self.maxIndex
        #note use of class level var see http://stackoverflow.com/questions/68645/static-class-variables-in-python
        LogType.maxIndex += 1
        self.logtypes[name] = self
        self.logTypeUids[uid] = self
        #logger.debug("__init__ index: "+str(self.index)+" name: "+str(self.name))

    @classmethod
    def getLogType(cls, name):
        """ returns object matching name from types dictionary """
        logType = cls.logtypes.get(name)
        if logType == None:
            logger.debug("--getLogType() log type matching: {0} not found".format(name))
        return logType
    
    @classmethod
    def getUidFromName(cls, name):
        """ returns object's uid matching name from types dictionary """
        logType = cls.logtypes.get(name)
        if logType == None:
            logger.debug("--getUidFromName() log type matching: {0} not found".format(name))
        return logType.uid
    
    @classmethod
    def getLogTypeFromUid(cls, uid):
        """ returns object matching uid from types uid dictionary """
        logType = cls.logTypeUids.get(uid)
        if logType == None:
            logger.debug("--getLogTypeFromUid() log type matching uid: {0} not found".format(uid))
        return logType
        #return cls.logTypeUids.get(uid)

    @classmethod
    def findLogTypeFromMnemonic(cls, mnemonic):
        for key, value in iteritems(cls.logtypes):
            #logger.debug("--findLogTypeFromMnemonic() key: "+str(key)+" mnem: "+str(mnemonic))
            mnemList = value.curveMnemonic.split()
            for item in mnemList:
                if item.lower() == mnemonic.strip().lower():
                    logger.debug("--findLogTypeFromMnemonic() match: "+str(key))
                    return value
        #logger.debug("--findLogTypeFromMnemonic() no match: ")   
        return LogType.UNKNOWN

    def __str__(self):
        return self.name
    
    #deprecated
    def getName(self):
        return self.name
    
    #deprecated
    def getUid(self):
        return self.uid

    #deprecated
    def getIndex(self):
        return self.index

    #deprecated
    def getCurveMnemonic(self):
        return self.curveMnemonic

    def setCurveMnemonic(self, s):
        self.curveMnemonic = s

    @classmethod
    def getLogTypes(cls):
        return cls.logtypes
    
    @classmethod
    def getLogTypeUids(cls):
        return cls.logTypeUids
    
    @classmethod
    def getAllLogTypesStringList(cls):
        """ returns logtype names in a list """
        logTypeNames = []
        for key in cls.logtypes.keys():
            logTypeNames.append(key)
        return sorted(logTypeNames)
    
    @classmethod
    def getAllLogTypesPetrophysicsStringList(cls):
        """ returns logtype names in a petrophysics priority list """
        petrophysics_names= []
        log_type_names = []
        for key, value in cls.logTypeUids.items():
            if key == "cal" or key == "rho" or key == "dt" \
                or key == "gamma" or key == "porosity" or key == "porosityneutron" \
                or key == "resistivity" or key == "saturation" or key == "sp":
                petrophysics_names.append(value.getName())
            else:
                log_type_names.append(key)
        
        return sorted(petrophysics_names)+sorted(log_type_names)

    def setName(self, s):
        self.name = s

    def getDisplayUnits(self):
        """ returns display units for class """
        if self.displayUnits == LogUnitsType.UNKNOWN:
            self.displayUnits = self.stdUnits
        return self.displayUnits

    @classmethod
    def getLogUnitsForType(cls, logType):
        """ returns a list of LogUnitsType for the input LogType """
        rs = []
        logUnitsType = LogUnitsType
        if logType.getUid() == LogType.GAMMA.getUid():
            rs.append(logUnitsType.API)
            return rs
        elif logType.getUid() == cls.RHO.getUid() or logType.getUid() == cls.DENSITY_CORRECTION.getUid():
            rs.append(logUnitsType.GpCC)
            rs.append(logUnitsType.KGpM3)
        elif logType.getUid() == cls.POROSITY.getUid() or logType.getUid() == cls.POROSITY_NEUTRON.getUid():
            rs.append(logUnitsType.FRACT)
            rs.append(logUnitsType.PERCENT)
        elif logType.getUid() == cls.DT.getUid() or logType.getUid() == cls.DTSM.getUid():
            rs.append(logUnitsType.USpM)
            rs.append(logUnitsType.USpFT)
        return rs

    def getStdUnits(self):
        return self.stdUnits

logUnitsType = LogUnitsType
domain = Domain
unit = Unit
LogType.RHO = LogType("rho","Rho (Density)", logUnitsType.GpCC, domain.MASS_PER_VOLUME, unit.lookupByName("grams/cubic centimeter"), 1.45, 2.9500000000000002, 2.2000000000000002,
                "Rho RhoB Drho DENS BDCFM")
LogType.DENSITY_CORRECTION = LogType("densitycorrection","RhoCorr (Density-correction)", logUnitsType.GpCC, domain.MASS_PER_VOLUME, unit.lookupByName("grams/cubic centimeter") , 1.45, 2.9500000000000002, 2.2000000000000002,
                "2DRH DC DCOR DECR DRH DRHO HBDC HDRA HDRH HHDRA RPCL_DCOR ZCOR ZCOR2 ZCOR2QH ZCORQH HHDR Z-COR")

LogType.DEPTH = LogType("depth","Depth", logUnitsType.M, domain.DISTANCE, unit.lookupByName("meters"), 0.0, 5000, 0.0, "Depth Dept M_Depth")

LogType.DT = LogType("dt","Dt (Sonic-P)", logUnitsType.USpM,  domain.TIME_PER_LENGTH, unit.lookupByName("microseconds/meter"), 1476.3779999999999, 492.12599999999998, 1000,
                "Sonic DT DTL SON DTPM DTCO")
LogType.DTSM = LogType("dts","Dts (Sonic-S)", logUnitsType.USpM,  domain.TIME_PER_LENGTH, unit.lookupByName("microseconds/meter"), 1312.336, 328.084, 500, "DTSM DTSML")

LogType.GAMMA = LogType("gamma","Gr (Gamma ray)", logUnitsType.API, domain.GAMMA_RAY_API_UNIT, unit.lookupByName("API gamma ray units"), 0.0, 150, 100, "GR Gamma CGR SGR GR1 GR2 GR3 GRCFM")

LogType.POROSITY = LogType("porosity","Porosity", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction"), 0.0, 0.40000000000000002, 0.20000000000000001,
                "Phi Phie Phit")
LogType.POROSITY_NEUTRON = LogType("porosityneutron","Porosity-neutron", logUnitsType.FRACT,  domain.DIMENSIONLESS, unit.lookupByName("volume fraction"), 0.75, -0.14999999999999999,0.0, "CNCS CNCSGS CNCSS CNCSSQH CNSS HASC HNPO_SAN HNPS HNPSS HTNP_SAN NPHI_SAN NPHIS NPHS NPOR_SAN NPORSS NPRS "
                + "NPSS NPSS_C POS TNPH_SAN TNPH_SAN1 HNPH NPHI_S CN CNC FNPS HHNPO HNPHI HNPO HTNP NCN NCNL NPHI NPOR NPOR_ NPOR_1 RPOR SNP "
                + "TNPH ENPH FPSC PRON QNP-1A QNP-5A NPLFM")

