'''
Created on 4 Apr 2015

@author: a
'''
from PyQt4.QtCore import Qt

import logging
from globalvalues.constants.plottingconstants import PenLineStyles
from PyQt4 import QtCore
from globalvalues.appsettings import AppSettings
from PyQt4.QtGui import QLayout

logger = logging.getLogger('console')

class WidgetUtils(object):
    '''
    classdocs
    '''

    @classmethod
    def removeWidgets(cls, layout):
        ''' remove widgets from a layout '''
        #TODO change exception to specific type
        try:
            for cnt in reversed(range(layout.count())):
                # takeAt does both the jobs of itemAt and removeWidget
                # namely it removes an item and returns it
                widget = layout.takeAt(cnt).widget()
        
                if widget is not None: 
                    # widget will be None if the item is a layout
                    widget.deleteLater()
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.debug(message)
        
    @classmethod
    def getQtPenStyle(cls, style):  
        '''
        returns Qt.PenStyle given PenLineStyles string
        '''
        #logger.debug(">>getQtPenStyle() "+str(style)+" "+PenLineStyles.solid.name)
        if style == PenLineStyles.solid.name:
            #logger.debug("--getQtPenStyle() PenLineStyles.solid ")
            return Qt.SolidLine
        elif style == PenLineStyles.dashed:
            return Qt.DashLine
        elif style == PenLineStyles.dash_dot:
            return Qt.DashDotLine
        elif style == PenLineStyles.dotted:
            return Qt.DotLine
        elif style == PenLineStyles.no_line:
            return Qt.NoPen
        elif style == PenLineStyles.dash_dot_dot:
            return Qt.DashDotDotLine
        elif style == PenLineStyles.custom:
            #A custom pattern defined using QPainterPathStroker.setDashPattern().
            return Qt.CustomDashLine
        
    @classmethod
    def getLabelWidthHeight(cls, label):
        brWidth = label.fontMetrics().boundingRect(label.text()).width()
        brHeight = label.fontMetrics().boundingRect(label.text()).height()
        return brWidth, brHeight
    
    @classmethod
    def getQtCheckObject(cls, flag):
        ''' if flag is True returns a checked object if False then unchecked '''
        if flag:
            return QtCore.Qt.Checked
        else:
            return QtCore.Qt.Unchecked
        
    @classmethod
    def getBoolFromQtCheck(cls, widgetState):
        if widgetState == QtCore.Qt.Checked:
            return True
        elif widgetState == QtCore.Qt.Unchecked:
            return False
        elif widgetState == QtCore.Qt.PartiallyChecked:
            logger.debug("Widget is partially checked")
            return False
        else:
            logger.error("Input data is invalid")
            if AppSettings.isDebugMode:
                raise ValueError
            return False
        
    @classmethod
    def getBoolFromQtCheckState(cls, widgetState):
        if widgetState == 2:
            return True
        elif widgetState == 0:
            return False
        else:
            logger.error("Input data is invalid")
            if AppSettings.isDebugMode:
                raise ValueError
            return False
        
    @classmethod
    def getLayoutsWidgets(cls, layout):
        assert isinstance(layout, QLayout)
        widgets = (layout.itemAt(i) for i in range(layout.count()))
        return widgets
        
        
