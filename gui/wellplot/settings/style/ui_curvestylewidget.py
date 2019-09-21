# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curvestylewidget.ui'
#
# Created: Sun Jun 14 05:42:28 2015
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

class Ui_CurveStyleWidget(object):
    def setupUi(self, CurveStyleWidget):
        CurveStyleWidget.setObjectName(_fromUtf8("CurveStyleWidget"))
        CurveStyleWidget.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(CurveStyleWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.curveScrollArea = QtGui.QScrollArea(CurveStyleWidget)
        self.curveScrollArea.setWidgetResizable(True)
        self.curveScrollArea.setObjectName(_fromUtf8("curveScrollArea"))
        self.curveAreaWidget = QtGui.QWidget()
        self.curveAreaWidget.setGeometry(QtCore.QRect(0, 0, 386, 286))
        self.curveAreaWidget.setObjectName(_fromUtf8("curveAreaWidget"))
        self.horizontalLayout_16 = QtGui.QHBoxLayout(self.curveAreaWidget)
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.curveTableWidget = QtGui.QTableWidget(self.curveAreaWidget)
        self.curveTableWidget.setObjectName(_fromUtf8("curveTableWidget"))
        self.curveTableWidget.setColumnCount(0)
        self.curveTableWidget.setRowCount(0)
        self.horizontalLayout_16.addWidget(self.curveTableWidget)
        self.curveScrollArea.setWidget(self.curveAreaWidget)
        self.horizontalLayout.addWidget(self.curveScrollArea)

        self.retranslateUi(CurveStyleWidget)
        QtCore.QMetaObject.connectSlotsByName(CurveStyleWidget)

    def retranslateUi(self, CurveStyleWidget):
        CurveStyleWidget.setWindowTitle(_translate("CurveStyleWidget", "Form", None))

