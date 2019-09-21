from PyQt4.QtGui import QWidget, QStandardItemModel, QTreeView, QListView,\
    QHBoxLayout, QLabel, QStandardItem, QIcon, QTreeWidgetItem, QMenu, QAbstractItemView

import logging
import numpy as np

from gui.wellplot.settings.layout.widgets.ui_tracklayoutwidget import Ui_TrackLayoutWidget
from gui.wellplot.settings.layout.widgets.tracklayouttreewidget import TrackLayoutTreeWidget
from globalvalues.appsettings import AppSettings
from gui.signals.wellplotsignals import WellPlotSignals
from gui.util.pymimedata import PyMimeData
from PyQt4.QtCore import pyqtSlot, Qt
from db.core.log.log import Log
from db.core.logset.logset import LogSet
from views.tree.myqtsqltreeview import DataTreeView, DataTreeItem
from db.windows.wellplot.wellplotdata.wellplotdatadao import WellPlotDataDao
from db.windows.wellplot.wellplotdata.wellplotdata import WellPlotData
from gui.util.wellplotutils import WellPlotUtils
from db.windows.wellplot.zaxistrackdata.zaxisdata import ZAxisData
from db.windows.wellplot.logtrackdata.logtrackdata import LogTrackData
from gui.wellplot.settings.layout.widgets.layouttree.layoutcontextmenu import LayoutItemSettings
from db.windows.wellplot.logtrackdata.logtrackdatadao import LogTrackDataDao
import copy
from db.windows.wellplot.zaxistrackdata.zaxisdatadao import ZAxisDataDao
from db.windows.wellplot.logtrackdata.logtrackutility import LogTrackUtility
from db.windows.wellplot.zaxistrackdata.zaxisdatautility import ZAxisDataUtility

logger = logging.getLogger('console')

class TrackTypes(object):
    INSERT_TRACK = "Insert track"
    INSERT_AXIS = "Insert axis"
    #items in tree
    TRACK = "Track"
    AXIS = "Axis"
    

class TrackLayoutWidget(QWidget, Ui_TrackLayoutWidget):
    '''
    TrackLayoutWidget for well plot settings
    Using QTreeWidget instead of QTreeView due to simpler model
    '''

    
    def __init__(self, wellPlotData, parent=None):
        super(TrackLayoutWidget, self).__init__(parent)
        self._wellPlotData = wellPlotData
        self._addIcon = None
        self._trackLayoutTreeWidget = None
        self._trackCount = 0
        self._axisCount = 0
        self._axisIcon = None
        self._trackIcon = None
        self._logIcon = None
        #reference to main DataTreeView singleton
        self._dataTreeView = DataTreeView()
        self._contextMenu = None
        self.wellPlotSignals = WellPlotSignals()
        self.isDirty = False
        self.setupUi(self)
        #self.populateTracksCreateCombo()
        self.addTreeWidget()
        self.setIcons()
        self.setInitialState()
        self.connectSlots()
        self.setContextMenu()

    def setIcons(self):
        logger.debug(">>setInitialState()")
        addAxisIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"insert-vertical-rule.ico")
        self.addAxisPushButton.setIcon(addAxisIcon)
        addTrackIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"addbkmrk_co.gif")
        self.addTrackPushButton.setIcon(addTrackIcon)
        rightArrowIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"arrow-right.png")
        self.rightArrowPushButton.setIcon(rightArrowIcon)
        upArrowIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"arrow-up-2.png")
        self.upPushButton.setIcon(upArrowIcon)
        downArrowIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"arrow-down-2.png")
        self.downPushButton.setIcon(downArrowIcon)
        deleteIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"dialog-cancel-3.png")
        self.deletePushButton.setIcon(deleteIcon)
        
        self._axisIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"vertical-rule.png")
        self._trackIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"bookmark_obj.gif")
        self._logIcon = QIcon(AppSettings.ACTIONS_ICON_PATH+"well-log.png")
        
    def setInitialState(self):
        '''Check dataset, populate tree with data'''
        

        
        plotDict = WellPlotUtils.createPlotDict(self._wellPlotData)
        for key, value in plotDict.items():
            if isinstance(value, ZAxisData):
                axisItem = self.createAxis(value)
                
            elif isinstance(value, LogTrackData):
                trackIem = self.createTrack(value)
                
                #Find the track, add logs to the tree
                logger.debug("--setInitialState() num tracks:{0}".format(len(self._wellPlotData.getLogTrackDatas())))
                for track in self._wellPlotData.getLogTrackDatas():
                    logger.debug("--setInitialState() track title:{0}, logs:{1}, index:{2}, id:{3}".format(track.title, track.getLogs(), track.plot_index, track.id))
                    if value.uid == track.uid:
                        for log in track.getLogs():
                            logItem = self.addChild(parent = trackIem, column=0, title= log.name, data= log)
                            logItem.setIcon(0, self._logIcon)

        
    def readWellPlotData(self):
        zAxes = WellPlotData.getZAxisDatas()
        tracks = WellPlotData.getLogTrackDatas()
        if (zAxes is None) or (len(zAxes) == 0):
            #if no axes, add an axis
            self.addAxisPushButtonClicked()
        
        
    def addTreeWidget(self):
        self._trackLayoutTreeWidget = TrackLayoutTreeWidget()
        #makes handling simpler if only single selection is enabled
        self._trackLayoutTreeWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        #if using QTableView
        #self._model = QStandardItemModel()
        #self._trackLayoutTreeWidget.setModel(self._model)
        self.scrollArea.setWidget(self._trackLayoutTreeWidget)
        self.scrollArea.setWidgetResizable(True)
        
    def rightArrowClicked(self):
        '''Checks data is right type, adds a track or appends to selected track '''
        selectedDataItems = self._dataTreeView.getSelectedItems()
        for item in selectedDataItems:
            self.addLogOnlyToTrack(item)
            #if using QTableView
            #addItemToQTableView


            
    def addLogOnlyToTrack(self, dataTreeItem):
        assert dataTreeItem is not None
        assert isinstance(dataTreeItem, DataTreeItem)
        self.isDirty = True
        try:
            if (dataTreeItem.tablename == Log.__tablename__) and not dataTreeItem.is_root:
                selectedTreeItems = self._trackLayoutTreeWidget.selectedItems()
                if selectedTreeItems:
                    firstNode = selectedTreeItems[0]
                    firstNodeData = firstNode.data(0, Qt.UserRole)
                    #check that child Node is a 'Track'
                    if isinstance(firstNodeData, LogTrackData):
                        logger.debug("--rightArrowClicked() firstNode: {0}, item.data: {1}".format(firstNode, dataTreeItem.data))
                        logItem = self.addChild(parent = firstNode, column=0, title= dataTreeItem.name, data=dataTreeItem.data)
                        logItem.setIcon(0, self._logIcon)
                    else:
                        self.addItemToNewTrack(dataTreeItem)
                else:
                    self.addItemToNewTrack(dataTreeItem)
        except:
            attrs = vars(dataTreeItem)
            logger.error("--addLogOnlyToTrack() paramItem properties: ")
            logger.error(', '.join("%s: %s" % item for item in attrs.items()))
            if AppSettings.isDebugMode:
                raise ValueError
                
    def addItemToNewTrack(self, item):
        self.isDirty = True
        #create the track
        trackItem = self.createTrack()
        
        newItem = self.addChild(parent = trackItem, column=0, title= item.name, data=item.data)
        if isinstance(item.data, Log):
            newItem.setIcon(0, self._logIcon)
             
    def addAxisPushButtonClicked(self):
        logger.debug(">>addAxisPushButtonClicked()")
        self.isDirty = True
        axisItem = self.createAxis()
        self._trackLayoutTreeWidget.setCurrentItem(axisItem)
      
    def createAxis(self, data = None):
        '''Creates new Axis from preferences if data parameter is none'''
        if data is None:
            zAxis = ZAxisDataUtility.createNewZAxis()
        else:
            assert isinstance(data, ZAxisData)
            zAxis = data
        self._axisCount += 1
        axisItem = self.addParent(parent = self._trackLayoutTreeWidget.invisibleRootItem(), column=0, title='Axis '+str(self._axisCount), data = zAxis)
        axisItem.setIcon(0, self._axisIcon)
        return axisItem

          
    def addTrackPushButtonClicked(self):
        logger.debug(">>addTrackPushButtonClicked()")
        self.isDirty = True
        trackIem = self.createTrack()
        self._trackLayoutTreeWidget.setCurrentItem(trackIem)
    
    def createTrack(self, data = None):
        '''Creates new Track from preferences if data parameter is none'''
        if data is None:
            trackData = LogTrackUtility.createNewTrack()
        else:
            assert isinstance(data, LogTrackData)
            trackData = data
            
        self._trackCount += 1
        title = TrackTypes.TRACK+" "+str(self._trackCount)
        trackIem = self.addParent(parent = self._trackLayoutTreeWidget.invisibleRootItem(), column=0, title=title, data=trackData)
        trackIem.setIcon(0, self._trackIcon)
        return trackIem
    
    def addParent(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, Qt.UserRole, data)
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        return item

    def addChild(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, Qt.UserRole, data)
        return item
    
    def setContextMenu(self):
        self._contextMenu = LayoutItemSettings()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.callContextMenu)
        
    def upPushButtonClicked(self):
        logger.debug(">>upPushButtonClicked()")
        self.isDirty = True
        selectedTreeItems = self._trackLayoutTreeWidget.selectedItems()
        if selectedTreeItems:

            firstNode = selectedTreeItems[0]
            firstNodeData = firstNode.data(0, Qt.UserRole)
            #index = self._trackLayoutTreeWidget.currentIndex()
            #parent = index.parent()
            #check that child Node is a 'Track'
            if isinstance(firstNodeData, Log):
                logger.debug("up for log")
                parent = firstNode.parent()
                parentData = parent.data(0, Qt.UserRole)
                siblings = parent.childCount()
                logger.debug("--upPushButtonClicked() siblings:{0}".format(str(siblings)))
                i = 0
                if siblings>1:
                    self.moveCurrentItemUp()
                    '''
                    for i in range(siblings):
                        item = parent.child(i) 
                        itemData =  item.data(0, Qt.UserRole)
                        if parentData is itemData:
                            logger.debug("Found track in multi sibling i:"+str(i))
                    '''
                else:
                    #find and add to next track yp
                    root = self._trackLayoutTreeWidget.invisibleRootItem()
                    childCount = root.childCount()
                    nonTrackCount = 0
                    trackCount = 0
                    for j in range(childCount):
                        item = root.child(j)
                        itemData =  item.data(0, Qt.UserRole)
                        if isinstance(itemData, LogTrackData):
                            trackCount += 1
                            if parentData is itemData: 
                                logger.debug(" found parent in single sibling {0}, text:{1}, count:{2}, trackCount:{3}".format(str(j), item.text(0), childCount, trackCount))
                                if trackCount == 1:
                                    #ignore the move
                                    return
                                else:
                                    #get next track up and put there
                                    logger.debug(" trackCount:{0}, nonTrackCount:{1}, childCount:{2}".format(trackCount, nonTrackCount, childCount))
                                    assert (childCount - 1) >= (trackCount - 1) + (nonTrackCount - 1)
                                    destination = root.child((trackCount - 1) + (nonTrackCount - 1))
                                    destinationData =  item.data(0, Qt.UserRole)
                                    assert isinstance(destinationData, LogTrackData)
                                    logItem = self.addChild(parent = destination, column = 0, title = firstNode.text(0), data = firstNodeData)
                                    logItem.setIcon(0, self._logIcon)
                                    #remove the current node, note has no siblings, i=0
                                    parent.takeChild(i)
                                    #set selected to item are moving so can keep moving up/down quickly
                                    self._trackLayoutTreeWidget.setCurrentItem(logItem)
                            
                        else:
                            nonTrackCount += 1
                '''work out where are
                what tree is
                if can move->move
                else ->ignore'''

            elif isinstance(firstNodeData, ZAxisData):
                logger.debug("up for axis")
                
            elif isinstance(firstNodeData, LogTrackData):
                logger.debug("up for track")
                
    def moveCurrentItemUp(self):
        '''Moves log order within track'''
        selectedTreeItems = self._trackLayoutTreeWidget.selectedItems()
        if selectedTreeItems and len(selectedTreeItems) == 1:
            item = selectedTreeItems[0]
            itemData =  item.data(0, Qt.UserRole)
            parent = item.parent()
            childCount = parent.childCount()
            
            #get children
            location = 0
            siblings = []
            if childCount > 1:
                for i in range(childCount):
                    sibling = parent.child(i)
                    logger.debug("--moveCurrentItemUp() sibling:{0}".format(i))
                    if sibling == item:
                        logger.debug("--moveCurrentItemUp() location:{0}".format(i))
                        location = i
                    siblings.append(sibling)
                    
                if location != 0:
                    #switch position
                    a, b = siblings.index(parent.child(location-1)), siblings.index(parent.child(location))
                    siblings[b], siblings[a] = siblings[a], siblings[b]
                
                #clear the tree
                #if parent.childCount()>1:
                #self._trackLayoutTreeWidget.setSelectionMode(QAbstractItemView.NoSelection)
                logger.debug("parent.childCount():{0}, childCount:{1}".format(parent.childCount(), childCount))
                #makes no differemce
                self._trackLayoutTreeWidget.setCurrentItem(self._trackLayoutTreeWidget.invisibleRootItem())
                for j in range(childCount): 
                    #tempNode = parent.child(j)
                    logger.debug("--moveCurrentItemUp() clearing tree:{0}".format(j))
                    #This runs but the child is not removed when j == childCount-1
                    parent.takeChild(j)
                    #parent.removeChild(tempNode)
                    logger.debug("child count:{0}".format(parent.childCount(), str(j)))
                
                assert parent.childCount() == 0
                assert childCount == len(siblings)
                #add all children back
                for node in siblings:
                #only works when have 1 selected item
                #row  = self._trackLayoutTreeWidget.currentIndex().row()
                #parent.takeChild(row)
                    logger.debug("--moveCurrentItemUp() addChild: {0}".format(node.text(0)))
                    self.addChild(parent, 0, node.text(0), node.data(0, Qt.UserRole))
                    item = None
                

            assert childCount == parent.childCount()
                
            
    def moveCurrentItemDown(self):
        item = self._trackLayoutTreeWidget.currentItem();
        row  = self._trackLayoutTreeWidget.currentIndex().row()
        if (item) and  (row > 0):
            self._trackLayoutTreeWidget.takeTopLevelItem(row);
            self._trackLayoutTreeWidget.insertTopLevelItem(row + 1, item);
            self._trackLayoutTreeWidget.setCurrentItem(item);
        

    def getTreePath(self, item):
        path = []
        while item is not None:
            path.append(str(item.text(0)))
            item = item.parent()
        return '/'.join(reversed(path))
    
    def downPushButtonClicked(self):
        logger.debug(">>downPushButtonClicked()")
        self.isDirty = True
        selectedTreeItems = self._trackLayoutTreeWidget.selectedItems()
        if selectedTreeItems:
            firstNode = selectedTreeItems[0]
            firstNodeData = firstNode.data(0, Qt.UserRole)
            #check that child Node is a 'Track'
            if isinstance(firstNodeData, LogTrackData):
                logger.debug("down for track")

            elif isinstance(firstNodeData, ZAxisData):
                logger.debug("down for axis")
                
            elif isinstance(firstNodeData, Log):
                logger.debug("down for log")
                
    def deletePushButtonClicked(self):
        logger.debug(">>deletePushButtonClicked()")
        self.isDirty = True
        selectedTreeItems = self._trackLayoutTreeWidget.selectedItems()
        if selectedTreeItems:
            firstNode = selectedTreeItems[0]
            firstNodeData = firstNode.data(0, Qt.UserRole)
            #check that child Node is a 'Track'
            if isinstance(firstNodeData, LogTrackData):
                #calling firstNode.parent() returns None so going to root
                root = self._trackLayoutTreeWidget.invisibleRootItem()
                index = root.indexOfChild(firstNode)
                logger.debug(str(index))
                root.takeChild(index)

            elif isinstance(firstNodeData, ZAxisData):
                logger.debug("delete for axis")
                if firstNodeData.is_primary:
                    logger.info("Cannot remove primary axis track")
                    return 
                else:
                    root = self._trackLayoutTreeWidget.invisibleRootItem()
                    index = root.indexOfChild(firstNode)
                    logger.debug(str(index))
                    root.takeChild(index)
                
            elif isinstance(firstNodeData, Log):
                logger.debug("delete for log")
                parent = firstNode.parent()
                index = parent.indexOfChild(firstNode)
                parent.takeChild(index)
            
    def callContextMenu(self):
        logger.debug(">>callContextMenu()")
        # is selection uniform
        tablenames= [ ]
        ids = [ ]
        
        selectedTreeItems = self._trackLayoutTreeWidget.selectedItems()
        if selectedTreeItems:
            firstNode = selectedTreeItems[0]
            firstNodeData = firstNode.data(0, Qt.UserRole)
            #check type of child Node 
            if isinstance(firstNodeData, ZAxisData):
                logger.debug("Axis, TODO - bring up settings dialog")

            elif isinstance(firstNodeData, LogTrackData):
                logger.debug("Track, TODO - bring up settings dialog")
                
            else:
                #check if is a Log
                if isinstance(firstNodeData, Log):
                    logger.debug("Log, TODO - bring up settings dialog")
                   
        '''        
        for index in self._trackLayoutTreeWidget.selectedIndexes():
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
        '''

    @pyqtSlot(PyMimeData)
    def trackLayoutItemDropped(self, pyMimeData):
        logger.debug(">>trackLayoutItemDropped()")
        if isinstance(pyMimeData, PyMimeData):
            instance = pyMimeData.instance()
            #only allow logs to be dragged across
            self.addLogOnlyToTrack(instance)

            #if using QTableView
            #self.addItemToQTableView()
        else:
            logger.debug("--trackLayoutItemDropped() mimeData not instance of PyMimeData")
        
    def connectSlots(self):
        self.wellPlotSignals.settingsTrackLayoutItemDropped.connect(self.trackLayoutItemDropped)
        self.rightArrowPushButton.clicked.connect(self.rightArrowClicked)
        self.addAxisPushButton.clicked.connect(self.addAxisPushButtonClicked)
        self.addTrackPushButton.clicked.connect(self.addTrackPushButtonClicked)
        self.upPushButton.clicked.connect(self.upPushButtonClicked)
        self.downPushButton.clicked.connect(self.downPushButtonClicked)
        self.deletePushButton.clicked.connect(self.deletePushButtonClicked)
        
    

    #deprecated
    def addItemToQTableView(self, item, selectedItems):
        standardItem = QStandardItem(item.name)
        standardItem.setData(item.data)
        logger.debug("--rightArrowClicked() self._model.appendRow(standardItem) selectedItems: {0}".format(len(selectedItems)))
        self._model.appendRow(standardItem)
    