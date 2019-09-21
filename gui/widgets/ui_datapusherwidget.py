# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'datapusherwidget.ui'
#
# Created: Sun Jun 21 04:19:26 2015
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

class Ui_DataPusherWidget(object):
    def setupUi(self, DataPusherWidget):
        DataPusherWidget.setObjectName(_fromUtf8("DataPusherWidget"))
        DataPusherWidget.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DataPusherWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.topButtonHolderWidget = QtGui.QWidget(DataPusherWidget)
        self.topButtonHolderWidget.setObjectName(_fromUtf8("topButtonHolderWidget"))
        self.verticalLayout_2.addWidget(self.topButtonHolderWidget)
        self.quickPlotSetupWidget = QtGui.QWidget(DataPusherWidget)
        self.quickPlotSetupWidget.setEnabled(True)
        self.quickPlotSetupWidget.setObjectName(_fromUtf8("quickPlotSetupWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.quickPlotSetupWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.leftScrollArea = QtGui.QScrollArea(self.quickPlotSetupWidget)
        self.leftScrollArea.setWidgetResizable(True)
        self.leftScrollArea.setObjectName(_fromUtf8("leftScrollArea"))
        self.leftScrollAreaWidget = QtGui.QWidget()
        self.leftScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 151, 264))
        self.leftScrollAreaWidget.setObjectName(_fromUtf8("leftScrollAreaWidget"))
        self.leftVerticalLayout = QtGui.QVBoxLayout(self.leftScrollAreaWidget)
        self.leftVerticalLayout.setObjectName(_fromUtf8("leftVerticalLayout"))
        self.leftScrollArea.setWidget(self.leftScrollAreaWidget)
        self.horizontalLayout.addWidget(self.leftScrollArea)
        self.centralButtonsWidget = QtGui.QWidget(self.quickPlotSetupWidget)
        self.centralButtonsWidget.setObjectName(_fromUtf8("centralButtonsWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralButtonsWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rightArrowPushButton = QtGui.QPushButton(self.centralButtonsWidget)
        self.rightArrowPushButton.setText(_fromUtf8(""))
        self.rightArrowPushButton.setObjectName(_fromUtf8("rightArrowPushButton"))
        self.verticalLayout.addWidget(self.rightArrowPushButton)
        self.deletePushButton = QtGui.QPushButton(self.centralButtonsWidget)
        self.deletePushButton.setText(_fromUtf8(""))
        self.deletePushButton.setObjectName(_fromUtf8("deletePushButton"))
        self.verticalLayout.addWidget(self.deletePushButton)
        self.upPushButton = QtGui.QPushButton(self.centralButtonsWidget)
        self.upPushButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.upPushButton.setText(_fromUtf8(""))
        self.upPushButton.setObjectName(_fromUtf8("upPushButton"))
        self.verticalLayout.addWidget(self.upPushButton)
        self.downPushButton = QtGui.QPushButton(self.centralButtonsWidget)
        self.downPushButton.setText(_fromUtf8(""))
        self.downPushButton.setObjectName(_fromUtf8("downPushButton"))
        self.verticalLayout.addWidget(self.downPushButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.centralButtonsWidget)
        self.rightScrollArea = QtGui.QScrollArea(self.quickPlotSetupWidget)
        self.rightScrollArea.setWidgetResizable(True)
        self.rightScrollArea.setObjectName(_fromUtf8("rightScrollArea"))
        self.rightScrollAreaWidget = QtGui.QWidget()
        self.rightScrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 151, 264))
        self.rightScrollAreaWidget.setObjectName(_fromUtf8("rightScrollAreaWidget"))
        self.rightVerticalLayout = QtGui.QVBoxLayout(self.rightScrollAreaWidget)
        self.rightVerticalLayout.setObjectName(_fromUtf8("rightVerticalLayout"))
        self.rightScrollArea.setWidget(self.rightScrollAreaWidget)
        self.horizontalLayout.addWidget(self.rightScrollArea)
        self.verticalLayout_2.addWidget(self.quickPlotSetupWidget)

        self.retranslateUi(DataPusherWidget)
        QtCore.QMetaObject.connectSlotsByName(DataPusherWidget)

    def retranslateUi(self, DataPusherWidget):
        DataPusherWidget.setWindowTitle(_translate("DataPusherWidget", "Form", None))
        self.rightArrowPushButton.setToolTip(_translate("DataPusherWidget", "Create track for log type", None))
        self.deletePushButton.setToolTip(_translate("DataPusherWidget", "Delete selected track", None))
        self.upPushButton.setToolTip(_translate("DataPusherWidget", "Promote track (moves towards left in plot)", None))
        self.downPushButton.setToolTip(_translate("DataPusherWidget", "Demote track (moves towards right in plot)", None))

