from __future__ import absolute_import

from PyQt4.QtGui import QTabWidget, QWidget


__centralTabWidgetInstance = None


def CentralTabWidget(*args, **kw):
    global __centralTabWidgetInstance
    if __centralTabWidgetInstance is None:
        __centralTabWidgetInstance = __CentralTabWidget(*args, **kw)
    return __centralTabWidgetInstance


class __CentralTabWidget(QTabWidget):
    
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.parent = parent
        