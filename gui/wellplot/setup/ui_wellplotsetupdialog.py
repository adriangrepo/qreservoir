# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wellplotsetupdialog.ui'
#
# Created: Sat Jun 20 11:57:48 2015
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

class Ui_WellPlotSetupDialog(object):
    def setupUi(self, WellPlotSetupDialog):
        WellPlotSetupDialog.setObjectName(_fromUtf8("WellPlotSetupDialog"))
        WellPlotSetupDialog.setWindowModality(QtCore.Qt.NonModal)
        WellPlotSetupDialog.resize(436, 314)
        self.verticalLayout_2 = QtGui.QVBoxLayout(WellPlotSetupDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.wellHolderWidget = QtGui.QWidget(WellPlotSetupDialog)
        self.wellHolderWidget.setObjectName(_fromUtf8("wellHolderWidget"))
        self.verticalLayout_2.addWidget(self.wellHolderWidget)
        self.plotSelectionWidget = QtGui.QWidget(WellPlotSetupDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotSelectionWidget.sizePolicy().hasHeightForWidth())
        self.plotSelectionWidget.setSizePolicy(sizePolicy)
        self.plotSelectionWidget.setObjectName(_fromUtf8("plotSelectionWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.plotSelectionWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.quickPlotGroupBox = QtGui.QGroupBox(self.plotSelectionWidget)
        self.quickPlotGroupBox.setFlat(True)
        self.quickPlotGroupBox.setObjectName(_fromUtf8("quickPlotGroupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.quickPlotGroupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.quickPlotRadioButton = QtGui.QRadioButton(self.quickPlotGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickPlotRadioButton.sizePolicy().hasHeightForWidth())
        self.quickPlotRadioButton.setSizePolicy(sizePolicy)
        self.quickPlotRadioButton.setObjectName(_fromUtf8("quickPlotRadioButton"))
        self.gridLayout_3.addWidget(self.quickPlotRadioButton, 0, 0, 1, 1)
        self.quickPlotComboBox = QtGui.QComboBox(self.quickPlotGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickPlotComboBox.sizePolicy().hasHeightForWidth())
        self.quickPlotComboBox.setSizePolicy(sizePolicy)
        self.quickPlotComboBox.setObjectName(_fromUtf8("quickPlotComboBox"))
        self.gridLayout_3.addWidget(self.quickPlotComboBox, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.quickPlotGroupBox)
        self.wellPlotGroupBox = QtGui.QGroupBox(self.plotSelectionWidget)
        self.wellPlotGroupBox.setFlat(True)
        self.wellPlotGroupBox.setObjectName(_fromUtf8("wellPlotGroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.wellPlotGroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.selectWellPlotComboBox = QtGui.QComboBox(self.wellPlotGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectWellPlotComboBox.sizePolicy().hasHeightForWidth())
        self.selectWellPlotComboBox.setSizePolicy(sizePolicy)
        self.selectWellPlotComboBox.setObjectName(_fromUtf8("selectWellPlotComboBox"))
        self.gridLayout.addWidget(self.selectWellPlotComboBox, 0, 2, 1, 1)
        self.createWellPlotRadioButton = QtGui.QRadioButton(self.wellPlotGroupBox)
        self.createWellPlotRadioButton.setObjectName(_fromUtf8("createWellPlotRadioButton"))
        self.gridLayout.addWidget(self.createWellPlotRadioButton, 1, 0, 1, 1)
        self.createNewWellPlotLineEdit = QtGui.QLineEdit(self.wellPlotGroupBox)
        self.createNewWellPlotLineEdit.setObjectName(_fromUtf8("createNewWellPlotLineEdit"))
        self.gridLayout.addWidget(self.createNewWellPlotLineEdit, 1, 1, 1, 2)
        self.selectWellPlotRadioButton = QtGui.QRadioButton(self.wellPlotGroupBox)
        self.selectWellPlotRadioButton.setObjectName(_fromUtf8("selectWellPlotRadioButton"))
        self.gridLayout.addWidget(self.selectWellPlotRadioButton, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.wellPlotGroupBox)
        self.templateGroupBox = QtGui.QGroupBox(self.plotSelectionWidget)
        self.templateGroupBox.setFlat(True)
        self.templateGroupBox.setObjectName(_fromUtf8("templateGroupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.templateGroupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.templatesComboBox = QtGui.QComboBox(self.templateGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.templatesComboBox.sizePolicy().hasHeightForWidth())
        self.templatesComboBox.setSizePolicy(sizePolicy)
        self.templatesComboBox.setObjectName(_fromUtf8("templatesComboBox"))
        self.gridLayout_2.addWidget(self.templatesComboBox, 0, 2, 1, 1)
        self.createNewTemplateRadioButton = QtGui.QRadioButton(self.templateGroupBox)
        self.createNewTemplateRadioButton.setObjectName(_fromUtf8("createNewTemplateRadioButton"))
        self.gridLayout_2.addWidget(self.createNewTemplateRadioButton, 1, 0, 1, 1)
        self.newTemplateNameLineEdit = QtGui.QLineEdit(self.templateGroupBox)
        self.newTemplateNameLineEdit.setObjectName(_fromUtf8("newTemplateNameLineEdit"))
        self.gridLayout_2.addWidget(self.newTemplateNameLineEdit, 1, 1, 1, 2)
        self.selectTemplateRadioButton = QtGui.QRadioButton(self.templateGroupBox)
        self.selectTemplateRadioButton.setObjectName(_fromUtf8("selectTemplateRadioButton"))
        self.gridLayout_2.addWidget(self.selectTemplateRadioButton, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.templateGroupBox)
        self.verticalLayout_2.addWidget(self.plotSelectionWidget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(WellPlotSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(WellPlotSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), WellPlotSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), WellPlotSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(WellPlotSetupDialog)

    def retranslateUi(self, WellPlotSetupDialog):
        WellPlotSetupDialog.setWindowTitle(_translate("WellPlotSetupDialog", "Well plot setup", None))
        WellPlotSetupDialog.setToolTip(_translate("WellPlotSetupDialog", "Select template style", None))
        self.quickPlotGroupBox.setTitle(_translate("WellPlotSetupDialog", "Quick plot", None))
        self.quickPlotRadioButton.setText(_translate("WellPlotSetupDialog", "Create quick plot", None))
        self.wellPlotGroupBox.setTitle(_translate("WellPlotSetupDialog", "Well plot", None))
        self.createWellPlotRadioButton.setText(_translate("WellPlotSetupDialog", "Create new well plot", None))
        self.selectWellPlotRadioButton.setText(_translate("WellPlotSetupDialog", "Select well plot", None))
        self.templateGroupBox.setTitle(_translate("WellPlotSetupDialog", "Template", None))
        self.createNewTemplateRadioButton.setText(_translate("WellPlotSetupDialog", "Create new template", None))
        self.selectTemplateRadioButton.setText(_translate("WellPlotSetupDialog", "Select template", None))

