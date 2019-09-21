from PyQt4.QtCore import (QAbstractTableModel, QModelIndex, QVariant, Qt)
  
import logging
  
logger = logging.getLogger('console')

IMPORT, NAME, TYPE, UNIT, FILE_MNEMONIC, FILE_UNIT, FILE_DESCRIPTION = range(7)
                        
class LogTableModel(QAbstractTableModel):
    '''
    Qt model wrapper for logitem POPO
    '''
    HEADERS = ["Import", "Name", "Type", "Unit", "File type","File unit","File description"]

    def __init__(self, logs):
        logger.debug(">>__init__() len(logs): "+str(len(logs)))
        super(LogTableModel, self).__init__()
        self.dirty = False
        self.logs = logs
        
    def getLog(self, identity):
        return self.logs[identity]
    
    def getLogFromIndex(self, index):
        return self.logs[index]
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable) 
        
    def data(self, index, role=Qt.DisplayRole):
        logger.debug(">>data() index: "+str(index))
        if (not index.isValid() or
            not (0 <= index.row() < len(self.logs))):
            return QVariant()
        log = self.logs[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == IMPORT:
                return QVariant(log.importLog)
            elif column == NAME:
                logger.debug(">>data() NAME: "+str(log.name))
                return QVariant(log.name)
            elif column == TYPE:
                return QVariant(log.type)
            elif column == UNIT:
                return QVariant(log.unit)
            elif column == FILE_MNEMONIC:
                return QVariant(log.fileMnemonic)
            elif column == FILE_UNIT:
                return QVariant(log.fileUnit)
            elif column == FILE_DESCRIPTION:
                return QVariant(log.fileDescription)
        return QVariant()


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == IMPORT:
                return QVariant("Import")
            elif section == NAME:
                return QVariant("Name")
            elif section == TYPE:
                return QVariant("Owner")
            elif section == UNIT:
                return QVariant("Unit")
            elif section == FILE_MNEMONIC:
                return QVariant("File mnemonic")
            elif section == FILE_UNIT:
                return QVariant("File unit")
            elif section == FILE_DESCRIPTION:
                return QVariant("File description")
        return QVariant(int(section + 1))


    def rowCount(self, index=QModelIndex()):
        return len(self.logs)


    def columnCount(self, index=QModelIndex()):
        ''' prone to error - is there a better way? '''
        return 7


    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.logs):
            log = self.logs[index.row()]
            column = index.column()
            if column == IMPORT:
                log.importLog = value.toString()
            elif column == NAME:
                log.name = value.toString()
            elif column == TYPE:
                log.type = value.toString()
            elif column == UNIT:
                log.unit = value.toString()
            elif column == FILE_MNEMONIC:
                log.las_mnemonic = value.toString()
            elif column == FILE_UNIT:
                log.las_unit = value.toString()
            elif column == FILE_DESCRIPTION:
                log.las_description = value.toString()
            self.dirty = True
            self.dataChanged.emit(index, index)
            return True
        return False

    '''
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.logs.insert(position + row,
                              log())
        self.endInsertRows()
        self.dirty = True
        return True


    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.logs = (self.logs[:position] +
                      self.logs[position + rows:])
        self.endRemoveRows()
        self.dirty = True
        return True
    '''
