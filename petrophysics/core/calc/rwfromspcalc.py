#!/usr/bin/env python

# 
#  * 
#  * @author a
#  * 
#  
class RwFromSPCalc(object):
    """ generated source for class RwFromSPCalc """
    SP_CONSTANT1 = 25.0
    SP_CONSTANT2 = 0.17

    # 
    #      * 
    #      * @param sp
    #      * @param ri
    #      * @param rmCorrected
    #      * @param bedThickness
    #      * @param bedThicknessType
    #      * @return
    #      
    def correctedSPForBedThickness(self, sp, ri, rmCorrected, bedThickness, bedThicknessType):
        staticSP = float()
        #  convert to meters - then we know is SI then convert to feet
        if bedThicknessType != LogUnitsType.M:
            bedThickness = bedThicknessType.convertToSI(bedThickness)
        bedThicknessFt = LogUnitsType.FT.convertFromSI(bedThickness)
        staticSP = sp * (1.0 + (ri / rmCorrected + self.SP_CONSTANT1) * self.SP_CONSTANT2 * Math.pow(bedThicknessFt, -2.0))
        return staticSP

    def calcRmfeq(self, rmfStandardConditions):
        rmfeq = float()
        if rmfStandardConditions >= 0.1:
            rmfeq = (float((0.85 * rmfStandardConditions)))
        else:
            rmfeq = ((rmfStandardConditions * 146.0 - 5.0) / (337.0 * rmfStandardConditions + 77.0))
        return rmfeq

    # 
    #      * 
    #      * @param formationTemp
    #      * @param formationTempUnitsType
    #      * @param sSP
    #      * @param rmfeq
    #      * @return
    #      
    def calcRweq(self, rmfeq, sSP, formationTemp, formationTempUnitsType):
        rweq = float()
        #  double conversion in case units are in kelvin or rankin
        if formationTempUnitsType != LogUnitsType.CELCIUS and formationTempUnitsType != LogUnitsType.FAHRENHEIT:
            formationTemp = formationTempUnitsType.convertToSI(formationTemp)
        if formationTempUnitsType != LogUnitsType.FAHRENHEIT:
            formationTemp = LogUnitsType.FAHRENHEIT.convertFromSI(formationTemp)
        rweq = float((rmfeq / Math.pow(10.0, sSP / (-61.0 - 0.133 * formationTemp))))
        return rweq

    def calcRwStandardConditions(self, rweq):
        rwStandardCond = float()
        if rweq < 0.12:
            rwStandardCond = ((77.0 * rweq + 5.0) / (146.0 - 377.0 * rweq))
        else:
            rwStandardCond = (float((-(0.58 - Math.pow(10.0, 0.69 * rweq - 0.24)))))
        return rwStandardCond

    # 
    #      * @param rwStandardCond
    #      * @param logUnitsType
    #      * @param formationTemp
    #      * @return Rw of formation connate water
    #      
    def calcRw(self, rwStandardCond, formationTemp, fmnTempUnitsType):
        rw = 0.0
        if fmnTempUnitsType != LogUnitsType.CELCIUS:
            formationTemp = fmnTempUnitsType.convertToSI(formationTemp)
        rw = (float((rwStandardCond * (JLogCalcConstants.CELSIUS_STANDARD_COND_DENOMINATOR / (formationTemp + PetrophysicsConstants.ARPS_CELSIUS_CONSTANT)))))
        return rw

    def calcSalinity(self, rwStandardCond):
        x = float(((3.562 - Math.log(rwStandardCond - 0.0123) / Math.log(10.0)) / 0.955))
        salinity = float(Math.pow(10.0, x))
        return salinity

