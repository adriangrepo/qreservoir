from PyQt4 import QtGui, QtCore


from PyQt4.QtGui import QSplitter, QWidget, QScrollArea


from gui.wellplot.subplots.wellplotwidget import WellPlotWidget

class UIWellPlotPG(QtCore.QObject):

        
    def setupUI(self):
        self.mainWidget = WellPlotWidget()
        vBox = QtGui.QVBoxLayout()
        
        
        self.splitter = QSplitter(QtCore.Qt.Vertical)
        
        self.headerScrollArea = QScrollArea()
        self.headerScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.headerScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.headerScrollArea.setWidgetResizable(False)

        
        self.scrollArea = QScrollArea()  
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #Needs to be true to allow widget in scroll area size to change
        self.scrollArea.setWidgetResizable(True)
        #self.scrollArea.setWidget(self.dataWidget)
        #see http://stackoverflow.com/questions/29583927/pyqt-qscrollarea-within-qscrollarea/29584939#29584939
        self.scrollArea.horizontalScrollBar().valueChanged.connect(
            self.headerScrollArea.horizontalScrollBar().setValue)
        
        self.splitter.addWidget(self.headerScrollArea)
        self.splitter.addWidget(self.scrollArea)
        
        #test
        hBox = QtGui.QHBoxLayout()
        #set parent so can access it for widget sizing
        self.scaleWidget = QWidget()
        self.scaleWidgetLayout = QtGui.QVBoxLayout()
        self.scaleWidget.setLayout(self.scaleWidgetLayout)
        self.scaleWidget.setMinimumWidth(30)
        hBox.addWidget(self.splitter, 1)
        hBox.addWidget(self.scaleWidget)
        self.mainWidget.setLayout(hBox)
        #end test
        '''
        #uncomment following when finished test
        self.mainWidget.setLayout(vBox)
        vBox.addWidget(self.splitter)
        '''