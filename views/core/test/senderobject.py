from PyQt4 import QtCore as QC
import logging

logger = logging.getLogger(__name__)

__SOInstance = None

def SenderObject(*args, **kw):
    global __SOInstance
    if __SOInstance is None:
        __SOInstance = __SenderObject(*args, **kw)
    return __SOInstance


class __SenderObject(QC.QObject):
    ''' general signal object '''
    something_happened = QC.pyqtSignal()
    core_event = QC.pyqtSignal()
    #emit signal when plot has been changed
    logPlotSettingsModified = QC.pyqtSignal()
    
    def __init__(self):
        QC.QObject.__init__(self)