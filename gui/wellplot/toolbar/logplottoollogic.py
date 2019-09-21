from __future__ import absolute_import

from PyQt4.QtGui import QWidget, QPushButton, QVBoxLayout
from gui.wellplot.settings.templatesettingsdialog import TemplateSettingsDialog
import logging
from PyQt4 import QtCore, QtGui
from views.core.toolbarwidget import ToolbarWidget
import gui.wellplot.toolbar.logsettingstoolbar as logsettingstoolbar

logger = logging.getLogger('console')


class LogPlotToolLogic(QtCore.QObject):
    
    def __init__(self, parent=None):
        super(LogPlotToolLogic, self).__init__(parent)
        self.setupUi()
        
    def settingsButtonClicked(self):
        logger.debug(">>settingsButtonClicked()")
        if self._logSet == None:
            dialog = TemplateSettingsDialog(self._well)
        else:
            dialog = TemplateSettingsDialog(self._well, self._logSet)
        dialog.exec_()
    
    def setupUi(self):
        toolbarWidget = logsettingstoolbar.LogSettingsToolbar()

        '''
        toolbarWidget.modifyToolbar()
        
        settingsAction = QtGui.QAction( 'Settings', self)
        settingsAction.triggered.connect(self.settingsTriggered)
        toolbarWidget.addAction(settingsAction)
        '''
        
        '''
        self.settingsButton = QPushButton("+")
        #button.setStyleSheet("font-size:40px;background-color:#333333;border: 2px solid #222222")
        #button.setFixedSize(40,40)
        self.settingsButton.clicked.connect(self.settingsButtonClicked)
        buttons=[self.settingsButton]
        toolWidget.setupUi(buttons)
        '''
    def settingsTriggered(self):
        logger.debug(">>settingsTriggered()")
