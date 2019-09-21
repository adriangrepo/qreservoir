# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qrbase_view.ui'
#
# Created: Mon Jun  8 19:24:42 2015
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(795, 613)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 795, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName(_fromUtf8("menu_Edit"))
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName(_fromUtf8("menu_View"))
        self.menu_Insert = QtGui.QMenu(self.menubar)
        self.menu_Insert.setObjectName(_fromUtf8("menu_Insert"))
        self.menu_Project = QtGui.QMenu(self.menubar)
        self.menu_Project.setObjectName(_fromUtf8("menu_Project"))
        self.menu_Tools = QtGui.QMenu(self.menubar)
        self.menu_Tools.setObjectName(_fromUtf8("menu_Tools"))
        self.menu_Window = QtGui.QMenu(self.menubar)
        self.menu_Window.setObjectName(_fromUtf8("menu_Window"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBarTop = QtGui.QToolBar(MainWindow)
        self.toolBarTop.setObjectName(_fromUtf8("toolBarTop"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarTop)
        self.toolBarBottom = QtGui.QToolBar(MainWindow)
        self.toolBarBottom.setObjectName(_fromUtf8("toolBarBottom"))
        MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBarBottom)
        self.toolBarRHS = QtGui.QToolBar(MainWindow)
        self.toolBarRHS.setObjectName(_fromUtf8("toolBarRHS"))
        MainWindow.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBarRHS)
        self.actionNew_project = QtGui.QAction(MainWindow)
        self.actionNew_project.setObjectName(_fromUtf8("actionNew_project"))
        self.actionOpen_project = QtGui.QAction(MainWindow)
        self.actionOpen_project.setObjectName(_fromUtf8("actionOpen_project"))
        self.actionImport_file = QtGui.QAction(MainWindow)
        self.actionImport_file.setObjectName(_fromUtf8("actionImport_file"))
        self.actionSave_project = QtGui.QAction(MainWindow)
        self.actionSave_project.setObjectName(_fromUtf8("actionSave_project"))
        self.actionSave_project_as = QtGui.QAction(MainWindow)
        self.actionSave_project_as.setObjectName(_fromUtf8("actionSave_project_as"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.action2D_window = QtGui.QAction(MainWindow)
        self.action2D_window.setObjectName(_fromUtf8("action2D_window"))
        self.action3D_window = QtGui.QAction(MainWindow)
        self.action3D_window.setObjectName(_fromUtf8("action3D_window"))
        self.actionWell_plot_window = QtGui.QAction(MainWindow)
        self.actionWell_plot_window.setObjectName(_fromUtf8("actionWell_plot_window"))
        self.actionWell_correlation_window = QtGui.QAction(MainWindow)
        self.actionWell_correlation_window.setObjectName(_fromUtf8("actionWell_correlation_window"))
        self.actionX_Y_plot_window = QtGui.QAction(MainWindow)
        self.actionX_Y_plot_window.setObjectName(_fromUtf8("actionX_Y_plot_window"))
        self.actionX_Y_Z_plot_window = QtGui.QAction(MainWindow)
        self.actionX_Y_Z_plot_window.setObjectName(_fromUtf8("actionX_Y_Z_plot_window"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menu_File.addAction(self.actionNew_project)
        self.menu_File.addAction(self.actionOpen_project)
        self.menu_File.addAction(self.actionImport_file)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionSave_project)
        self.menu_File.addAction(self.actionSave_project_as)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionExit)
        self.menu_Window.addAction(self.action2D_window)
        self.menu_Window.addAction(self.action3D_window)
        self.menu_Window.addAction(self.actionWell_plot_window)
        self.menu_Window.addAction(self.actionWell_correlation_window)
        self.menu_Window.addAction(self.actionX_Y_plot_window)
        self.menu_Window.addAction(self.actionX_Y_Z_plot_window)
        self.menu_Help.addAction(self.actionAbout)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Insert.menuAction())
        self.menubar.addAction(self.menu_Project.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menubar.addAction(self.menu_Window.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBarBottom.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menu_File.setTitle(_translate("MainWindow", "&File", None))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit", None))
        self.menu_View.setTitle(_translate("MainWindow", "&View", None))
        self.menu_Insert.setTitle(_translate("MainWindow", "&Insert", None))
        self.menu_Project.setTitle(_translate("MainWindow", "&Project", None))
        self.menu_Tools.setTitle(_translate("MainWindow", "&Tools", None))
        self.menu_Window.setTitle(_translate("MainWindow", "&Window", None))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help", None))
        self.toolBarTop.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.toolBarBottom.setWindowTitle(_translate("MainWindow", "toolBar_2", None))
        self.toolBarRHS.setWindowTitle(_translate("MainWindow", "toolBar_3", None))
        self.actionNew_project.setText(_translate("MainWindow", "New project", None))
        self.actionOpen_project.setText(_translate("MainWindow", "Open project", None))
        self.actionImport_file.setText(_translate("MainWindow", "Import file", None))
        self.actionSave_project.setText(_translate("MainWindow", "Save project", None))
        self.actionSave_project_as.setText(_translate("MainWindow", "Save project as", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.action2D_window.setText(_translate("MainWindow", "2D window", None))
        self.action3D_window.setText(_translate("MainWindow", "3D window", None))
        self.actionWell_plot_window.setText(_translate("MainWindow", "Well plot window", None))
        self.actionWell_correlation_window.setText(_translate("MainWindow", "Well correlation window", None))
        self.actionX_Y_plot_window.setText(_translate("MainWindow", "X/Y plot window", None))
        self.actionX_Y_Z_plot_window.setText(_translate("MainWindow", "X/Y/Z plot window", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))

