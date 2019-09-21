#!/usr/bin/env python

class FormationUtility(object):
    # 
    #      * 
    #      * @return depth of midpoint of formation or zero
    #      
    def calcMidPointFormationDepth(self, top, bottom):
        midpoint = 0.0
        if bottom > top:
            midpoint = top + ((bottom - top) / 2)
        return midpoint

    def calcFormationThickness(self, top, bottom):
        thickness = 0.0
        if bottom > top:
            thickness = bottom - top
        return thickness

