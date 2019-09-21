'''
Created on 12 Jan 2015

@author: a
'''

class ImportExportPreferences(object):
    '''
    Preferences for all import/export related use
    '''
    #import log service, parameters
    IMPORT_ALL_LAS_DATA = False
    #direct write las data depth values ignoring header start stop
    #if false uses header start and step to calculate depth values
    HONOUR_LAS_DEPTH_VALUES = True
    #pads data out to start / stop as per las file
    PAD_DATA_TO_LAS_LIMITS = False

