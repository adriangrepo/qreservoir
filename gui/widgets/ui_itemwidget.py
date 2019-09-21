# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itemwidget.ui'
#
# Created: Sun Jun 28 06:32:13 2015
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

class Ui_itemWidget(object):
    def setupUi(self, itemWidget):
        itemWidget.setObjectName(_fromUtf8("itemWidget"))
        itemWidget.resize(400, 300)
        itemWidget.setWindowTitle(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(itemWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.infoWidget = QtGui.QWidget(itemWidget)
        self.infoWidget.setObjectName(_fromUtf8("infoWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.infoWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.nameLabel = QtGui.QLabel(self.infoWidget)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.gridLayout_2.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.nameLineEdit = QtGui.QLineEdit(self.infoWidget)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.gridLayout_2.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.classLabel = QtGui.QLabel(self.infoWidget)
        self.classLabel.setObjectName(_fromUtf8("classLabel"))
        self.gridLayout_2.addWidget(self.classLabel, 1, 0, 1, 1)
        self.classLineEdit = QtGui.QLineEdit(self.infoWidget)
        self.classLineEdit.setEnabled(False)
        self.classLineEdit.setObjectName(_fromUtf8("classLineEdit"))
        self.gridLayout_2.addWidget(self.classLineEdit, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.infoWidget)
        self.commentsTabWidget = QtGui.QTabWidget(itemWidget)
        self.commentsTabWidget.setObjectName(_fromUtf8("commentsTabWidget"))
        self.notesTab = QtGui.QWidget()
        self.notesTab.setObjectName(_fromUtf8("notesTab"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.notesTab)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.notesTextEdit = QtGui.QTextEdit(self.notesTab)
        self.notesTextEdit.setObjectName(_fromUtf8("notesTextEdit"))
        self.horizontalLayout_7.addWidget(self.notesTextEdit)
        self.commentsTabWidget.addTab(self.notesTab, _fromUtf8(""))
        self.historyTab = QtGui.QWidget()
        self.historyTab.setObjectName(_fromUtf8("historyTab"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.historyTab)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.historyTableWidget = QtGui.QTableWidget(self.historyTab)
        self.historyTableWidget.setObjectName(_fromUtf8("historyTableWidget"))
        self.historyTableWidget.setColumnCount(0)
        self.historyTableWidget.setRowCount(0)
        self.horizontalLayout_8.addWidget(self.historyTableWidget)
        self.commentsTabWidget.addTab(self.historyTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.commentsTabWidget)

        self.retranslateUi(itemWidget)
        self.commentsTabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(itemWidget)

    def retranslateUi(self, itemWidget):
        self.nameLabel.setText(_translate("itemWidget", "Name", None))
        self.nameLineEdit.setToolTip(_translate("itemWidget", "template name", None))
        self.classLabel.setToolTip(_translate("itemWidget", "Class of object", None))
        self.classLabel.setText(_translate("itemWidget", "Class", None))
        self.classLineEdit.setToolTip(_translate("itemWidget", "Template class", None))
        self.commentsTabWidget.setTabText(self.commentsTabWidget.indexOf(self.notesTab), _translate("itemWidget", "Notes", None))
        self.commentsTabWidget.setTabText(self.commentsTabWidget.indexOf(self.historyTab), _translate("itemWidget", "History", None))

