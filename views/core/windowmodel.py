'''
Created on 15 Mar 2015

@author: a
'''
from enum import Enum
class WindowTypes(Enum):
    #see https://docs.python.org/3/library/enum.html  use .name to get the string name
    twoD = 1
    threeD = 2
    logPlot = 3
    wellCorrelation = 4
    xyPlot = 5
    xyzPlot = 6
    
class WindowModel(object):
    '''
    Keeps track of open windows in central widget, and their focus state
    '''


    def __init__(self, params):
        self.windows = {}
        self.activeWindow = ()
        
    def setActiveWindow(self, name, type):
        self.activeWindow(name, type)
        
