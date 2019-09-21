#!/usr/bin/env python

class WellBoreConstants(object):
    #  TODO Alpha C finalise these rd constants
    MIN_WELL_STEP = 1.0000000000000001E-05
    MIN_TVD_STEP = 0.15240000000000001
    MIN_TWT_STEP = 2
    MIN_ADH_STEP = 0.15240000000000001

    @classmethod
    def getMinWellStep(cls):
        return cls.MIN_WELL_STEP

    @classmethod
    def getMinTvdStep(cls):
        return cls.MIN_TVD_STEP

    @classmethod
    def getMinTwtStep(cls):
        return cls.MIN_TWT_STEP

    @classmethod
    def getMinAdhStep(cls):
        return cls.MIN_ADH_STEP

