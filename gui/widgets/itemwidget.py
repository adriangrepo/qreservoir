from PyQt4.QtGui import QWidget
from gui.widgets.ui_itemwidget import Ui_itemWidget
from db.base import Base
from globalvalues.constants.wellplotconstants import WellPlotConstants
from globalvalues.constants.settingsconstants import SettingsConstants



class ItemWidget(QWidget, Ui_itemWidget):
    '''
    Item widget for all settings dialogs
    '''
    def __init__(self, item, parent=None):
        super(ItemWidget, self).__init__(parent)
        #ensure we have correct table type as accessing parameters
        assert isinstance(item, Base)
        assert item is not None
        
        self._item = item
        self.isDirty = False
        self.setupUi(self)
        self.setInitialValues()
        
    def setInitialValues(self):
        self.nameLineEdit.setText(self._item.name)
        self.classLineEdit.setText(self._item.qr_classname)
        self.notesTextEdit.setText(self._item.comments)
        

    def populateHistoryTable(self):
        pass

        
        headers = SettingsConstants.SETTINGS_ITEM_HISTORY_HEADERS
        numberOfColumns = len(headers)
        self.historyTableWidget.clear()
        self.historyTableWidget.setSortingEnabled(True)
        itemCount = 0
        countIds = []
        
        #TODO when sort out how to store History
        '''
        historyItems = 
        for history in self._item.getLogTrackDatas():
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
                    logarithmicCheckBox.setData(QtCore.Qt.UserRole, str(log.id))
    
                    buttonQColor = ImageUtils.rbgToQColor(log.rgb)
                    #logger.debug("--populateCurveTable() "+log.rgb+" converted rgb: "+str(buttonQColor.getRgb()))
                    qColorButton = QColorButton()
                    qColorButton.setColor(buttonQColor)
                    qColorButton.setData(QtCore.Qt.UserRole, str(log.id))
                    
                    opacityLineEdit = QtGui.QLineEdit(log.alpha)
                    widthLineEdit = QtGui.QLineEdit(str(log.line_width))
                    styleLineEdit = QtGui.QLineEdit(log.line_style)
                    pointSizeLineEdit = QtGui.QLineEdit(str(log.point_size))
                    pointStyleLineEdit = QtGui.QLineEdit(log.point_style)
                    pointsOn = QtGui.QTableWidgetItem()
                    pointsOn.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    pointsOn.setCheckState(log.log_plot_points_on)
                    pointsOn.setData(QtCore.Qt.UserRole, str(log.id))
        
                    twItem0 = QtGui.QTableWidgetItem(nameLineEdit.text())
                    twItem0.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem1 = QtGui.QTableWidgetItem(typeLineEdit.text())
                    twItem1.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem2 = QtGui.QTableWidgetItem(unitsLineEdit.text())
                    twItem2.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem3 = QtGui.QTableWidgetItem(trackLineEdit.text())
                    twItem3.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem4 = QtGui.QTableWidgetItem(leftScaleLineEdit.text())
                    twItem4.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem5 = QtGui.QTableWidgetItem(rightScaleLineEdit.text())
                    twItem5.setData(QtCore.Qt.UserRole, str(log.id))
    
                    
                    twItem8 = QtGui.QTableWidgetItem(opacityLineEdit.text())
                    twItem8.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem9 = QtGui.QTableWidgetItem(widthLineEdit.text())
                    twItem9.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem10 = QtGui.QTableWidgetItem(styleLineEdit.text())
                    twItem10.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem11 = QtGui.QTableWidgetItem(pointSizeLineEdit.text())
                    twItem11.setData(QtCore.Qt.UserRole, str(log.id))
                    twItem12 = QtGui.QTableWidgetItem(pointStyleLineEdit.text())
                    twItem12.setData(QtCore.Qt.UserRole, str(log.id))
    
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
                    self.curveTableWidget.setItem(j+i,10, twItem10)
                    self.curveTableWidget.setItem(j+i,11, twItem11)
                    self.curveTableWidget.setItem(j+i,12, twItem12)
                    self.curveTableWidget.setItem(j+i,13, pointsOn)
        
                    #logger.debug("--populateCurveTable() j: "+str(j)+" i: "+str(i)) 
                    ids.append(log.id)  
                    j+=1 
        self.curveTableWidget.itemChanged.connect(self.curveStyleChanged)
        '''
