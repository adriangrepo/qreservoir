'''
Created on 6 Apr 2015

@author: a
'''
from globalvalues.constants.siconversionconstants import SIConversionConstants
from statics.types.zaxis import ZAxis
from statics.types.referenceleveltype import ReferenceLevelType
from statics.types.unit import Unit

class WellPlotConstants(object):
    #see ip.mp4 malek et al. 2:225
    WELL_PLOT_CURVE_STYLE_HEADERS = ["Log name", "Type", "Units", "Track", "Left scale", \
                                      "Right scale", "Logarithmic", "Colour", "Opacity", \
                                      'Line thickness', "Style", "Point size", "Point style", "Points displayed"]
    WELL_PLOT_TRACK_STYLE_HEADERS= ["Track","Title","Logs","Width","Gap"]
    #min/max in inches
    WELL_PLOT_TRACK_GAP_MIN = 0
    WELL_PLOT_TRACK_GAP_MAX = 10*SIConversionConstants.MM_PER_INCH
    WELL_PLOT_TRACK_WIDTH_MIN = 0.1*SIConversionConstants.MM_PER_INCH
    WELL_PLOT_TRACK_WIDTH_MAX = 10*SIConversionConstants.MM_PER_INCH
    WELL_PLOT_TRACK_DECIMALS = 1
    #numer essentially is inches
    WELL_PLOT_TRACK_WIDTH_DEFAULT = round(1.5*SIConversionConstants.MM_PER_INCH, 2)
    WELL_PLOT_TRACK_GAP_DEFAULT = 0
    WELL_PLOT_GRID_DIVISIONS_DEFAULT = 10
    
    #Matplotlib figure related
    WELL_PLOT_FIGURE_LEFT = 0.001
    WELL_PLOT_FIGURE_BOTTOM = 0.001
    WELL_PLOT_FIGURE_RIGHT = 0.999
    WELL_PLOT_FIGURE_TOP = 0.999
    WELL_PLOT_FIGURE_WSPACE = 0.0001
    WELL_PLOT_FIGURE_HSPACE = 0.0001
    
    #500m y scale shown on plot open
    WELL_PLOT_DEFAULT_ZOOM = 500
    
    WELL_PLOT_DOMAIN_TRACK_WIDTH = 60
    
    WELL_PLOT_MAX_TRACK_NUMBER = 20
    
    mdKB = ZAxis.MD.getUid()+" "+ReferenceLevelType.KB.getAbbreviation()
    tvdMSL = ZAxis.TVD.getUid()+" "+ReferenceLevelType.MSL.getAbbreviation()
    mdRT = ZAxis.MD.getUid()+" "+ReferenceLevelType.RT.getAbbreviation()
    WELL_PLOT_DOMAIN_PRIORITY = [mdKB,tvdMSL,mdRT]
    
    WELL_PLOT_DEFAULT_Z_MEASURE_TYPE_UID = ZAxis.MD.getUid()
    WELL_PLOT_DEFAULT_Z_MEASURE_REFERENCE_UID = ReferenceLevelType.KB.getUid()
    
    OVERVIEW_LONGEST_GR_LOG = "longestGRLog"
    OVERVIEW_LONGEST_LOG = "longestLog"
    OVERVIEW_MANUAL_SELECTION = "manualSelection"