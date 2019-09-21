from PyQt4.QtGui import QWidget, QIcon

from gui.widgets.ui_datapusherwidget import Ui_DataPusherWidget
from globalvalues.appsettings import AppSettings
from PyQt4.QtCore import Qt, QModelIndex

import logging

logger = logging.getLogger('console')


class DataPusherWidget(QWidget, Ui_DataPusherWidget):
    '''
    DataPusherWidget widget for settings dialogs
    Right pane needs to be set (QListView of QTreeView before use)
    Left pane SelectionMode is 'ExtendedSelection' 
    see http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemview.html#SelectionMode-enum
    '''
    def __init__(self, parent=None):
        super(DataPusherWidget, self).__init__(parent)
        self.setupUi(self)
        self.setInitialState()
        
    def setInitialState(self):
        logger.debug(">>setInitialState()")
        rightArrowIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"arrow-right.png")
        self.rightArrowPushButton.setIcon(rightArrowIcon)
        upArrowIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"arrow-up-2.png")
        self.upPushButton.setIcon(upArrowIcon)
        downArrowIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"arrow-down-2.png")
        self.downPushButton.setIcon(downArrowIcon)
        deleteIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"dialog-cancel-3.png")
        self.deletePushButton.setIcon(deleteIcon)
        
    
        
