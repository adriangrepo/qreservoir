'''
Created on 31 Jan 2015

@author: a
'''
from enum import Enum


class PenLineStyles(Enum):
    solid = 1
    dashed = 2
    dotted = 5
    dash_dot = 4
    dash_dot_dot = 5
    custom_dash = 6
    no_line = 7
    
class PGPointStyles(Enum):
    circle = 1
    square = 2
    triangle = 3
    diamond = 4
    plus = 5
    
class MatPlotLibLines(object):
    #see http://matplotlib.org/users/pyplot_tutorial.html
    #and http://stackoverflow.com/questions/8409095/matplotlib-set-markers-for-individual-points-on-a-line/8409110#8409110
    lineStyles = {}
    lineStyles[PenLineStyles.solid] = '-' 
    lineStyles[PenLineStyles.dashed] = '--' 
    lineStyles[PenLineStyles.dash_dot] = '-.'
    lineStyles[PenLineStyles.dotted] = ':' 
    lineStyles[PenLineStyles.no_line]= 'None' 
    
    markerStyles = {}
    markerStyles['point'] = '.'         
    markerStyles['pixel'] = ','
    markerStyles['circle'] = 'o'
    markerStyles['triangle_down'] = 'v' 
    markerStyles['triangle_up'] = '^'
    markerStyles['triangle_left'] = '<' 
    markerStyles['triangle_right'] = '>'
    markerStyles['tri_down'] = '1'
    markerStyles['tri_up'] = '2'
    markerStyles['tri_left'] = '3'
    markerStyles['tri_right'] = '4'
    markerStyles['square'] = 's' 
    markerStyles['pentagon'] = 'p' 
    markerStyles['star'] = '*'
    markerStyles['hexagon1'] = 'h' 
    markerStyles['hexagon2'] = 'H' 
    markerStyles['plus'] = '+'  
    markerStyles['x'] = 'x'
    markerStyles['diamond'] = 'D'
    markerStyles['thin_diamond'] = 'd'
    markerStyles['vline'] = '|' 
    markerStyles['hline'] = '_'

class PlottingConstants(object):
    #plot defaults
    SINGLE_WELL_LOG_PLOT_DEPTH_MIN = 0
    SINGLE_WELL_LOG_PLOT_DEPTH_MAX = 3000
    LOG_LAYOUT_HEADER_NAME = "Log"
    LOG_LINE_WIDTH = 1.0
    LOG_LINE_STYLE = 'solid'
    LOG_MARKER_SIZE = 1.0

    LOG_CYCLES = 4
    
    
