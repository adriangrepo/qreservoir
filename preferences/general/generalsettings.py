'''
Created on 5 Jun 2015

@author: a
'''
from enum import Enum

class WorkflowType(Enum):
    petrophysics = 1
    rockphysics = 2

__Instance = None

def GeneralSettings(*args, **kw):
    global __Instance
    if __Instance is None:
        __Instance = __GeneralSettings(*args, **kw)
    return __Instance


class __GeneralSettings(object):
    ''' similar to actions class in ninja ide '''

    workflowType = WorkflowType.petrophysics
        