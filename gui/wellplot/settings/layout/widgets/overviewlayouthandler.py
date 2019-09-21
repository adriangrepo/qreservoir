from db.core.well.well import Well
from db.core.well.welldao import WellDao
from db.core.log.logdao import LogDao
from statics.types.logtype import LogType
import logging
from db.core.log.log import Log
from globalvalues.appsettings import AppSettings

from globalvalues.constants.wellplotconstants import WellPlotConstants


logger = logging.getLogger('console')

class OverviewLayoutHandler(object):
    '''
    Logic for OverviewLayout
    '''
    def checkHasGR(self, wellPlotData):
        if wellPlotData is not None:
            logTypeName = LogType.GAMMA.name
            logs = LogDao.getLogTypeLogs(wellPlotData.well.id, logTypeName)
            if len(logs)>0:
                return True
        return False

    def findLongestGRLog(self, well):
        '''Input parameter Well object
        Returns None no GR found'''
        assert isinstance(well, Well)
        grTypeName = LogType.GAMMA.name
        grLogs = LogDao.getLogTypeLogs(well.id, grTypeName)
        log = Log()
        longestLog = None
        if grLogs is not None:
            longestLog = log.findLogWithLargestDepthRange(grLogs)
        else:
            logger.info("No GR log found in well: {1}".format(well.name))
        return longestLog
    
    def findLongestLog(self, well):
        '''Input parameter Well object
        Returns longest log in well'''
        assert isinstance(well, Well)

        log = Log()
        longestLog = None

        allLogs = LogDao.getWellLogs(well.id)
        longestLog = log.findLogWithLargestDepthRange(allLogs)
        if longestLog == None:
            logger.warn("No log found in well: {1}".format(well.name))
        
        return longestLog

    def saveDataState(self, wellPlotData, overviewLayoutWidget):
        if overviewLayoutWidget.grRadioButton.isChecked():
            wellPlotData.overview_layout_selection == WellPlotConstants.OVERVIEW_LONGEST_GR_LOG
        elif overviewLayoutWidget.longestLogRadioButton.isChecked():
            wellPlotData.overview_layout_selection == WellPlotConstants.OVERVIEW_LONGEST_LOG
        else:
            wellPlotData.overview_layout_selection == WellPlotConstants.OVERVIEW_MANUAL_SELECTION
            wellPlotData.overview_layout_data_class == str(overviewLayoutWidget.dataClassComboBox.currentText())
            index = overviewLayoutWidget.dataClassComboBox.currentIndex() 
            data = overviewLayoutWidget.dataClassComboBox.itemData(index)
            wellPlotData.overview_layout_log_id == data
            

