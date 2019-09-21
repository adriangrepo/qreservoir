from PyQt4.QtGui import QWidget, QIcon, QListView, QVBoxLayout, QStandardItem,\
    QStandardItemModel, QHBoxLayout, QItemSelectionModel, QAbstractItemView

from gui.widgets.ui_datapusherwidget import Ui_DataPusherWidget
from globalvalues.appsettings import AppSettings
from PyQt4.QtCore import Qt, QModelIndex

import logging
from gui.widgets.datapusherwidget import DataPusherWidget

logger = logging.getLogger('console')


class DataListToListWidget(DataPusherWidget):
    '''
    DataListToListWidget widget for settings dialogs
    '''
    def __init__(self, parent=None):
        super(DataListToListWidget, self).__init__(parent)
        self.rightListView = None
        self.leftDataTypeListView = None
        self.setupLeftPane()
        self.setupRightPane()
        self.connectSlots()
        
    def setupLeftPane(self):
        self.leftDataTypeListView = QListView()
        self.leftScrollArea.setWidgetResizable(True)
        self.leftVerticalLayout.addWidget(self.leftDataTypeListView)
        self.leftDataTypeListView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        
    def setupRightPane(self):
        self.rightListView = QListView()
        self.rightScrollArea.setWidgetResizable(True)
        self.rightVerticalLayout.addWidget(self.rightListView)
        self.rightListView.setSelectionMode(QAbstractItemView.SingleSelection)
        
    def connectSlots(self):
        self.rightArrowPushButton.clicked.connect(self.rightArrowClicked)
        self.upPushButton.clicked.connect(self.upClicked)
        self.downPushButton.clicked.connect(self.downClicked)
        self.deletePushButton.clicked.connect(self.deleteClicked)
        
    def setLeftModel(self, model):
        logger.debug(">>setLeftModel()")
        self.leftDataTypeListView.setModel(model)
        
    def populateRightListView(self, rightDataList):
        assert all(isinstance(item, str) for item in rightDataList)
        model = self.rightListView.model()
        if model is None:
            model = QStandardItemModel(self.rightListView)
        for data in rightDataList:
            item = QStandardItem(data)
            # disable checkbox as is confusing
            item.setCheckable(False)
            model.appendRow(item)
        self.rightListView.setModel(model)
        
    def rightArrowClicked(self):
        selectionModel = self.leftDataTypeListView.selectionModel()
        rightDataList = []
        if selectionModel is not None:
            indexes = selectionModel.selectedIndexes()
            for index in indexes:
                dataText = self.leftDataTypeListView.model().itemFromIndex(index).text()
                rightDataList.append(dataText)
            self.populateRightListView(rightDataList)
                
    #see https://wiki.python.org/moin/PyQt/Reading%20selections%20from%20a%20selection%20model
    def upClicked(self):
        logger.debug("upClicked")

        promoteList = []
        indexes = self.rightListView.selectionModel().selectedIndexes()
        model = self.rightListView.model()
        parent = QModelIndex()
        #selectedItems = self.rightListView.selectionModel().selectedItems()
        for index in indexes:
            #item = model.index(index.row(), index.column(), parent)
            item = self.getComboBoxItemFromIndex(model, index)
            #promoteList.append(item)
            promoteList.append(str(item.data()))
            logger.debug("data: {0}".format(item.data()))
        promotedList = self.resortRightList(promoteList)
        self.populateRightListView(promotedList)
        
    def getComboBoxItemFromIndex(self, model, index):
        parent = QModelIndex()
        item = model.index(index.row(), index.column(), parent)
        return item
        
    def downClicked(self):
        logger.debug("downClicked")
        
    def deleteClicked(self):
        logger.debug("delete clicked")
        model = self.rightListView.model()
        trackList = []
        for row in range(model.rowCount()):
            item = model.item(row)
            #keep unchecked items
            if item.checkState() == Qt.Unchecked:
                trackList.append(item)
        self.populateRightListView(trackList)
        logger.debug("deleteClicked")
        
    def resortRightList(self,  promoteList):
        trackList = self.getRightListViewStrings()
        assert all(isinstance(item, str) for item in trackList)
        for item in promoteList:
            index = trackList.index(item)
            if index>0:
                trackList.insert(index-1, trackList.pop(index))          
        return trackList
    
    def getLeftListViewStrings(self):
        model = self.leftDataTypeListView.model()
        itemList = []
        if model is not None:
            for row in range(model.rowCount()):
                item = model.item(row)
                itemList.append(item.text())
        return itemList
    
    def getRightListViewStrings(self):
        model = self.rightListView.model()
        itemList = []
        if model is not None:
            for row in range(model.rowCount()):
                item = model.item(row)
                itemList.append(item.text())
        return itemList
        
