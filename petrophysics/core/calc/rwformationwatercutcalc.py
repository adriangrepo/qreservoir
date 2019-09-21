#!/usr/bin/env python

class RwFormationWaterCutCalc(object):
    def calcPercentFormationWater(self, rw, rmf, rrf):
        xPercent = float()
        if rrf == rw:
            xPercent = 1.0
        elif rrf == rmf:
            xPercent = 0.0
        elif (rw < rmf) and (rrf < rw):
            xPercent = 1.0
        elif (rw > rmf) and (rrf > rw):
            xPercent = 1.0
        elif (rw < rmf) and (rrf > rmf):
            xPercent = 0.0
        elif (rw > rmf) and (rrf < rmf):
            xPercent = 0.0
        else:
            xPercent = ((rw * rmf / rrf - rw) / (rmf - rw))
        xPercent = (100.0 * xPercent)
        return xPercent

