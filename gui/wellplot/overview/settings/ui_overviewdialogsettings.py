# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overviewdialogsettings.ui'
#
# Created: Fri Jun 12 12:17:42 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_overviewTrackSettingsDialog(object):
    def setupUi(self, overviewTrackSettingsDialog):
        overviewTrackSettingsDialog.setObjectName(_fromUtf8("overviewTrackSettingsDialog"))
        overviewTrackSettingsDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(overviewTrackSettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.overviewTabWidget = QtGui.QTabWidget(overviewTrackSettingsDialog)
        self.overviewTabWidget.setObjectName(_fromUtf8("overviewTabWidget"))
        self.detailsTab = QtGui.QWidget()
        self.detailsTab.setObjectName(_fromUtf8("detailsTab"))
        self.overviewTabWidget.addTab(self.detailsTab, _fromUtf8(""))
        self.dataTab = QtGui.QWidget()
        self.dataTab.setObjectName(_fromUtf8("dataTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dataTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.dataWidget = QtGui.QWidget(self.dataTab)
        self.dataWidget.setObjectName(_fromUtf8("dataWidget"))
        self.gridLayout = QtGui.QGridLayout(self.dataWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plotLongestDataRadioButton = QtGui.QRadioButton(self.dataWidget)
        self.plotLongestDataRadioButton.setObjectName(_fromUtf8("plotLongestDataRadioButton"))
        self.gridLayout.addWidget(self.plotLongestDataRadioButton, 0, 0, 1, 3)
        self.plotLongestWellLogRadioButton = QtGui.QRadioButton(self.dataWidget)
        self.plotLongestWellLogRadioButton.setObjectName(_fromUtf8("plotLongestWellLogRadioButton"))
        self.gridLayout.addWidget(self.plotLongestWellLogRadioButton, 1, 0, 1, 2)
        self.plotLongestOfTypeRadioButton = QtGui.QRadioButton(self.dataWidget)
        self.plotLongestOfTypeRadioButton.setObjectName(_fromUtf8("plotLongestOfTypeRadioButton"))
        self.gridLayout.addWidget(self.plotLongestOfTypeRadioButton, 2, 0, 1, 2)
        self.logTypeSelectionComboBox = QtGui.QComboBox(self.dataWidget)
        self.logTypeSelectionComboBox.setObjectName(_fromUtf8("logTypeSelectionComboBox"))
        self.gridLayout.addWidget(self.logTypeSelectionComboBox, 2, 2, 1, 1)
        self.radioButton = QtGui.QRadioButton(self.dataWidget)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.gridLayout.addWidget(self.radioButton, 3, 0, 1, 1)
        self.logSelectionComboBox = QtGui.QComboBox(self.dataWidget)
        self.logSelectionComboBox.setObjectName(_fromUtf8("logSelectionComboBox"))
        self.gridLayout.addWidget(self.logSelectionComboBox, 3, 1, 1, 2)
        self.verticalLayout_3.addWidget(self.dataWidget)
        spacerItem = QtGui.QSpacerItem(20, 108, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.overviewTabWidget.addTab(self.dataTab, _fromUtf8(""))
        self.styleTab = QtGui.QWidget()
        self.styleTab.setObjectName(_fromUtf8("styleTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.styleTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.curveScrollArea = QtGui.QScrollArea(self.styleTab)
        self.curveScrollArea.setWidgetResizable(True)
        self.curveScrollArea.setObjectName(_fromUtf8("curveScrollArea"))
        self.curveAreaWidget = QtGui.QWidget()
        self.curveAreaWidget.setGeometry(QtCore.QRect(0, 0, 370, 219))
        self.curveAreaWidget.setObjectName(_fromUtf8("curveAreaWidget"))
        self.horizontalLayout_16 = QtGui.QHBoxLayout(self.curveAreaWidget)
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.curveTableWidget = QtGui.QTableWidget(self.curveAreaWidget)
        self.curveTableWidget.setObjectName(_fromUtf8("curveTableWidget"))
        self.curveTableWidget.setColumnCount(0)
        self.curveTableWidget.setRowCount(0)
        self.horizontalLayout_16.addWidget(self.curveTableWidget)
        self.curveScrollArea.setWidget(self.curveAreaWidget)
        self.verticalLayout_2.addWidget(self.curveScrollArea)
        self.overviewTabWidget.addTab(self.styleTab, _fromUtf8(""))
        self.scaleTab = QtGui.QWidget()
        self.scaleTab.setObjectName(_fromUtf8("scaleTab"))
        self.overviewTabWidget.addTab(self.scaleTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.overviewTabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(overviewTrackSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(overviewTrackSettingsDialog)
        self.overviewTabWidget.setCurrentIndex(3)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), overviewTrackSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), overviewTrackSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(overviewTrackSettingsDialog)

    def retranslateUi(self, overviewTrackSettingsDialog):
        overviewTrackSettingsDialog.setWindowTitle(_translate("overviewTrackSettingsDialog", "Overview track settings", None))
        self.overviewTabWidget.setTabText(self.overviewTabWidget.indexOf(self.detailsTab), _translate("overviewTrackSettingsDialog", "Details", None))
        self.plotLongestDataRadioButton.setText(_translate("overviewTrackSettingsDialog", "Plot longest dataset", None))
        self.plotLongestWellLogRadioButton.setText(_translate("overviewTrackSettingsDialog", "Plot longest well log", None))
        self.plotLongestOfTypeRadioButton.setText(_translate("overviewTrackSettingsDialog", "Plot longest well log of type", None))
        self.radioButton.setText(_translate("overviewTrackSettingsDialog", "Plot log", None))
        self.overviewTabWidget.setTabText(self.overviewTabWidget.indexOf(self.dataTab), _translate("overviewTrackSettingsDialog", "Data", None))
        self.overviewTabWidget.setTabText(self.overviewTabWidget.indexOf(self.styleTab), _translate("overviewTrackSettingsDialog", "Style", None))
        self.overviewTabWidget.setTabText(self.overviewTabWidget.indexOf(self.scaleTab), _translate("overviewTrackSettingsDialog", "Scale", None))

