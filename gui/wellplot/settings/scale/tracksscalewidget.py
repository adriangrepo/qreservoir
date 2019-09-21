from PyQt4.QtGui import QWidget, QButtonGroup, QDoubleValidator

import logging

from statics.types.zaxis import ZAxis
from globalvalues.appsettings import AppSettings
from statics.types.screenunitstype import ScreenUnitsType
from PyQt4.QtCore import pyqtSignal, QEvent, pyqtSlot
from PyQt4 import QtCore
from gui.wellplot.settings.scale.ui_tracksscalewidget import Ui_TracksScaleWidget


logger = logging.getLogger('console')

#TODO link up isDirty to events
class TracksScaleWidget(QWidget, Ui_TracksScaleWidget):
    '''
    TracksScaleWidget for well plot
    '''
    def __init__(self, verticalSpacing, spacingUnits, scale, primaryZType, parent=None):
        super(TracksScaleWidget, self).__init__(parent)
        self._verticalSpacing = verticalSpacing
        self._spacingUnits = spacingUnits
        self._scale = scale
        self._primaryZType = primaryZType
        self.isDirty = False
        self.setupUi(self)
        self.setGroupBox()
        self.populateUnitsCombo()
        self.setData()
        self.connectSlots()

    def setGroupBox(self):
        groupBox = QButtonGroup()
        groupBox.addButton(self.verticalSpacingRadioButton)
        groupBox.addButton(self.scaleRadioButton)
        self.verticalSpacingRadioButton.setChecked(True)
        
    def populateUnitsCombo(self):
        if self._primaryZType.z_axis_type == ZAxis.MD.uid or self._primaryZType.z_axis_type == ZAxis.TVD.uid:
            depthTypes = ScreenUnitsType.getAllDepthNames()
            self.verticalSpacingUnitsComboBox.addItems(depthTypes)
        elif self._primaryZType.z_axis_type == ZAxis.OWT.uid or self._primaryZType.z_axis_type == ZAxis.TWT.uid:
            timeTypes = ScreenUnitsType.getAllTimeNames()
            self.verticalSpacingUnitsComboBox.addItems(timeTypes)
        elif self._primaryZType.z_axis_type == ZAxis.AGE.uid:
            logger.warn("No implemented")
            if AppSettings.isDebugMode:
                raise TypeError
        else:
            logger.debug("PrimaryZType not recognised: {0}".format(self._primaryZType.z_axis_type))
            if AppSettings.isDebugMode:
                raise TypeError
            
        
    def setData(self):
        self.verticalSpacingLineEdit.setText(str(self._verticalSpacing))
        #TODO
        #self.verticalSpacingUnitsComboBox.setCurrentIndex()
        self.scaleLineEdit.setText(str(self._scale))

    def setValidators(self):
        doubleValidator = QDoubleValidator()
        doubleValidator.setBottom(0)
        self.verticalSpacingLineEdit.setValidator(doubleValidator)
        self.scaleLineEdit.setValidator(doubleValidator)
        
    def calculateScale(self):
        verticalSpacing = self.verticalSpacingLineEdit.text()
        if isinstance(verticalSpacing, float):
            units = self.verticalSpacingUnitsComboBox.currentText()

        
    @pyqtSlot(QWidget)
    def lineEditFocusOutHandler(self, widget):
        logger.debug(">>focusLost()")
        if widget.objectName() == "scaleLineEdit":
            self.calculateScale()
        elif widget.objectName() == "verticalSpacingLineEdit":
            self.calculateSpacing()
        
    def connectSlots(self):
        self._focusOutFilter = FocusOutFilter()
        self.verticalSpacingLineEdit.installEventFilter(self._focusOutFilter)  
        self.scaleLineEdit.installEventFilter(self._focusOutFilter)  
        self._focusOutFilter.lineEditFocusOut.connect(self.lineEditFocusOutHandler)
        
class FocusOutFilter(QtCore.QObject):
    #see http://stackoverflow.com/questions/15066913/how-to-connect-qlineedit-focusoutevent
    lineEditFocusOut = pyqtSignal(QWidget)
    def eventFilter(self, widget, event):
        if event.type() == QEvent.FocusOut:
            if widget.objectName() == "verticalSpacingLineEdit" or widget.objectName() == "scaleLineEdit":
                self.lineEditFocusOut.emit(widget)
            return False
        else:
            return False
    