from __future__ import absolute_import

from PyQt4.QtGui import QToolBar
from PyQt4 import QtGui, QtCore 

import logging
from views.core import centraltabwidget


logger = logging.getLogger('console')


class ToolbarWidget(QToolBar):
    ''' must be created by using ToolbarWidget.getInstance() '''
    instance = None

    @classmethod
    def getInstance(cls, parent = None):
        logger.debug(">>getInstance(cls)")
        if cls.instance is None:
            cls.instance = cls(parent)
        return cls.instance

    def __init__(self, parent = None):
        super(ToolbarWidget, self).__init__(parent)
        self.initUI()

        #self.eventObject = EventObject()
        
    def changeToolbar(self):
        #self.eventObject.toolbarChanged.emit(self)
        logger.debug(">>changeToolbar()")

        
    def initUI(self):
        importAction = QtGui.QAction('import', self)
        importAction.triggered.connect(self.importAction)
        self.addAction(importAction)
        
    def importAction(self):
        logger.debug(">>importAction()")
        
        
    def modifyToolbar(self):
        logger.debug(">>modifyToolbar")    
        #stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        
    def settingsAction(self):
        logger.debug(">>settingsAction")   
        settingsAction = QtGui.QAction( 'Settings', self)
        settingsAction.triggered.connect(self.settingsTriggered)

    def settingsTriggered(self):
        logger.debug(">>settingsTriggered") 
