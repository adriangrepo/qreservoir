# -*- coding: utf-8 -*-


"""
This modules provide a explorer for managing treeviews
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from views.tree.myqtsqltreeview import DataTreeDescription, QtSqlTreeView
from db.databasemanager import DM
from views.tree.contextmenu import context_menu
#from .contextmenu import context_menu
#from gui.guiutil.icons import icons
#from gui.viewdesigner import ViewDesigner
#from gui.schemadesign import SchemaDesign
#from gui.importdata import ImportData



def get_standard_treeview():
    td = DataTreeDescription(
                                        name = 'Data',
                                        #dbinfo = dbinfo,
                                        table_children = { 'well' : ['log_set'],
                                                                    'log_set' : [ 'log'],
                                                                    },
                                        table_on_top = 'well',
                                        )
    
    td.columns_to_show = {  'well' : ['name'],
                                'log_set' : ['name',],
                                'log' : ['name', ],
                            }
    #td.check_and_complete()
    return td



#using own dbinfo
class MainExplorer(QWidget) :
    """
    Widget to design the treeview.
    """
    def __init__(self  , parent = None ,
                            #dbinfo = None,
                            settings = None,
                            name = None,
                            context_menu = context_menu,
                            ):
        QWidget.__init__(self, parent)
        
        #self.dbinfo = dbinfo
        self._session = DM.getSession()
        #here is where we connect database modified signal to refresh slot
        DM.databaseModifiedSignal.connect(self.refresh)
        
        self.name = name
        self.context_menu = context_menu
        
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.listTreeDescription = get_standard_treeview()

        self.settings = settings
        '''
        if self.settings is not None and self.name is not None:
            self.listTreeDescription = self.settings.getValueOrDefault('/listTreeDescription'+self.name, self.listTreeDescription)
            for td in self.listTreeDescription:
                td.check_and_complete(self.dbinfo)
        '''
        self.tabViews = QTabWidget()
        self.mainLayout.addWidget(self.tabViews)
        self.setObjectName("mainExplorer")
        self.createAction()
        self.createConfigureMenu() 
        self.deepRefresh()

    def createAction(self):
        #self.actionImport = QAction(u'&Import data in this db', self,
        #                                                        icon =QIcon(':/svn-update.png'))
        #self.actionImport.triggered.connect(self.openImportData)
        #self.addAction(self.actionImport)
        
        self.actionRefresh = QAction(self.tr("&Refresh view"), self,
                                                                icon = QIcon(':/view-refresh.png'),
                                                                shortcut = QKeySequence("F5"),
                                                                )
        self.actionRefresh.triggered.connect(self.refresh)
        self.addAction(self.actionRefresh)
        
        #self.actionAddTab = QAction(self.tr("&Add a new view"), self,
        #                                                    icon = QIcon(':/list-add.png'),
        #                                                    shortcut = QKeySequence("Ctrl+T"))
        #self.actionAddTab.triggered.connect(self.addOneTab)
        #self.addAction(self.actionAddTab)
        
        #self.actionDelTab = QAction(self.tr("&Remove this view"), self,
        #                                                    icon = QIcon(':/list-remove.png'),
        #                                                    shortcut = QKeySequence("Ctrl+W"))
        #self.actionDelTab.triggered.connect(self.closeCurrentTab)
        #self.addAction(self.actionDelTab)
        
        #self.actionEditTab = QAction(self.tr("&Edit this view"), self,
        #                                                    icon = QIcon(':/document-properties.png'))
        #self.actionEditTab.triggered.connect(self.editCurrentTab)
        #self.addAction(self.actionEditTab)
        
        
        #if hasattr(self.dbinfo, 'kargs_reopen'):
        #    self.actionSchemaDesign = QAction(self.tr("Modify schema (add columns and tables)"), self,
        #                                                        icon = QIcon(':/vcs_diff.png'))
        #    self.actionSchemaDesign.triggered.connect(self.openSchemaDesign)
        #    self.addAction(self.actionSchemaDesign)
        
        
        
    def createConfigureMenu(self):
        self.menuConfigure = QMenu()
        self.menuConfigure.addAction(self.actionRefresh)
        '''
        self.menuConfigure.addSeparator()
        self.menuConfigure.addAction(self.actionImport)
        self.menuConfigure.addSeparator()
        self.menuConfigure.addAction(self.actionAddTab)
        self.menuConfigure.addAction(self.actionDelTab)
        self.menuConfigure.addAction(self.actionEditTab)
        self.menuConfigure.addSeparator()
        if hasattr(self.dbinfo, 'kargs_reopen'):
            self.menuConfigure.addAction(self.actionSchemaDesign)
        '''
        
    
    def deepRefresh(self):
        """
        To be call in case on modification on schema.
        """
        #if dbinfo is not None: 
        #    self.dbinfo = dbinfo
        #for i in range(len(self.tabViews)):
        #    self.tabViews.removeTab(0)
        #self.session = self.dbinfo.Session()
        #for td in self.listTreeDescription:
        sqltreeview = QtSqlTreeView(session = self._session, treedescription = self.listTreeDescription, 
                            settings = self.settings, context_menu = self.context_menu,
                            explorer = self)
        self.tabViews.addTab(sqltreeview , self.listTreeDescription.name)
      
    # A slot for the "resfresh" signal
    @pyqtSlot()  
    def refresh(self):
        #self.dbinfo.Session.expire_all()
        #if self.dbinfo.cache is not None:
        #    self.dbinfo.cache.clear()
        #~ self.session = self.dbinfo.Session()
        #for i in range(len(self.listTreeDescription)):
        sqltreeview = self.tabViews.widget(0)
        #~ sqltreeview.session = self.session
        sqltreeview.refresh()

    def closeCurrentTab(self):
        self.closeOneTab(self.tabViews.currentIndex())
    
    def closeOneTab(self, num):
        if len(self.listTreeDescription) ==1:
            return
        self.tabViews.removeTab(num)
        self.listTreeDescription.pop(num)
        self.writeSettings()
        
    def addOneTab(self):
        self.editCurrentTab(new = True)
        
    def editCurrentTab(self, new = False):
        '''
        if new:
            td = DataTreeDescription(dbinfo = self.dbinfo)
        else:
            num = self.tabViews.currentIndex()
            td = self.listTreeDescription[num]
        w = ViewDesigner(dbinfo = self.dbinfo, treedescription = td, settings = self.settings)
        if w.exec_() : 
            td = w.getTreeDescription()
            if new:
                sqltreeview = QtSqlTreeView(session = self.session, treedescription = td, 
                                settings = self.settings, context_menu = self.context_menu,
                                explorer = self)
                self.tabViews.addTab(sqltreeview , td.name)
                self.listTreeDescription.append(td)
            else:
                self.listTreeDescription[num] = td
                sqltreeview = self.tabViews.currentWidget()
                sqltreeview.treedescription = td
                sqltreeview.refresh()
        self.writeSettings()
        '''
        pass

    def writeSettings(self):
        if self.settings is not None :
            self.settings[ '/listTreeDescription'+self.name] = self.listTreeDescription
    
    def showConfigureMenu(self):
        self.menuConfigure. exec_(QCursor.pos())
        
    def getCurrentSqlTreeView(self):
        return  self.tabViews.currentWidget()
    
    def openSchemaDesign(self):
        '''
        d = SchemaDesign(dbinfo = self.dbinfo)
        d.schema_changed.connect(self.schemaDesignRefresh)
        d.exec_()
        '''
        pass
    
    def schemaDesignRefresh(self):
        # open the data again to remap everything
        dia = self.sender()
        self.deepRefresh(dbinfo = dia.dbinfo)

    def openImportData(self):
        '''
        w = ImportData(dbinfo = self.dbinfo)
        w.setWindowTitle('Import new data in database')
        if w.exec_():
            self.refresh()
        '''
        pass

