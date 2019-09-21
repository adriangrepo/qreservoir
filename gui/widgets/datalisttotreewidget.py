from PyQt4.QtGui import QWidget, QIcon, QTreeView, QVBoxLayout, QListView

from gui.widgets.ui_datapusherwidget import Ui_DataPusherWidget
from globalvalues.appsettings import AppSettings
from PyQt4.QtCore import Qt, QModelIndex

import logging
from gui.widgets.datapusherwidget import DataPusherWidget

logger = logging.getLogger('console')


class DataListToTreeWidget(DataPusherWidget):
    '''
    DataPusherWidget widget for settings dialogs
    '''
    def __init__(self, parent=None):
        super(DataListToTreeWidget, self).__init__(parent)
        self.rightTreeView = None
        self.leftDataTypeListView = None
        self.setupRightPane()
        
    def setupLeftPane(self):
        self.leftDataTypeListView = QListView()
        vBox = QVBoxLayout()
        self.leftScrollAreaWidget.setLayout(vBox)
        vBox.addWidget(self.leftDataTypeListView)
        
    def setupRightPane(self):
        self.rightTreeView = QTreeView()
        vBox = QVBoxLayout()
        self.rightScrollAreaWidget.setLayout(vBox)
        vBox.addWidget(self.rightTreeView)
        

    def connectSlots(self):
        self.rightArrowPushButton.clicked.connect(self.rightArrowClicked)
        self.upPushButton.clicked.connect(self.upClicked)
        self.downPushButton.clicked.connect(self.downClicked)
        self.deletePushButton.clicked.connect(self.deleteClicked)
        
    def rightArrowClicked(self):
        logger.debug("rightArrowClicked")
        model = self.logTypeListView.model()
        trackList = []
        if model is not None:
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.checkState() == Qt.Checked:
                    trackList.append(item.text())
            self.populateRightListView(trackList)
            
        #see https://wiki.python.org/moin/PyQt/Reading%20selections%20from%20a%20selection%20model
    def upClicked(self):
        logger.debug("upClicked")

        promoteList = []
        indexes = self.trackListView.selectionModel().selectedIndexes()
        model = self.trackListView.model()
        parent = QModelIndex()
        #selectedItems = self.trackListView.selectionModel().selectedItems()
        for index in indexes:
            #item = model.index(index.row(), index.column(), parent)
            item = self.getComboBoxItemFromIndex(model, index)
            #promoteList.append(item)
            promoteList.append(str(item.data()))
            logger.debug("data: {0}".format(item.data()))
        promotedList = self.resortRightList(promoteList)
        self.populateTrackListView(promotedList)
        
