
from globalvalues.appsettings import AppSettings

from db.databasemanager import DM
from db.core.basedao import BaseDao
from db.windows.wellplot.logtrackdata.logtrackdatadao import LogTrackDataDao

from db.windows.wellplot.zaxistrackdata.zaxisdatadao import ZAxisDataDao
from db.windows.wellplot.wellplotdata.wellplotdatabase import WellPlotDataBase

import logging


logger = logging.getLogger('console')

'''
class PlotStartDefaults(Enum):
    #see https://docs.python.org/3/library/enum.html  use .name to get the string name
    active = 1
    all = 2
    template = 3
'''
    
class WellPlotData(WellPlotDataBase):
    '''
    classdocs
    '''

    def getAllLogs(self):
        '''Returns all logs from all tracks '''
        logTrackDatas = self.getLogTrackDatas()
        logList = []
        for track in logTrackDatas:
            for log in track.getLogs():
                logList.append(log)
        return logList
        
    def getLogTrackDatas(self):
        ''' Retrieves lit of sub-plots from db on first call and stores them here '''
        if (len(self._log_track_datas) == 0) and (self._log_track_ids != ""):
            logger.debug("--getLogTrackDatas() getting sub_plots from DB")
            session = DM.getSession()
            subPlotIdList = LogTrackDataDao.convertJSONtoData(self._log_track_ids)
            self._log_track_datas = LogTrackDataDao.getLogTrackDatasFromIds(subPlotIdList, session)   
        return self._log_track_datas
        
    def getYData(self):
        ''' Retrieves lit of yData from db on first call and stores it here '''
        if (len(self.y_data) == 0) and (self.y_data_string != ""):
            session = DM.getSession()
            self.y_data = BaseDao.convertJSONtoData(self.y_data_string)
        return self.y_data

    def getZAxisDatas(self):
        ''' Retrieves lit of _z_axis_track_datas from db on first call and stores them here '''
        if (len(self._z_axis_track_datas) == 0) and (self._z_axis_track_ids != ""):
            session = DM.getSession()
            domainDataIdList = BaseDao.convertJSONtoData(self._z_axis_track_ids)
            domainTrackData = ZAxisDataDao()
            self._z_axis_track_datas = domainTrackData.getDomainTrackDatasFromIds(domainDataIdList, session)   
        return self._z_axis_track_datas
    
    def getZAxisPriority(self):
        ''' Retrieves lit of z measure track priorities  from db on first call and stores them here 
        eg MDKB highest priority followed by TVDSS etc..'''
        if (len(self.z_axis_track_priority) == 0):
            logger.debug("--getZAxisPriority() getting domain track priorities from DB")
            session = DM.getSession()
            self.z_axis_track_priority = LogTrackDataDao.convertJSONtoData(self.z_axis_priority_str)
        return self.z_axis_track_priority
    
    def getLogTrackData(self, index):
        '''Uses index parameter to retrieve specific track data item'''
        if index < len(self.getLogTrackDatas()):
            return self.getLogTrackDatas()[index] 
        else:
            logger.error("--getLogTrackData() index out of range of list")
            if AppSettings.isDebugMode:
                raise IndexError
            
    def getZAxisData(self, index):
        '''Uses index parameter to retrieve specific zAxis data item'''
        if index < len(self.getZAxisDatas()):
            return self.getZAxisDatas()[index] 
        else:
            logger.error("--getZAxisData() index out of range of list")
            if AppSettings.isDebugMode:
                raise IndexError
            
    def getMaximumLogsPerPlot(self):
        ''' returns maximum number of logs in any plot '''
        maxLogs = 0
        for plot in self.getLogTrackDatas():
            numLogs = len(plot.logs)
            if numLogs > maxLogs:
                maxLogs = numLogs
        return maxLogs
    
    