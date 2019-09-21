# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'okcanceldialog.ui'
#
# Created: Tue Jun 16 20:03:08 2015
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

class Ui_OkCancelDialog(object):
    def setupUi(self, OkCancelDialog):
        OkCancelDialog.setObjectName(_fromUtf8("OkCancelDialog"))
        OkCancelDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(OkCancelDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.placeholderWidget = QtGui.QWidget(OkCancelDialog)
        self.placeholderWidget.setObjectName(_fromUtf8("placeholderWidget"))
        self.verticalLayout.addWidget(self.placeholderWidget)
        self.buttonBox = QtGui.QDialogButtonBox(OkCancelDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(OkCancelDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OkCancelDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OkCancelDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OkCancelDialog)

    def retranslateUi(self, OkCancelDialog):
        OkCancelDialog.setWindowTitle(_translate("OkCancelDialog", "Dialog", None))

