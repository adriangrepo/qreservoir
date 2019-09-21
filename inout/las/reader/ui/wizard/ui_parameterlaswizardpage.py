# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameterlaswizardpage.ui'
#
# Created: Mon Dec 29 19:44:33 2014
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

class Ui_ParameterLasWizardPage(object):
    def setupUi(self, ParameterLasWizardPage):
        ParameterLasWizardPage.setObjectName(_fromUtf8("ParameterLasWizardPage"))
        ParameterLasWizardPage.resize(579, 478)
        self.verticalLayout = QtGui.QVBoxLayout(ParameterLasWizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.upperGroupBox = QtGui.QGroupBox(ParameterLasWizardPage)
        self.upperGroupBox.setTitle(_fromUtf8(""))
        self.upperGroupBox.setObjectName(_fromUtf8("upperGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.upperGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.newParameterSetLineEdit = QtGui.QLineEdit(self.upperGroupBox)
        self.newParameterSetLineEdit.setObjectName(_fromUtf8("newParameterSetLineEdit"))
        self.gridLayout.addWidget(self.newParameterSetLineEdit, 3, 1, 1, 1)
        self.existingParameterSetRadioButton = QtGui.QRadioButton(self.upperGroupBox)
        self.existingParameterSetRadioButton.setObjectName(_fromUtf8("existingParameterSetRadioButton"))
        self.gridLayout.addWidget(self.existingParameterSetRadioButton, 4, 0, 1, 1)
        self.existingParameterSetComboBox = QtGui.QComboBox(self.upperGroupBox)
        self.existingParameterSetComboBox.setObjectName(_fromUtf8("existingParameterSetComboBox"))
        self.gridLayout.addWidget(self.existingParameterSetComboBox, 4, 1, 1, 1)
        self.newParameterSetRadioButton = QtGui.QRadioButton(self.upperGroupBox)
        self.newParameterSetRadioButton.setObjectName(_fromUtf8("newParameterSetRadioButton"))
        self.gridLayout.addWidget(self.newParameterSetRadioButton, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        self.verticalLayout.addWidget(self.upperGroupBox)
        self.parametersTableWidget = QtGui.QTableWidget(ParameterLasWizardPage)
        self.parametersTableWidget.setObjectName(_fromUtf8("parametersTableWidget"))
        self.parametersTableWidget.setColumnCount(0)
        self.parametersTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.parametersTableWidget)
        self.lowerGroupbox = QtGui.QGroupBox(ParameterLasWizardPage)
        self.lowerGroupbox.setTitle(_fromUtf8(""))
        self.lowerGroupbox.setObjectName(_fromUtf8("lowerGroupbox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.lowerGroupbox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.viewfilePushButton = QtGui.QPushButton(self.lowerGroupbox)
        self.viewfilePushButton.setObjectName(_fromUtf8("viewfilePushButton"))
        self.horizontalLayout_2.addWidget(self.viewfilePushButton)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.lowerGroupbox)

        self.retranslateUi(ParameterLasWizardPage)
        QtCore.QMetaObject.connectSlotsByName(ParameterLasWizardPage)

    def retranslateUi(self, ParameterLasWizardPage):
        ParameterLasWizardPage.setWindowTitle(_translate("ParameterLasWizardPage", "Parameter details", None))
        self.existingParameterSetRadioButton.setText(_translate("ParameterLasWizardPage", "Existing parameter set", None))
        self.newParameterSetRadioButton.setText(_translate("ParameterLasWizardPage", "New parameter set", None))
        self.viewfilePushButton.setText(_translate("ParameterLasWizardPage", "View file ", None))

