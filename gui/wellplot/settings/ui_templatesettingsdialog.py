# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templatesettingsdialog.ui'
#
# Created: Fri Jun 26 12:53:21 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(747, 534)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.itemTab = QtGui.QWidget()
        self.itemTab.setObjectName(_fromUtf8("itemTab"))
        self.detailsTabLayout = QtGui.QVBoxLayout(self.itemTab)
        self.detailsTabLayout.setObjectName(_fromUtf8("detailsTabLayout"))
        self.tabWidget.addTab(self.itemTab, _fromUtf8(""))
        self.layoutTab = QtGui.QWidget()
        self.layoutTab.setObjectName(_fromUtf8("layoutTab"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.layoutTab)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.layoutTabWidget = QtGui.QTabWidget(self.layoutTab)
        self.layoutTabWidget.setObjectName(_fromUtf8("layoutTabWidget"))
        self.tracksLayoutTab = QtGui.QWidget()
        self.tracksLayoutTab.setObjectName(_fromUtf8("tracksLayoutTab"))
        self.layoutTabWidget.addTab(self.tracksLayoutTab, _fromUtf8(""))
        self.overviewLayoutTab = QtGui.QWidget()
        self.overviewLayoutTab.setObjectName(_fromUtf8("overviewLayoutTab"))
        self.layoutTabWidget.addTab(self.overviewLayoutTab, _fromUtf8(""))
        self.horizontalLayout_6.addWidget(self.layoutTabWidget)
        self.tabWidget.addTab(self.layoutTab, _fromUtf8(""))
        self.styleTab = QtGui.QWidget()
        self.styleTab.setObjectName(_fromUtf8("styleTab"))
        self.horizontalLayout_18 = QtGui.QHBoxLayout(self.styleTab)
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.styleTabWidget = QtGui.QTabWidget(self.styleTab)
        self.styleTabWidget.setObjectName(_fromUtf8("styleTabWidget"))
        self.wellPlotStyleTab = QtGui.QWidget()
        self.wellPlotStyleTab.setObjectName(_fromUtf8("wellPlotStyleTab"))
        self.styleTabWidget.addTab(self.wellPlotStyleTab, _fromUtf8(""))
        self.trackStyleTab = QtGui.QWidget()
        self.trackStyleTab.setObjectName(_fromUtf8("trackStyleTab"))
        self.styleTabWidget.addTab(self.trackStyleTab, _fromUtf8(""))
        self.curveStyleTab = QtGui.QWidget()
        self.curveStyleTab.setObjectName(_fromUtf8("curveStyleTab"))
        self.styleTabWidget.addTab(self.curveStyleTab, _fromUtf8(""))
        self.horizontalLayout_18.addWidget(self.styleTabWidget)
        self.tabWidget.addTab(self.styleTab, _fromUtf8(""))
        self.scaleTab = QtGui.QWidget()
        self.scaleTab.setObjectName(_fromUtf8("scaleTab"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.scaleTab)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.tracksRangePlaceholderWidget = QtGui.QWidget(self.scaleTab)
        self.tracksRangePlaceholderWidget.setObjectName(_fromUtf8("tracksRangePlaceholderWidget"))
        self.verticalLayout_7.addWidget(self.tracksRangePlaceholderWidget)
        self.overviewGroupBox = QtGui.QGroupBox(self.scaleTab)
        self.overviewGroupBox.setFlat(True)
        self.overviewGroupBox.setObjectName(_fromUtf8("overviewGroupBox"))
        self.verticalLayout_7.addWidget(self.overviewGroupBox)
        self.tracksGroupBox = QtGui.QGroupBox(self.scaleTab)
        self.tracksGroupBox.setFlat(True)
        self.tracksGroupBox.setObjectName(_fromUtf8("tracksGroupBox"))
        self.verticalLayout_7.addWidget(self.tracksGroupBox)
        spacerItem = QtGui.QSpacerItem(20, 303, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        self.tabWidget.addTab(self.scaleTab, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.layoutTabWidget.setCurrentIndex(0)
        self.styleTabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.itemTab.setToolTip(_translate("Dialog", "Summary details for object", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.itemTab), _translate("Dialog", "Item", None))
        self.layoutTabWidget.setToolTip(_translate("Dialog", "Track layout settings", None))
        self.layoutTabWidget.setTabText(self.layoutTabWidget.indexOf(self.tracksLayoutTab), _translate("Dialog", "Tracks", None))
        self.layoutTabWidget.setTabText(self.layoutTabWidget.indexOf(self.overviewLayoutTab), _translate("Dialog", "Overview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.layoutTab), _translate("Dialog", "Layout", None))
        self.styleTabWidget.setTabText(self.styleTabWidget.indexOf(self.wellPlotStyleTab), _translate("Dialog", "Well plot style", None))
        self.styleTabWidget.setTabText(self.styleTabWidget.indexOf(self.trackStyleTab), _translate("Dialog", "Track style", None))
        self.styleTabWidget.setTabText(self.styleTabWidget.indexOf(self.curveStyleTab), _translate("Dialog", "Curve style", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.styleTab), _translate("Dialog", "Style", None))
        self.overviewGroupBox.setTitle(_translate("Dialog", "Overview", None))
        self.tracksGroupBox.setTitle(_translate("Dialog", "Tracks", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scaleTab), _translate("Dialog", "Scale", None))

