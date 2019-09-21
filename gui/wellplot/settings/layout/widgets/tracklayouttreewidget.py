from PyQt4.QtCore import QModelIndex, Qt
from PyQt4.Qt import QComboBox
from PyQt4.QtGui import QApplication, QItemSelectionModel, \
                        QPushButton, QStandardItem, \
                        QStandardItemModel, QTreeView, QTreeWidget

import logging
from gui.wellplot.settings.layout.widgets.ui_tracklayouttreewidget import Ui_trackLayouttreWidget
from PyQt4 import QtCore
from gui.signals.wellplotsignals import WellPlotSignals
import pickle
from gui.util.pymimedata import PyMimeData
from db.core.log.log import Log
from db.core.logset.logset import LogSet

logger = logging.getLogger('console')


class TrackLayoutTreeWidget(QTreeWidget, Ui_trackLayouttreWidget):
    '''
    TrackLayoutTreeWidget for well plot settings
    '''
    
    
    def __init__(self, parent=None):
        super(TrackLayoutTreeWidget, self).__init__(parent)
        self.setupUi(self)
        self.wellPlotSignals = WellPlotSignals()
        self.setAcceptDrops(True)
        

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        logger.debug("--dragEnterEvent() type(mimeData) {0}".format(type(mimeData)))
        if isinstance(mimeData, PyMimeData):
            instance = mimeData.instance()
            logger.debug("--dragEnterEvent() instance")
            try:
                logger.debug("--dragEnterEvent() instance.tablename: {0}".format(instance.tablename))
                if instance.tablename == Log.__tablename__:
                    logger.debug("--dragEnterEvent() log")
                    event.accept()
                elif instance.tablename == LogSet.__tablename__:
                    event.accept()

            except:
                logger.debug("--dragEnterEvent() mimeData has no tablename property ")
        else:
            logger.debug("--dragEnterEvent() mimeData not instance of PyMimeData type(mimeData) {0}".format(type(mimeData)))
            super(TrackLayoutTreeWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        mimeData = event.mimeData()
        if isinstance(mimeData, PyMimeData):
            instance = mimeData.instance()
            try:
                if instance.tablename == Log.__tablename__:
                    event.setDropAction(QtCore.Qt.CopyAction)
                    event.accept()
                elif instance.tablename == LogSet.__tablename__:
                    event.setDropAction(QtCore.Qt.CopyAction)
                    event.accept()

            except:
                logger.debug("--dragMoveEvent() mimeData has no tablename property ")
        else:
            logger.debug("--dragMoveEvent() mimeData not instance of PyMimeData type(mimeData) {0}".format(type(mimeData)))
            super(TrackLayoutTreeWidget, self).dragEnterEvent(event)

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if isinstance(mimeData, PyMimeData):
            instance = mimeData.instance()
            logger.debug("--dropEvent() type(instance) {0}".format(type(instance)))
            try:
                if instance.tablename == Log.__tablename__:
                    event.setDropAction(QtCore.Qt.CopyAction)
                    event.accept()
                    logger.debug("--dropEvent() emit(mimeData)")
                    self.wellPlotSignals.settingsTrackLayoutItemDropped.emit(mimeData)
                elif instance.tablename == LogSet.__tablename__:
                    event.setDropAction(QtCore.Qt.CopyAction)
                    event.accept()
                    self.wellPlotSignals.settingsTrackLayoutItemDropped.emit(mimeData)
            except:
                logger.debug("--dragEnterEvent() mimeData has no tablename property ")
        else:
            logger.debug("--dropEvent() mimeData not instance of PyMimeData")
            super(TrackLayoutTreeWidget, self).dropEvent(event)
        
    
    