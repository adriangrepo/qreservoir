'''
Created on 3 Jul 2015

@author: a
'''
from globalvalues.constants.wellconstants import WellConstants
import logging

logger = logging.getLogger('console')

class OverviewWidgetHandler(object):
    ''' Logic for OverviewWidgetHandler '''
    # zoom in/out factor
    ZOOM_FACTOR = 0.8
    
    def calcMDRegionStartStop(self, mdstart, mdstop):
        ''' calculate md start stop range '''
        regionStart = 0
        regionStop = 0
        if mdstop < WellConstants.DEFAULT_MD_LENGTH: 
            if mdstop - (WellConstants.DEFAULT_MD_LENGTH/2) < 0 :
                regionStart = mdstart
                regionStop = mdstart + WellConstants.DEFAULT_MD_LENGTH/2
            else:
                regionStart = mdstop - WellConstants.DEFAULT_MD_LENGTH/2
                regionStop = mdstop
        else:
            regionStart = mdstop - WellConstants.DEFAULT_MD_LENGTH/2
            regionStop = mdstop
        return regionStart, regionStop

    def calcZoomInMinMax(self, region):
        '''select and calc revised range based on input polarity '''
        minY, maxY = region.getRegion()
        zoomedMinY = 0
        zoomedMaxY = 0
        if minY >= 0 and maxY >= 0:
            if maxY >= minY:
                zoomedMinY, zoomedMaxY = self.calcZoomWhenMinMaxSameSign(minY, maxY, zoomIn = True)
            else:
               logger.error("Error:  minY > maxY ") 
        elif minY < 0 and maxY >= 0:
            zoomedMinY, zoomedMaxY = self.handleMinNegMaxPos(minY, maxY, paramZoomIn = True)
        elif minY >= 0 and maxY < 0:
            logger.error("Error: minY >= 0 and maxY < 0 ")
        elif minY < 0 and maxY < 0:
            zoomedMinY, zoomedMaxY = self.handleNegativeMinMax(minY, maxY, paramZoomIn = True)
        return zoomedMinY, zoomedMaxY
    
    def calcZoomWhenMinMaxSameSign(self, minY, maxY, zoomIn):
        '''Calculates revised range based on zoom factor'''
        diff = maxY - minY
        centre = diff/2 + minY
        if zoomIn:
            difZoomFactor = self.ZOOM_FACTOR * diff
            logger.debug("--calcZoomWhenMinMaxSameSign() difZoomFactor: {0}, diff: {1}, centre: {2}, maxY: {3}, minY: {4}".format(difZoomFactor, diff, centre, maxY, minY))
        else:
            #zoom out
            assert self.ZOOM_FACTOR != 0
            difZoomFactor =  diff/self.ZOOM_FACTOR
        changeAmmount = difZoomFactor/2
        logger.debug("--calcZoomWhenMinMaxSameSign() changeAmmount: {0}".format(changeAmmount))

        zoomedMinY = centre - changeAmmount
        zoomedMaxY = centre + changeAmmount
        return zoomedMinY, zoomedMaxY
    
    def calcZoomOutMinMax(self, region):
        '''select and calc revised range based on input polarity '''
        minY, maxY = region.getRegion()
        zoomedMinY = 0
        zoomedMaxY = 0
        if minY >= 0 and maxY >= 0:
            zoomedMinY, zoomedMaxY = self.calcZoomWhenMinMaxSameSign(minY, maxY, zoomIn = False)
        elif minY < 0 and maxY >= 0:
            zoomedMinY, zoomedMaxY = self.handleMinNegMaxPos(minY, maxY, paramZoomIn = False)
        elif minY >= 0 and maxY < 0:
            logger.error("minY>=0 and maxY < 0 should not happen")
        elif minY < 0 and maxY < 0:
            zoomedMinY, zoomedMaxY = self.handleNegativeMinMax(minY, maxY, paramZoomIn = False)
        return zoomedMinY, zoomedMaxY
    
    def handleNegativeMinMax(self, minY, maxY, paramZoomIn):
        '''Both min, max are -ve, flip, calc, flip back'''
        zoomedMinY = 0
        zoomedMaxY = 0
        if minY <= maxY:
            #swap order as -ve
            minY,maxY = maxY *(-1), minY *(-1)
            zoomedMinY, zoomedMaxY = self.calcZoomWhenMinMaxSameSign(minY, maxY, zoomIn = paramZoomIn)
            #swap back
            zoomedMinY, zoomedMaxY = zoomedMaxY *(-1), zoomedMinY *(-1)
        else:
            logger.error("Error:  minY > maxY (both minY < 0 and maxY < 0)")
        return zoomedMinY, zoomedMaxY
    
    def handleMinNegMaxPos(self, minY, maxY, paramZoomIn):
        zoomedMinY = 0
        zoomedMaxY = 0
        diff = maxY + (-1)*minY
        centre = diff/2 + minY
        if paramZoomIn:
            difZoomFactor = self.ZOOM_FACTOR * diff
        else:
            assert self.ZOOM_FACTOR != 0
            difZoomFactor =  diff/self.ZOOM_FACTOR
        changeAmmount = difZoomFactor/2
        zoomedMinY = centre - changeAmmount
        zoomedMaxY = centre + changeAmmount
        return zoomedMinY, zoomedMaxY
        
    
    
