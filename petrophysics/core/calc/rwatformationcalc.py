#!/usr/bin/env python

#  Performs calculations on ReservoirFluidCalcModel
#  * 
#  * @author a
#  *
#  
class RwAtFormationCalc(object):
    def ppmNaCalFromSpecialStandardResistivity(self, fluidResistivity):
        """ generated source for method ppmNaCalFromSpecialStandardResistivity """
        d = (3.562 - Math.log(fluidResistivity - 0.0123) / Math.log(10.0)) / 0.955
        ppmNaCl = float(Math.pow(10.0, d))
        return ppmNaCl

    def sigmaFormationWater(self, salinity):
        d = 0.001 * salinity
        sigmaWater = float((22.195699999999999 + 0.3384 * d + 0.00017587 * d * d + 1.34E-007 * d * d * d))
        return sigmaWater

    def temperatureGadient(self, bottmHoleTemp, surfaceTemp, totalDepth, surfaceDepth):
        gradient = ((bottmHoleTemp - surfaceTemp) / (totalDepth - surfaceDepth))
        return gradient

    def reservoirTemperature(self, gradient, reservoirDepth, surfaceDepth, surfaceTemperature):
        reservoirTemperature = float((gradient * (reservoirDepth - surfaceDepth) + surfaceTemperature))
        return reservoirTemperature

    def specialStandardResistivity(self, measuredResistivity, measuredTemperature, reservoirTemperature):
        specialResistivity = (measuredResistivity * ((measuredTemperature + PetrophysicsConstants.ARPS_CELSIUS_CONSTANT) / 45.390000000000001))
        return specialResistivity

