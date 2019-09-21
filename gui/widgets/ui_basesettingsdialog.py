# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basesettingsdialog.ui'
#
# Created: Fri Jun 26 13:44:08 2015
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

class Ui_BaseSettingsDialog(object):
    def setupUi(self, BaseSettingsDialog):
        BaseSettingsDialog.setObjectName(_fromUtf8("BaseSettingsDialog"))
        BaseSettingsDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(BaseSettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.placeholderWidget = QtGui.QWidget(BaseSettingsDialog)
        self.placeholderWidget.setObjectName(_fromUtf8("placeholderWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.placeholderWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.placeholderWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.itemTab = QtGui.QWidget()
        self.itemTab.setObjectName(_fromUtf8("itemTab"))
        self.tabWidget.addTab(self.itemTab, _fromUtf8(""))
        self.detailsTab = QtGui.QWidget()
        self.detailsTab.setObjectName(_fromUtf8("detailsTab"))
        self.detailsHorizontalLayout = QtGui.QHBoxLayout(self.detailsTab)
        self.detailsHorizontalLayout.setObjectName(_fromUtf8("detailsHorizontalLayout"))
        self.detailsScrollArea = QtGui.QScrollArea(self.detailsTab)
        self.detailsScrollArea.setWidgetResizable(True)
        self.detailsScrollArea.setObjectName(_fromUtf8("detailsScrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 362, 211))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.detailsScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.detailsHorizontalLayout.addWidget(self.detailsScrollArea)
        self.tabWidget.addTab(self.detailsTab, _fromUtf8(""))
        self.styleTab = QtGui.QWidget()
        self.styleTab.setObjectName(_fromUtf8("styleTab"))
        self.tabWidget.addTab(self.styleTab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.verticalLayout.addWidget(self.placeholderWidget)
        self.buttonBox = QtGui.QDialogButtonBox(BaseSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(BaseSettingsDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), BaseSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), BaseSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BaseSettingsDialog)

    def retranslateUi(self, BaseSettingsDialog):
        BaseSettingsDialog.setWindowTitle(_translate("BaseSettingsDialog", "Dialog", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.itemTab), _translate("BaseSettingsDialog", "Item", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.detailsTab), _translate("BaseSettingsDialog", "Details", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.styleTab), _translate("BaseSettingsDialog", "Style", None))

