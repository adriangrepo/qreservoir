# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracksscalewidget.ui'
#
# Created: Sun Jun 28 11:27:31 2015
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

class Ui_TracksScaleWidget(object):
    def setupUi(self, TracksScaleWidget):
        TracksScaleWidget.setObjectName(_fromUtf8("TracksScaleWidget"))
        TracksScaleWidget.resize(401, 67)
        self.verticalLayout = QtGui.QVBoxLayout(TracksScaleWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_7 = QtGui.QWidget(TracksScaleWidget)
        self.widget_7.setObjectName(_fromUtf8("widget_7"))
        self.gridLayout_11 = QtGui.QGridLayout(self.widget_7)
        self.gridLayout_11.setMargin(0)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.verticalSpacingRadioButton = QtGui.QRadioButton(self.widget_7)
        self.verticalSpacingRadioButton.setObjectName(_fromUtf8("verticalSpacingRadioButton"))
        self.gridLayout_11.addWidget(self.verticalSpacingRadioButton, 0, 1, 1, 1)
        self.verticalSpacingUnitsLabel = QtGui.QLabel(self.widget_7)
        self.verticalSpacingUnitsLabel.setObjectName(_fromUtf8("verticalSpacingUnitsLabel"))
        self.gridLayout_11.addWidget(self.verticalSpacingUnitsLabel, 0, 3, 1, 1)
        self.verticalSpacingLineEdit = QtGui.QLineEdit(self.widget_7)
        self.verticalSpacingLineEdit.setObjectName(_fromUtf8("verticalSpacingLineEdit"))
        self.gridLayout_11.addWidget(self.verticalSpacingLineEdit, 0, 2, 1, 1)
        self.verticalSpacingUnitsComboBox = QtGui.QComboBox(self.widget_7)
        self.verticalSpacingUnitsComboBox.setObjectName(_fromUtf8("verticalSpacingUnitsComboBox"))
        self.gridLayout_11.addWidget(self.verticalSpacingUnitsComboBox, 0, 4, 1, 1)
        self.scaleRadioButton = QtGui.QRadioButton(self.widget_7)
        self.scaleRadioButton.setObjectName(_fromUtf8("scaleRadioButton"))
        self.gridLayout_11.addWidget(self.scaleRadioButton, 1, 1, 1, 1)
        self.scaleLineEdit = QtGui.QLineEdit(self.widget_7)
        self.scaleLineEdit.setEnabled(False)
        self.scaleLineEdit.setObjectName(_fromUtf8("scaleLineEdit"))
        self.gridLayout_11.addWidget(self.scaleLineEdit, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.widget_7)

        self.retranslateUi(TracksScaleWidget)
        QtCore.QMetaObject.connectSlotsByName(TracksScaleWidget)

    def retranslateUi(self, TracksScaleWidget):
        TracksScaleWidget.setWindowTitle(_translate("TracksScaleWidget", "Form", None))
        self.verticalSpacingRadioButton.setText(_translate("TracksScaleWidget", "Vertical spacing", None))
        self.verticalSpacingUnitsLabel.setText(_translate("TracksScaleWidget", "Units", None))
        self.verticalSpacingUnitsComboBox.setToolTip(_translate("TracksScaleWidget", "Screen units per well unit", None))
        self.scaleRadioButton.setText(_translate("TracksScaleWidget", "Scale", None))

