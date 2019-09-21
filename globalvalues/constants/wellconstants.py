'''
Created on 30 Dec 2014

@author: a
'''

class WellConstants(object):
    #well settings constants
    MAX_START_DEPTH = 100000
    MIN_START_DEPTH = -100000
    
    MAX_STOP_DEPTH = 100000
    MIN_STOP_DEPTH = -100000

    MAX_X_COORDINATE = 100000
    MIN_X_COORDINATE = -100000
    MAX_Y_COORDINATE = 100000
    MIN_Y_COORDINATE = -100000
    #one hundred thousand
    MAX_ELEVATION = 100000
    MIN_ELEVATION = -100000
    
    #Well bore constants
    #TODO Alpha C finalise these rd constants
    MIN_WELL_STEP = 1.0000000000000001E-05
    MIN_TVD_STEP = 0.15240000000000001
    MIN_TWT_STEP = 2.0
    MIN_MD_STEP = 0.15240000000000001
    #used in plots when well exists but has no logs or survey
    DEFAULT_MD_LENGTH = 1000.0
    