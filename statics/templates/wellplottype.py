#!/usr/bin/env python

import logging
from statics.types.rangetype import RangeType

#from base.types import LogType
from statics.types.logunitstype import LogUnitsType
from statics.types.domain import Domain
from statics.types.unit import Unit
from statics.types.logtype import LogType
from statics.types.referenceleveltype import ReferenceLevelType
from statics.types.zaxis import ZAxis



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
class WellPlotType(object):
    """ Default well plot templates """
    #define constants sole reference point
    PRIMARYZAXIS = "primaryZAxis"
    INDEX = "index"
    ZAXISUNIT = "zAxisUnit"
    ZAXISREFERENCELEVEL = "zAxisReferenceLevel"
    ZAXES= "zAxes"
    TRACKNAME= "trackName"
    TRACKS = "tracks"
    
    typeName = "Well plot template"
    uid = str()
    #  simplified name, should be unique
    name = str()
    templateTypes = {}
    templateTypeUids = {}
    
    def __init__(self, uid, name, trackDataList):
        """ generated source for method __init__ """

        self.uid = uid
        self.name = name
        self.trackDataList = trackDataList
        self.templateTypes[name] = self
        self.templateTypeUids[uid] = self
        #test
        #for templateType in self.templateTypes:
        #    logger.debug("__init__() templateType:{0} type: {1}, self.templateTypes[name]:{2}".format(templateType, type(templateType), self.templateTypes[name]))
        #end test
        
    @classmethod
    def getTemplateType(cls, name):
        """ returns object matching name from types dictionary """
        templateType = cls.templateTypes.get(name)
        if templateType == None:
            logger.debug("--getTemplateType() template type matching: {0} not found".format(name))
        return templateType
    
    @classmethod
    def getTemplateTypeFromUid(cls, uid):
        """ returns object matching uid from types uid dictionary """
        templateType = cls.templateTypeUids.get(uid)
        if templateType == None:
            logger.debug("--getTemplateTypeFromUid() template type matching uid: {0} not found".format(uid))
        return templateType
    
    @classmethod
    def getAllTemplatesStringList(cls):
        """ returns names in a list """
        templateNames = []
        for key in cls.templateTypes.keys():
            templateNames.append(key)
        return sorted(templateNames)
    
    #deprecated
    def getName(self):
        """ generated source for method toString """
        return self.name
    
    def getPrimaryZAxisDict(self):
        ''' returns primaryZAxis dict '''
        for dictItem in self.dataList:
            for key in dictItem.keys():
                if key == WellPlotType.PRIMARYZAXIS:
                    return dictItem
        
    def getSecondaryZAxesDict(self):
        ''' returns secondaryZAxes dict  '''
        for dictItem in self.dataList:
            for key in dictItem.keys():
                if key == WellPlotType.ZAXES:
                    return dictItem
        
    def getTracksDict(self):
        ''' returns tracks dict  '''
        for dictItem in self.dataList:
            for key in dictItem.keys():
                if key == WellPlotType.TRACKS:
                    return dictItem     

    
zAxis = ZAxis.NONE
zAxisClassName = zAxis.__class__.__name__
logType = LogType.GAMMA
logTypeClassName = logType.__class__.__name__
#see http://docs.python-guide.org/en/latest/scenarios/json/
#use a list so can add different types as required (eg seismic trace, wavelet etc...)
#Triple combo
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
secondaryZAxesDict = {WellPlotType.ZAXES: [{WellPlotType.INDEX: 4, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.TVD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.MSL.uid}, \
            {WellPlotType.INDEX: 5, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.TVD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.RT.uid}]}
tracksDict = {WellPlotType.TRACKS:[{WellPlotType.INDEX: 1, WellPlotType.TRACKNAME: "",logTypeClassName:[ LogType.GAMMA.name, LogType.CAL.name, LogType.SP.name]}, \
                        {WellPlotType.INDEX: 2, WellPlotType.TRACKNAME: "",logTypeClassName: [LogType.RESIS_DEEP.name, LogType.RESIS_SHALLOW.name]},
                        {WellPlotType.INDEX: 3, WellPlotType.TRACKNAME: "",logTypeClassName:  [LogType.RHO.name, LogType.POROSITY_NEUTRON.name, LogType.DENSITY_CORRECTION.name]}]}
dataList.append(zAxisDict)
dataList.append(secondaryZAxesDict)
dataList.append(tracksDict)
WellPlotType.TRIPLECOMBO = WellPlotType("triplecombo","Triple combo", dataList)


#Density Neutron
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
secondaryZAxesDict = {WellPlotType.ZAXES: [{WellPlotType.INDEX: 3, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.TVD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.MSL.uid}]}
tracksDict = {WellPlotType.TRACKS:[{WellPlotType.INDEX: 1, WellPlotType.TRACKNAME: "",logTypeClassName: [ LogType.GAMMA.name, LogType.CAL.name,  \
                        WellPlotType.INDEX, 2, WellPlotType.TRACKNAME, "",logTypeClassName,  LogType.RHO.name, LogType.POROSITY_NEUTRON.name, LogType.DENSITY_CORRECTION.name]}]}
dataList.append(zAxisDict)
dataList.append(secondaryZAxesDict)
dataList.append(tracksDict)
WellPlotType.DENSITYNEUTRON = WellPlotType("densityneutron","Density Neutron", dataList)


#Resistivity Sonic
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
secondaryZAxesDict = {WellPlotType.ZAXES: [{WellPlotType.INDEX: 4, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.TVD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.MSL.uid}]}
tracksDict = {WellPlotType.TRACKS:[{WellPlotType.INDEX:1, WellPlotType.TRACKNAME: "", logTypeClassName: [ LogType.GAMMA.name, LogType.CAL.name, \
                        WellPlotType.INDEX, 2, WellPlotType.TRACKNAME, "", logTypeClassName, LogType.RESIS_DEEP.name, LogType.RESIS_SHALLOW.name, 
                        WellPlotType.INDEX, 3, WellPlotType.TRACKNAME, "", logTypeClassName,  LogType.DT.name]}]}
dataList.append(zAxisDict)
dataList.append(secondaryZAxesDict)
dataList.append(tracksDict)
WellPlotType.RESISTIVITYSONIC = WellPlotType("resistivitysonic","Resistivity Sonic", dataList)


#Rock physics
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
secondaryZAxesDict = {WellPlotType.ZAXES: [{WellPlotType.INDEX: 6, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.TVD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.MSL.uid}]}
tracksDict = {WellPlotType.TRACKS:[{WellPlotType.INDEX: 1, WellPlotType.TRACKNAME: "", logTypeClassName: [ LogType.GAMMA.name, \
                        WellPlotType.INDEX, 2, WellPlotType.TRACKNAME, "", logTypeClassName, LogType.VP.name, 
                        WellPlotType.INDEX, 3, WellPlotType.TRACKNAME, "", logTypeClassName,  LogType.VS.name,
                        WellPlotType.INDEX, 4, WellPlotType.TRACKNAME, "", logTypeClassName,  LogType.RHO.name,
                        WellPlotType.INDEX, 5, WellPlotType.TRACKNAME, "", logTypeClassName,  LogType.AI.name]}]}
dataList.append(zAxisDict)
dataList.append(secondaryZAxesDict)
dataList.append(tracksDict)
WellPlotType.ROCKPHYSICS = WellPlotType("rockphysics","Rock physics", dataList)

#Formation evaluation
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
secondaryZAxesDict = {WellPlotType.ZAXES: [{WellPlotType.INDEX: 6, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.TVD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.MSL.uid}]}
tracksDict = {WellPlotType.TRACKS:[{WellPlotType.INDEX: 1, WellPlotType.TRACKNAME: "", logTypeClassName: [ LogType.CAL.name, LogType.SIZE.name, \
                        WellPlotType.INDEX, 2, WellPlotType.TRACKNAME, "", logTypeClassName, LogType.SP.name, LogType.GAMMA.name, 
                        WellPlotType.INDEX, 3, WellPlotType.TRACKNAME, "", logTypeClassName, LogType.RESIS_DEEP.name, LogType.RESIS_MEDIUM.name, LogType.RESIS_SHALLOW.name,
                        WellPlotType.INDEX, 4, WellPlotType.TRACKNAME, "", logTypeClassName, LogType.RHO.name, LogType.POROSITY_NEUTRON.name, LogType.DENSITY_CORRECTION.name, LogType.PHOTOELECTRIC_EFFECT.name,
                        WellPlotType.INDEX, 5, WellPlotType.TRACKNAME, "", logTypeClassName, LogType.SATURATION.name]}]}
dataList.append(zAxisDict)
dataList.append(secondaryZAxesDict)
dataList.append(tracksDict)
WellPlotType.FORMATIONEVALUATION = WellPlotType("formationevaluation","Formation evaluation", dataList)



#Generic templates
#All logs
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
dataList.append(zAxisDict)
WellPlotType.ALLLOGS = WellPlotType("alllogs","All logs", dataList)

#Active logs
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
dataList.append(zAxisDict)
WellPlotType.ACTIVELOGS = WellPlotType("activelogs","Active logs", dataList)

#Empty plot
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
dataList.append(zAxisDict)
WellPlotType.EMPTY = WellPlotType("empty","Empty plot", dataList)

#Quick plot
dataList = []
zAxisDict = {WellPlotType.PRIMARYZAXIS :{WellPlotType.INDEX: 0, WellPlotType.TRACKNAME: "",zAxisClassName: ZAxis.MD.uid, \
              WellPlotType.ZAXISUNIT: Unit.METER._symbol, \
              WellPlotType.ZAXISREFERENCELEVEL: ReferenceLevelType.KB.uid}}
dataList.append(zAxisDict)
WellPlotType.QUICKPLOT = WellPlotType("quickplot","Quick plot", dataList)
