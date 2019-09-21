from PyQt4.QtGui import QWidget, QButtonGroup
from gui.widgets.ui_rangewidget import Ui_rangeWidget

import logging

from globalvalues.appsettings import AppSettings
from statics.types.wellplotrangetype import WellPlotRangeType
from statics.types.zaxis import ZAxis
from globalvalues.constants.wellconstants import WellConstants

logger = logging.getLogger('console')

class RangeWidget(QWidget, Ui_rangeWidget):
    '''
    Range widget for well plot 
    '''
    
    def __init__(self, rangeType, primaryZType, well, parent = None):
        super(RangeWidget, self).__init__(parent)
        self._rangeType = rangeType
        self._primaryZType = primaryZType
        self._well = well
        self.setupUi(self)
        self.populateRangeComboBox()
        self.connectSlots()

    def enableDisableRangeLines(self, isEnabled):
        self.displayStartLineEdit.setEnabled(isEnabled)
        self.displayStopLineEdit.setEnabled(isEnabled)
         
    def connectSlots(self):
        self.rangeComboBox.currentIndexChanged.connect(self.rangeComboBoxChanged)    
            
    def populateRangeComboBox(self):
        self.rangeComboBox.setEditable(False)
        rangePlotNames = WellPlotRangeType.getSubsetWellPlotRangeTypeNames(WellPlotRangeType.SET.name)
        i = 0
        for name in rangePlotNames:
            self.rangeComboBox.addItem(name, userData=None)
            i += 1
        if i > 0:
            self.rangeComboBox.insertSeparator(i)
            self.rangeComboBox.addItem(WellPlotRangeType.SET.name)
        index = self.rangeComboBox.findText(self._rangeType)
        self.rangeComboBox.setCurrentIndex(index)
        self.rangeComboBoxChanged()
        
    def rangeComboBoxChanged(self):
        rangeName = self.rangeComboBox.currentText()
        logger.debug("--rangeComboBoxChanged text: {0}".format(rangeName))
        if rangeName == WellPlotRangeType.SET.name:
            self.specifiedRangedSelected()
        elif rangeName == WellPlotRangeType.DATASTARTSTOP.name:
            self.dataStartToStopSelected()
        elif rangeName == WellPlotRangeType.ZEROSTOP.name:
            self.zeroToDataStopSelected()
        elif rangeName == WellPlotRangeType.WELL.name:
            self.wholeWellSelected()
        else:
            logger.debug("Range combo text not recognised: {0}".format(rangeName))
               
    def specifiedRangedSelected(self):
        self.enableDisableRangeLines(True)
        
    def wholeWellSelected(self):
        self.enableDisableRangeLines(False)
        if self._primaryZType.z_axis_type == ZAxis.MD.uid:
            if self._well.td_md_kb is None: 
                stop = self._well.mdstop
            elif self._well.td_md_kb < self._well.mdstop:
                stop = self._well.mdstop
            else:
                stop = self._well.td_md_kb
            self.setDisplayStartStopText(0, stop)
        else:
            logger.warn("TODO self._primaryZType: {0} not handled".format(self._primaryZType.z_axis_type))
            if AppSettings.isDebugMode:
                raise ValueError
        
    def dataStartToStopSelected(self):
        self.enableDisableRangeLines(False)
        if self._primaryZType.z_axis_type == ZAxis.MD.uid:
            if self._well.getMdLength() is None:
                logger.warn("No measured data for this well, using default value for data range")
                defaultMdStop = WellConstants.DEFAULT_MD_LENGTH
                self.setDisplayStartStopText(0, defaultMdStop)
            else:
                self.setDisplayStartStopText(self._well.mdstart, self._well.mdstop)
        else:
            logger.warn("TODO self._primaryZType: {0} not handled".format(self._primaryZType.z_axis_type))
            if AppSettings.isDebugMode:
                raise ValueError
            
    def zeroToDataStopSelected(self):
        self.enableDisableRangeLines(False)
        if self._primaryZType.z_axis_type == ZAxis.MD.uid:
            if self._well.getMdLength() is None:
                logger.warn("No measured data for this well, using default value for data range")
                defaultMdStop = WellConstants.DEFAULT_MD_LENGTH
                self.setDisplayStartStopText(0, defaultMdStop)
            else:
                self.setDisplayStartStopText(0, self._well.mdstop)
        else:
            logger.warn("TODO self._primaryZType: {0} not handled".format(self._primaryZType.z_axis_type))
            if AppSettings.isDebugMode:
                raise ValueError
            
    def setDisplayStartStopText(self, displayStart, displayStop):
        self.displayStartLineEdit.setText(str(displayStart))
        self.displayStopLineEdit.setText(str(displayStop))
            