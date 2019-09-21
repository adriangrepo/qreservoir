import pyqtgraph as pg
from pyqtgraph.Qt import QtCore,QtGui
#from pyqtgraph.debug import Profiler as profiler
import numpy as np
#from ROI import ROI,RectROIcustom, PolyLineROIcustom
#from customItems import QActionCustom, QMenuCustom, ImageExporterCustom
import matplotlib
import pickle
import pyqtgraph.functions as fn
import types

import logging
from gui.signals.wellplotsignals import WellPlotSignals
logger = logging.getLogger('console')

class WellPlotViewBox(pg.ViewBox):
    """
    Subclass of ViewBox
    """
    signalShowT0 = QtCore.Signal()
    signalShowS0 = QtCore.Signal()
    
    ## additional mouse modes
    ValueMode = 4
    LineMode = 5

    def __init__(self, parent=None):
        """
        Constructor of the WellPlotViewBox
        """
        super(WellPlotViewBox, self).__init__(parent)
        #default mode
        #self.setValueMode()
        # Override pyqtgraph ViewBoxMenu
        self.menu = None 
        self.wellPlotSignals = WellPlotSignals()
        self.menu = self.getMenu() 

    def raiseContextMenu(self, ev):
        """
        Raise the context menu
        """
        if not self.menuEnabled():
            return
        menu = self.getMenu()
        pos  = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def getMenu(self):
        """
        Create the menu
        """
        if self.menu is None:
            self.menu = QtGui.QMenu()
            settings = QtGui.QAction("Settings", self.menu)
            self.menu.addAction(settings)
            settings.triggered.connect(self.openSettings)
            
            self.zoomMenu = QtGui.QMenu("Zoom")
            zoomGroup = QtGui.QActionGroup(self)
            viewAll = QtGui.QAction("View all", self.zoomMenu)
            viewAll.triggered.connect(self.autoRange)
            zoomIn = QtGui.QAction(u'Zoom in', self.zoomMenu)
            zoomIn.triggered.connect(self.zoomIn)
            zoomOut = QtGui.QAction(u'Zoom out', self.zoomMenu)
            zoomOut.triggered.connect(self.zoomOut)
            self.zoomMenu.addAction(viewAll)
            self.zoomMenu.addAction(zoomIn)
            self.zoomMenu.addAction(zoomOut)
            
            self.LMBMenu = QtGui.QMenu("Left mouse button mode")
            lmbGroup = QtGui.QActionGroup(self)
            horizontalLine = QtGui.QAction(u'Line', self.LMBMenu)
            value = QtGui.QAction(u'Value', self.LMBMenu)
            pan = QtGui.QAction(u'Pan', self.LMBMenu)
            zoomBox = QtGui.QAction(u'Zoom box', self.LMBMenu)
            self.LMBMenu.addAction(horizontalLine)           
            self.LMBMenu.addAction(value)
            self.LMBMenu.addAction(pan)
            self.LMBMenu.addAction(zoomBox)
            horizontalLine.triggered.connect(self.setLineMode)
            pan.triggered.connect(self.setPanMode)
            value.triggered.connect(self.setValueMode)
            zoomBox.triggered.connect(self.setRectMode)
            
            horizontalLine.setCheckable(True)
            pan.setCheckable(True)
            value.setCheckable(True)
            zoomBox.setCheckable(True)
            
            horizontalLine.setActionGroup(lmbGroup)
            pan.setActionGroup(lmbGroup)
            value.setActionGroup(lmbGroup)
            zoomBox.setActionGroup(lmbGroup)
            
            self.menu.addMenu(self.LMBMenu)
            self.menu.addMenu(self.zoomMenu)
            self.menu.addSeparator()
            self.showT0 = QtGui.QAction(u'Afficher les marqueurs d\'amplitude', self.menu)
            self.showT0.triggered.connect(self.emitShowT0)
            self.showT0.setCheckable(True)
            self.showT0.setEnabled(False)
            self.menu.addAction(self.showT0)
            self.showS0 = QtGui.QAction(u'Afficher les marqueurs de Zone d\'intégration', self.menu)
            self.showS0.setCheckable(True)
            self.showS0.triggered.connect(self.emitShowS0)
            self.showS0.setEnabled(False)
            self.menu.addAction(self.showS0)
        return self.menu

    def emitShowT0(self):
        """
        Emit signalShowT0
        """
        self.signalShowT0.emit()

    def emitShowS0(self):
        """
        Emit signalShowS0
        """
        self.signalShowS0.emit()
        
    def openSettings(self):
        self.wellPlotSignals.settingsOpenFired.emit()
        
    def setLineMode(self):
        pass
    
    def setValueMode(self):
        pass

    def setRectMode(self):
        """
        Set mouse mode to rect
        """
        self.setMouseMode(self.RectMode)

    def setPanMode(self):
        """
        Set mouse mode to pan
        """
        self.setMouseMode(self.PanMode)
        
    def setSelectMode(self):
        """
        Set mouse mode to select
        """
        #self.setMouseMode(self.)
        
    def setMouseMode(self, mode):
        """
        Set the mouse interaction mode. *mode* must be either ViewBox.PanMode or ViewBox.RectMode.
        In PanMode, the left mouse button pans the view and the right button scales.
        In RectMode, the left button draws a rectangle which updates the visible region (this mode is more suitable for single-button mice)
        """
        if mode not in [self.PanMode, self.RectMode, self.ValueMode, self.LineMode]:
            logger.error("Mode must be ViewBox.PanMode, ViewBox.RectMode, ViewBox.ValueMode or ViewBox.LineMode")
        self.state['mouseMode'] = mode
        self.sigStateChanged.emit(self)
        
    def zoomIn(self):
        pass
    
    def zoomOut(self):
        pass
        
    def autoRange(self, padding=None, items=None, item=None):
        '''Override autoRange so that x range is reset to within track limits'''
        super(WellPlotViewBox, self).autoRange(padding, items, item)
        #self.parent().autoRange(padding, items, item)
        #reset x scales for each widget
        
    '''        
    def childrenBoundingRect(self, *args, **kwds):
        range = self.childrenBounds(*args, **kwds)
        tr = self.targetRange()
        if range[0] is None:
            range[0] = tr[0]
        if range[1] is None:
            range[1] = tr[1]
            
        bounds = QtCore.QRectF(range[0][0], range[1][0], range[0][1]-range[0][0], range[1][1]-range[1][0])
        return bounds
            
    def childrenBounds(self, frac=None, orthoRange=(None,None), items=None):
        """Return the bounding range of all children.
        [[xmin, xmax], [ymin, ymax]]
        Values may be None if there are no specific bounds for an axis.
        """
        profiler = debug.Profiler()
        if items is None:
            items = self.addedItems
        
        ## measure pixel dimensions in view box
        px, py = [v.length() if v is not None else 0 for v in self.childGroup.pixelVectors()]
        
        ## First collect all boundary information
        itemBounds = []
        for item in items:
            if not item.isVisible():
                continue
        
            useX = True
            useY = True
            
            if hasattr(item, 'dataBounds'):
                #bounds = self._itemBoundsCache.get(item, None)
                #if bounds is None:
                if frac is None:
                    frac = (1.0, 1.0)
                xr = item.dataBounds(0, frac=frac[0], orthoRange=orthoRange[0])
                yr = item.dataBounds(1, frac=frac[1], orthoRange=orthoRange[1])
                pxPad = 0 if not hasattr(item, 'pixelPadding') else item.pixelPadding()
                if xr is None or (xr[0] is None and xr[1] is None) or np.isnan(xr).any() or np.isinf(xr).any():
                    useX = False
                    xr = (0,0)
                if yr is None or (yr[0] is None and yr[1] is None) or np.isnan(yr).any() or np.isinf(yr).any():
                    useY = False
                    yr = (0,0)

                bounds = QtCore.QRectF(xr[0], yr[0], xr[1]-xr[0], yr[1]-yr[0])
                bounds = self.mapFromItemToView(item, bounds).boundingRect()
                
                if not any([useX, useY]):
                    continue
                
                ## If we are ignoring only one axis, we need to check for rotations
                if useX != useY:  ##   !=  means  xor
                    ang = round(item.transformAngle())
                    if ang == 0 or ang == 180:
                        pass
                    elif ang == 90 or ang == 270:
                        useX, useY = useY, useX 
                    else:
                        ## Item is rotated at non-orthogonal angle, ignore bounds entirely.
                        ## Not really sure what is the expected behavior in this case.
                        continue  ## need to check for item rotations and decide how best to apply this boundary. 
                
                
                itemBounds.append((bounds, useX, useY, pxPad))
                    #self._itemBoundsCache[item] = (bounds, useX, useY)
                #else:
                    #bounds, useX, useY = bounds
            else:
                if int(item.flags() & item.ItemHasNoContents) > 0:
                    continue
                else:
                    bounds = item.boundingRect()
                bounds = self.mapFromItemToView(item, bounds).boundingRect()
                itemBounds.append((bounds, True, True, 0))
        
        #print itemBounds
        
        ## determine tentative new range
        range = [None, None]
        for bounds, useX, useY, px in itemBounds:
            if useY:
                if range[1] is not None:
                    range[1] = [min(bounds.top(), range[1][0]), max(bounds.bottom(), range[1][1])]
                else:
                    range[1] = [bounds.top(), bounds.bottom()]
            if useX:
                if range[0] is not None:
                    range[0] = [min(bounds.left(), range[0][0]), max(bounds.right(), range[0][1])]
                else:
                    range[0] = [bounds.left(), bounds.right()]
            profiler()
        
        #print "range", range
        
        ## Now expand any bounds that have a pixel margin
        ## This must be done _after_ we have a good estimate of the new range
        ## to ensure that the pixel size is roughly accurate.
        w = self.width()
        h = self.height()
        #print "w:", w, "h:", h
        if w > 0 and range[0] is not None:
            pxSize = (range[0][1] - range[0][0]) / w
            for bounds, useX, useY, px in itemBounds:
                if px == 0 or not useX:
                    continue
                range[0][0] = min(range[0][0], bounds.left() - px*pxSize)
                range[0][1] = max(range[0][1], bounds.right() + px*pxSize)
        if h > 0 and range[1] is not None:
            pxSize = (range[1][1] - range[1][0]) / h
            for bounds, useX, useY, px in itemBounds:
                if px == 0 or not useY:
                    continue
                range[1][0] = min(range[1][0], bounds.top() - px*pxSize)
                range[1][1] = max(range[1][1], bounds.bottom() + px*pxSize)

        return range
    '''