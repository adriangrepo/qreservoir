# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'primaryztypewidget.ui'
#
# Created: Sun Jun 14 05:43:38 2015
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

class Ui_PrimaryZTypeWidget(object):
    def setupUi(self, PrimaryZTypeWidget):
        PrimaryZTypeWidget.setObjectName(_fromUtf8("PrimaryZTypeWidget"))
        PrimaryZTypeWidget.resize(312, 112)
        PrimaryZTypeWidget.setWindowTitle(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(PrimaryZTypeWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.primaryMeasurementGroupBox = QtGui.QGroupBox(PrimaryZTypeWidget)
        self.primaryMeasurementGroupBox.setEnabled(False)
        self.primaryMeasurementGroupBox.setFlat(True)
        self.primaryMeasurementGroupBox.setObjectName(_fromUtf8("primaryMeasurementGroupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.primaryMeasurementGroupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.primaryMeasurementWidget = QtGui.QWidget(self.primaryMeasurementGroupBox)
        self.primaryMeasurementWidget.setObjectName(_fromUtf8("primaryMeasurementWidget"))
        self.gridLayout = QtGui.QGridLayout(self.primaryMeasurementWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.datumLabel = QtGui.QLabel(self.primaryMeasurementWidget)
        self.datumLabel.setObjectName(_fromUtf8("datumLabel"))
        self.gridLayout.addWidget(self.datumLabel, 2, 0, 1, 1)
        self.measurementTypeLabel = QtGui.QLabel(self.primaryMeasurementWidget)
        self.measurementTypeLabel.setObjectName(_fromUtf8("measurementTypeLabel"))
        self.gridLayout.addWidget(self.measurementTypeLabel, 1, 0, 1, 2)
        self.measurementTypeLineEdit = QtGui.QLineEdit(self.primaryMeasurementWidget)
        self.measurementTypeLineEdit.setEnabled(False)
        self.measurementTypeLineEdit.setObjectName(_fromUtf8("measurementTypeLineEdit"))
        self.gridLayout.addWidget(self.measurementTypeLineEdit, 1, 2, 1, 1)
        self.measurementTypeUnitsLabel = QtGui.QLabel(self.primaryMeasurementWidget)
        self.measurementTypeUnitsLabel.setObjectName(_fromUtf8("measurementTypeUnitsLabel"))
        self.gridLayout.addWidget(self.measurementTypeUnitsLabel, 1, 3, 1, 1)
        self.measurementTypeUnitsLineEdit = QtGui.QLineEdit(self.primaryMeasurementWidget)
        self.measurementTypeUnitsLineEdit.setEnabled(False)
        self.measurementTypeUnitsLineEdit.setObjectName(_fromUtf8("measurementTypeUnitsLineEdit"))
        self.gridLayout.addWidget(self.measurementTypeUnitsLineEdit, 1, 4, 1, 1)
        self.datumLineEdit = QtGui.QLineEdit(self.primaryMeasurementWidget)
        self.datumLineEdit.setObjectName(_fromUtf8("datumLineEdit"))
        self.gridLayout.addWidget(self.datumLineEdit, 2, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.primaryMeasurementWidget)
        self.verticalLayout.addWidget(self.primaryMeasurementGroupBox)

        self.retranslateUi(PrimaryZTypeWidget)
        QtCore.QMetaObject.connectSlotsByName(PrimaryZTypeWidget)

    def retranslateUi(self, PrimaryZTypeWidget):
        self.primaryMeasurementGroupBox.setTitle(_translate("PrimaryZTypeWidget", "Primary measurement type", None))
        self.datumLabel.setText(_translate("PrimaryZTypeWidget", "Datum", None))
        self.measurementTypeLabel.setText(_translate("PrimaryZTypeWidget", "Type", None))
        self.measurementTypeLineEdit.setToolTip(_translate("PrimaryZTypeWidget", "Data measurement type (eg MDKB (ft))", None))
        self.measurementTypeUnitsLabel.setText(_translate("PrimaryZTypeWidget", "Units", None))
        self.measurementTypeUnitsLineEdit.setToolTip(_translate("PrimaryZTypeWidget", "Data units", None))

