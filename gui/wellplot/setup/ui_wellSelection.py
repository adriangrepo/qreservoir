# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wellSelection.ui'
#
# Created: Mon Jun  8 20:27:53 2015
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

class Ui_WellSelectionDialog(object):
    def setupUi(self, WellSelectionDialog):
        WellSelectionDialog.setObjectName(_fromUtf8("WellSelectionDialog"))
        WellSelectionDialog.setWindowModality(QtCore.Qt.NonModal)
        WellSelectionDialog.resize(400, 150)
        self.verticalLayout = QtGui.QVBoxLayout(WellSelectionDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.wellSelectionWidget = QtGui.QWidget(WellSelectionDialog)
        self.wellSelectionWidget.setObjectName(_fromUtf8("wellSelectionWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wellSelectionWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.selectWellLabel = QtGui.QLabel(self.wellSelectionWidget)
        self.selectWellLabel.setObjectName(_fromUtf8("selectWellLabel"))
        self.horizontalLayout.addWidget(self.selectWellLabel)
        self.wellsComboBox = QtGui.QComboBox(self.wellSelectionWidget)
        self.wellsComboBox.setObjectName(_fromUtf8("wellsComboBox"))
        self.horizontalLayout.addWidget(self.wellsComboBox)
        self.verticalLayout.addWidget(self.wellSelectionWidget)
        self.buttonBox = QtGui.QDialogButtonBox(WellSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(WellSelectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), WellSelectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), WellSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WellSelectionDialog)

    def retranslateUi(self, WellSelectionDialog):
        WellSelectionDialog.setWindowTitle(_translate("WellSelectionDialog", "Well plot setup", None))
        WellSelectionDialog.setToolTip(_translate("WellSelectionDialog", "Select template style", None))
        self.selectWellLabel.setText(_translate("WellSelectionDialog", "Select well to plot", None))

