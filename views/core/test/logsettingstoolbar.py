
from __future__ import absolute_import

from PyQt4.QtGui import QToolBar
from PyQt4 import QtGui, QtCore 

from views.core import centraltabwidget

from views.core.test.layoutdialogtest import HeaderViewerTest



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

import logging

logger = logging.getLogger(__name__)

__Instance = None

class Communicator(QtCore.QObject):
    
    hideToolbar = QtCore.pyqtSignal() 
    showToolbar = QtCore.pyqtSignal() 

# LogSettingsToolbar Singleton
def LogSettingsToolbar(*args, **kw):
    global __Instance
    if __Instance is None:
        __Instance = __LogSettingsToolbar(*args, **kw)
    return __Instance


class __LogSettingsToolbar(QToolBar):

    def __init__(self, parent=None):
        super(QToolBar, self).__init__(parent)
        self.parent = parent
        self.well = None
        self.logSet = None
        self.communicator = Communicator()
        self.initUI()
        self.setWidgetText()
        
    def initUI(self):
        #self.toolBarRHS = QtGui.QToolBar(self.parent)
        #self.setObjectName(_fromUtf8("toolBarRHS"))
        self.actionSettings = QtGui.QAction(self.parent) 
        self.addAction(self.actionSettings)
        self.actionSettings.triggered.connect(self.actionSettingsTriggered)
        logger.debug("<<initUI() ")
            
    def emitShowToolbarSignal(self):
        logger.debug(">>emitShowToolbarSignal() ")
        self.communicator.showToolbar.emit()
        
    def actionSettingsTriggered(self):
        logger.debug(">>actionSettings()")
        centralWidget = centraltabwidget.CentralTabWidget()
        currentWidget = centralWidget.currentWidget()
        self.layoutDialogTest = HeaderViewerTest()
        dialog = HeaderViewerTest(parent = self)
        dialog.setModal(True)
        dialog.show()
        
    def setWidgetText(self):
        self.actionSettings.setText("Settings")
        