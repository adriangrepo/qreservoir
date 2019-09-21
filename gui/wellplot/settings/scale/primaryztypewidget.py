from PyQt4.QtGui import QWidget



import logging
from gui.wellplot.settings.scale.ui_primaryztypewidget import Ui_PrimaryZTypeWidget
logger = logging.getLogger('console')

class PrimaryZTypeWidget(QWidget, Ui_PrimaryZTypeWidget):
    '''
    PrimaryZTypeWidget for well plot 
    '''
    
    def __init__(self, primaryZType, primaryZReference, parent=None):
        super(PrimaryZTypeWidget, self).__init__(parent)
        self._primaryZType = primaryZType
        self._primaryZReference = primaryZReference
        self.setupUi(self)
        self.isDirty = False
        self.setMeasurementTypeData()

    def setMeasurementTypeData(self):
        self.measurementTypeLineEdit.setText(self._primaryZType)
        #TODO
        self.measurementTypeUnitsLineEdit.setText("")
        self.datumLineEdit.setText(self._primaryZReference)

        
    
    