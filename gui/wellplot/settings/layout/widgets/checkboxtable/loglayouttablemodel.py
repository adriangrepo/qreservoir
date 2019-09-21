from PyQt4.QtCore import (QAbstractTableModel, QModelIndex, QVariant, Qt,
    SIGNAL)
import operator
import logging

from globalvalues.constants.plottingconstants import PlottingConstants
from PyQt4 import QtGui, QtCore
from globalvalues.appsettings import AppSettings

logger = logging.getLogger('console')

class LogLayoutTableModel(QAbstractTableModel):
    '''see http://stackoverflow.com/questions/13144486/pyqt-checkbox-delegate-inside-tableview
     QTableView can display checkboxes without a delegate. Look for the CheckStateRole. 
     If you use the proper data, setData and flags methods for your model, you should be fine without any delegate.
    '''
    def __init__(self, parent, logList, logHeaders, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.logList = logList
        self.logHeaders = logHeaders

    def rowCount(self, parent):
        return len(self.logList)

    def columnCount(self, parent):
        return len(self.logHeaders)
    
    

    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or 
            not (0 <= index.row() < len(self.logList))):
            return None
        column = index.column()
        if role == Qt.DisplayRole:
            #Magic number here but how else to specify this column?
            if column == 0:
                try:
                    logger.debug(" row: "+str(index.row())+" column: "+str(index.column()))
                    idNameList = self.logList[index.row()]
                    #check that the sub-list is correct length
                    if AppSettings.isDebugMode:
                        assert len(idNameList)==2
                    value = idNameList[1]
                    return value
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    logger.debug(message)
                    return None
            else:
                chkBoxItem = QtGui.QTableWidgetItem()
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked) 
                return chkBoxItem
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            logger.debug("--logHeadersData() "+str(self.logHeaders[col]))
            return self.logHeaders[col]
        return QAbstractTableModel.headerData(self, col, orientation, role)

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.logList = sorted(self.logList,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.logList.reverse()
        self.emit(SIGNAL("layoutChanged()"))