from PyQt4.QtGui import QWidget, QHBoxLayout


import logging
from gui.wellplot.settings.style.ui_wellplotstylewidget import Ui_WellPlotStyleWidget
from gui.util.qt.widgetutils import WidgetUtils
from qrutilities.imageutils import ImageUtils
from gui.widgets.qcolorbutton import QColorButton
from qrutilities.numberutils import NumberUtils

from PyQt4.Qt import QPushButton

logger = logging.getLogger('console')

class WellPlotStyleWidget(QWidget, Ui_WellPlotStyleWidget):
    '''
    CurveStyleWidget for well plot settings
    '''
    
    def __init__(self, wellPlotData, parent=None):
        super(WellPlotStyleWidget, self).__init__(parent)
        self._wellPlotData = wellPlotData
        self.isDirty = False
        self.setupUi(self)
        self.setWidgetProperties()
        if self._wellPlotData is not None:
            self.populateData()

    def setWidgetProperties(self):
        ''' sets initial ranges for sliders and combos '''
        
        self.labelBackgroundOpacitySpinBox.setMinimum(0)
        self.labelBackgroundOpacitySpinBox.setMaximum(255)
        self.trackBackgroundOpacitySpinBox.setMinimum(0)
        self.trackBackgroundOpacitySpinBox.setMaximum(255)
        self.labelForegroundOpacitySpinBox.setMinimum(0)
        self.labelForegroundOpacitySpinBox.setMaximum(255)

        
    def populateData(self):
        logger.debug(">>populateData()")
        
        
        titleOnCheckState = WidgetUtils.getQtCheckObject(self._wellPlotData.title_on)
        self.plotTitleOnCheckBox.setCheckState(titleOnCheckState)
        self.plotTitleOnCheckBox.stateChanged.connect(self.styleChanged)
        self.plotTitleLineEdit.setText(self._wellPlotData.title)
        self.plotTitleLineEdit.textChanged.connect(self.styleChanged)

        #not enabled for this version
        self.plotTitleOnCheckBox.setEnabled(False)
        self.plotTitleLineEdit.setEnabled(False)
        #track background button
        trackBackButtonQColor = ImageUtils.rgbToQColor(self._wellPlotData.plot_background_rgb)
        hBox1 = QHBoxLayout()
        self.trackBGColourBtnHolderWidget.setLayout(hBox1)
        self.trackBackgroundColorPushButton = QColorButton()
        self.trackBackgroundColorPushButton.setColor(trackBackButtonQColor)
        hBox1.addWidget(self.trackBackgroundColorPushButton)
        self.trackBackgroundColorPushButton.clicked.connect(self.styleChanged)
        
        plotBackgroundAlpha = NumberUtils.stringToInt(self._wellPlotData.plot_background_alpha)
        self.trackBackgroundOpacitySpinBox.setValue(plotBackgroundAlpha)
        self.trackBackgroundOpacitySpinBox.valueChanged.connect(self.styleChanged)
        
        singleRowCheckState = WidgetUtils.getQtCheckObject(self._wellPlotData.single_row_header_labels)
        self.singleRowLabelsCheckBox.setCheckState(singleRowCheckState)
        self.singleRowLabelsCheckBox.stateChanged.connect(self.styleChanged)
        #header label background button
        labelBackButtonQColor = ImageUtils.rgbToQColor(self._wellPlotData.label_background_rgb)
        hBox2 = QHBoxLayout()
        self.headerLabelBGColourBtnHolderWidget.setLayout(hBox2)
        self.labelBackgroundColorPushButton = QColorButton()
        self.labelBackgroundColorPushButton.setColor(labelBackButtonQColor)
        hBox2.addWidget(self.labelBackgroundColorPushButton)
        self.labelBackgroundColorPushButton.clicked.connect(self.styleChanged)
        
        labelBackgroundAlpha = NumberUtils.stringToInt(self._wellPlotData.label_background_alpha)
        self.labelBackgroundOpacitySpinBox.setValue(labelBackgroundAlpha)
        self.labelBackgroundOpacitySpinBox.valueChanged.connect(self.styleChanged)
        

        #label foreground button
        
        #labelForegroundRGB = NumberUtils.stringToInt(self._wellPlotData.label_foreground_rgb)
        labelForeButtonQColor = ImageUtils.rgbToQColor(self._wellPlotData.label_foreground_rgb)
        hBox3 = QHBoxLayout()
        self.headerLabelTextColourBtnHolderWidget.setLayout(hBox3)
        self.labelForegroundColorPushButton = QColorButton()
        self.labelForegroundColorPushButton.setColor(labelForeButtonQColor)
        hBox3.addWidget(self.labelForegroundColorPushButton)
        self.labelForegroundColorPushButton.clicked.connect(self.styleChanged)
        
        labelForegroundAlpha = NumberUtils.stringToInt(self._wellPlotData.label_foreground_alpha)
        self.labelForegroundOpacitySpinBox.setValue(labelForegroundAlpha)
        self.labelForegroundOpacitySpinBox.valueChanged.connect(self.styleChanged)
        
    def styleChanged(self):
        self.isDirty = True
        sender = self.sender()
        logger.debug("<<styleChanged() sender: "+str(sender))
    