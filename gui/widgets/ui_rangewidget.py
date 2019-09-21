# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rangewidget.ui'
#
# Created: Sat Jun 13 10:16:53 2015
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

class Ui_rangeWidget(object):
    def setupUi(self, rangeWidget):
        rangeWidget.setObjectName(_fromUtf8("rangeWidget"))
        rangeWidget.resize(298, 105)
        rangeWidget.setWindowTitle(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(rangeWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plotRangeWidget = QtGui.QWidget(rangeWidget)
        self.plotRangeWidget.setObjectName(_fromUtf8("plotRangeWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.plotRangeWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.displayStartLabel = QtGui.QLabel(self.plotRangeWidget)
        self.displayStartLabel.setObjectName(_fromUtf8("displayStartLabel"))
        self.gridLayout_2.addWidget(self.displayStartLabel, 1, 0, 1, 1)
        self.displayLabel = QtGui.QLabel(self.plotRangeWidget)
        self.displayLabel.setObjectName(_fromUtf8("displayLabel"))
        self.gridLayout_2.addWidget(self.displayLabel, 0, 0, 1, 1)
        self.displayStartLineEdit = QtGui.QLineEdit(self.plotRangeWidget)
        self.displayStartLineEdit.setEnabled(False)
        self.displayStartLineEdit.setObjectName(_fromUtf8("displayStartLineEdit"))
        self.gridLayout_2.addWidget(self.displayStartLineEdit, 1, 1, 1, 1)
        self.rangeComboBox = QtGui.QComboBox(self.plotRangeWidget)
        self.rangeComboBox.setObjectName(_fromUtf8("rangeComboBox"))
        self.gridLayout_2.addWidget(self.rangeComboBox, 0, 1, 1, 1)
        self.displayStopLabel = QtGui.QLabel(self.plotRangeWidget)
        self.displayStopLabel.setObjectName(_fromUtf8("displayStopLabel"))
        self.gridLayout_2.addWidget(self.displayStopLabel, 2, 0, 1, 1)
        self.displayStopLineEdit = QtGui.QLineEdit(self.plotRangeWidget)
        self.displayStopLineEdit.setEnabled(False)
        self.displayStopLineEdit.setObjectName(_fromUtf8("displayStopLineEdit"))
        self.gridLayout_2.addWidget(self.displayStopLineEdit, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.plotRangeWidget)

        self.retranslateUi(rangeWidget)
        QtCore.QMetaObject.connectSlotsByName(rangeWidget)

    def retranslateUi(self, rangeWidget):
        self.displayStartLabel.setText(_translate("rangeWidget", "Display start", None))
        self.displayLabel.setText(_translate("rangeWidget", "Display range", None))
        self.displayStartLineEdit.setToolTip(_translate("rangeWidget", "Specify start data value to display", None))
        self.rangeComboBox.setToolTip(_translate("rangeWidget", "Select maximum data range in plot", None))
        self.displayStopLabel.setText(_translate("rangeWidget", "Display stop", None))
        self.displayStopLineEdit.setToolTip(_translate("rangeWidget", "Specify stop data value to display", None))

