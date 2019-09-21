# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'buttonboxwidget.ui'
#
# Created: Sat Jun 20 14:13:20 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(754, 56)
        self.ButtonBoxWidget = QtGui.QDialogButtonBox(Form)
        self.ButtonBoxWidget.setGeometry(QtCore.QRect(0, 20, 745, 25))
        self.ButtonBoxWidget.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBoxWidget.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.ButtonBoxWidget.setObjectName(_fromUtf8("ButtonBoxWidget"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

