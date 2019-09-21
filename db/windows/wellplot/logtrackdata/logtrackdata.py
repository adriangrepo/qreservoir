'''
Created on 1 Jun 2015

@author: a
'''
from db.windows.wellplot.logtrackdata.logtrackdatabase import LogTrackDataBase
from db.databasemanager import DM
from db.core.log.logdao import LogDao

from globalvalues.appsettings import AppSettings

import logging



logger = logging.getLogger('console')

class LogTrackData(LogTrackDataBase):
    '''Functionality on top of base Track class'''
    

    

    def getLogs(self):
        ''' Retrieves lit of logs from db on first call and stores them here '''
        if (len(self._logs) == 0) and (self.log_ids != None) and (self.log_ids != ""):
            session = DM.getSession()
            logIdList = (self.log_ids).split(",")
            self._logs = LogDao.getLogsFromIds(logIdList, session)  
            session.close()  
        return self._logs
    

    def addLog(self,  paramlog):
        ''' add a log if it's not in the logs list '''
        exists = False
        for log in self._logs:
            if paramlog.id == log.id:
                exists = True
                logger.error("--addLog() attempted to add an existing log "+str(paramlog.name))
                if AppSettings.isDebugMode:
                    raise ValueError
        if not exists:
            self._logs.append(paramlog)
            #debug
            logger.debug("--addLog() added log "+str(paramlog.name))
        
    def removeLog(self, paramlog):
        ''' remove a log if it exists '''
        #see http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
        newlogs = []
        logger.debug("--removeLog() len self._logs:"+str(len(self._logs)))
        for log in self._logs:
            logger.debug("--removeLog() paramlog.id: {0} log.id: {1}".format(paramlog.id, log.id))
            logger.debug("--removeLog() paramlog name: {0}".format(paramlog.name))
            logger.debug("--removeLog() log.name: {0}".format(log.name))
            if paramlog.id != log.id:
                newlogs.append(paramlog)
                
        #debugging
        original = LogDao.getLogNamesCSV(self._logs )
        new = LogDao.getLogNamesCSV(newlogs)
        logger.debug("--removeLog() original list: {0} new list: {1} ".format(original, new))
        #end debugging
        
        self._logs = newlogs
        
    def compareLogs(self, paramPlot):
        ''' returns boolean, if plot indexes are the same returns True if log id's differ in same track '''
        different = False
        if paramPlot.plot_index == self.plot_index:
            if len(paramPlot.getLogs()) != len(self._logs):
                logger.debug("--compareLogs() number of logs for plot "+str(self.plot_index)+" differ")
                different = True
            else: 
                #same length, check if id's are the different
                for inLog in paramPlot.getLogs():
                    logger.debug("--compareLogs() inLog.id: "+str(inLog.id))
                    for log in self._logs:
                        logger.debug("--compareLogs() inLog.id: "+str(inLog.id)+" log.id: "+str(log.id))
                        if inLog.id != log.id:
                            logger.debug("--compareLogs() inLog.id: "+str(inLog.id)+" != log.id: "+str(log.id))
                            different = True
                            return different
        return different