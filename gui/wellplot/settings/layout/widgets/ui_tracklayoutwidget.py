# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracklayoutwidget.ui'
#
# Created: Sun Jun 21 09:48:01 2015
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

class Ui_TrackLayoutWidget(object):
    def setupUi(self, TrackLayoutWidget):
        TrackLayoutWidget.setObjectName(_fromUtf8("TrackLayoutWidget"))
        TrackLayoutWidget.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(TrackLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.LayoutButtonsOuterWidget = QtGui.QWidget(TrackLayoutWidget)
        self.LayoutButtonsOuterWidget.setMinimumSize(QtCore.QSize(40, 0))
        self.LayoutButtonsOuterWidget.setMaximumSize(QtCore.QSize(100, 16777215))
        self.LayoutButtonsOuterWidget.setObjectName(_fromUtf8("LayoutButtonsOuterWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.LayoutButtonsOuterWidget)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(45, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.layoutButtonsWidget = QtGui.QWidget(self.LayoutButtonsOuterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layoutButtonsWidget.sizePolicy().hasHeightForWidth())
        self.layoutButtonsWidget.setSizePolicy(sizePolicy)
        self.layoutButtonsWidget.setMinimumSize(QtCore.QSize(40, 0))
        self.layoutButtonsWidget.setMaximumSize(QtCore.QSize(40, 16777215))
        self.layoutButtonsWidget.setObjectName(_fromUtf8("layoutButtonsWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutButtonsWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addAxisPushButton = QtGui.QPushButton(self.layoutButtonsWidget)
        self.addAxisPushButton.setText(_fromUtf8(""))
        self.addAxisPushButton.setObjectName(_fromUtf8("addAxisPushButton"))
        self.verticalLayout.addWidget(self.addAxisPushButton)
        self.addTrackPushButton = QtGui.QPushButton(self.layoutButtonsWidget)
        self.addTrackPushButton.setText(_fromUtf8(""))
        self.addTrackPushButton.setObjectName(_fromUtf8("addTrackPushButton"))
        self.verticalLayout.addWidget(self.addTrackPushButton)
        self.rightArrowPushButton = QtGui.QPushButton(self.layoutButtonsWidget)
        self.rightArrowPushButton.setText(_fromUtf8(""))
        self.rightArrowPushButton.setObjectName(_fromUtf8("rightArrowPushButton"))
        self.verticalLayout.addWidget(self.rightArrowPushButton)
        self.deletePushButton = QtGui.QPushButton(self.layoutButtonsWidget)
        self.deletePushButton.setText(_fromUtf8(""))
        self.deletePushButton.setObjectName(_fromUtf8("deletePushButton"))
        self.verticalLayout.addWidget(self.deletePushButton)
        self.upPushButton = QtGui.QPushButton(self.layoutButtonsWidget)
        self.upPushButton.setText(_fromUtf8(""))
        self.upPushButton.setObjectName(_fromUtf8("upPushButton"))
        self.verticalLayout.addWidget(self.upPushButton)
        self.downPushButton = QtGui.QPushButton(self.layoutButtonsWidget)
        self.downPushButton.setText(_fromUtf8(""))
        self.downPushButton.setObjectName(_fromUtf8("downPushButton"))
        self.verticalLayout.addWidget(self.downPushButton)
        spacerItem1 = QtGui.QSpacerItem(20, 328, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_3.addWidget(self.layoutButtonsWidget, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.LayoutButtonsOuterWidget)
        self.mainLayoutWidget = QtGui.QWidget(TrackLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainLayoutWidget.sizePolicy().hasHeightForWidth())
        self.mainLayoutWidget.setSizePolicy(sizePolicy)
        self.mainLayoutWidget.setMaximumSize(QtCore.QSize(2000, 16777215))
        self.mainLayoutWidget.setObjectName(_fromUtf8("mainLayoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.mainLayoutWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.scrollArea = QtGui.QScrollArea(self.mainLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 274, 278))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.scrollArea)
        self.horizontalLayout.addWidget(self.mainLayoutWidget)

        self.retranslateUi(TrackLayoutWidget)
        QtCore.QMetaObject.connectSlotsByName(TrackLayoutWidget)

    def retranslateUi(self, TrackLayoutWidget):
        TrackLayoutWidget.setWindowTitle(_translate("TrackLayoutWidget", "Form", None))
        self.addAxisPushButton.setToolTip(_translate("TrackLayoutWidget", "Add axis", None))
        self.addTrackPushButton.setToolTip(_translate("TrackLayoutWidget", "Add track", None))
        self.rightArrowPushButton.setToolTip(_translate("TrackLayoutWidget", "Add selected item", None))
        self.deletePushButton.setToolTip(_translate("TrackLayoutWidget", "Delete selected item", None))
        self.upPushButton.setToolTip(_translate("TrackLayoutWidget", "Promote item", None))
        self.downPushButton.setToolTip(_translate("TrackLayoutWidget", "Demote item", None))

