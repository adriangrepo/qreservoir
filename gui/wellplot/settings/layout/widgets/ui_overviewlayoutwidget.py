# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overviewlayoutwidget.ui'
#
# Created: Sun Jun 28 08:46:24 2015
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

class Ui_OverviewLayoutWidget(object):
    def setupUi(self, OverviewLayoutWidget):
        OverviewLayoutWidget.setObjectName(_fromUtf8("OverviewLayoutWidget"))
        OverviewLayoutWidget.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(OverviewLayoutWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.layoutButtonWidget = QtGui.QWidget(OverviewLayoutWidget)
        self.layoutButtonWidget.setObjectName(_fromUtf8("layoutButtonWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutButtonWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grRadioButton = QtGui.QRadioButton(self.layoutButtonWidget)
        self.grRadioButton.setObjectName(_fromUtf8("grRadioButton"))
        self.gridLayout.addWidget(self.grRadioButton, 0, 0, 1, 1)
        self.longestLogRadioButton = QtGui.QRadioButton(self.layoutButtonWidget)
        self.longestLogRadioButton.setObjectName(_fromUtf8("longestLogRadioButton"))
        self.gridLayout.addWidget(self.longestLogRadioButton, 1, 0, 1, 1)
        self.specifyDataRadioButton = QtGui.QRadioButton(self.layoutButtonWidget)
        self.specifyDataRadioButton.setObjectName(_fromUtf8("specifyDataRadioButton"))
        self.gridLayout.addWidget(self.specifyDataRadioButton, 2, 0, 1, 1)
        self.lineEditLongestLog = QtGui.QLineEdit(self.layoutButtonWidget)
        self.lineEditLongestLog.setEnabled(False)
        self.lineEditLongestLog.setObjectName(_fromUtf8("lineEditLongestLog"))
        self.gridLayout.addWidget(self.lineEditLongestLog, 1, 1, 1, 1)
        self.lineEditLongestGRLog = QtGui.QLineEdit(self.layoutButtonWidget)
        self.lineEditLongestGRLog.setEnabled(False)
        self.lineEditLongestGRLog.setObjectName(_fromUtf8("lineEditLongestGRLog"))
        self.gridLayout.addWidget(self.lineEditLongestGRLog, 0, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.layoutButtonWidget)
        self.selectDataWidget = QtGui.QWidget(OverviewLayoutWidget)
        self.selectDataWidget.setObjectName(_fromUtf8("selectDataWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.selectDataWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.typeComboBox = QtGui.QComboBox(self.selectDataWidget)
        self.typeComboBox.setObjectName(_fromUtf8("typeComboBox"))
        self.gridLayout_2.addWidget(self.typeComboBox, 2, 1, 1, 1)
        self.dataComboBox = QtGui.QComboBox(self.selectDataWidget)
        self.dataComboBox.setObjectName(_fromUtf8("dataComboBox"))
        self.gridLayout_2.addWidget(self.dataComboBox, 6, 1, 1, 1)
        self.DataTypeLabel = QtGui.QLabel(self.selectDataWidget)
        self.DataTypeLabel.setObjectName(_fromUtf8("DataTypeLabel"))
        self.gridLayout_2.addWidget(self.DataTypeLabel, 2, 0, 1, 1)
        self.dataClassComboBox = QtGui.QComboBox(self.selectDataWidget)
        self.dataClassComboBox.setObjectName(_fromUtf8("dataClassComboBox"))
        self.gridLayout_2.addWidget(self.dataClassComboBox, 1, 1, 1, 1)
        self.dataLabel = QtGui.QLabel(self.selectDataWidget)
        self.dataLabel.setObjectName(_fromUtf8("dataLabel"))
        self.gridLayout_2.addWidget(self.dataLabel, 6, 0, 1, 1)
        self.dataClassLabel = QtGui.QLabel(self.selectDataWidget)
        self.dataClassLabel.setObjectName(_fromUtf8("dataClassLabel"))
        self.gridLayout_2.addWidget(self.dataClassLabel, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.selectDataWidget)
        spacerItem = QtGui.QSpacerItem(17, 114, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(OverviewLayoutWidget)
        QtCore.QMetaObject.connectSlotsByName(OverviewLayoutWidget)

    def retranslateUi(self, OverviewLayoutWidget):
        OverviewLayoutWidget.setWindowTitle(_translate("OverviewLayoutWidget", "Form", None))
        self.grRadioButton.setToolTip(_translate("OverviewLayoutWidget", "Plot longest GR log. Disabled if no GR log exists", None))
        self.grRadioButton.setText(_translate("OverviewLayoutWidget", "Longest gamma ray (GR) log", None))
        self.longestLogRadioButton.setToolTip(_translate("OverviewLayoutWidget", "Plots longest log of any type", None))
        self.longestLogRadioButton.setText(_translate("OverviewLayoutWidget", "Longest log", None))
        self.specifyDataRadioButton.setToolTip(_translate("OverviewLayoutWidget", "Select specific data to display", None))
        self.specifyDataRadioButton.setText(_translate("OverviewLayoutWidget", "Select data to display", None))
        self.typeComboBox.setToolTip(_translate("OverviewLayoutWidget", "Data type (eg GR log type)", None))
        self.dataComboBox.setToolTip(_translate("OverviewLayoutWidget", "Data (eg specific GR log)", None))
        self.DataTypeLabel.setText(_translate("OverviewLayoutWidget", "Data type", None))
        self.dataClassComboBox.setToolTip(_translate("OverviewLayoutWidget", "Data class (eg Well log)", None))
        self.dataLabel.setText(_translate("OverviewLayoutWidget", "Data", None))
        self.dataClassLabel.setText(_translate("OverviewLayoutWidget", "Data class", None))

