import logging
from qrutilities.systemutils import SystemUtils
from statics.types.screenunitstype import ScreenUnitsType

logger = logging.getLogger('console')

class ScaleUtils(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Scale utility for screen to well use
        '''
        self._dpi = SystemUtils.getScreenDPI
        self._dpmm = SystemUtils.getScreenDPMM
        self._dpcm = SystemUtils.getScreenDPCM
        
        
    @classmethod
    def calculateScaleFromVerticalSpacing(cls, units, verticalSpacing, pyQtGraphScale):
        pass
    #TODO
    '''
        if units ==  ScreenUnitsType.MMpS.name:
            logger.debug("TODO")
        elif units == ScreenUnitsType.CMpS.name:
            logger.debug("TODO")
        elif units == ScreenUnitsType.INpS.name:
            logger.debug("TODO")
        elif units == ScreenUnitsType.MMpM.name:
            SystemUtils.getScreenDPMM
        elif units == ScreenUnitsType.CMpM.name:
            SystemUtils.getScreenDPCM
        elif units == ScreenUnitsType.INpM.name:
            dpi = SystemUtils.getScreenDPI
        elif units == ScreenUnitsType.MMpFT.name:
        elif units == ScreenUnitsType.CMpFT.name:
        elif units == ScreenUnitsType.INpFT.name:
        #per hundred of well unit - easier t
        elif units == ScreenUnitsType.MMpHM.name:
        elif units == ScreenUnitsType.CMpHM.name:
        elif units == ScreenUnitsType.INpHM.name:
        elif units == ScreenUnitsType.MMpHFT.name:
        elif units == ScreenUnitsType.CMpHFT.name:
        elif units == ScreenUnitsType.INpHFT.name:
    '''