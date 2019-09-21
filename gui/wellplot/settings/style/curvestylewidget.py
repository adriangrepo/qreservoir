import logging

from PyQt4.QtGui import QWidget, QComboBox
from PyQt4 import QtGui, QtCore, Qt

from gui.wellplot.settings.style.ui_curvestylewidget import Ui_CurveStyleWidget
from globalvalues.constants.wellplotconstants import WellPlotConstants
from statics.types.logtype import LogType
from qrutilities.imageutils import ImageUtils
from gui.widgets.qcolorbutton import QColorButton
from globalvalues.constants.plottingconstants import PGPointStyles,\
    PenLineStyles


logger = logging.getLogger('console')

class CurveStyleWidget(QWidget, Ui_CurveStyleWidget):
    '''
    CurveStyleWidget for well plot settings
    '''
    
    def __init__(self, wellPlotData, parent=None):
        super(CurveStyleWidget, self).__init__(parent)
        self._wellPlotData = wellPlotData
        self.setupUi(self)
        self.populateCurveTable()
        self.isDirty = False
        
    

    def populateCurveTable(self):
        logger.debug(">>populateCurveTable()")
        try: 
            self.curveTableWidget.itemChanged.disconnect(self.styleChanged)
        except TypeError as ex:
            logger.debug(str(ex))
        
        headers = WellPlotConstants.WELL_PLOT_CURVE_STYLE_HEADERS
        numberOfColumns = len(headers)
        self.curveTableWidget.clear()
        self.curveTableWidget.setSortingEnabled(False)
        logCount = 0
        countIds = []
        if self._wellPlotData is not None:
            for plot in self._wellPlotData.getLogTrackDatas():
                for log in  plot.getLogs():
                    #only want unique curve attributes
                    if log.id not in countIds:
                        logCount += 1
                        countIds.append(log.id) 
            self.curveTableWidget.setRowCount(logCount)
            self.curveTableWidget.setColumnCount(numberOfColumns)
            self.curveTableWidget.setHorizontalHeaderLabels(headers)
            #only want unique curve attributes
            ids = []
            for i, plot in enumerate(self._wellPlotData.getLogTrackDatas()):
                j = 0
                for log in  plot.getLogs():
                    if log.id not in ids:
                        #add one so starts at 1 not zero?
                        nameLineEdit = QtGui.QLineEdit(log.name)
                        typeLineEdit = QtGui.QLineEdit(log.log_type_name)
                        logType = LogType.getLogType(log.log_type_name)
                        unit = logType.getUnit()
                        unitsLineEdit = QtGui.QLineEdit(unit.getName())
                        trackLineEdit = QtGui.QLineEdit(str(plot.plot_index))
                        leftScaleLineEdit = QtGui.QLineEdit(str(log.log_plot_left))
                        rightScaleLineEdit = QtGui.QLineEdit(str(log.log_plot_right))
                        
                        logarithmicCheckBox = QtGui.QTableWidgetItem()
                        logarithmicCheckBox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        logarithmicCheckBox.setCheckState(log.is_logarithmic)
                        logarithmicCheckBox.setData(QtCore.Qt.UserRole, (plot, log))
    
                        buttonQColor = ImageUtils.rgbToQColor(log.rgb)
                        #logger.debug("--populateCurveTable() "+log.rgb+" converted rgb: "+str(buttonQColor.getRgb()))
                        qColorButton = QColorButton()
                        qColorButton.setColor(buttonQColor)
                        qColorButton.setData(QtCore.Qt.UserRole, (plot, log))
                        
                        opacityLineEdit = QtGui.QLineEdit(log.alpha)
                        widthLineEdit = QtGui.QLineEdit(str(log.line_width))
                        
                        lineStylesCombo = QComboBox()
                        for lineStyle in PenLineStyles:
                            lineStylesCombo.addItem(lineStyle.name)

                        pointSizeLineEdit = QtGui.QLineEdit(str(log.point_size))
                        
                        pointStylesCombo = QComboBox()
                        for pointStyle in PGPointStyles:
                            pointStylesCombo.addItem(pointStyle.name)

                        index = pointStylesCombo.findText(log.point_style, QtCore.Qt.MatchFixedString)
                        if index >= 0:
                            pointStylesCombo.setCurrentIndex(index)
                        
                        pointsOn = QtGui.QTableWidgetItem()
                        pointsOn.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        pointsOn.setCheckState(log.log_plot_points_on)
                        pointsOn.setData(QtCore.Qt.UserRole, (plot, log))
        
                        twItem0 = QtGui.QTableWidgetItem(nameLineEdit.text())
                        twItem0.setData(QtCore.Qt.UserRole,  (plot, log))
                        #lock the cell to editing
                        twItem0.setFlags(QtCore.Qt.ItemIsEnabled)
                        twItem1 = QtGui.QTableWidgetItem(typeLineEdit.text())
                        twItem1.setData(QtCore.Qt.UserRole,  (plot, log))
                        twItem1.setFlags(QtCore.Qt.ItemIsEnabled)
                        twItem2 = QtGui.QTableWidgetItem(unitsLineEdit.text())
                        twItem2.setData(QtCore.Qt.UserRole,  (plot, log))
                        twItem2.setFlags(QtCore.Qt.ItemIsEnabled)
                        twItem3 = QtGui.QTableWidgetItem(trackLineEdit.text())
                        twItem3.setData(QtCore.Qt.UserRole,  (plot, log))
                        twItem3.setFlags(QtCore.Qt.ItemIsEnabled)
                        twItem4 = QtGui.QTableWidgetItem(leftScaleLineEdit.text())
                        twItem4.setData(QtCore.Qt.UserRole,  (plot, log))
                        twItem5 = QtGui.QTableWidgetItem(rightScaleLineEdit.text())
                        twItem5.setData(QtCore.Qt.UserRole,  (plot, log))
    
                        twItem8 = QtGui.QTableWidgetItem(opacityLineEdit.text())
                        twItem8.setData(QtCore.Qt.UserRole,  (plot, log))
                        twItem9 = QtGui.QTableWidgetItem(widthLineEdit.text())
                        twItem9.setData(QtCore.Qt.UserRole,  (plot, log))
                        
                        twItem11 = QtGui.QTableWidgetItem(pointSizeLineEdit.text())
                        twItem11.setData(QtCore.Qt.UserRole,  (plot, log))

    
                        #row, column
                        self.curveTableWidget.setItem(j+i,0,  twItem0)
                        self.curveTableWidget.setItem(j+i,1,  twItem1)
                        self.curveTableWidget.setItem(j+i,2, twItem2)
                        self.curveTableWidget.setItem(j+i,3, twItem3)
                        self.curveTableWidget.setItem(j+i,4,  twItem4)
                        self.curveTableWidget.setItem(j+i,5, twItem5)
                        self.curveTableWidget.setItem(j+i,6, logarithmicCheckBox)
                        self.curveTableWidget.setCellWidget(j+i,7, qColorButton)
                        self.curveTableWidget.setItem(j+i,8, twItem8)
                        self.curveTableWidget.setItem(j+i,9, twItem9)
                        self.curveTableWidget.setCellWidget(j+i,10, lineStylesCombo)
                        self.curveTableWidget.setItem(j+i,11, twItem11)
                        self.curveTableWidget.setCellWidget(j+i,12, pointStylesCombo)
                        self.curveTableWidget.setItem(j+i,13, pointsOn)
        
                        #logger.debug("--populateCurveTable() j: "+str(j)+" i: "+str(i)) 
                        ids.append(log.id)  
                        j+=1 
        self.curveTableWidget.itemChanged.connect(self.styleChanged)

        
    def styleChanged(self):
        self.isDirty = True
        sender = self.sender()
        logger.debug("<<styleChanged() sender: "+str(sender))
    