from PyQt4.QtGui import QPushButton, QColorDialog, QColor
from PyQt4.QtCore import pyqtSignal
from PyQt4.Qt import Qt
import logging
from PyQt4 import QtCore

logger = logging.getLogger('console')
#http://martinfitzpatrick.name/article/qcolorbutton-a-color-selector-tool-for-pyqt/
class QColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).    
    '''

    colorChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        logger.debug(">>__init__")
        super(QColorButton, self).__init__(*args, **kwargs)
        self._color = None
        self._data = None
        self.setMaximumWidth(100)
        self.pressed.connect(self.onColorPicker)
        self.clicked.connect(self.onColorPicker)

    def setColor(self, color):
        logger.debug(">>setColor")
        if color != self._color:
            self._color = color
            self.colorChanged.emit()
        if self._color:
            colors = QColor(self._color).getRgb()
            self.setStyleSheet("background-color: rgb{0};".format(colors))
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        '''
        Show color-picker dialog to select color.
        Qt will use the native dialog by default.
        '''
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())
            
    

    def mousePressEvent(self, e):
        logger.debug(">>mousePressEvent")
        if e.button() == Qt.RightButton:
            self.setColor(None)

        return super(QColorButton, self).mousePressEvent(e)
    
    def setData(self, role, data):
        if role == QtCore.Qt.EditRole:
            logger.debug("new value, previous value: ", data, self._data)
            self._data = data
