# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importlaswizardpage.ui'
#
# Created: Mon Dec 29 19:45:15 2014
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

class Ui_ImportLasWizardPage(object):
    def setupUi(self, ImportLasWizardPage):
        ImportLasWizardPage.setObjectName(_fromUtf8("ImportLasWizardPage"))
        ImportLasWizardPage.resize(579, 478)
        self.verticalLayout = QtGui.QVBoxLayout(ImportLasWizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.upperGroupBox = QtGui.QGroupBox(ImportLasWizardPage)
        self.upperGroupBox.setTitle(_fromUtf8(""))
        self.upperGroupBox.setObjectName(_fromUtf8("upperGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.upperGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.selectalldefinedRadioButton = QtGui.QRadioButton(self.upperGroupBox)
        self.selectalldefinedRadioButton.setObjectName(_fromUtf8("selectalldefinedRadioButton"))
        self.horizontalLayout.addWidget(self.selectalldefinedRadioButton)
        self.selectallRadioButton = QtGui.QRadioButton(self.upperGroupBox)
        self.selectallRadioButton.setObjectName(_fromUtf8("selectallRadioButton"))
        self.horizontalLayout.addWidget(self.selectallRadioButton)
        self.selectnoneRadioButton = QtGui.QRadioButton(self.upperGroupBox)
        self.selectnoneRadioButton.setObjectName(_fromUtf8("selectnoneRadioButton"))
        self.horizontalLayout.addWidget(self.selectnoneRadioButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.upperGroupBox)
        self.logsTableWidget = QtGui.QTableWidget(ImportLasWizardPage)
        self.logsTableWidget.setObjectName(_fromUtf8("logsTableWidget"))
        self.logsTableWidget.setColumnCount(0)
        self.logsTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.logsTableWidget)
        self.lowerGroupbox = QtGui.QGroupBox(ImportLasWizardPage)
        self.lowerGroupbox.setTitle(_fromUtf8(""))
        self.lowerGroupbox.setObjectName(_fromUtf8("lowerGroupbox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.lowerGroupbox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.viewfilePushButton = QtGui.QPushButton(self.lowerGroupbox)
        self.viewfilePushButton.setObjectName(_fromUtf8("viewfilePushButton"))
        self.horizontalLayout_2.addWidget(self.viewfilePushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.lowerGroupbox)

        self.retranslateUi(ImportLasWizardPage)
        QtCore.QMetaObject.connectSlotsByName(ImportLasWizardPage)

    def retranslateUi(self, ImportLasWizardPage):
        ImportLasWizardPage.setWindowTitle(_translate("ImportLasWizardPage", "Import .las file", None))
        self.selectalldefinedRadioButton.setText(_translate("ImportLasWizardPage", "Select all defined", None))
        self.selectallRadioButton.setText(_translate("ImportLasWizardPage", "Select all", None))
        self.selectnoneRadioButton.setText(_translate("ImportLasWizardPage", "Select none", None))
        self.viewfilePushButton.setText(_translate("ImportLasWizardPage", "View file ", None))

