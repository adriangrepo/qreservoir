#encoding : utf-8 


"""
This modules provide a widget able to display a treeview of a SQL schema


TODO : context menu
TODO : filter and order

"""



from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np
#import quantities as pq
#from gui.guiutil.icons import icons

from sqlalchemy.sql import select

from operator import itemgetter, attrgetter

import time
import logging
from globalvalues.appsettings import AppSettings
from db.classmapper import ClassMapper
from PyQt4 import QtCore
import pickle
from copy import deepcopy
from gui.util.pymimedata import PyMimeData

logger = logging.getLogger('console')

__TreeViewInstance = None

class DataTreeDescription(object):
    def __init__(self,
                            name = 'New',
                            #dbinfo = None,
                            table_children = { },
                            columns_to_show = { },
                            table_on_top = 'well',
                            table_order = { },
                        ):
        object.__init__(self)
        
        
        self.name = name
        self.table_children = table_children
        
        #test
        for item in table_children:
            logger.debug("DataTreeDescription __init__ table_children item: "+str(item))
        #end test
        
        self.columns_to_show = columns_to_show
        self.table_on_top = table_on_top
        self.table_order = table_order
        logger.debug("__init__ name: "+str(name)+" table_on_top: "+str(table_on_top)+" table_order: "+str(table_order))
        for item in table_children:
            logger.debug("DataTreeDescription __init__ name: "+str(name)+" child: "+str(item))
        self.check_and_complete()
    
    def __getstate__(self):
        # for pickle
        d = { }
        for attr in ['name', 'table_children', 'columns_to_show', 'table_on_top', 'table_order']:
            d[attr] = self.__dict__[attr]
        return d
    
    def check_and_complete(self):
        pass
        


class DataTreeItem(object):
    def __init__(self, tablename, id, parent, row):
        logger.debug("DataTreeItem __init__  tablename: "+str(tablename))
        self.tablename = tablename
        self.id = id
        self.parent = parent
        self.row = row
        #is set in data() = name of log/logset
        self.name = None
        #is set in data() = actual well, log/logset etc instance
        self.data = None
        self.children = None
        self.is_root = self.tablename is None and self.id is None

        logger.debug("DataTreeItem __init__ parent: "+str(parent)+" tablename: "+str(tablename)+" row: "+str(row)+" is_root: "+str(self.is_root))
        self.columns_display = { }
    
    def children_count(self, session, treedescription):
        return len(self.get_children(session, treedescription))
    
    def get_child(self, row, session, treedescription):
        return self.get_children(session, treedescription)[row]
    
    def get_children(self, session, treedescription):
        if self.children is None:
            if self.is_root:
                childnames = [ treedescription.table_on_top ]
            else:
                try:
                    childnames = treedescription.table_children[self.tablename]
                #log has no children (cf OpenElectrophy where eg SpikeTrain does)
                except KeyError as e:
                    logger.debug("DataTreeItem --get_children() no children for "+str(self.tablename)+" "+str(e))
                    self.children = []
                    return self.children
            
            self.children = [ ]
            row = 0
            for childname in childnames:
                if childname in  treedescription.table_order:
                    #~ order_by = childname+'.'+treedescription.table_order[childname]
                    order_by = treedescription.table_order[childname]
                else:
                    order_by = None
                if self.is_root:
                    q = select(columns = [ childname+'.id'],
                                    from_obj = [childname],
                                    order_by = order_by,
                                    )
                    '''
                    elif childname in treedescription.tablename_to_class[self.tablename].many_to_many_relationship:
                        #many to many
                        xref = self.tablename+'XREF'+childname
                        if xref not in treedescription.dbinfo.metadata.tables:
                            xref =childname+'XREF'+self.tablename
                        q = select(columns = [ childname+'.id'],
                                        whereclause = '{}.id = {}.{}_id AND {}.{}_id = {}'.format(childname, xref,childname.lower(), xref, self.tablename.lower(), self.id),
                                        from_obj = [childname, xref],
                                        order_by = order_by,
                                        )
                    
                    else:
                    '''
                else:
                    # one to many
                    q = select(columns = [ childname+'.id'],
                                        whereclause = '{}.{}_id = {}'.format(str(childname).lower(), self.tablename, self.id),
                                        from_obj = [childname],
                                        order_by = order_by,
                                        )
                    logger.debug("DataTreeItem --get_children() self is not root: "+str(q))
                #~ for id, in session.execute(q):
                for id, in session.bind.execute(q):
                    logger.debug("DataTreeItem --get_children() appending child: "+str(childname)+" id: "+str(id)+" row: "+str(row))
                    self.children.append(DataTreeItem(childname, id, self, row))
                    row +=1
                    
        
        return self.children
        
        def get_parent(self):
            return self.parentitem

def DataTreeView(*args, **kw):
    global __TreeViewInstance
    if __TreeViewInstance is None:
        __TreeViewInstance = __DataTreeView(*args, **kw)
    return __TreeViewInstance


class __DataTreeView(QTreeView):
    ''' Data tree view singleton so can access selected item from anywhere '''

    def __init__(self, parent =None):
        QTreeView.__init__(self,parent)
        self.setIconSize(QSize(22,22))
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDropIndicatorShown(True)
        
        
    def getSelectedItems(self):       
        '''returns list of items selected in tree '''
        indexes = self.selectionModel().selectedIndexes()
        
        #indexes = self.selectedIndexes()
        selectedItems = []
        #two indexes at same row are getting added - only want one
        previousRow = -1
        for index in indexes:
            if index.row() != previousRow:
                logger.debug("--getSelectedItems() indexes selected:{0}, row:{1}".format(len(indexes), index.row()))
                selectedItem = index.model().nodeFromIndex(index) 
                selectedItems.append(selectedItem)
                previousRow = index.row()
        return selectedItems
    
    def getFirstSelectedItem(self):
        '''returns selected item in tree with index 0 '''
        index = self.selectionModel().selectedIndexes()[0]
        firstItem = index.model().nodeFromIndex(index)
        return firstItem


class DataTreeModel(QAbstractItemModel):
    """
    Implementation of a treemodel base on OpenElectrophy mapper layer on top of  sqlalchemy
    and mapper.
    """
    def __init__(self, parent =None ,
                        session = None,
                        treedescription = None,):

        QAbstractItemModel.__init__(self,parent)
        self.session= session
        self.td = treedescription
        
        self.rootItem = DataTreeItem(None, None, None, None)
        self._classMapper = ClassMapper()
        
        # nb of columns
        self.maxColumn = 0
        for fieldnames in self.td.columns_to_show.values() :
            if len(fieldnames)>self.maxColumn:
                self.maxColumn = len(fieldnames)+1
        
    
    def columnCount(self , parentIndex):
        #~ print '##columnCount', parentIndex, parentIndex.isValid()
        return self.maxColumn

    def rowCount(self, parentIndex):
        if not parentIndex.isValid():
            n= self.rootItem.children_count(self.session, self.td)
        else:
            item = parentIndex.internalPointer()
            n= item.children_count(self.session, self.td)
            #logger.debug("--rowCount() "+str(item.tablename)+" child count: "+str(n))

        return n


    def index(self, row, column, parentIndex):

        if not parentIndex.isValid():
            ind = self.createIndex(row, column, self.rootItem.get_children(self.session, self.td)[row])
        else:
            parentItem = parentIndex.internalPointer()
            ind = self.createIndex(row, column, parentItem.children[row])
        return ind
        
    def parent(self, index):
        if not index.isValid():
            ind = QModelIndex()
        else:
            item = index.internalPointer()
            if item.parent is None or item.parent.tablename is None:
                ind = QModelIndex()
            else:
                ind = self.createIndex(item.parent.row, 0, item.parent)
        return ind


    def data(self, index, role):
        if not index.isValid():
            return None    
        item = index.internalPointer()
        col = index.column()
        if role ==Qt.DisplayRole :
            fieldnames = self.td.columns_to_show[item.tablename]
            if col > len(fieldnames):
                ret = None
            else:
                if col not in item.columns_display:
                    if  col ==0:
                        item.columns_display[col] =  u'{} : {}'.format( item.tablename, item.id) 
                    else :
                        logger.debug("--data() query: "+str(self._classMapper.getMappedClasses().get(item.tablename))+" id: "+str(item.id))
                        inst = self.session.query(self._classMapper.getMappedClasses().get(item.tablename)).get(item.id) 
                            
                        fieldname= fieldnames[col-1]
                        if hasattr(inst, fieldname):
                            value = getattr(inst, fieldname)
                            logger.debug("--data() value: "+str(value))
                            item.columns_display[col] =  u'{} : {}'.format( fieldname, value)
                            #set the name attribute
                            item.name = value
                            item.data = inst
                            logger.debug("--data() fieldname: {0} value: {1}".format( fieldname, value))
                        else:
                            item.columns_display[col] =  u''
                    
                ret = item.columns_display[col]

        elif role == 'table_and_id':
            ret = item.tablename, item.id
            logger.debug("--data() table_and_id: "+str(item.tablename)+" "+str(item.id))
        else :
            ret = None
        return ret


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
            #return QtCore.Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | \
               Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled    
         
    def mimeTypes(self): 
        types = []
        types.append('application/x-ets-qt4-instance') 
        return types 

    def mimeData(self, index): 
        node = self.nodeFromIndex(index[0])       
        mimeData = PyMimeData(node) 
        return mimeData 


    def dropMimeData(self, mimedata, action, row, column, parentIndex): 
        if action == Qt.IgnoreAction: 
            return True 

        dragNode = mimedata.instance() 
        parentNode = self.nodeFromIndex(parentIndex) 

        # make an copy of the node being moved 
        newNode = deepcopy(dragNode) 
        newNode.setParent(parentNode) 
        self.insertRow(len(parentNode)-1, parentIndex) 
        
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), parentIndex, parentIndex) 
        return True 
    
    def nodeFromIndex(self, index): 
        return index.internalPointer() if index.isValid() else self.root 
    
    '''      
    def mimeTypes(self):
        return ['bstream', 'text/xml', 'text/plain']

    def mimeData(self, indexes):
        mimedata = QtCore.QMimeData()
        nodes = []
        for index in indexes:
            nodes.append(index.internalPointer())
        bstream = pickle.dumps(nodes)
        mimedata.setData('bstream', bstream)
        return mimedata


    def dropMimeData(self, mimedata, action, row, column, parent):
        if action == Qt.IgnoreAction: 
            return True   
        data = pickle.loads(str(mimedata.data('bstream')))
        print ('\n\t incoming row number:', row, ', incoming column:', column, \
            ', action:', action, ' mimedata: ', data.tablename)
        return True
    '''
    
    def supportedDropActions(self): 
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction         


class QtSqlTreeView(QWidget) :
    def __init__(self  , parent = None ,
                            session = None,
                            treedescription = None,
                            explorer = None,
                            settings = None,
                            context_menu = None,
                            ):
        QWidget.__init__(self, parent)
        
        self.session = session
        self.treedescription = treedescription
        self.explorer = explorer
        
        self.settings = settings
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.treeview = DataTreeView()
        self.mainLayout.addWidget(self.treeview)
        
        #~ self.model = DataTreeModel( session = self.session,treedescription = self.treedescription,)
        #~ self.treeview.setModel(self.model)
        self.refresh()
        
        self.context_menu = context_menu
        if self.context_menu is not None:
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.callContextMenu)
        
    def refresh(self):
        #~ self.layoutAboutToBeChanged.emit()
        self.model = DataTreeModel( session = self.session,treedescription = self.treedescription,)
        self.treeview.setModel(self.model)
        self.resizeColumWidth()
        
    def resizeColumWidth(self):
        # FIXME: this is a  draft
        # resize column
        for c in range( self.model.columnCount(QModelIndex()) ):
            if c == 0: N=200
            else: N = 150
            if self.treeview.columnWidth(c) <N:
                self.treeview.setColumnWidth(c, N)

    def callContextMenu(self):
        logger.debug(">>callContextMenu()")
        # is selection uniform
        tablenames= [ ]
        ids = [ ]
        for index in self.treeview.selectedIndexes():
            if index.column()==0:
                tablename, id = self.model.data(index , 'table_and_id')
                tablenames.append(tablename)
                ids.append( id )
        homogeneous = np.unique(tablenames).size == 1
        
        # create menu
        menu = QMenu()
        actions = { }
        for m in self.context_menu:
            if  m.table is None and \
                  ( (m.mode == 'unique' and len(ids)==1) or\
                    (m.mode == 'homogeneous' and homogeneous) or\
                    (m.mode =='all' ) or \
                    (m.mode =='empty' and len(ids)==0) ):
                act = menu.addAction(QIcon(m.icon), m.name)
                actions[act] = m
            if  m.table is not None and \
                ( (m.mode =='unique' and len(ids)==1) or \
                    (m.mode =='homogeneous' and homogeneous) ) and \
                m.table == tablenames[0] :
                act = menu.addAction(QIcon(m.icon), m.name)
                actions[act] = m
        
        # execute action
        act = menu.exec_(self.cursor().pos())
        if act is None : return
        m = actions[act]()
        kargs = dict( treeview = self,
                      settings = self.settings,
                      treedescription = self.treedescription,
                      session = self.session,
                      explorer = self.explorer,
                      )
        if m.mode == 'unique':
            kargs['id'] = ids[0]
            kargs['tablename'] = tablenames[0]
        elif m.mode == 'homogeneous':
            kargs['ids'] = ids
            kargs['tablename'] = tablenames[0]
        elif m.mode == 'all' :
            kargs['ids'] = ids
            kargs['tablenames'] = tablenames
        #~ print kargs.keys()
        m.execute( **kargs)

    
    #~ def getSelectedObject(self):
        #~ objects = [ ]
        #~ for index in self.treeview.selectedIndexes():
            #~ if index.column()==0:
                #~ objects.append(self.model.data(index , 'object'))
        #~ return objects
    
    #~ def getSelectedTableAndIDs(self):
        #~ tablenames= [ ]
        #~ ids = [ ]
        #~ for index in self.treeview.selectedIndexes():
            #~ if index.column()==0:
                #~ tablename, id = self.model.data(index , 'table_and_id')
                #~ tablenames.append(tablename)
                #~ ids.append( id )
        #~ return tablenames, ids