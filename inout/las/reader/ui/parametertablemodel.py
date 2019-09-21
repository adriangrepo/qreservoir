from PyQt4.QtCore import (QAbstractTableModel, QModelIndex, QVariant, Qt)
  
import logging
  
logger = logging.getLogger('console')

MNEMONIC, VALUE, UNIT, DESCRIPTION = range(4)
                        
class ParameterTableModel(QAbstractTableModel):
    '''
    Qt model wrapper for parameter POPO 
    '''
    HEADERS = ["Mnemonic", "Value", "Unit", "Description"]

    def __init__(self, parameters):
        super(ParameterTableModel, self).__init__()
        self.dirty = False
        self._parameters = parameters
        
    def getParameter(self, identity):
        return self._parameters[identity]
    
    def getParameterFromIndex(self, index):
        return self._parameters[index]
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable) 
        
    def data(self, index, role=Qt.DisplayRole):
        logger.debug(">>data() index: "+str(index))
        if (not index.isValid() or
            not (0 <= index.row() < len(self._parameters))):
            return QVariant()
        parameter = self._parameters[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == MNEMONIC:
                return QVariant(parameter.mnemonic)
            elif column == VALUE:
                return QVariant(parameter.value)
            elif column == UNIT:
                return QVariant(parameter.unit)
            elif column == DESCRIPTION:
                return QVariant(parameter.description)
        return QVariant()


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == MNEMONIC:
                return QVariant("Mnemonic")
            elif section == VALUE:
                return QVariant("Value")
            elif section == UNIT:
                return QVariant("Unit")
            elif section == DESCRIPTION:
                return QVariant("Description")
        return QVariant(int(section + 1))


    def rowCount(self, index=QModelIndex()):
        return len(self._parameters)


    def columnCount(self, index=QModelIndex()):
        return 4





