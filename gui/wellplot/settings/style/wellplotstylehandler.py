import logging
from qrutilities.imageutils import ImageUtils
from PyQt4.QtGui import QColor
logger = logging.getLogger('console')

class WellPlotStyleHandler(object):
    '''
    classdocs
    '''


    def saveDataState(self, wellPlotData, wellPlotStyleWidget):   
        if wellPlotStyleWidget.plotTitleOnCheckBox.isChecked():
            wellPlotData.title_on = True
        else:
            wellPlotData.title_on = False
        wellPlotData.title = wellPlotStyleWidget.plotTitleLineEdit.text()
        r,g,b,a = QColor(wellPlotStyleWidget.trackBackgroundColorPushButton.color()).getRgb()
        rgbString = ImageUtils.rgbToString(r,g,b)
        wellPlotData.plot_background_rgb = rgbString
        wellPlotData.plot_background_alpha = wellPlotStyleWidget.trackBackgroundOpacitySpinBox.value()
        
        r,g,b,a = QColor(wellPlotStyleWidget.labelBackgroundColorPushButton.color()).getRgb()
        rgbString = ImageUtils.rgbToString(r,g,b)
        wellPlotData.label_background_rgb = rgbString
        wellPlotData.label_background_alpha = wellPlotStyleWidget.labelBackgroundOpacitySpinBox.value()
        
        r,g,b,a = QColor(wellPlotStyleWidget.labelForegroundColorPushButton.color()).getRgb()
        rgbString = ImageUtils.rgbToString(r,g,b)
        wellPlotData.label_foreground_rgb = rgbString
        wellPlotData.label_foreground_alpha = wellPlotStyleWidget.labelForegroundOpacitySpinBox.value()
        
        if wellPlotStyleWidget.singleRowLabelsCheckBox.isChecked():
            wellPlotData.single_row_header_labels = True
        else:
            wellPlotData.single_row_header_labels = False