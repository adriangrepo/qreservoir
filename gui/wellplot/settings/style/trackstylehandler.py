import logging
from qrutilities.numberutils import NumberUtils
from PyQt4.Qt import Qt
from gui.signals.wellplotsignals import WellPlotSignals
from qrutilities.imageutils import ImageUtils
from PyQt4.QtGui import QColor


logger = logging.getLogger('console')

class TrackStyleHandler(object):
    '''
    Logic for track style widget
    '''

    #should only be called on OK or Apply
    def saveDataState(self, wellPlotData, trackStyleWidget):     
        self.saveAllTableRows(wellPlotData, trackStyleWidget)
                        
        #run this after table code above - as title for a track may have been changed    
        self.saveAllTrackWidthGap(wellPlotData, trackStyleWidget)
        
    def saveAllTableRows(self, wellPlotData, trackStyleWidget):
        allRows = trackStyleWidget.trackTableWidget.rowCount()
        for row in range(0, allRows):
            twItemIndex = trackStyleWidget.trackTableWidget.item(row,0)
            twItemTitle = trackStyleWidget.trackTableWidget.item(row,1)
            twItemWidth = trackStyleWidget.trackTableWidget.item(row,3)
            twItemGap = trackStyleWidget.trackTableWidget.item(row,4)
            for track in wellPlotData.getLogTrackDatas():
                if (track.plot_index != -1) and track.is_displayed:
                    if str(track.plot_index) == twItemIndex.text():
                        track.title = twItemTitle.text()
                        track.track_width = NumberUtils.straightStringToFloat(twItemWidth.text())
                        track.track_gap = NumberUtils.straightStringToFloat(twItemGap.text())
                    
    def saveAllTrackWidthGap(self, wellPlotData, trackStyleWidget):
        if trackStyleWidget.trackApplyAllCheckBox.isChecked():
            trackWidth = trackStyleWidget.trackWidthLineEdit.text()
            trackGap = trackStyleWidget.trackGapLineEdit.text()
            for track in wellPlotData.getLogTrackDatas():
                if (track.plot_index != -1):
                    track.track_width = NumberUtils.straightStringToFloat(trackWidth)
                    track.track_gap = NumberUtils.straightStringToFloat(trackGap)
                    
    def saveGridStyle(self, wellPlotData, trackStyleWidget):
        showGrid = False
        if trackStyleWidget.applyGridToAllCheckBox.isChecked():
            if trackStyleWidget.gridDisplayedCheckBox.isChecked():
                showGrid = True
            r,g,b,a = QColor(trackStyleWidget.gridColorPushButton.color()).getRgb()
            rgbStr = ImageUtils.rgbToString(r,g,b)
            gridOpacity = trackStyleWidget.gridOpacitySpinBox.value()
            gridLineStyle = trackStyleWidget.gridLineStyleComboBox.currentText()
            linearVerticalDivisions = trackStyleWidget.linearGridVerticalDivisionsSpinBox.value()
            logVerticalDivisions = trackStyleWidget.logarithmicGridVerticalDivisionsSpinBox.value()
            
            for track in wellPlotData.getLogTrackDatas():
                if (track.plot_index != -1):
                    track.grid_rgb = rgbStr
                    track.grid_alpha = str(a)
                    track.grid_line_style = gridLineStyle
           
        
    def getNumberOfDisplayedTracks(self, wellPlotData):
        assert wellPlotData is not None
        numDisplayedTracks = 0
        if wellPlotData is not None:
            for trackData in wellPlotData.getLogTrackDatas():
                if trackData.is_displayed:
                    numDisplayedTracks +=1
        return numDisplayedTracks