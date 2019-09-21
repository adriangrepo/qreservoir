
from db.core.well.wellbase import WellBase

import logging

logger = logging.getLogger('console')

class Well(WellBase):
    '''
    classdocs
    '''

    def getMdLength(self):
        '''returns measured length of wellbore, 
        NB md should always be positive'''
        if (self.mdstart is None):
            logger.debug("--getMdLength() mdstart is None")
            return None
        elif (self.mdstop is None):
            logger.debug("--getMdLength() mdstop is None")
            return None
        if self.mdstart>=0:
            if self.mdstop>=0:
                if self.mdstop>=self.mdstart:
                    difference = self.mdstop-self.mdstart
                else:
                    difference = self.mdstart-self.mdstop
            elif self.mdstop<0:
                difference = (-1)*self.mdstop+self.mdstart
        else:
            if self.mdstop>=0:
                difference =  self.mdstop+(-1)*self.mdstart
            elif self.mdstart>self.mdstop:
                difference = (-1)*self.mdstop - (-1)*self.mdstart
            else:
                difference = (-1)*self.mdstart - (-1)*self.mdstop
        return difference        