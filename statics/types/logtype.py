#!/usr/bin/env python
""" generated source for module LogType """

import logging
from statics.types.rangetype import RangeType

#from base.types import LogType
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
# 
#  * TODO add a description field - eg for Vp 'Velocity - P'
#  * Note currently in transition phase from logUnitTypes to Unit and Domain - both code is active atm
#  * @author a
#  *
#  
class LogType(object):
    """ generated source for class LogType """
    uid = str()

    #  simplified name, should be unique
    name = str()
    curveMnemonic = str()
    index = int()
    #stdUnits = LogUnitsType()
    #logPlotRange = RangeType()
    #displayUnits = LogUnitsType()
    colour = ""  #RGB()
    alpha = "" #transparency
    #domain = Domain()
    #unit = Unit()
    defaultValue = float()
    maxIndex = 0
    logtypes = {}
    logTypeUids = {}
    
    # 
    #      * Can't just move logs around here as defined by numbers in XML file
    #      
    #  TODO rename to AVOImpedance projection see http://archives.datapages.com/data/HGS/vol45/no08/26.htm
    #  NB rd uses 'reflectivity' units???
    #  NB rd uses 'reflectivity' units???
    #  have put POROSITY_NEUTRON here instead of end as removed CNL and
    #  havent worked out how to re-arange yet
    #  CNL = new LogType("","CNL", LogUnitsType.FRACT, 0.75D,
    #  -0.14999999999999999D, 0.0D,
    #  "CNL TNPH NPOR NPHI CN CNC ENPH GNT NDL NEUT NPHU PGNT PHIN SNP NEUT");
    #  TODO QC domain, QC xml and all unit types in xml
    #  TODO work out domain for LAMBDARHO MURHO
    #  TODO work out domain
    #  additional types
    #  TODO rename as VOLUME
    def __init__(self, uid, name, logunitstype, domain, unit, d1, d2, defaultValue, curveMnemonic):
        """ generated source for method __init__ """
        #logger.debug("__init__() "+s+" type: "+logunitstype.__str__()+" domain: "+str(domain)+" unit: "+str(unit))
        self.uid = uid
        #instantiate LogUnitsType then can reference internals
        lut = LogUnitsType
        self.displayUnits = lut.UNKNOWN
        self.domain = domain
        self.unit = unit
        #default sgi gray 16
        #http://cloford.com/resources/colours/500col.htm
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
        """ generated source for method toString """
        return self.name
    
    #deprecated
    def getName(self):
        """ generated source for method toString """
        return self.name
    
    #deprecated
    def getUid(self):
        return self.uid

    #deprecated
    def getIndex(self):
        """ returns item index """
        return self.index

    #deprecated
    def getCurveMnemonic(self):
        """ returns mnemonics in one space sep. string"""
        return self.curveMnemonic

    def setCurveMnemonic(self, s):
        """ generated source for method setDefaultIdentifiersString """
        self.curveMnemonic = s

    @classmethod
    def getLogTypes(cls):
        """ returns logtypes dictionary """
        return cls.logtypes
    
    @classmethod
    def getLogTypeUids(cls):
        """ returns logtypes uid dictionary """
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
    
    @classmethod
    def getAllLogTypesRockPhysicsStringList(cls):
        """ returns logtype names in a rockPhysics priority list """
        rock_physics_names= []
        log_type_names = []
        for key, value in cls.logTypeUids.iteritems():
            if key == "rho" or key == "vp" or key == "vs" or key == "acimp":
                rock_physics_names.append(value.getName())
            else:
                log_type_names.append(key)
        
        return sorted(rock_physics_names)+sorted(log_type_names)

    
    def setDefaultLogPlotRange(self, rangetype):
        """ generated source for method setDefaultLogPlotRange """
        self.logPlotRange = rangetype

    def getDefaultLogPlotRange(self):
        """ generated source for method getDefaultLogPlotRange """
        return self.logPlotRange

    def setDisplayUnits(self, unit):
        """ generated source for method setDisplayUnits """
        self.displayUnits = unit

    def setName(self, s):
        """ generated source for method setName """
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
        if logType.getUid() == LogType.VP.getUid() or logType.getUid() == LogType.VS.getUid():
            rs.append(logUnitsType.MpS)
            rs.append(logUnitsType.FTpS)
            rs.append(logUnitsType.KMpS)
            rs.append(logUnitsType.KFTpS)
            return rs
        elif logType.getUid() == LogType.GAMMA.getUid():
            rs.append(logUnitsType.API)
            return rs
        elif logType.getUid() == cls.RHO.getUid() or logType.getUid() == cls.DENSITY_CORRECTION.getUid():
            rs.append(logUnitsType.GpCC)
            rs.append(logUnitsType.KGpM3)
        elif logType.getUid() == cls.POROSITY.getUid() or logType.getUid() == cls.VOLUME_FRACTION.getUid() or logType.getUid() == cls.SATURATION.getUid() or logType.getUid() == cls.SATURATIONSET.getUid() or logType.getUid() == cls.VOLUME_FRACTIONSET.getUid() or logType.getUid() == cls.LAMBDAOVERMU.getUid() or logType.getUid() == cls.POROSITY_DENSITY.getUid() or logType.getUid() == cls.POROSITY_NEUTRON.getUid() or logType.getUid() == cls.POROSITY_SONIC.getUid():
            rs.append(logUnitsType.FRACT)
            rs.append(logUnitsType.PERCENT)
        elif logType.getUid() == cls.CAL.getUid():
            rs.append(logUnitsType.M)
            rs.append(logUnitsType.CM)
            rs.append(logUnitsType.MM)
            rs.append(logUnitsType.INCH)
        elif logType.getUid() == cls.DT.getUid() or logType.getUid() == cls.DTSM.getUid():
            rs.append(logUnitsType.USpM)
            rs.append(logUnitsType.USpFT)
        elif logType.getUid() == cls.TEMP.getUid():
            rs.append(logUnitsType.CELCIUS)
            rs.append(logUnitsType.FAHRENHEIT)
        elif logType.getUid() == cls.RESIS_DEEP.getUid() or logType.getUid() == cls.RESIS_MEDIUM.getUid() or logType.getUid() == cls.RESIS_SHALLOW.getUid() or logType.getUid() == cls.EM_RTA.getUid() or logType.getUid() == cls.RESIS.getUid():
            rs.append(logUnitsType.OHMM)
        elif logType.getUid() == cls.ACIMP.getUid() or logType.getUid() == cls.AI.getUid() or logType.getUid() == cls.GI.getUid() or logType.getUid() == cls.SI.getUid():
            rs.append(logUnitsType.GpCCMpS)
            rs.append(logUnitsType.GpCCFTpS)
            rs.append(logUnitsType.GpCCKMpS)
            rs.append(logUnitsType.GpCCKFTpS)
            rs.append(logUnitsType.KGpM3MpS)
            rs.append(logUnitsType.KGpM3FTpS)
            rs.append(logUnitsType.KGpM3KMpS)
            rs.append(logUnitsType.KGpM3KFTpS)
        elif logType.getUid() == cls.MOD.getUid() or logType.getUid() == cls.E.getUid() or logType.getUid() == cls.K.getUid() or logType.getUid() == cls.LAMBDA.getUid() or logType.getUid() == cls.M.getUid() or logType.getUid() == cls.MU.getUid():
            rs.append(logUnitsType.GPA)
            rs.append(logUnitsType.DYNEpCM2)
        elif logType.getUid() == cls.PERM.getUid():
            rs.append(logUnitsType.MD)
            rs.append(logUnitsType.D)
        elif logType.getUid() == cls.SAL.getUid():
            rs.append(logUnitsType.PPM)
        elif logType.getUid() == cls.GOR.getUid():
            rs.append(logUnitsType.VpV)
            rs.append(logUnitsType.SCFpSTB)
        elif logType.getUid() == cls.ODEN.getUid():
            rs.append(logUnitsType.APIOilDen)
            rs.append(logUnitsType.GpCCOilDen)
        elif logType.getUid() == cls.DEPTH.getUid():
            rs.append(logUnitsType.M)
            rs.append(logUnitsType.CM)
            rs.append(logUnitsType.MM)
            rs.append(logUnitsType.INCH)
            rs.append(logUnitsType.FT)
            rs.append(logUnitsType.KM)
            rs.append(logUnitsType.KFT)
        elif logType.getUid() == cls.HORIZONTALDIST.getUid() or logType.getUid() == cls.COORDINATEDIST.getUid():
            rs.append(logUnitsType.M)
            rs.append(logUnitsType.FT)
            rs.append(logUnitsType.FTUS)
            rs.append(logUnitsType.KM)
            rs.append(logUnitsType.KFT)
        elif logType.getUid() == cls.TIME.getUid():
            rs.append(logUnitsType.MS)
            rs.append(logUnitsType.S)
        elif logType.getUid() == cls.POISSONRATIO.getUid() or logType.getUid() == cls.EIMP.getUid() or logType.getUid() == cls.THOMSEN.getUid() or logType.getUid() == cls.EPSILONANI.getUid() or logType.getUid() == cls.DELTAANI.getUid() or logType.getUid() == cls.GAMMAANI.getUid() or logType.getUid() == cls.FACIES.getUid() or logType.getUid() == cls.LITHOLOGY.getUid() or logType.getUid() == cls.EEI.getUid() or logType.getUid() == cls.EI2.getUid() or logType.getUid() == cls.EI3.getUid() or logType.getUid() == cls.SEI2.getUid() or logType.getUid() == cls.SEI3.getUid() or logType.getUid() == cls.ANISOTROPY_SYSTEM.getUid():
            rs.append(logUnitsType.NONE)
        elif logType.getUid() == cls.REFLECT.getUid() or logType.getUid() == cls.TRACE.getUid():
            rs.append(logUnitsType.REFLECT)
        elif logType.getUid() == cls.SP.getUid():
            rs.append(logUnitsType.MV)
        elif logType.getUid() == cls.MISC.getUid() or logType.getUid() == cls.UNKNOWN.getUid():
            rs.append(logUnitsType.NONE)
            rs.append(logUnitsType.MpS)
            rs.append(logUnitsType.FTpS)
            rs.append(logUnitsType.KMpS)
            rs.append(logUnitsType.KFTpS)
            rs.append(logUnitsType.API)
            rs.append(logUnitsType.GpCC)
            rs.append(logUnitsType.KGpM3)
            rs.append(logUnitsType.FRACT)
            rs.append(logUnitsType.PERCENT)
            rs.append(logUnitsType.M)
            rs.append(logUnitsType.CM)
            rs.append(logUnitsType.MM)
            rs.append(logUnitsType.INCH)
            rs.append(logUnitsType.FT)
            rs.append(logUnitsType.FTUS)
            rs.append(logUnitsType.KM)
            rs.append(logUnitsType.KFT)
            rs.append(logUnitsType.MS)
            rs.append(logUnitsType.S)
            rs.append(logUnitsType.USpM)
            rs.append(logUnitsType.USpFT)
            rs.append(logUnitsType.CELCIUS)
            rs.append(logUnitsType.FAHRENHEIT)
            rs.append(logUnitsType.OHMM)
            rs.append(logUnitsType.GpCCMpS)
            rs.append(logUnitsType.GpCCFTpS)
            rs.append(logUnitsType.GpCCKMpS)
            rs.append(logUnitsType.GpCCKFTpS)
            rs.append(logUnitsType.KGpM3MpS)
            rs.append(logUnitsType.KGpM3FTpS)
            rs.append(logUnitsType.KGpM3KMpS)
            rs.append(logUnitsType.KGpM3KFTpS)
            rs.append(logUnitsType.MPA)
            rs.append(logUnitsType.PSI)
            rs.append(logUnitsType.GPA)
            rs.append(logUnitsType.DYNEpCM2)
            rs.append(logUnitsType.MD)
            rs.append(logUnitsType.D)
            rs.append(logUnitsType.PPM)
            rs.append(logUnitsType.VpV)
            rs.append(logUnitsType.SCFpSTB)
            rs.append(logUnitsType.APIOilDen)
            rs.append(logUnitsType.GpCCOilDen)
            rs.append(logUnitsType.REFLECT)
        elif logType.getUid() == cls.PRES_FORMATION.getUid() or logType.getUid() == cls.PRES_FRACTURE.getUid() or logType.getUid() == cls.PRES_HYDROSTATIC.getUid() or logType.getUid() == cls.PRES_LITHOSTATIC.getUid() or logType.getUid() == cls.PRES_VES.getUid():
            rs.append(logUnitsType.MPA)
            rs.append(logUnitsType.PSI)
            rs.append(logUnitsType.BAR)
            rs.append(logUnitsType.KPA)
        elif logType.getUid() == cls.ANGLE.getUid():
            rs.append(logUnitsType.DEG)
            rs.append(logUnitsType.RAD)
        elif logType.getUid() == cls.PRESSURE_GRADIENT.getUid():
            rs.append(logUnitsType.MPApM)
            rs.append(logUnitsType.MPApFT)
            rs.append(logUnitsType.PSIpFT)
            rs.append(logUnitsType.PSIpM)
            rs.append(logUnitsType.BARpM)
            rs.append(logUnitsType.BARpFT)
            rs.append(logUnitsType.KPApM)
            rs.append(logUnitsType.KPApFT)
            rs.append(logUnitsType.GpCC)
            rs.append(logUnitsType.PPG)
            rs.append(logUnitsType.KGpM3)
        elif logType.getUid() == cls.MUDWEIGHT.getUid():
            rs.append(logUnitsType.GpCC)
            rs.append(logUnitsType.PPG)
            rs.append(logUnitsType.KGpM3)
            rs.append(logUnitsType.MPApM)
            rs.append(logUnitsType.MPApFT)
            rs.append(logUnitsType.PSIpFT)
            rs.append(logUnitsType.PSIpM)
            rs.append(logUnitsType.BARpM)
            rs.append(logUnitsType.BARpFT)
            rs.append(logUnitsType.KPApM)
            rs.append(logUnitsType.KPApFT)
        elif logType.getUid() == cls.WELLCASING.getUid() or logType.getUid() == cls.SIZE.getUid():
            rs.append(logUnitsType.MM)
            rs.append(logUnitsType.INCH)
            rs.append(logUnitsType.CM)
            rs.append(logUnitsType.M)
        elif logType.getUid() == cls.MOBILITY.getUid():
            rs.append(logUnitsType.NONE)
        elif logType.getUid() == cls.PHOTOELECTRIC_EFFECT.getUid():
            rs.append(logUnitsType.BpE)
        elif logType.getUid() == cls.FLUIDVOLUME.getUid():
            rs.append(logUnitsType.CC)
        return rs

    def setDefaultColor(self, color):
        """ generated source for method setDefaultColor """
        self.defaultColor = color

    def getDefaultColor(self):
        """ generated source for method getDefaultColor """
        return self.defaultColor

    def getStdUnits(self):
        """ generated source for method getStdUnits """
        return self.stdUnits

    '''
    def getDefaultDisplayValue(self):
        """ generated source for method getDefaultDisplayValue """
        return self.getDisplayUnits().convertFromSI(self.defaultValue)

    def isPressureLogType(self):
        """ generated source for method isPressureLogType """
        return self == self.PRES_HYDROSTATIC or self == self.PRES_LITHOSTATIC or self == self.PRES_FORMATION or self == self.PRES_VES or self == self.PRES_FRACTURE
    '''

    def getDomain(self):
        """ generated source for method getDomain """
        return self.domain

    def setDomain(self, domain):
        """ generated source for method setDomain """
        self.domain = domain

    def getUnit(self):
        """ generated source for method getUnit """
        return self.unit

    def setUnit(self, unit):
        """ generated source for method setUnit """
        self.unit = unit


logUnitsType = LogUnitsType
domain = Domain
unit = Unit
LogType.CAL = LogType("cal","Caliper", logUnitsType.M,  domain.DISTANCE, unit.lookupByName("meters"), 0.14999999999999999, 0.5, 0.20000000000000001, "Cal Cali Caliper")
LogType.RHO = LogType("rho","Rho (Density)", logUnitsType.GpCC, domain.MASS_PER_VOLUME, unit.lookupByName("grams/cubic centimeter"), 1.45, 2.9500000000000002, 2.2000000000000002,
                "Rho RhoB Drho DENS BDCFM")
LogType.DENSITY_CORRECTION = LogType("densitycorrection","RhoCorr (Density-correction)", logUnitsType.GpCC, domain.MASS_PER_VOLUME, unit.lookupByName("grams/cubic centimeter") , 1.45, 2.9500000000000002, 2.2000000000000002,
                "2DRH DC DCOR DECR DRH DRHO HBDC HDRA HDRH HHDRA RPCL_DCOR ZCOR ZCOR2 ZCOR2QH ZCORQH HHDR Z-COR")
LogType.DENSITY_APPARENT_MATRIX = LogType("densityapparentmatrix","RhoMaa (Density-apparent-matrix)", logUnitsType.GpCC, domain.MASS_PER_VOLUME, unit.lookupByName("grams/cubic centimeter"), 1.45, 2.9500000000000002, 2.2000000000000002,"Rhomaa")
LogType.ODEN = LogType("oden","RhoOil (Density-oil)", logUnitsType.APIOilDen,  domain.API_OIL_GRAVITY, unit.lookupByName("API gravity"), 0.0, 50, 10, "ODEN")
LogType.TIME = LogType("time","Time", logUnitsType.MS,  domain.TIME, unit.lookupByName("milliseconds"), 0.0, 5000, 0.0, "Time twt TWT owt")

LogType.DEPTH = LogType("depth","Depth", logUnitsType.M, domain.DISTANCE, unit.lookupByName("meters"), 0.0, 5000, 0.0, "Depth Dept M_Depth")

LogType.DT = LogType("dt","Dt (Sonic-P)", logUnitsType.USpM,  domain.TIME_PER_LENGTH, unit.lookupByName("microseconds/meter"), 1476.3779999999999, 492.12599999999998, 1000,
                "Sonic DT DTL SON DTPM DTCO")
LogType.DTSM = LogType("dts","Dts (Sonic-S)", logUnitsType.USpM,  domain.TIME_PER_LENGTH, unit.lookupByName("microseconds/meter"), 1312.336, 328.084, 500, "DTSM DTSML")
LogType.DT_APPARENT_MATRIX = LogType("dtapparentmatrix","DtMa (Dt Apparent Matrix)", logUnitsType.USpM,  domain.TIME_PER_LENGTH, unit.lookupByName("microseconds/meter"), 1476.3779999999999, 492.12599999999998, 1000,
                "DTMAA DTMXA")
LogType.DT_APPARENT_FLUID = LogType("dtapparentfluid","DtFa (DT Apparent Fluid)", logUnitsType.USpM,  domain.TIME_PER_LENGTH, unit.lookupByName("microseconds/meter"), 0.0, 0.0, 0.0,
                "DTFA")
LogType.GAMMA = LogType("gamma","Gr (Gamma ray)", logUnitsType.API, domain.GAMMA_RAY_API_UNIT, unit.lookupByName("API gamma ray units"), 0.0, 150, 100, "GR Gamma CGR SGR GR1 GR2 GR3 GRCFM")

LogType.POROSITY = LogType("porosity","Porosity", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction"), 0.0, 0.40000000000000002, 0.20000000000000001,
                "Phi Phie Phit")
LogType.POROSITY_NEUTRON = LogType("porosityneutron","Porosity-neutron", logUnitsType.FRACT,  domain.DIMENSIONLESS, unit.lookupByName("volume fraction"), 0.75, -0.14999999999999999,0.0, "CNCS CNCSGS CNCSS CNCSSQH CNSS HASC HNPO_SAN HNPS HNPSS HTNP_SAN NPHI_SAN NPHIS NPHS NPOR_SAN NPORSS NPRS "
                + "NPSS NPSS_C POS TNPH_SAN TNPH_SAN1 HNPH NPHI_S CN CNC FNPS HHNPO HNPHI HNPO HTNP NCN NCNL NPHI NPOR NPOR_ NPOR_1 RPOR SNP "
                + "TNPH ENPH FPSC PRON QNP-1A QNP-5A NPLFM")
LogType.POROSITY_DENSITY = LogType("porositydensity", "Porosity-density", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction") , 0.0, 0.40000000000000002, 0.20000000000000001, "2DPS APSC APSU DEPO DPHI_SAN DPHI_SLDT DPHI_SLDT_HR DPHIS DPHS DPHZ DPHZSS DPRS DPSS DPSZ HDPH HDPH_SAN HDPHI HDPO HDPSS HFSC NDPH PDS "
                + "POD PORS PORZ PORZ2QH PORZQH PORZS2"
                        + " PORZS2QH PORZSS PORZSS2 PORZSSQH PZCSS PZCSSQH PZCSSS PZSS PZSS2 PZSS2QH PZSSQH PZSSS RPSS SSD DPH DDPP DNPH DPH8 DPHI DPHI_ "
                        + "DPO DPOR DPS8 HDPH8 PXND DPS1 POR")
LogType.POROSITY_SONIC = LogType("porositysonic","Porosity-sonic", logUnitsType.FRACT, domain.DIMENSIONLESS,  unit.lookupByName("volume fraction") , 0.0, 0.40000000000000002,
                0.20000000000000001, "ACPS PORA RPHI SPHI SPSS TPHI ACPL ACPD SPOR")
        
LogType.RESIS = LogType("resis","Resistivity", logUnitsType.OHMM,  domain.RESISTIVITY, unit.lookupByName("ohm meters"), 0.20000000000000001, 100, 5, "RESIS")
        
LogType.RESIS_MEDIUM = LogType("resismedium",
                "Resistivity-medium",
                logUnitsType.OHMM,  domain.RESISTIVITY, unit.lookupByName("ohm meters") ,
                0.20000000000000001,
                100,
                5,
                "AE60 AF30 AHF3 AHF30 AHO3 AHO30 AHT3 AHT30 AIT3 AIT30 AO30 AS30 ASF3 ASF30 ASO30 AST3 AST30 AT30 DSLL HAT3 HILM HLLS HRL3 ILD25 ILM ILM1 ILM2 "
                + "ILM25 ILM4 IM IM10 IM20 IM25 IM40 IMER IMPH IMVR LLS M0R3 M1R3 M2R3 M4R3 MVR1 MVR2 MVR4 PIRM REIM RESM RILM RIPM RLLS RMLL RPCL VILM VP25")
LogType.RESIS_SHALLOW = LogType("resisshallow",
                "Resistivity-shallow",
                logUnitsType.OHMM,  domain.RESISTIVITY, unit.lookupByName("ohm meters") ,
                0.20000000000000001,
                100,
                5,
                "AE20 AE30 AF10 AF20 AFRX AHF1 AHF10 AHF2 AHF20 AHO1 AHO10 AHO2 AHO20 AHSFI AHT1 AHT10 AHT2 AHT20 AHTRX AIT10 AIT20 AO10 AO20 AORX AS10 AS20 "
                + "ASF1 ASF10 ASF2 ASF20 ASFI ASFL ASN ASO10 ASO20 ASRX AST1 AST10 AST2 AST20 AT10 AT12 AT20 ATRX FE1 FEFE FR FRA HAT1 HAT2 HRL1 HRL2 HRLS "
                + "HSFL HSFLU ILS LL8 LLA M0R1 M0R2 M1R1 M1R2 M2R1 M2R2 M4R1 M4R2 MFR MLL MSFF MSFL PSHG Res Resis RESS RILS RLL1 RLL2 RS RSFE RSFL RSG "
                + "RXO RXO_HRLT RXO1D RXO8 RXOH RXOI RXOZ SFBC SFL SFL4 SFLA SFLR SFLU SN")
LogType.RESIS_DEEP = LogType("resisdeep",
                "Resistivity-deep",
                logUnitsType.OHMM,  domain.RESISTIVITY, unit.lookupByName("ohm meters") ,
                0.20000000000000001,
                100,
                5,
                "A22H A22H_ A22H_UNC A28H A28H_ A28H_UNC A34H A34H_ A34H_UNC AF60 AF90 AFRT AHF6 AHF60 AHF9 AHF90 AHO6 AHO60 AHO9 AHO90 AHOR AHT6 AHT60 AHT9 AHT90"
                        + " AHTR AHTRT AILD AIT AIT120 AIT6 AIT60 AIT9 AIT90 AO12 AO60 AO90 AORT AS60 AS90 ASF6 ASF60 ASF9 ASF90 ASFR ASO60 ASO90"
                        + " ASRT AST6 AST60 AST9 AST90 ASTR AT60 AT90 ATRT DDLL DIPH DVR1 DVR2 DVR4 EIRD FE2 GRD HAT6 HAT9 HATR HILD HLLD HRL4 HRL5 HRLD ID10 "
                        + "ID20 ID25 ID40 IDER"
                        + " IDPH IDVR IL ILD ILD1 ILD2 ILD4 LL LL3 LL7 LLD LLG LN M0R6 M0R9 M0RX M1R6 M1R9 M1RX M2R6 M2R9 M2RX M4R6 M4R9 M4RX P10H P10H_ "
                        + "P10H_UNC P16H P16H_ P16H_UNC P22H"
                        + "P22H_ P22H_UNC P28H P28H_ P28H_UNC P34H P34H_ P34H_UNC REID RESD RFOC RILD RIPD RLA1 RLA2 RLA3 RLA4 RLA5 RLL RLL3 RLL4 RLL5 "
                        + "RLLD RT RT_H RT_HRLT VILD VP65 VRSD")
        

LogType.SATURATION = LogType("saturation","Saturation", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction"), 0.0, 1.0, 1.0, "Sat Sw So Sg sxo swirr")
LogType.TEMP = LogType("temp","Temperature", logUnitsType.CELCIUS,  domain.TEMPERATURE, unit.lookupByName("degrees Celsius"), 0.0, 120, 20, "Temp")
LogType.ACIMP = LogType("acimp","ACImp (Acoustic impedance)", logUnitsType.GpCCMpS,  domain.VELOCITY_MASS_PER_VOLUME, unit.lookupByName("acoustic impedance"), 4000, 12000, 6000, "ACIMP")
LogType.PRES_FORMATION = LogType("presformation","Pressure-formation", logUnitsType.MPA,  domain.PRESSURE, unit.lookupByName("megapascals"), 0.0, 100, 30, "Pres Pressure")
LogType.MOD = LogType("mod","Mod", logUnitsType.GPA, domain.PRESSURE, unit.lookupByName("gigapascals"), 0.0, 100, 15, "Mod MOD")
LogType.PERM = LogType("perm","Permeability", logUnitsType.M,  domain.AREA, unit.lookupByName("millidarcies"), 0.0, 4000, 100, "Perm Permeability CORK")
LogType.SAL = LogType("sal","Salinity", logUnitsType.PPM,  domain.DIMENSIONLESS, unit.lookupByName("parts per million"), 0.0, 200000, 100000, "Sal Salinity")
LogType.GOR = LogType("gor","GOR (Gas to oil ratio)", logUnitsType.VpV, domain.DIMENSIONLESS, unit.lookupByName("volume fraction"), 0.0, 500, 50, "GOR")
LogType.POISSONRATIO = LogType("poissonratio","Poisson's ratio", logUnitsType.NONE,  domain.DIMENSIONLESS,  unit.lookupByName("unitless"), 0.0, 0.5, 0.10000000000000001,
                "Poisson Poissons Pois sigma ratio PR")
# rename to AVOImpedance projection see http://archives.datapages.com/data/HGS/vol45/no08/26.htm
LogType.PROJECTION = LogType("projtn","Projection", logUnitsType.NONE,  domain.DIMENSIONLESS, unit.lookupByName("unitless"),  -1000, 1000, 0.0, "AVOImp AVOI")
LogType.EIMP = LogType("eimp","Impedance-elastic", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 100, 10000, 1000, "EImp")
LogType.SATURATIONSET = LogType("saturationset","Saturation set", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction"),  0.0, 1.0, 0.5, "FLUIDFRACT")
LogType.VOLUME_FRACTIONSET = LogType("volumefractionset","Volume set", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction"),  0.0, 1.0, 0.5, "VOLUME_FRACTIONFRACT")
#NB rd uses 'reflectivity' units???
LogType.REFLECT = LogType("reflect","Reflectivity", logUnitsType.REFLECT, domain.DIMENSIONLESS, unit.lookupByName("unitless"), -1, 1.0, 0.0, "Reflect ref Reflectivity")
LogType.MISC = LogType("misc","Misc", logUnitsType.NONE,  domain.UNDEFINED, unit.lookupByName("undefined"), -100, 100, 0.0, "Misc")
#NB rd uses 'reflectivity' units???
LogType.TRACE = LogType("trace","Trace", logUnitsType.REFLECT, domain.DIMENSIONLESS, unit.lookupByName("unitless"), -1, 1.0, 0.0, "TRACE")
LogType.THOMSEN = LogType("thomsen","Thomsen", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 0.0, 1.0, 0.0, "thom Thomsen")
LogType.SP = LogType("sp","Spontaneous potential", logUnitsType.MV, domain.ELECTRIC_POTENTIAL, unit.lookupByName("millivolts"), -60, 60, 0.0, "sp SP Sp")
LogType.EPSILONANI = LogType("epsilon","Anisotropy-epsilon", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), -1.5, 1.5, 0.0,
                "Epsilon EpsilonAni Anisotropy_Epsilon")
LogType.DELTAANI = LogType("deltaani","Anisotropy-delta", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), -1.5, 1.5, 0.0,
                "Delta DeltaAni Anisotropy_Delta")
LogType.GAMMAANI = LogType("gammaani","Anisotropy-gamma", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), -1.5, 1.5, 0.0, "GammaAni Anisotropy_Gamma")
LogType.PRES_HYDROSTATIC = LogType("preshydrostatic","Pressure-hydrostatic", logUnitsType.MPA,  domain.PRESSURE, unit.lookupByName("megapascals"), 0.0, 100, 30, "Pres_Hydro Pressure_Hydro")
LogType.PRES_LITHOSTATIC = LogType("preslithostatic","Pressure-lithostatic", logUnitsType.MPA,  domain.PRESSURE, unit.lookupByName("megapascals"), 0.0, 100, 30, "Pres_Litho Pressure_Litho")
LogType.PRES_VES = LogType("presves","Pres_VES", logUnitsType.MPA,  domain.PRESSURE, unit.lookupByName("megapascals"), 0.0, 100, 30, "Pres_VES Pressure_VES")
LogType.PRES_FRACTURE = LogType("presfracture","Pressure-fracture", logUnitsType.MPA,  domain.PRESSURE, unit.lookupByName("megapascals"), 0.0, 100, 30, "Pres_Fract Pressure_Fract")
# have put POROSITY_NEUTRON here instead of end as removed CNL and
# havent worked out how to re-arange yet

# CNL = LogType("","CNL", LogUnitsType.FRACT, 0.75,
# -0.14999999999999999, 0.0,
#/ "CNL TNPH NPOR NPHI CN CNC ENPH GNT NDL NEUT NPHU PGNT PHIN SNP NEUT")
LogType.FACIES = LogType("facies","Facies", logUnitsType.NONE,  domain.DIMENSIONLESS, unit.lookupByName("unitless"), 0.0, 10, 0.0, "FACIES")
#TODO QC domain, QC xml and all unit types in xml
LogType.CAPTURE_CROSS_SECTION_APPARENT_MATRIX = LogType("capturecrosssectionapparentmatrix","Umaa", logUnitsType.BpCM3, domain.CROSS_SECTION_ABSORPTION, unit.lookupByName("barns/cubic centimeter"),1.0, 20.0, 8.0, "Umaa")
LogType.LITHOLOGY_N = LogType("lithologyn","LithologyN", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"),0.1, 1.0, 0.5, "NLITH")
LogType.LITHOLOGY_M = LogType("lithologym","LithologyM", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"),0.1, 2.0, 0.8, "MLITH")

LogType.UD_6 = LogType("undefined1","Undefined1", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"),0.0, 1000, 0.0, "")
LogType.UD_7 = LogType("undefined2","Undefined2", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"),0.0, 1000, 0.0, "")
LogType.UD_8 = LogType("undefined3","Undefined3", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"),0.0, 1000, 0.0, "")
LogType.UD_9 = LogType("undefined4","Undefined4", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"),0.0, 1000, 0.0, "")
LogType.HORIZONTALDIST = LogType("horizontaldist","Distance-horizontal", logUnitsType.M,  domain.DISTANCE, unit.lookupByName("meters"), 0.0, 0.0, 0.0, "Horizontal_Dist")
LogType.COORDINATEDIST = LogType("coordinatedist","Distance-coordinate", logUnitsType.M,  domain.DISTANCE, unit.lookupByName("meters"), 0.0, 0.0, 0.0, "Coordinate_Dist")
LogType.LITHOLOGY = LogType("lithology","Lithology", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"),  0.0, 15, 0.0, "Lithology_Lith LITH")
LogType.AI = LogType("ai","AI", logUnitsType.GpCCMpS, domain.VELOCITY_MASS_PER_VOLUME, unit.lookupByName("acoustic impedance"), 4000, 12000, 6000, "AI")
LogType.GI = LogType("gi","GI", logUnitsType.GpCCMpS,  domain.VELOCITY_MASS_PER_VOLUME, unit.lookupByName("acoustic impedance"), 4000, 12000, 6000, "GI")
LogType.SI = LogType("si","SI", logUnitsType.GpCCMpS, domain.VELOCITY_MASS_PER_VOLUME, unit.lookupByName("acoustic impedance"),  4000, 12000, 6000, "SI")
LogType.EEI = LogType("eei","EEI", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 100, 10000, 1000, "EEI")
LogType.EI2 = LogType("ei2","EI2", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 100, 10000, 1000, "EI2 EI_2T")
LogType.EI3 = LogType("ei3","EI3", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 100, 10000, 1000, "EI3 EI_3T")
LogType.SEI2 = LogType("sei2","SEI2", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 100, 10000, 1000, "SEI2 SEI_2T")
LogType.SEI3 = LogType("sei3","SEI3", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 100, 10000, 1000, "SEI3 SEI_3T")
LogType.M = LogType("modulusm","Modulus, P-wave (M)", logUnitsType.GPA, domain.PRESSURE, unit.lookupByName("gigapascals"), 0.0, 100, 15, "PMOD")
LogType.MU = LogType("modulusshearmu","Modulus, Shear (Mu)", logUnitsType.GPA, domain.PRESSURE, unit.lookupByName("gigapascals"), 0.0, 100, 15, "MU")
LogType.K = LogType("moduludbulkk","Modulus, Bulk (K)", logUnitsType.GPA,  domain.PRESSURE, unit.lookupByName("gigapascals"), 0.0, 100, 15, "KMOD")
LogType.LAMBDA = LogType("lambda","Lambda", logUnitsType.GPA, domain.PRESSURE, unit.lookupByName("gigapascals"), 0.0, 100, 15, "LAMBDA")
LogType.E = LogType("modulusyoungse","Modulus, Young's (E)", logUnitsType.GPA, domain.PRESSURE, unit.lookupByName("gigapascals"), 0.0, 100, 15, "YMOD")
LogType.ANGLE = LogType("angle","ANGLE", logUnitsType.DEG,  domain.PLANE_ANGLE, unit.lookupByName("degrees of an angle"), 0.0, 180, 0.0, "ANGLE")
#TODO work out domain for LAMBDARHO MURHO
LogType.LAMBDARHO = LogType("lambdarho","LambdaRho", logUnitsType.GPAGpCC, domain.DIMENSIONLESS, unit.lookupByName("unitless"),0.0, 442.5, 33, "LambdaRho")
LogType.MURHO = LogType("murho","MuRho", logUnitsType.GPAGpCC, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 0.0, 442.5, 33, "MuRho")
LogType.LAMBDAOVERMU = LogType("lambdaovermu","LambdaOverMu", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction") , 0.0, 1.0, 0.5, "LambdaOverMu")
LogType.PRESSURE_GRADIENT = LogType("pressuregradient","PressureGradient", logUnitsType.GpCC, domain.MASS_PER_VOLUME, unit.lookupByName("grams/cubic centimeter") ,1.45, 2.9500000000000002,
                2.2000000000000002, "Pressure_Gradient")
LogType.MUDWEIGHT = LogType("mudweight","MudWeight", logUnitsType.GpCC, domain.MASS_PER_VOLUME, unit.lookupByName("grams/cubic centimeter") , 1.45, 2.9500000000000002, 2.2000000000000002,
                "MudWeight, Mud_Weight")
LogType.WELLCASING = LogType("wellcasing","WellCasing", logUnitsType.M, domain.DISTANCE, unit.lookupByName("meters") , 0.1143, 0.27305000000000001, 0.1143,
                "Casing, Well_Casing")
#TODO work out domain
LogType.EM_COMMONOFFSET = LogType("emcommonoffset","EMCommonOffset", logUnitsType.NanoVOLTSpMS, domain.DIMENSIONLESS, unit.lookupByName("unitless"), 0.0, 10, 0.0, "EMCommonOffset")
LogType.EM_RTA = LogType("emrta","EMRTA", logUnitsType.OHMM, domain.RESISTIVITY, unit.lookupByName("ohm meters") , 0.0, 1.0, 0.0, "EMRTA")
LogType.ANISOTROPY_SYSTEM = LogType("anisotropysystem","AnisotropySystem", logUnitsType.NONE, domain.DIMENSIONLESS, unit.lookupByName("unitless") , 0.0, 3, 0.0, "Anisotropy System")
LogType.MOBILITY = LogType("mobility","Mobility", logUnitsType.MDpCP,  domain.MOBILITY, unit.lookupByName("millidarcies/centipoise") , 0.0, 40000, 200, "Mobility")
# additional types

LogType.PHOTOELECTRIC_EFFECT = LogType("photoelectriceffect", "PE", logUnitsType.BpE,  domain.CROSS_SECTION_ABSORPTION, unit.lookupByName("barns/electron") , 0.0, 20.0, 3.0, "HPEDN HPEF8 PDPE PE PE2 PE2QH PEDF PEDN PEF PEF_SLDT PEF_SLDT_HR PEF8 PEFA PEFSA PEFZ PEQH SPEF HPEF PEFI PEFL LPE 2PEF PEFS PEF_ DPEFM")

        
LogType.MASS = LogType("mass","Mass", logUnitsType.KG,  domain.MASS, unit.lookupByName("kilograms") , 0.0, 1000.0, 10.0, "GeneralMass")
LogType.SIZE =  LogType("size","Size", logUnitsType.M, domain.DISTANCE, unit.lookupByName("meters") , 0.0, 1000.0, 100.0, "GeneralSize")
#TODO rename as VOLUME
LogType.FLUIDVOLUME  =  LogType("fluidvolume","FluidVolume", logUnitsType.CC,   domain.VOLUME, unit.lookupByName("cubic centimeters") , 0.0, 1000.0, 100.0, "FluidVolume")
LogType.MUD_GAS = LogType("mudgas","Mud gas", logUnitsType.PERCENT, domain.DIMENSIONLESS, unit.lookupByName("volume percent"), 0.0, 10.0, 2.0, "MLC! MLC@ MLC# MLIC4 MLIC5 MLNC4 MLNC5")
LogType.UNKNOWN = LogType("unknown","UNKNOWN", logUnitsType.UNKNOWN, domain.UNDEFINED, unit.lookupByName("undefined"), 0.0, 0.0, 3000, "")

LogType.VOLUME_FRACTION = LogType("volumefraction","Volume fraction", logUnitsType.FRACT, domain.DIMENSIONLESS, unit.lookupByName("volume fraction"), 0.0, 1.0, 1.0,
                "Vol VQtz VClay VQuartz SST LST DOL VSh VShale VCL VLST VSST")
LogType.VP = LogType("vp","Velocity-P", logUnitsType.MpS, domain.VELOCITY, unit.lookupByName("meters/second"), 2000, 6000, 3000, "Vp VpL")
LogType.VS = LogType("vs","Velocity-S", logUnitsType.MpS, domain.VELOCITY, unit.lookupByName("meters/second"), 500, 2500, 1500, "Vs")


