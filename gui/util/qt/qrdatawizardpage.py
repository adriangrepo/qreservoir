
import sys
from PyQt4 import QtGui, QtCore

class QrDataWizardPage(QtGui.QWizardPage):
    '''
    QWizardPage with a _data field
    '''

    def __init__(self, params):
        super(QrDataWizardPage, self).__init__()
        self._data = ""
        