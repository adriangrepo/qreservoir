

from PyQt4.QtGui import QDialog
from gui.widgets.ui_okcanceldialog import Ui_OkCancelDialog


class OkCancelDialog(QDialog, Ui_OkCancelDialog):
    '''
    Base dialog
    add widgets to placeholderWidget
    '''
    def __init__(self, parent=None):
        super(OkCancelDialog, self).__init__(parent)
        self.setupUi(self)
        
