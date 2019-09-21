from PyQt4 import QtGui, QtCore


from views.core.test.wellplottest import WellPlotTest
#from views.core.test.layoutdialogtest import LayoutDialogTest

import logging
from views.core import centraltabwidget
from PyQt4.QtGui import QMainWindow
from views.core.ui_qrbase_view import Ui_MainWindow
from views.core.test import logsettingstoolbar
#In Py3.x, QString doesn't exist in PyQt4
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(600, 400)
        self.central = centraltabwidget.CentralTabWidget(self)
        self.setCentralWidget(self.central)
        
        self.button = QtGui.QPushButton('Test', self.central)
        self.button.clicked.connect(self.handleButton)
        layout = QtGui.QVBoxLayout(self.central)
        layout.addWidget(self.button)
        self.connectRHSToolbar()
        
        #self.layoutDialogTest = LayoutDialogTest()
        #dialog = LayoutDialogTest(parent = self)
        #dialog.setModal(True)
        #dialog.show()
        
    def connectRHSToolbar(self):
        self.toolBarRHS = logsettingstoolbar.LogSettingsToolbar(self)
        self.toolBarRHS.setObjectName(_fromUtf8("toolBarRHS"))
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBarRHS)
        self.toolBarRHS.hide()
        self.toolBarRHS.communicator.showToolbar.connect(self.showRHSToolbarTriggered)
        self.toolBarRHS.communicator.hideToolbar.connect(self.hideRHSToolbarTriggered)

    def showRHSToolbarTriggered(self):
        logger.debug(">>showRHSToolbarTriggered()")
        self.toolBarRHS.show()
        
    def hideRHSToolbarTriggered(self):
        logger.debug(">>hideRHSToolbarTriggered()")
        self.toolBarRHS.hide()

    def handleButton(self):
        logger.debug(">>handleButton() pressed")
        self.wellPlotTest = WellPlotTest(self)
        #self.layoutDialogTest.notifyOnPlotsChanged()


        


if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

    
'''
if __name__=="__main__":
    #doesn't do anything...
    signaldebug.enableSignalDebugging()
    
    roimanager = ROIManager()
    snaproi = SnapROIItem()
    roimanager.add_snaproi()
    snaproi.do_something_and_emit()
'''