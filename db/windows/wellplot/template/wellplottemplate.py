'''
Created on 5 Jun 2015

@author: a
'''
from db.windows.wellplot.template.wellplottemplatebase import WellPlotTemplateBase

import logging

logger = logging.getLogger('console')

class WellPlotTemplate(WellPlotTemplateBase):
    '''
    classdocs
    '''
    
    def getZAxes(self):
        ''' _z_axes auto populated by Dao, use this accessor to be consistent with other db classes '''
        if self._z_axes is not None:
            return self._z_axes
        else:
            return None
    
    #not sure why these were commented out, revised unit tests to reflect this
    '''
    def getTracks(self):
        return self._tracks

    def getPrimaryZTrackIndex(self):
        return self._primary_z_track_index
        
    def getPrimaryZTrackName(self):
        return self._primary_z_track_name
    
    def getPrimaryZTrackType(self):
        return self._primary_z_type
    
    def getPrimaryZTrackUnit(self):
        return self._primary_z_unit
    
    def getPrimaryZTrackDisplayUnit(self):
        return self._primary_z_display_unit
    
    def getPrimaryZTrackReference(self):
        return self._primary_z_reference
    '''