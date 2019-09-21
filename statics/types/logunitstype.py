#!/usr/bin/env python

import logging
import math
from statics.types.domain import Domain
from statics.types.unit import Unit

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



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
    
class LogUnitsType(object):
    """ generated source for class LogUnitsType """
    name = str()
    uid = str()
    index = int()
    conversionToSIFactor = float()
    decimalPlaces = int()
    canBeNegative = bool()
    maxIndex = 0
    #domain = Domain()
    logUnitTypes = {}
    
    def __init__(self, conversionFactor, name, uid, decimalPlaces, canBeNegative):
        """ generated source for method __init__ """
        self.conversionToSIFactor = 1.0
        self.decimalPlaces = 0
        self.canBeNegative = False
        self.name = name
        self.conversionToSIFactor = conversionFactor
        self.uid = uid
        self.decimalPlaces = decimalPlaces
        self.canBeNegative = canBeNegative
        self.index = self.maxIndex
        #must use class level counter
        LogUnitsType.maxIndex += 1
        self.logUnitTypes[name] = self

    #  use toString so can get string name from objects
    def __str__(self):
        """ generated source for method toString """
        return self.name
    
    def getName(self):
        return self.name

    def getIndex(self):
        """ generated source for method getValue """
        return self.index

    def convertNumberToSI(self, d):
        """ generated source for method convertToSI """
        if self.uid == self.UNKNOWN.getUid() or self.uid == self.MpS.getUid() or self.uid == self.GpCC.getUid() or self.uid == self.USpM.getUid() or self.uid == self.API.getUid() or self.uid == self.URTGpH.getUid() or self.uid == self.FRACT.getUid() or self.uid == self.M.getUid() or self.uid == self.CELCIUS.getUid() or self.uid == self.OHMM.getUid() or self.uid == self.GpCCMpS.getUid() or self.uid == self.MPA.getUid() or self.uid == self.GPA.getUid() or self.uid == self.MD.getUid() or self.uid == self.PPM.getUid() or self.uid == self.VpV.getUid() or self.uid == self.APIOilDen.getUid() or self.uid == self.MS.getUid() or self.uid == self.NONE.getUid() or self.uid == self.REFLECT.getUid() or self.uid == self.MV.getUid() or self.uid == self.DEG.getUid() or self.uid == self.GPAGpCC.getUid() or self.uid == self.NanoVOLTSpMS.getUid() or self.uid == self.MDpCP.getUid() or self.uid == self.BpE.getUid():
            return d
        if self.uid == self.FTpS.getUid() or self.uid == self.KMpS.getUid() or self.uid == self.KFTpS.getUid() or self.uid == self.KGpM3.getUid() or self.uid == self.USpFT.getUid() or self.uid == self.PERCENT.getUid() or self.uid == self.MM.getUid() or self.uid == self.CM.getUid() or self.uid == self.INCH.getUid() or self.uid == self.FT.getUid() or self.uid == self.KGpM3MpS.getUid() or self.uid == self.KGpM3FTpS.getUid() or self.uid == self.KGpM3KMpS.getUid() or self.uid == self.KGpM3KFTpS.getUid() or self.uid == self.GpCCFTpS.getUid() or self.uid == self.GpCCKMpS.getUid() or self.uid == self.GpCCKFTpS.getUid() or self.uid == self.PSI.getUid() or self.uid == self.BAR.getUid() or self.uid == self.KPA.getUid() or self.uid == self.DYNEpCM2.getUid() or self.uid == self.D.getUid() or self.uid == self.SCFpSTB.getUid() or self.uid == self.S.getUid() or self.uid == self.KM.getUid() or self.uid == self.KFT.getUid() or self.uid == self.RAD.getUid() or self.uid == self.GPAKGpM3.getUid() or self.uid == self.DYNEpCM2GpCC.getUid() or self.uid == self.DYNEpCM2KGpM3.getUid() or self.uid == self.FTUS.getUid() or self.uid == self.MPApM.getUid() or self.uid == self.MPApFT.getUid() or self.uid == self.PSIpFT.getUid() or self.uid == self.PSIpM.getUid() or self.uid == self.PPG.getUid() or self.uid == self.BARpM.getUid() or self.uid == self.KPApM.getUid() or self.uid == self.BARpFT.getUid() or self.uid == self.KPApFT.getUid():
            return d * self.conversionToSIFactor
        if self.uid == self.GpCCOilDen.getUid():
            return (141.5 - 131.5 * d) / d
        if self.uid == self.FAHRENHEIT.getUid():
            return ((d - 32) * 5) / 9
        else:
            return d


    def convertNumberListToSI(self, ad):
        """ generated source for method convertToSI_0 """
        if self.uid == self.UNKNOWN.getUid() or self.uid == self.MpS.getUid() or self.uid == self.GpCC.getUid() or self.uid == self.USpM.getUid() or self.uid == self.API.getUid() or self.uid == self.URTGpH.getUid() or self.uid == self.FRACT.getUid() or self.uid == self.M.getUid() or self.uid == self.CELCIUS.getUid() or self.uid == self.OHMM.getUid() or self.uid == self.GpCCMpS.getUid() or self.uid == self.MPA.getUid() or self.uid == self.GPA.getUid() or self.uid == self.MD.getUid() or self.uid == self.PPM.getUid() or self.uid == self.VpV.getUid() or self.uid == self.APIOilDen.getUid() or self.uid == self.MS.getUid() or self.uid == self.NONE.getUid() or self.uid == self.REFLECT.getUid() or self.uid == self.MV.getUid() or self.uid == self.DEG.getUid() or self.uid == self.GPAGpCC.getUid() or self.uid == self.NanoVOLTSpMS.getUid() or self.uid == self.MDpCP.getUid() or self.uid == self.BpE.getUid():
            return ad
        if self.uid == self.FTpS.getUid() or self.uid == self.KMpS.getUid() or self.uid == self.KFTpS.getUid() or self.uid == self.KGpM3.getUid() or self.uid == self.USpFT.getUid() or self.uid == self.PERCENT.getUid() or self.uid == self.MM.getUid() or self.uid == self.CM.getUid() or self.uid == self.INCH.getUid() or self.uid == self.FT.getUid() or self.uid == self.KGpM3MpS.getUid() or self.uid == self.KGpM3FTpS.getUid() or self.uid == self.KGpM3KMpS.getUid() or self.uid == self.KGpM3KFTpS.getUid() or self.uid == self.GpCCFTpS.getUid() or self.uid == self.GpCCKMpS.getUid() or self.uid == self.GpCCKFTpS.getUid() or self.uid == self.PSI.getUid() or self.uid == self.BAR.getUid() or self.uid == self.KPA.getUid() or self.uid == self.DYNEpCM2.getUid() or self.uid == self.D.getUid() or self.uid == self.SCFpSTB.getUid() or self.uid == self.S.getUid() or self.uid == self.KM.getUid() or self.uid == self.KFT.getUid() or self.uid == self.RAD.getUid() or self.uid == self.GPAKGpM3.getUid() or self.uid == self.DYNEpCM2GpCC.getUid() or self.uid == self.DYNEpCM2KGpM3.getUid() or self.uid == self.FTUS.getUid() or self.uid == self.PPG.getUid():
            ad1 = []
            for i in range(len(ad)):
                if not math.isnan(ad[i]):
                    ad1.append(ad[i] * self.conversionToSIFactor)
                else:
                    ad1.append((0.0 / 0.0))
            return ad1
        if self.uid == self.GpCCOilDen.getUid():
            ad2 = []
            for j in range(len(ad)):
                if not math.isnan(ad[j]):
                    ad2.append((141.5 - 131.5 * ad[j]) / ad[j])
                else:
                    ad2.append(0.0 / 0.0)
            return ad2
        if self.uid == self.FAHRENHEIT.getUid():
            ad3 = []
            for k in range(len(ad)):
                if not math.isnan(ad[k]):
                    ad3.append(((ad[k] - 32) * 5) / 9)
                else:
                    ad3.append(0.0 / 0.0)
            return ad3
        else:
            return ad

    def convertNumberFromSI(self, d):
        if self.uid == self.UNKNOWN.getUid() or self.uid == self.MpS.getUid() or self.uid == self.GpCC.getUid() or self.uid == self.USpM.getUid() or self.uid == self.API.getUid() or self.uid == self.URTGpH.getUid() or self.uid == self.FRACT.getUid() or self.uid == self.M.getUid() or self.uid == self.CELCIUS.getUid() or self.uid == self.OHMM.getUid() or self.uid == self.GpCCMpS.getUid() or self.uid == self.MPA.getUid() or self.uid == self.GPA.getUid() or self.uid == self.MD.getUid() or self.uid == self.PPM.getUid() or self.uid == self.VpV.getUid() or self.uid == self.APIOilDen.getUid() or self.uid == self.MS.getUid() or self.uid == self.NONE.getUid() or self.uid == self.REFLECT.getUid() or self.uid == self.MV.getUid() or self.uid == self.DEG.getUid() or self.uid == self.GPAGpCC.getUid() or self.uid == self.NanoVOLTSpMS.getUid() or self.uid == self.MDpCP.getUid() or self.uid == self.BpE.getUid():
            return d
        if self.uid == self.FTpS.getUid() or self.uid == self.KMpS.getUid() or self.uid == self.KFTpS.getUid() or self.uid == self.KGpM3.getUid() or self.uid == self.USpFT.getUid() or self.uid == self.PERCENT.getUid() or self.uid == self.MM.getUid() or self.uid == self.CM.getUid() or self.uid == self.INCH.getUid() or self.uid == self.FT.getUid() or self.uid == self.KGpM3MpS.getUid() or self.uid == self.KGpM3FTpS.getUid() or self.uid == self.KGpM3KMpS.getUid() or self.uid == self.KGpM3KFTpS.getUid() or self.uid == self.GpCCFTpS.getUid() or self.uid == self.GpCCKMpS.getUid() or self.uid == self.GpCCKFTpS.getUid() or self.uid == self.PSI.getUid() or self.uid == self.BAR.getUid() or self.uid == self.KPA.getUid() or self.uid == self.DYNEpCM2.getUid() or self.uid == self.D.getUid() or self.uid == self.SCFpSTB.getUid() or self.uid == self.S.getUid() or self.uid == self.KM.getUid() or self.uid == self.KFT.getUid() or self.uid == self.RAD.getUid() or self.uid == self.GPAKGpM3.getUid() or self.uid == self.DYNEpCM2GpCC.getUid() or self.uid == self.DYNEpCM2KGpM3.getUid() or self.uid == self.FTUS.getUid() or self.uid == self.PPG.getUid():
            return d / self.conversionToSIFactor
        if self.uid == self.GpCCOilDen.getUid():
            return 141.5 / (131.5 + d)
        if self.uid == self.FAHRENHEIT.getUid():
            return (9 * d) / 5 + 32
        else:
            return d

    def convertNumberListFromSI(self, ad):
        if self.uid == self.UNKNOWN.getUid() or self.uid == self.MpS.getUid() or self.uid == self.GpCC.getUid() or self.uid == self.USpM.getUid() or self.uid == self.API.getUid() or self.uid == self.URTGpH.getUid() or self.uid == self.FRACT.getUid() or self.uid == self.M.getUid() or self.uid == self.CELCIUS.getUid() or self.uid == self.OHMM.getUid() or self.uid == self.GpCCMpS.getUid() or self.uid == self.MPA.getUid() or self.uid == self.GPA.getUid() or self.uid == self.MD.getUid() or self.uid == self.PPM.getUid() or self.uid == self.VpV.getUid() or self.uid == self.APIOilDen.getUid() or self.uid == self.MS.getUid() or self.uid == self.NONE.getUid() or self.uid == self.REFLECT.getUid() or self.uid == self.MV.getUid() or self.uid == self.DEG.getUid() or self.uid == self.GPAGpCC.getUid() or self.uid == self.NanoVOLTSpMS.getUid() or self.uid == self.BpE.getUid():
            return ad
        if self.uid == self.FTpS.getUid() or self.uid == self.KMpS.getUid() or self.uid == self.KFTpS.getUid() or self.uid == self.KGpM3.getUid() or self.uid == self.USpFT.getUid() or self.uid == self.PERCENT.getUid() or self.uid == self.MM.getUid() or self.uid == self.CM.getUid() or self.uid == self.INCH.getUid() or self.uid == self.FT.getUid() or self.uid == self.KGpM3MpS.getUid() or self.uid == self.KGpM3FTpS.getUid() or self.uid == self.KGpM3KMpS.getUid() or self.uid == self.KGpM3KFTpS.getUid() or self.uid == self.GpCCFTpS.getUid() or self.uid == self.GpCCKMpS.getUid() or self.uid == self.GpCCKFTpS.getUid() or self.uid == self.PSI.getUid() or self.uid == self.BAR.getUid() or self.uid == self.KPA.getUid() or self.uid == self.DYNEpCM2.getUid() or self.uid == self.D.getUid() or self.uid == self.SCFpSTB.getUid() or self.uid == self.S.getUid() or self.uid == self.KM.getUid() or self.uid == self.KFT.getUid() or self.uid == self.RAD.getUid() or self.uid == self.GPAKGpM3.getUid() or self.uid == self.DYNEpCM2GpCC.getUid() or self.uid == self.DYNEpCM2KGpM3.getUid() or self.uid == self.FTUS.getUid() or self.uid == self.PPG.getUid():
            ad1 = []
            for i in range(len(ad)):
                if not math.isnan(ad[i]):
                    ad1.append(ad[i] / self.conversionToSIFactor)
                else:
                    ad1.append(0.0 / 0.0)
            return ad1
        if self.uid == self.GpCCOilDen.getUid():
            ad2 = []
            for j in range(len(ad)):
                if not math.isnan(ad[j]):
                    ad2.append(141.5 / (131.5 + ad[j]))
                else:
                    ad2.append(0.0 / 0.0)
            return ad2
        if self.uid == self.FAHRENHEIT.getUid():
            ad3 = []
            for k in range(len(ad)):
                if not math.isnan(ad[k]):
                    ad3.append((9 * ad[k]) / 5 + 32)
                else:
                    ad3.append(0.0 / 0.0)
            return ad3
        else:
            return ad

    def getUid(self):
        return self.uid

    def setUid(self, s):
        self.uid = s

    def getDisplayDecimalPlaces(self):
        return self.decimalPlaces

    @classmethod
    def getLogUnitTypes(cls):
        return cls.logUnitTypes

    @classmethod
    def getLogUnitsTypeFromIndex(cls, i):
        for logunitstype in range(len(cls.logUnitTypes)):
            if (logunitstype.index == i):
                return logunitstype
        return LogUnitsType.NOT_FOUND
    
    
    @classmethod
    def getLogUnitsType(cls, s):
        """ returns match from LogUnitsType uid """
        for name, value in iteritems(cls.logUnitTypes):   
            s1 = value.uid
            #logger.debug("--getLogUnitsType() uid: "+str(s1))
            asplit = s1.split();
            for j in range(len(asplit)):
                #logger.debug("--getLogUnitsType() s: "+str(s.strip().lower())+" asplit: "+str((asplit[j]).lower()))
                if s.strip().lower() == (asplit[j]).lower():
                    return value
                if s == "":
                    return cls.NONE
                if s == "v/v decimal":
                    return cls.FRACT
        return cls.UNKNOWN
    
    
    '''
    @classmethod
    def getLogUnitsTypeFromString(cls, s, logtype):
        """ generated source for method getLogUnitsTypeFromString """
        i = 0
        while i < len(cls.typesArrayList):
            while len(as_):
                #  logger.debug("--getLogUnitsTypeFromString() "+s+" "+as[j]);
                if 0 == s.trim().compareToIgnoreCase(as_[j]):
                    if logtype == LogType.ODEN:
                        if logunitstype == cls.API:
                            logunitstype = cls.APIOilDen
                        if logunitstype == cls.GpCC:
                            logunitstype = cls.GpCCOilDen
                    return logunitstype
                if s.matches(""):
                    return cls.NONE
                if s.matches("v/v decimal"):
                    return cls.FRACT
                j += 1
            i += 1
        return cls.UNKNOWN
    
    
    # 
    #      * TODO replace this when move to Dimension and Unit
    #      * Units specific to ParameterType
    #      * @param s
    #      * @param parametertype
    #      * @return
    #      
    @classmethod
    #@getLogUnitsTypeFromString.register(object, str, ParameterType)
    def getLogUnitsTypeFromString_0(cls, s, parametertype):
        """ generated source for method getLogUnitsTypeFromString_0 """
        i = 0
        while i < len(cls.typesArrayList):
            while len(as_):
                if 0 == s.trim().compareToIgnoreCase(as_[j]):
                    return logunitstype
                if s.matches(""):
                    return cls.NONE
                if s.matches("v/v decimal"):
                    return cls.FRACT
                j += 1
            i += 1
        return cls.UNKNOWN
    '''

LogUnitsType.UNKNOWN = LogUnitsType(1.0, "UNKNOWN", "", 2, True)
LogUnitsType.NOT_FOUND = LogUnitsType(1.0, "", "", 2, True)
LogUnitsType.MpS = LogUnitsType(1.0, "m/s", "m/s", 0, False)
LogUnitsType.FTpS = LogUnitsType(0.30480000000000002, "ft/s", "ft/s f/s", 0, False)
LogUnitsType.KMpS = LogUnitsType(1000, "km/s", "km/s", 3, False)
LogUnitsType.KFTpS = LogUnitsType(304.80000000000001, "kft/s", "kft/s", 3, False)
LogUnitsType.GpCC = LogUnitsType(1.0, "g/cm3", "g/cc g/cm3 g/cm G/C3", 2, False)
LogUnitsType.KGpM3 = LogUnitsType(0.001, "kg/m3", "kg/m3 k/m3 k/m", 0, False)
LogUnitsType.USpM = LogUnitsType(9.9999999999999995E-07, "us/m", "us/m", 0, False)
LogUnitsType.USpFT = LogUnitsType(3.280839895013123, "us/ft", "us/ft us/f", 0, False)
LogUnitsType.API = LogUnitsType(1.0, "API", "API GAPI dAPI", 0, False)
LogUnitsType.URTGpH = LogUnitsType(1.0, "uRtg/h", "uRtg/h", 0, False)
LogUnitsType.FRACT = LogUnitsType(1.0, "fract", "fract dec FRAC v/v", 2, True)
LogUnitsType.PERCENT = LogUnitsType(0.01, "%", "% PU", 0, False)
LogUnitsType.M = LogUnitsType(1.0, "m", "m meters", 2, True)
LogUnitsType.MM = LogUnitsType(0.001, "mm", "mm", 0, True)
LogUnitsType.CM = LogUnitsType(0.01, "cm", "cm", 1, True)
LogUnitsType.INCH = LogUnitsType(0.025400000000000002, "in", "inch inches in", 1, True)
LogUnitsType.FT = LogUnitsType(0.30480000000000002, "ft", "ft feet", 2, True)
LogUnitsType.CELCIUS = LogUnitsType(1.0, "degC", "c degc", 2, True)
LogUnitsType.FAHRENHEIT = LogUnitsType(1.0, "degF", "f degf", 2, True)
LogUnitsType.OHMM = LogUnitsType(1.0, "ohm.m", "Ohmm ohm.m", 5, False)
LogUnitsType.OHMFT = LogUnitsType(0.30480000000000002, "ohm.ft", "Ohmft ohm.ft", 5, False)
LogUnitsType.KGpM3MpS = LogUnitsType(0.001, "kg/m3_m/s", "kg/m3.m/s kg/m2.s", 3, False)
LogUnitsType.KGpM3FTpS = LogUnitsType(0.00030480000000000004, "kg/m3_ft/s", "kg/m3.ft/s", 3, False)
LogUnitsType.KGpM3KMpS = LogUnitsType(1.0, "kg/m3_km/s", "kg/m3.km/s", 3, False)
LogUnitsType.KGpM3KFTpS = LogUnitsType(0.30480000000000002, "kg/m3_kft/s", "kg/m3.kft/s", 3, False)
LogUnitsType.GpCCMpS = LogUnitsType(1.0, "g/cm3_m/s", "g/cc.m/s g/cm3_m/s", 3, False)
LogUnitsType.GpCCFTpS = LogUnitsType(0.30480000000000002, "g/cm3_ft/s", "g/cc.ft/s g/cm3_ft/s", 3, False)
LogUnitsType.GpCCKMpS = LogUnitsType(1000, "g/cm3_km/s", "g/cc.km/s g/cm3_km/s", 3, False)
LogUnitsType.GpCCKFTpS = LogUnitsType(304.80000000000001, "g/cm3_kft/s", "g/cc.kft/s g/cm3_kft/s", 3, False)
LogUnitsType.MPA = LogUnitsType(1.0, "MPa", "mpa", 5, False)
LogUnitsType.PSI = LogUnitsType(0.0068947573000000002, "psi", "psi", 5, False)
LogUnitsType.GPA = LogUnitsType(1.0, "GPa", "gpa", 5, False)
LogUnitsType.DYNEpCM2 = LogUnitsType(1E-10, "dyne/cm2", "dyne/cm2", 5, False)
LogUnitsType.MD = LogUnitsType(1.0, "mD", "mD", 5, False)
LogUnitsType.D = LogUnitsType(1000, "D", "D", 5, False)
LogUnitsType.PPM = LogUnitsType(1.0, "ppm", "ppm", 0, False)
LogUnitsType.VpV = LogUnitsType(1.0, "v/v", "VpV", 5, False)
LogUnitsType.SCFpSTB = LogUnitsType(0.17809439002671415, "scf/stb", "SCF/STB", 5, False)
LogUnitsType.APIOilDen = LogUnitsType(1.0, "API_od", "APIod", 5, False)
LogUnitsType.GpCCOilDen = LogUnitsType(1.0, "g/cm3_od", "GpCCod", 5, False)
LogUnitsType.MS = LogUnitsType(1.0, "ms", "ms", 0, True)
LogUnitsType.S = LogUnitsType(1000, "s", "s", 3, True)
LogUnitsType.NONE = LogUnitsType(1.0, "unitless", "none unitless", 2, True)
LogUnitsType.REFLECT = LogUnitsType(1.0, "reflectivity", "reflect", 5, True)
LogUnitsType.MV = LogUnitsType(1.0, "mV", "mv", 3, True)
LogUnitsType.KM = LogUnitsType(1000, "km", "km", 3, True)
LogUnitsType.KFT = LogUnitsType(304.80000000000001, "kft", "kft", 3, True)
LogUnitsType.RAD = LogUnitsType(57.295779513082323, "rad", "rad radians", 2, True)
LogUnitsType.DEG = LogUnitsType(1.0, "deg", "deg degrees", 1, True)
LogUnitsType.GPAGpCC = LogUnitsType(1.0, "GPa_g/cm3", "GPa_g/cc GPa_g/cm3 GPa_g/cm GPa_G/C3", 5, False)
LogUnitsType.GPAKGpM3 = LogUnitsType(0.001, "GPa_kg/m3", "GPa.kg/m3", 5, False)
LogUnitsType.DYNEpCM2GpCC = LogUnitsType(1E-10, "dyne/cm2_g/cm3", "dyne/cm2_g/cc dyne/cm2_g/cm3 dyne/cm2_g/cm dyne/cm2_G/C3", 5, False)
LogUnitsType.DYNEpCM2KGpM3 = LogUnitsType(1E-13, "dyne/cm2_kg/m3", "dyne/cm2_kg/m3", 5, False)
LogUnitsType.FTUS = LogUnitsType(0.30480060960121924, "ftUS", "ftUS feetUS", 2, True)
LogUnitsType.PPG = LogUnitsType(0.1198264, "ppg", "ppg", 4, True)
LogUnitsType.NanoVOLTSpMS = LogUnitsType(1.0, "NanoVolts/m_s", "nanoVolts/m.s", 5, True)
LogUnitsType.BAR = LogUnitsType(0.10000000000000001, "bar", "bar", 4, False)
LogUnitsType.KPA = LogUnitsType(0.001, "KPa", "kpa", 4, False)
LogUnitsType.MDpCP = LogUnitsType(1.0, "mD/cp", "mD/cp", 5, False)
LogUnitsType.BpE = LogUnitsType(1.0, "barns/electron", "barns/electron", 6, False)
LogUnitsType.KG = LogUnitsType(1.0, "kg", "kg", 2, False)
LogUnitsType.CC = LogUnitsType(1.0, "cc", "cc", 2, False)
LogUnitsType.BpCM3 = LogUnitsType(1.0, "barns/cm3", "barns/cm3", 2, False)


