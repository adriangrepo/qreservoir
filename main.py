from __future__ import unicode_literals
import logging.config, os, sys

from db.databasemanager import DM

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QRect, Qt
from PyQt4.QtGui import QMainWindow, QApplication, QTabWidget, QDialog, QDockWidget,QDesktopWidget,\
    QToolBar, QStatusBar
import views.core.ui_qrbase_view
from views.tree.mainexplorer import MainExplorer
#import views.io.ui_importlas_view.Ui_ImportLasDialog
#from views.io.importlas_view import ImportLas_View

#from inout.las.reader.ui.importlasdialog import ImportLasDialog
from inout.las.reader.ui.wizard.importlaswizard import ImportLasWizard
#from inout.las.reader.ui.logselectwizardpage import LogSelectWizardPage
from globalvalues.picklesettings import PickleSettings
from globalvalues.appsettings import AppSettings


from views.core import centraltabwidget, toolbarwidget

from gui.wellplot.toolbar import logsettingstoolbar
from db.defaultsinitialiser import DefaultsInitialiser


from gui.wellplot.setup.wellplotsetupdialog import WellPlotSetupDialog





#from views.core.nonqtsignalmodified import ROIManager, SnapROIItem

#In Py3.x, QString doesn't exist in PyQt4
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


if __name__ == '__main__':
    '''
    logging.config.fileConfig('logging.conf')
    '''
    # set up logging
    logging.config.fileConfig(AppSettings.getLoggingConfig())
    # create logger
    logger = logging.getLogger(__name__)
    



class MainApp(QMainWindow, views.core.ui_qrbase_view.Ui_MainWindow):
    """ A python singleton see http://code.activestate.com/recipes/52558/ """
    class __impl:
        """ Implementation of the singleton interface """
        def spam(self):
            """ Test method, return singleton id """
            return id(self)
    # storage for the instance reference
    __instance = None


    def __init__(self,parent=None):
        super(MainApp, self).__init__(parent)
        """ Create singleton instance """
        # Check whether we already have an instance
        if MainApp.__instance is None:
            # Create and remember instance
            MainApp.__instance = MainApp.__impl()
        # Store instance reference as the only member in the handle
        self.__dict__['_MainApp__instance'] = MainApp.__instance
        
        self.settings = PickleSettings(AppSettings.applicationName)
        self.setupUi(self)
        self.setWindowSize()
        self.setCentralWindow()
        self.createDockWidgets()
        self.configureWidgets()
        self.connectRHSToolbar()
        self.disableActionsOnStart()
        self.connectSlots()
        self.startDatabase()
        self.addDBTree()
        
    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

    def setWindowSize(self):

        titleBarHeight = self.style().pixelMetric(
            QtGui.QStyle.PM_TitleBarHeight,
            QtGui.QStyleOptionTitleBar(),
            self
        )
        if AppSettings.START_ON_SECOND_SCREEN is False:
            geometry = app.desktop().availableGeometry()
            width = geometry.width()
            height = geometry.height() - (titleBarHeight*2)
            geometry.setHeight(height)
            self.setGeometry(geometry)


        else:
            numberScreens = app.desktop().screenCount()
            if numberScreens > 0:
                logger.debug("--setWindowSize() number of screens: "+str(numberScreens))
                #Get 1st screen's geometry
                rectScreen = app.desktop().screenGeometry(1);
                #Move the widget to first screen without changing its geometry
                self.move (rectScreen.left(),rectScreen.top());
                width = rectScreen.width()
                height = rectScreen.height()- (titleBarHeight*2)
                self.resize (width, height);

                #self.showMaximized();
        AppSettings.screenHeight = height
        AppSettings.screenWidth = width
        #allow window resize
        self.statusBar().setSizeGripEnabled( True )
        
    def setCentralWindow(self):
        self.central = centraltabwidget.CentralTabWidget(self)
        self.setCentralWidget(self.central)
        
        
    def connectRHSToolbar(self):
        self.toolBarRHS = logsettingstoolbar.LogSettingsToolbar(self)
        self.toolBarRHS.setObjectName(_fromUtf8("toolBarRHS"))
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBarRHS)
        self.toolBarRHS.hide()
        self.toolBarRHS.communicator.showToolbar.connect(self.showRHSToolbarTriggered)
        self.toolBarRHS.communicator.hideToolbar.connect(self.hideRHSToolbarTriggered)
        
        #self.toolbarWidget = ToolbarWidget(self)
        #self.addToolBar(Qt.TopToolBarArea , self.toolbarWidget )
        #self.toolbarWidget.sender.toolbar_changed.connect(self.changeToolbar)
        
    def showRHSToolbarTriggered(self):
        logger.debug(">>showRHSToolbarTriggered()")
        self.toolBarRHS.show()
        
    def hideRHSToolbarTriggered(self):
        logger.debug(">>hideRHSToolbarTriggered()")
        self.toolBarRHS.hide()
        
    #TODO work out how to change it
    def changeToolbar(self, newToolbar):
        toolbars = self.findChildren(QToolBar)
        for bar in toolbars:
            bar = None
        self.toolbarWidget = newToolbar
        self.addToolBar(Qt.RightToolBarArea , self.toolbarWidget )
        self.toolbarWidget.sender.toolbar_changed.connect(self.changeToolbar)



    def createDockWidgets(self):
        #Create all dock widgets here, more flexibility than with QtDesigner
        leftDockWidget = QDockWidget(self)
        leftDockWidget.setObjectName(_fromUtf8("leftDockWidget"))
        leftDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea| QtCore.Qt.RightDockWidgetArea)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, leftDockWidget)
        self.setCorner(QtCore.Qt.TopLeftCorner, QtCore.Qt.LeftDockWidgetArea)
        self.setCorner(QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea)

        #Upper left dock widget - input and data
        self.mainTreeDockWidget = QtGui.QWidget()
        self.mainTreeDockWidget.setObjectName(_fromUtf8("inputDataDockWidget"))
        self.mainTreeDockWidgetHLayout = QtGui.QHBoxLayout(self.mainTreeDockWidget)
        '''
        self.inputTabWidget = QtGui.QTabWidget(self.mainTreeDockWidget)
        self.inputTabWidget.setObjectName(_fromUtf8("inputTabWidget"))
        self.inputTab = QtGui.QWidget()
        self.inputTab.setObjectName(_fromUtf8("inputTab"))
        self.inputTabGridLayout = QtGui.QGridLayout(self.inputTab)
        self.inputTabWidget.addTab(self.inputTab, _fromUtf8("Input explorer"))

        self.dataTab = QtGui.QWidget()
        self.dataTab.setObjectName(_fromUtf8("dataTab"))
        self.inputTabWidget.addTab(self.dataTab, _fromUtf8("Data"))
        '''
        #self.mainTreeDockWidgetHLayout.addWidget(self.inputTabWidget)
        leftDockWidget.setWidget(self.mainTreeDockWidget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), leftDockWidget)

        #Bottom left dock widget - process and view
        self.mainProcessesDockWidget = QtGui.QDockWidget(self)
        self.mainProcessesDockWidget.setObjectName(_fromUtf8("mainProcessesDockWidget"))
        self.processWidget = QtGui.QWidget()
        self.processWidget.setObjectName(_fromUtf8("processWidget"))
        self.processWidgetHLayout = QtGui.QHBoxLayout(self.processWidget)
        self.processTabWidget = QtGui.QTabWidget(self.processWidget)
        self.processTabWidget.setObjectName(_fromUtf8("processTabWidget"))
        self.processTab = QtGui.QWidget()
        self.processTab.setObjectName(_fromUtf8("processTab"))
        self.processTabHLayout = QtGui.QHBoxLayout(self.processTab)
        self.processTreeWidget = QtGui.QTreeWidget(self.processTab)
        self.processTreeWidget.setObjectName(_fromUtf8("processTreeWidget"))
        self.processTreeWidget.headerItem().setText(0, _fromUtf8("Root process"))
        self.processTabHLayout.addWidget(self.processTreeWidget)
        self.processTabWidget.addTab(self.processTab, _fromUtf8("Process explorer"))

        self.tabWindow = QtGui.QWidget()
        self.tabWindow.setObjectName(_fromUtf8("tabWindow"))
        self.processTabWidget.addTab(self.tabWindow, _fromUtf8("Windows"))
        self.processWidgetHLayout.addWidget(self.processTabWidget)
        self.mainProcessesDockWidget.setWidget(self.processWidget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.mainProcessesDockWidget)

        #Messages area

        self.bottomDockWidget = QtGui.QDockWidget(self)
        self.bottomDockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.RightDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.bottomDockWidget.setObjectName(_fromUtf8("bottomDockWidget"))
        #child widget
        self.mainMessagesDockWidget = QtGui.QWidget()
        self.mainMessagesDockWidget.setObjectName(_fromUtf8("mainMessagesDockWidget"))
        self.mainMessagesDockWidgetHLayout = QtGui.QHBoxLayout(self.mainMessagesDockWidget)
        self.loggerTabWidget = QtGui.QTabWidget(self.mainMessagesDockWidget)
        self.loggerTabWidget.setObjectName(_fromUtf8("loggerTabWidget"))
        self.loggerTab = QtGui.QWidget()
        self.loggerTab.setObjectName(_fromUtf8("loggerTab"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.loggerTab)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.scrollArea = QtGui.QScrollArea(self.loggerTab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 725, 99))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.loggerTextBrowser = QtGui.QTextBrowser(self.scrollAreaWidgetContents)
        self.loggerTextBrowser.setObjectName(_fromUtf8("loggerTextBrowser"))
        self.horizontalLayout_4.addWidget(self.loggerTextBrowser)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.scrollArea)
        self.loggerTabWidget.addTab(self.loggerTab, _fromUtf8("Logger"))
        self.otherTab = QtGui.QWidget()
        self.otherTab.setObjectName(_fromUtf8("otherTab"))
        self.loggerTabWidget.addTab(self.otherTab, _fromUtf8("Other"))
        self.mainMessagesDockWidgetHLayout.addWidget(self.loggerTabWidget)
        self.mainMessagesDockWidget.setSizePolicy(QtGui.QSizePolicy.Minimum,
                                  QtGui.QSizePolicy.Preferred)
        self.bottomDockWidget.setWidget(self.mainMessagesDockWidget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.bottomDockWidget)
        
        #see http://stackoverflow.com/questions/13151601/pyqt-dock-on-side-of-stacked-qdockwidgets
        #toolbar widget
        '''
        self.toolbarDockWidget = QtGui.QDockWidget(self)
        self.toolbarDockWidget.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.toolbarDockWidget.setObjectName(_fromUtf8("toolbarDockWidget"))
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.toolbarDockWidget)
        '''
        
    def configureWidgets(self):

        #set margins to zero

        self.mainTreeDockWidget.setContentsMargins(0, 0, 0, 0)
        self.mainTreeDockWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.mainProcessesDockWidget.setContentsMargins(0, 0, 0, 0)
        self.mainProcessesDockWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.processWidget.setContentsMargins(0, 0, 0, 0)
        self.processWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.mainMessagesDockWidget.setContentsMargins(0, 0, 0, 0)
        self.mainMessagesDockWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.loggerTabWidget.setContentsMargins(0, 0, 0, 0)
        self.loggerTab.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)
#        self.loggerTabWidget.layout().setContentsMargins(0, 0, 0, 0)

    def disableActionsOnStart(self):
        self.actionImport_file.setEnabled(False)
        self.actionWell_plot_window.setEnabled(False)
        self.actionSave_project_as.setEnabled(False)
        self.actionSave_project.setEnabled(False)
        
    def enableActionsOnNewOrOpenProject(self):
        self.actionImport_file.setEnabled(True)
        self.actionWell_plot_window.setEnabled(True)
        self.actionSave_project_as.setEnabled(True)
        self.actionSave_project.setEnabled(True)
        
    def connectSlots(self):
        logger.debug('>connectSlots')
        
        self.actionNew_project.triggered.connect(self.newProjectTriggered)
        self.actionImport_file.triggered.connect(self.importFileTriggered)
        self.actionWell_plot_window.triggered.connect(self.wellPlotTriggered)
        self.actionSave_project_as.triggered.connect(self.saveProjectAsTriggered)
        self.actionAbout.triggered.connect(self.actionAboutTriggered)

    def closeEvent(self, event):
        logger.info('Exiting')
        QMainWindow.closeEvent(self, event)

    def newProjectTriggered(self):
        logger.debug('>newProjectTriggered')
        defaultsInitialiser = DefaultsInitialiser()
        self.createProjectFile()
        self.enableActionsOnNewOrOpenProject()
        
    def createProjectFile(self):
        logger.debug(">>createProjectFile() TODO create file logic")
        
    def importFileTriggered(self):
        logger.debug('>importFileTriggered')
        self.showImportDialog()
    
    def wellPlotTriggered(self):
        logger.debug('>wellPlotTriggered')
        wellPlotSetupDialog = WellPlotSetupDialog(logs = None, well = None, logSet = None)
        wellPlotSetupDialog.exec_()
        #wellSelectionDialog = WellSelectionDialog()
        #wellSelectionDialog.exec_()
        
    def saveProjectAsTriggered(self):
        self.showSaveProjectAsDialog()

    def openFileDialog(self):
        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

    def showImportDialog(self):
        #see http://stackoverflow.com/questions/23002801/pyqt-how-to-make-getopenfilename-remember-last-opening-path/23003370#23003370
        dialog = QtGui.QFileDialog(self)
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        #fileName = dialog.getOpenFileName(self,
    #"Open file",  os.getenv('HOME'),"Ascii data (*.txt *.asc *.dat);;Checkshot data (*.asc *.chk *.txt *.vsp);;"
                                    #"Log data (*.las);;Well tops (*.asc *.txt);;Well survey (*.asc *.txt)")
        fileName = dialog.getOpenFileName(self, "/home/a/TestData/antelope-1_comp.las", "/home/a/TestData/antelope-1_comp.las")
        if fileName:
            logger.debug('--showImportDialog() '+str(fileName))
            self.openImportLasWizard(fileName)
        else:
            logger.debug('--showImportDialog()  cancelled')

        #f = open(fname, 'r')

        #with f:
        #    data = f.read()
        #    self.textEdit.setText(data)
        

        
    def showSaveProjectAsDialog(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        
        fileName = dialog.getOpenFileName(self, "", "")
        if fileName is not None:
            logger.debug('--showSaveProjectAsDialog() '+str(fileName))
            self.saveProjectAs(fileName)

    def openImportLasWizard(self, fileName):
        if fileName != None:
            wizard = ImportLasWizard(fileName, self)
            wizard.exec_()
        
    def openImportLasDialog(self, fileName):
        pass
        '''
        form = ImportLasDialog(fileName, self)
        logger.debug("--openImportLasDialog() opening modal dialog")
        form.exec_()
        '''
        #if form.exec_():
            #plotter=totaldepth.PlotLogs
            #logger.debug("--openImportLasDialog() called mockPlot()")
            #plotter.mockPlot()


        '''
        importLasDialog = QtGui.QDialog(self)
        importLasView = ImportLas_View()
        importLasView.setupUi(importLasDialog)
        importLasDialog.show()
        '''
    def saveProjectAs(self, fileName):
        #create file
        #create directory
        #copy database
        fileNoPostfix = fileName.split(".")[0]
        fileObj = open(fileNoPostfix, 'wb')
        fileObj.write(str(AppSettings.softwareVersion))
        fileObj.close
        
        
    def startDatabase(self):
        logger.debug(">>startDatabase()")
        if not DM.init_db():
            logger.debug("Exiting application")
            sys.exit(app.exec_())
        '''
        from inout.las.reader.orm.laspersister import LasPersister
        lasPersister = LasPersister()
        lasPersister.write()
        '''
    def addDBTree(self):
        self.inputTabWidget = MainExplorer(settings = self.settings, name = "inputTreeWidget")
        self.mainTreeDockWidgetHLayout.addWidget(self.inputTabWidget)

        #self.inputTabGridLayout.addWidget(self.inputTreeWidget, 0, 0, 1, 1)
        
    def createStatusBar(self):
        sb = QStatusBar()
        sb.setFixedHeight(18)
        self.setStatusBar(sb)
        self.statusBar().showMessage(self.tr("Ready"))
        
    def actionAboutTriggered(self):
        """ About Avoca message"""   
        name = AppSettings.softwareName 
        company = AppSettings.companyName
        version = AppSettings.softwareVersion
        buildDate = AppSettings.buildDate
        buildNumber = AppSettings.buildNumber
        
        QtGui.QMessageBox.about(self, name, 
            """
            <b>%s for petrophysicists</p>
            <p><table border="0" width="150">
            <tr>
            <td>Version:</td>
            <td>%s</td>
            </tr>
            <tr>
            <td>Build date:</td>
            <td>%s</td>
            </tr>
            <tr>
            <td>Build number:</td>
            <td>%s</td>
            </tr>  
            <tr>
            <td>%s</td>
            </tr>               
            </table></p>
            """ % (name, version,buildDate, buildNumber, company))


app = QApplication(sys.argv)
window = MainApp()
window.show()
app.exec_()
