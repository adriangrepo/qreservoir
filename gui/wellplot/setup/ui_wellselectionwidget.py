# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wellselectionwidget.ui'
#
# Created: Mon Jun 15 19:21:32 2015
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

class Ui_wellSelectionWidget(object):
    def setupUi(self, wellSelectionWidget):
        wellSelectionWidget.setObjectName(_fromUtf8("wellSelectionWidget"))
        wellSelectionWidget.resize(357, 43)
        self.horizontalLayout = QtGui.QHBoxLayout(wellSelectionWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.selectWellLabel = QtGui.QLabel(wellSelectionWidget)
        self.selectWellLabel.setObjectName(_fromUtf8("selectWellLabel"))
        self.horizontalLayout.addWidget(self.selectWellLabel)
        self.wellsComboBox = QtGui.QComboBox(wellSelectionWidget)
        self.wellsComboBox.setObjectName(_fromUtf8("wellsComboBox"))
        self.horizontalLayout.addWidget(self.wellsComboBox)

        self.retranslateUi(wellSelectionWidget)
        QtCore.QMetaObject.connectSlotsByName(wellSelectionWidget)

    def retranslateUi(self, wellSelectionWidget):
        wellSelectionWidget.setWindowTitle(_translate("wellSelectionWidget", "Form", None))
        self.selectWellLabel.setText(_translate("wellSelectionWidget", "Select well", None))

