import logging

from PyQt4.QtGui import QDialog, QVBoxLayout
from gui.widgets.itemwidget import ItemWidget
from gui.widgets.ui_basesettingsdialog import Ui_BaseSettingsDialog


logger = logging.getLogger('console')

class WellSettingsDialog(QDialog, Ui_BaseSettingsDialog):
    '''
    classdocs
    '''


    def __init__(self, well, parent= None):
        super(WellSettingsDialog, self).__init__(parent)
        self._well = well
        self.setupUi(self)
        self.addWidgets()
        self.populateData()
        
    def addWidgets(self):
        itemWidget = ItemWidget()
        vBoxlayout = QVBoxLayout()
        vBoxlayout.addWidget(itemWidget)
        self.itemTab.setLayout(vBoxlayout)
        
    def populateData(self):
        pass
    
