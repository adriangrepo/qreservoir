from PyQt4.QtGui import QWidget


import logging
from gui.wellplot.settings.style.ui_trackstylewidget import Ui_TrackStyleWidget
from statics.types.logunitstype import LogUnitsType
from PyQt4 import QtCore, QtGui
from inout.validation.realvalidator import RealValidator
from globalvalues.constants.wellplotconstants import WellPlotConstants
from db.core.log.logdao import LogDao
from globalvalues.constants.colorconstants import ColorConstants
from gui.wellplot.settings.style.trackstylehandler import TrackStyleHandler

logger = logging.getLogger('console')

class TrackStyleWidget(QWidget, Ui_TrackStyleWidget):
    '''
    TrackStyleWidget for well plot settings
    '''
    
    def __init__(self, wellPlotData, templateSettingsDialog, parent=None):
        super(TrackStyleWidget, self).__init__(parent)
        self.isDirty = False
        self._wellPlotData = wellPlotData
        self._templateSettingsDialog = templateSettingsDialog
        self.setupUi(self)
        self.populateData()
        self.populateTrackTable()

    def setWidgetProperties(self):
        ''' sets initial ranges for sliders and combos '''

        #lutCm = LogUnitsType.CM
        logUnitsTypeMM = LogUnitsType.MM 
        #self.trackGapUnitsComboBox.addItem(lutCm.name)
        self.trackGapUnitsComboBox.addItem(logUnitsTypeMM.name)
        #self.trackWidthUnitsComboBox.addItem(lutCm.name)
        self.trackWidthUnitsComboBox.addItem(logUnitsTypeMM.name)  
        self.trackGapUnitsComboBox.setEnabled(False)
        self.trackWidthUnitsComboBox.setEnabled(False)
        self.trackGapLineEdit.setEnabled(False)
        self.trackWidthLineEdit.setEnabled(False)
        
    def setGridProperties(self):
        '''
        gridOnCheckState = WidgetUtils.getQtCheckObject(self._wellPlotData.grid_on)
        self.gridOnCheckBox.setCheckState(gridOnCheckState)
        self.gridOnCheckBox.stateChanged.connect(self.styleChanged)

        buttonQColor = ImageUtils.rbgToQColor(self._wellPlotData.grid_rgb)
        qColorButton = QColorButton()
        qColorButton.setColor(buttonQColor)
        self.gridColorPushButton = qColorButton
        self.gridColorPushButton.clicked.connect(self.styleChanged)
        
        gridAlpha = NumberUtils.stringToInt(self._wellPlotData.grid_alpha)
        self.gridOpacitySpinBox.setValue(gridAlpha)
        self.gridOpacitySpinBox.valueChanged.connect(self.styleChanged)
        
        index = self.gridStyleComboBox.findText(self._wellPlotData.grid_line_style, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.gridStyleComboBox.setCurrentIndex(index)
        self.gridStyleComboBox.currentIndexChanged.connect(self.styleChanged)

        self.gridVerticalDivSpinBox.setValue(self._wellPlotData.grid_vertical_divisions)
        self.gridVerticalDivSpinBox.valueChanged.connect(self.styleChanged)
        '''
        
    def populateData(self): 
        logger.debug(">>populateData()")
        try: 
            self.trackApplyAllCheckBox.stateChanged.disconnect(self.handleApplyAllChkClicked)
            self.trackWidthLineEdit.textChanged.disconnect(self.checkReqiredState)
            self.trackGapLineEdit.textChanged.disconnect(self.checkReqiredState)
        except TypeError as ex:
            # will be disconnected on first run, log it and continue
            logger.debug(str(ex))
  
        self.populateTrackTable()
        self.trackApplyAllCheckBox.setCheckState(QtCore.Qt.Unchecked)
        self.trackApplyAllCheckBox.stateChanged.connect(self.handleApplyAllChkClicked)
        widthValidator = RealValidator()
        widthValidator.setRange (WellPlotConstants.WELL_PLOT_TRACK_WIDTH_MIN, WellPlotConstants.WELL_PLOT_TRACK_WIDTH_MAX, WellPlotConstants.WELL_PLOT_TRACK_DECIMALS)
        self.trackWidthLineEdit.setValidator(widthValidator)
        self.trackWidthLineEdit.setText(str(WellPlotConstants.WELL_PLOT_TRACK_WIDTH_DEFAULT))
        self.trackWidthLineEdit.textChanged.connect(self.checkReqiredState)
        
        gapValidator = RealValidator()
        gapValidator.setRange (WellPlotConstants.WELL_PLOT_TRACK_GAP_MIN, WellPlotConstants.WELL_PLOT_TRACK_GAP_MAX, WellPlotConstants.WELL_PLOT_TRACK_DECIMALS)
        self.trackGapLineEdit.setValidator(gapValidator)
        self.trackGapLineEdit.setText(str(WellPlotConstants.WELL_PLOT_TRACK_GAP_DEFAULT))
        self.trackGapLineEdit.textChanged.connect(self.checkReqiredState)


    def populateTrackTable(self):
        logger.debug(">>populateTrackTable()")

        try: 
            self.trackTableWidget.itemChanged.disconnect(self.styleChanged)
        except TypeError as ex:
            logger.debug(str(ex))
        
        headers = WellPlotConstants.WELL_PLOT_TRACK_STYLE_HEADERS
        numberOfColumns = len(headers)
        self.trackTableWidget.clear()
        self.trackTableWidget.setSortingEnabled(False)
        trackStyleHander = TrackStyleHandler()
        tracks = trackStyleHander.getNumberOfDisplayedTracks(self._wellPlotData)
        self.trackTableWidget.setRowCount(tracks)
        self.trackTableWidget.setColumnCount(numberOfColumns)
        self.trackTableWidget.setHorizontalHeaderLabels(headers)
        i = 0
        if self._wellPlotData is not None:
            for plot in self._wellPlotData.getLogTrackDatas():
                logger.debug("--populateTrackTable() plot_index:{0}, is_displayed:{1} ".format(plot.plot_index, plot.is_displayed))
                if (plot.plot_index != -1) and plot.is_displayed:
                    trackLineEdit = QtGui.QLineEdit(str(plot.plot_index))
                    titleLineEdit = QtGui.QLineEdit(plot.title)
                    logNames = LogDao.getLogNamesCSV(plot._logs)
                    curvesLineEdit = QtGui.QLineEdit(logNames)
                    widthLineEdit = QtGui.QLineEdit(str(plot.track_width))
                    gapLineEdit = QtGui.QLineEdit(str(plot.track_gap))
                    
                    twItem0 = QtGui.QTableWidgetItem(trackLineEdit.text())
                    twItem0.setData(QtCore.Qt.UserRole, str(plot.plot_index))
                    #make non editable
                    twItem0.setFlags(QtCore.Qt.ItemIsEnabled)
                    
                    twItem1 = QtGui.QTableWidgetItem(titleLineEdit.text())
                    twItem1.setData(QtCore.Qt.UserRole, str(plot.plot_index))
                    
                    twItem2 = QtGui.QTableWidgetItem(curvesLineEdit.text())
                    twItem2.setData(QtCore.Qt.UserRole, str(plot.plot_index))
                    #make non editable
                    twItem2.setFlags(QtCore.Qt.ItemIsEnabled)
                    
                    twItem3 = QtGui.QTableWidgetItem(widthLineEdit.text())
                    twItem3.setData(QtCore.Qt.UserRole, str(plot.plot_index))
                    
                    twItem4 = QtGui.QTableWidgetItem(gapLineEdit.text())
                    twItem4.setData(QtCore.Qt.UserRole, str(plot.plot_index))
                    #row, column
                    self.trackTableWidget.setItem(i,0, twItem0)
                    self.trackTableWidget.setItem(i,1,  twItem1)
                    self.trackTableWidget.setItem(i,2,  twItem2)
                    self.trackTableWidget.setItem(i,3,  twItem3)
                    self.trackTableWidget.setItem(i,4,  twItem4)
                    i += 1

        self.trackTableWidget.itemChanged.connect(self.styleChanged)
    
    def handleApplyAllChkClicked(self, state): 
        if state == QtCore.Qt.Checked:
            self.trackGapUnitsComboBox.setEnabled(True)
            self.trackWidthUnitsComboBox.setEnabled(True)
            self.trackGapLineEdit.setEnabled(True)
            self.trackWidthLineEdit.setEnabled(True)
        else:
            self.trackGapUnitsComboBox.setEnabled(False)
            self.trackWidthUnitsComboBox.setEnabled(False)
            self.trackGapLineEdit.setEnabled(False)
            self.trackWidthLineEdit.setEnabled(False)
            
    def checkReqiredState(self, *args, **kwargs):
        sender = self.sender()
        validator = sender.validator()
        #Note all lineedits will have a validator
        if validator is not None:
            state = validator.validate(sender.text(), 0)[0]
            s = sender.text()
            if state == QtGui.QValidator.Acceptable and sender.text() is not "":
                color = ColorConstants.QLE_GREEN
            #elif state == QtGui.QValidator.Intermediate or sender.text() is "":
            #    color = '#fff79a' # yellow
            else:
                color = ColorConstants.QLE_RED
            sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            logger.debug("--checkState() no validator for: "+str(sender.objectName()))
            
    #def trackStyleChanged(self, twItem):
    #    self._trackStyleHander.trackStyleChanged(twItem)
        
    def styleChanged(self):
        self.isDirty = True
        sender = self.sender()
        logger.debug("<<styleChanged() sender: "+str(sender))