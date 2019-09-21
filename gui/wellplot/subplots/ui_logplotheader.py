# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logPlotHeader.ui'
#
# Created: Fri Apr  3 12:18:24 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import Qt


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

class Ui_LogHeader(object):
    def setupUi(self, LogHeader):
        LogHeader.setObjectName(_fromUtf8("LogHeader"))
        LogHeader.resize(716, 735)
        self.widget = QtGui.QWidget(LogHeader)
        self.widget.setGeometry(QtCore.QRect(60, 230, 277, 36))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.headingText_widget = QtGui.QWidget(self.widget)
        self.headingText_widget.setObjectName(_fromUtf8("headingText_widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.headingText_widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.logValLeft_label = QtGui.QLabel(self.headingText_widget)
        self.logValLeft_label.setObjectName(_fromUtf8("logValLeft_label"))
        self.horizontalLayout_2.addWidget(self.logValLeft_label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.logName_label = QtGui.QLabel(self.headingText_widget)
        self.logName_label.setObjectName(_fromUtf8("logName_label"))
        self.horizontalLayout_2.addWidget(self.logName_label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.logValRight_label = QtGui.QLabel(self.headingText_widget)
        self.logValRight_label.setObjectName(_fromUtf8("logValRight_label"))
        self.horizontalLayout_2.addWidget(self.logValRight_label)
        self.verticalLayout.addWidget(self.headingText_widget)

        self.retranslateUi(LogHeader)
        QtCore.QMetaObject.connectSlotsByName(LogHeader)

    def retranslateUi(self, LogHeader):
        LogHeader.setWindowTitle(_translate("LogHeader", "Form", None))
        self.logValLeft_label.setText(_translate("LogHeader", "TextLabel", None))
        self.logName_label.setText(_translate("LogHeader", "TextLabel", None))
        self.logValRight_label.setText(_translate("LogHeader", "TextLabel", None))

