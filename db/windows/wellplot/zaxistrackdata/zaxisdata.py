'''
Created on 1 Jun 2015

@author: a
'''
from db.windows.wellplot.zaxistrackdata.zaxisdatabase import ZAxisDataBase

import copy

class ZAxisData(ZAxisDataBase):
    '''
    classdocs
    '''
    


    def getTypeReferenceTitle(self):
        self.z_axis_type+self.z_axis_reference_level
        
    def getTypeDisplayUnitReferenceTitle(self):
        self.z_axis_type+self.z_axis_display_units+self.z_axis_reference_level


