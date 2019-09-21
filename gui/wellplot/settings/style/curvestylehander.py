import logging
from qrutilities.numberutils import NumberUtils
from PyQt4.Qt import Qt
from gui.signals.wellplotsignals import WellPlotSignals
from gui.util.qt.widgetutils import WidgetUtils
from db.windows.wellplot.logtrackdata.logtrackdata import LogTrackData
from db.core.log.log import Log
from qrutilities.imageutils import ImageUtils
from PyQt4.QtGui import QColor


logger = logging.getLogger('console')

class CurveStyleHandler(object):
    '''
    classdocs
    '''
        
    def saveDataState(self, wellPlotData, curveStyleWidget):
        '''called from apply/OK button, saves all data to log objects '''
        #assert twItem.data != None
        #assert isinstance(twItem.data(Qt.UserRole), tuple)
        #assert isinstance(twItem.data(Qt.UserRole)[0], LogTrackData)
        #assert isinstance(twItem.data(Qt.UserRole)[1], Log)
        allRows = curveStyleWidget.curveTableWidget.rowCount()
        for row in range(0, allRows):
            twItemName = curveStyleWidget.curveTableWidget.item(row,0)
            trackData = twItemName.data(Qt.UserRole)[0]
            tableLog = twItemName.data(Qt.UserRole)[1]
            for track in wellPlotData.getLogTrackDatas():
                for log in track.getLogs():
                    if track.plot_index == trackData.plot_index:
                        if log.id == tableLog.id:
                            logger.debug("track.plot_index :{0}, trackData.plot_index: {1}, log.id: {2}, tableLog.id: {3}, log.name: {4}".format(track.plot_index, trackData.plot_index, log.id, tableLog.id, log.name))

                            twItemLeftScale = curveStyleWidget.curveTableWidget.item(row,4)
                            log.left_scale = NumberUtils.straightStringToFloat(twItemLeftScale.text())
                            twItemRightScale = curveStyleWidget.curveTableWidget.item(row,5)
                            log.right_scale = NumberUtils.straightStringToFloat(twItemRightScale.text())
                            twItemLogarithmic = curveStyleWidget.curveTableWidget.item(row,6)
                            log.logarithmic = WidgetUtils.getBoolFromQtCheck(twItemLogarithmic.checkState())
                            
                            twItemCurveColour = curveStyleWidget.curveTableWidget.cellWidget(row,7)
                            r,g,b,a = QColor(twItemCurveColour.color()).getRgb()
                            rgbStr = ImageUtils.rgbToString(r,g,b)
                            log.rgb = rgbStr
                            
                            twItemOpacity = curveStyleWidget.curveTableWidget.item(row,8)
                            log.alpha = NumberUtils.straightStringToFloat(twItemOpacity.text())
                            twItemLineWidth = curveStyleWidget.curveTableWidget.item(row,9)
                            log.line_width = NumberUtils.straightStringToFloat(twItemLineWidth.text())
                            
                            twItemLineStyle = curveStyleWidget.curveTableWidget.cellWidget(row,10)
                            log.line_style = twItemLineStyle.currentText()
                            
                            twItemPointSize = curveStyleWidget.curveTableWidget.item(row,11)
                            log.point_size = NumberUtils.straightStringToFloat(twItemPointSize.text())
                            
                            twItemPointStyle = curveStyleWidget.curveTableWidget.cellWidget(row,12)
                            log.point_style = twItemPointStyle.currentText()
                            
                            twItemPointsOn = curveStyleWidget.curveTableWidget.item(row,13)
                            log.log_plot_points_on = WidgetUtils.getBoolFromQtCheck(twItemPointsOn.checkState())
        