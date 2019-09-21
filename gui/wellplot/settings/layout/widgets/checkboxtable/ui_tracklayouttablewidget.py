# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracklayouttablewidget.ui'
#
# Created: Sun Jun 21 06:08:49 2015
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

class Ui_TrackLayoutTableWidget(object):
    def setupUi(self, TrackLayoutTableWidget):
        TrackLayoutTableWidget.setObjectName(_fromUtf8("TrackLayoutTableWidget"))
        TrackLayoutTableWidget.resize(772, 344)
        self.verticalLayout_2 = QtGui.QVBoxLayout(TrackLayoutTableWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea = QtGui.QScrollArea(TrackLayoutTableWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 758, 199))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.checkTabVerticalLayout = QtGui.QVBoxLayout()
        self.checkTabVerticalLayout.setObjectName(_fromUtf8("checkTabVerticalLayout"))
        self.checkTabTableLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.checkTabTableLabel.setObjectName(_fromUtf8("checkTabTableLabel"))
        self.checkTabVerticalLayout.addWidget(self.checkTabTableLabel)
        self.chkboxTableWidget = QtGui.QTableWidget(self.scrollAreaWidgetContents)
        self.chkboxTableWidget.setObjectName(_fromUtf8("chkboxTableWidget"))
        self.chkboxTableWidget.setColumnCount(0)
        self.chkboxTableWidget.setRowCount(0)
        self.checkTabVerticalLayout.addWidget(self.chkboxTableWidget)
        self.verticalLayout_4.addLayout(self.checkTabVerticalLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.selectionGroupBox = QtGui.QGroupBox(TrackLayoutTableWidget)
        self.selectionGroupBox.setFlat(False)
        self.selectionGroupBox.setObjectName(_fromUtf8("selectionGroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.selectionGroupBox)
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.selectDefaultRadioButton = QtGui.QRadioButton(self.selectionGroupBox)
        self.selectDefaultRadioButton.setObjectName(_fromUtf8("selectDefaultRadioButton"))
        self.verticalLayout.addWidget(self.selectDefaultRadioButton)
        self.selectActiveRadioButton = QtGui.QRadioButton(self.selectionGroupBox)
        self.selectActiveRadioButton.setObjectName(_fromUtf8("selectActiveRadioButton"))
        self.verticalLayout.addWidget(self.selectActiveRadioButton)
        self.selectAllRadioButton = QtGui.QRadioButton(self.selectionGroupBox)
        self.selectAllRadioButton.setObjectName(_fromUtf8("selectAllRadioButton"))
        self.verticalLayout.addWidget(self.selectAllRadioButton)
        self.selectNoneRadioButton = QtGui.QRadioButton(self.selectionGroupBox)
        self.selectNoneRadioButton.setObjectName(_fromUtf8("selectNoneRadioButton"))
        self.verticalLayout.addWidget(self.selectNoneRadioButton)
        self.horizontalLayout.addWidget(self.selectionGroupBox)
        self.miscGroupBox = QtGui.QGroupBox(TrackLayoutTableWidget)
        self.miscGroupBox.setTitle(_fromUtf8(""))
        self.miscGroupBox.setObjectName(_fromUtf8("miscGroupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.miscGroupBox)
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.addTrackPushButton = QtGui.QPushButton(self.miscGroupBox)
        self.addTrackPushButton.setObjectName(_fromUtf8("addTrackPushButton"))
        self.verticalLayout_5.addWidget(self.addTrackPushButton)
        self.horizontalLayout.addWidget(self.miscGroupBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(TrackLayoutTableWidget)
        QtCore.QMetaObject.connectSlotsByName(TrackLayoutTableWidget)

    def retranslateUi(self, TrackLayoutTableWidget):
        TrackLayoutTableWidget.setWindowTitle(_translate("TrackLayoutTableWidget", "Form", None))
        self.checkTabTableLabel.setText(_translate("TrackLayoutTableWidget", "Select logs to display in track numbers", None))
        self.selectionGroupBox.setTitle(_translate("TrackLayoutTableWidget", "Data selection", None))
        self.selectDefaultRadioButton.setToolTip(_translate("TrackLayoutTableWidget", "Default log types to plot can be set in preferences", None))
        self.selectDefaultRadioButton.setText(_translate("TrackLayoutTableWidget", "Select default", None))
        self.selectActiveRadioButton.setToolTip(_translate("TrackLayoutTableWidget", "Plot active logs", None))
        self.selectActiveRadioButton.setText(_translate("TrackLayoutTableWidget", "Select active", None))
        self.selectAllRadioButton.setText(_translate("TrackLayoutTableWidget", "Select all", None))
        self.selectNoneRadioButton.setText(_translate("TrackLayoutTableWidget", "Select none", None))
        self.addTrackPushButton.setText(_translate("TrackLayoutTableWidget", "Add track", None))

