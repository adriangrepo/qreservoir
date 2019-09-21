import collections
import importlib
import sys, random, re, os
import warnings
from globalvalues.appsettings import AppSettings
from PyQt4.QtGui import QColor
from qrutilities.numberutils import NumberUtils
try:
    import numpy
except ImportError:
    numpy = None
    import array
    
import logging

logger = logging.getLogger('console')
    
CLEAR_ALPHA = 0xFFFFFF00 # & to ARGB color int to get rid of alpha channel
MAX_RGBA = 0xFFFFFFFF
MAX_COMPONENT = 0xFF
SOLID = 0x000000FF # + to RGB color int to get a solid RGBA color int
DEFAULTRGBCOMPONENT = 0
DEFAULTALPHACOMPONENT = 255


class ImageUtils(object):
    '''
    classdocs
    '''

    @classmethod
    def rgbaToMPLrgba(cls, rgb, alpha):
        ''' convert rgba comma sep string to matplotlib tuple '''
        mpl_rgba = []
        if rgb != None:
            rgba_split = rgb.split(",")
            DEF_RGB = 0
            DEF_ALPHA = 1
            #test:
            #logger.debug("--rgbaToMPLrgba() raw alpha: "+str(alpha))
            #end test
            try:
                for component in rgba_split:
                    #test:
                    #logger.debug("--rgbaToMPLrgba() raw: "+str(component))
                    #end test
                    if component != 0:
                        mpl_comp = int(component)/255
                    else:
                        mpl_comp = DEF_RGB
                    mpl_rgba.append(mpl_comp)
                if alpha != 0:
                    mpl_rgba.append(int(alpha)/255)
                else:
                    mpl_rgba.append(0)
            except ValueError as e:
                logger.error("--rgbaToMPLrgba() "+str(e))
                if AppSettings.isDebugMode:
                    raise ValueError
                mpl_rgba =(DEF_RGB, DEF_RGB, DEF_RGB, DEF_ALPHA)
            #test:
            #for val in mpl_rgba:
            #    logger.debug("--rgbaToMPLrgba() converted: "+str(val))
            #end test
        else:
            logger.error("--rgbaToMPLrgba() NoneType input")
            if AppSettings.isDebugMode:
                raise AttributeError
        return mpl_rgba
    
    @classmethod
    def rbgaTointValues(self, rgb, alpha):
        (r, g, b, alpha) = (255, 255, 255, 255)
        try:
            (r, g, b) = [int(s) for s in rgb.split(',')]
            alpha = int(alpha)
        except ValueError as e:
            logger.error("--rbgaTointValues() "+str(e))
            if AppSettings.isDebugMode:
                raise ValueError
        return r, g, b, alpha
    
    @classmethod
    def rbgTointValues(self, rgb):
        (r, g, b) = (255, 255, 255)
        try:
            (r, g, b) = [int(s) for s in rgb.split(',')]
        except ValueError as e:
            logger.error("--rbgaTointValues() "+str(e))
            if AppSettings.isDebugMode:
                raise ValueError
        return r, g, b
    
    @classmethod
    def randomRGBColor(cls):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgb = ",".join([str(r), str(g), str(b)] )
        return ImageUtils.rgbToQColor(rgb)
    
    @classmethod
    def randomRGBAColor(cls):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        a = random.randint(0, 255)
        rgb = ",".join([str(r), str(g), str(b)] )
        return ImageUtils.rbgaToQColor(rgb, str(a))
        
    
    @classmethod
    def rgbToQColor(cls, rgb):
        logger.debug(">>rgbToQColor() rgb:{0}".format(rgb))
        color = None
        if rgb != None and isinstance(rgb, str):
            (r, g, b) = (255, 255, 255)
            try:
                (r, g, b) = [int(s) for s in rgb.split(',')]
                color = QColor(r, g, b)
            except ValueError as e:
                logger.error("--rgbToQColor() "+str(e))
                if AppSettings.isDebugMode:
                    raise ValueError
        else:
            logger.error("--rgbToQColor() rgb input is None/not a string")
        return color
    
    @classmethod
    def rbgaToQColor(cls, rgb, alpha):
        (r, g, b, alpha) = (255, 255, 255, 255)
        color = None
        try:
            (r, g, b) = [int(s) for s in rgb.split(',')]
            alpha = int(alpha)
            color = QColor(r, g, b, alpha)
        except ValueError as e:
            logger.error("--rbgaToQColor() "+str(e))
            if AppSettings.isDebugMode:
                raise ValueError
        return color
    
    @classmethod
    def checkIntColorValue(cls, band):
        if isinstance(band, int):
            if band>=0 and band <=255:
                return True
        return False
    
    @classmethod
    def checkColorValue(cls, band):
        if isinstance(band, str):
            value = NumberUtils.stringToInt(band)
            return ImageUtils.checkIntColorValue(value)
        elif isinstance(band, int):
            return ImageUtils.checkIntColorValue(band)
        return False

    @classmethod
    def rgbToString(cls, r, g, b):
        colourList = []
        if ImageUtils.checkColorValue(r):
            if ImageUtils.checkColorValue(g):
                if ImageUtils.checkColorValue(b):
                    colourList.append(str(r))
                    colourList.append(str(g))
                    colourList.append(str(b))
                    rgbString = ",".join(colourList )
                    return rgbString
        else:
            logger.error("r,g,b value not valid")
            return ""
