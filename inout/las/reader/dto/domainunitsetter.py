#!/usr/bin/env python
""" generated source for module DomainUnitSetter """
# package: com.qgs.qreservoir.io.las.reader.dto


from statics.types.logtype import LogType
from statics.types.logunitstype import LogUnitsType

class DomainUnitSetter(object):
    """ generated source for class DomainUnitSetter """
    #  String depthUnits = well.getWell_depth_units();
    def findDepthUnitsMatch(self, depthUnits, logType):
        """ generated source for method findDepthUnitsMatch """
        assert isinstance(depthUnits, str), "depthUnits is not a string: %r" % depthUnits
        assert isinstance(logType, LogType), "logType is not a LogType: %r" % logType

        
        match = ""
        if (depthUnits.strip()):
            depthUnitTypes = LogType.getLogUnitsForType(logType)
            for type_ in depthUnitTypes:
                types = type_.uid
                splitArr = types.split()
                for item in splitArr:
                    if (depthUnits.lower() == item.lower()):
                        #  have a match
                        match = depthUnits
                        break

        return match

    def populateWellDepthUnits(self, well, logDomain):
        """ Used if UNITS field not found in Well Header - sets well depth units to those used in start/stop/step """
        startStopStepUnits = logDomain.log_start_unit
        match = self.findDepthUnitsMatch(startStopStepUnits, LogType.DEPTH)
        if (match):
            well.file_depth_units = match

