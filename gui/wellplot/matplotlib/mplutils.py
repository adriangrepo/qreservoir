import numpy as np

import logging

logger = logging.getLogger('console')

class MplUtils(object):

    @classmethod 
    def getAxisLimits(cls, ax):
        ''' Warning not super accurate - use for data not frame size '''
        x = ax.get_xlim()
        y = ax.get_ylim()
        xy_pixels = ax.transData.transform(np.vstack([x,y]).T)
        xpix, ypix = xy_pixels.T
        return xpix, ypix
    
    
    @classmethod
    def calcFigCanvasWidthHeight(cls, figure):
        '''deprecated, not reliable for calculating accurate size
        calculates dimensions from axes. Caution, y not additive
        alternative to figure.canvas.get_width_height()  
        can be up to 2 pixels? out relative to get_width_height'''
        axes = figure.get_axes()
        totalW = 0
        for axis in axes:
            (xpix, ypix) = MplUtils.getAxisLimits(axis)
            dataW = xpix[1] - xpix[0]
            dataH = ypix[1] - ypix[0]
            totalW += dataW
            
        #test
        dWidth, dHeight = figure.canvas.get_width_height()
        if (float(dWidth) - totalW) >= 1.0 or (float(dWidth) - totalW) <= -1.0:
            logger.error("--calcFigCanvasWidthHeight() width: {0} differs by >1 pixel to canvas.get_width_height() width: {1}".format(totalW, dWidth))
        if (float(dHeight) - dataH) >= 1.0 or (float(dHeight) - dataH) <= -1.0:
            logger.error("--calcFigCanvasWidthHeight() height: {0} differs by >1 pixel to canvas.get_width_height() height: {1}".format(dataH, dHeight))
        #end test
        
        return totalW, dataH