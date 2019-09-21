#encoding : utf-8 

"""
This modules provide context menu classes for qtsqltreview.
"""

from db.databasemanager import DM
from db.core.well.well import Well


import logging

from db.core.well.welldao import WellDao
from db.core.log.logdao import LogDao
from db.core.logset.logsetdao import LogSetDao

from gui.wellplot.setup.wellplotsetupdialog import WellPlotSetupDialog
from gui.settings.wellsettingsdialog import WellSettingsDialog

logger = logging.getLogger('console')

class MenuItem(object):
    name = ''
    table = None # None  for alltable
    mode = 'all' # or all unique homogeneous empty
    icon = ''
    def execute(self, **kargs):
        logger.debug ('Not implemented', self.name)
        logger.debug (kargs)
            
class WellPlot(MenuItem):
    name = 'Well plot'
    table = None
    mode = 'homogeneous'
    icon = ''
    def execute(self, session, treeview, explorer, ids, tablename,  treedescription, **kargs):
        logger.debug("WellPlot --execute()")
        session = DM.getSession()
        selectedLogSet = None
        if tablename.title() == "Well":
            if len(ids)>1:
                logger.info("Plotting first selected well")
            selectedWell = WellDao.getWell(ids[0], session)
            logs = LogDao.getWellLogs(ids[0], session)
        elif tablename.title() == "Log_Set":
            if len(ids)>1:
                logger.info("Plotting first selected log set")
            selectedWell = WellDao.getWell(ids[0], session)
            selectedLogSet = LogSetDao.getLogSet(ids[0], session)
            logs = LogDao.getLogSetLogs(ids[0], session)
        session.close()
        if (logs != None) and (selectedWell != None):
            #need to connect WellPlotMPL to main application so can receive signals
            #centralTabWidget = CentralTabWidget()
            wellPlotSetupDialog = WellPlotSetupDialog(logs, well = selectedWell, logSet = selectedLogSet)
            wellPlotSetupDialog.exec_()
            '''
            settings = RendererSettings()
            if settings.plotRenderer == PlotRenderer.pyqtgraph:
                wellPlotPyQtGraph = WellPlotPG(logs, well = selectedWell, logSet = selectedLogSet, parent = centralTabWidget)
            elif settings.plotRenderer == PlotRenderer.matplotlib:
                wellPlot = WellPlotMPL(logs, well = selectedWell, logSet = selectedLogSet, parent = centralTabWidget)
            '''
        else:
            logger.warn("Error getting data from database, cannot plot logs")
        explorer.refresh()
        
class Settings(MenuItem):
    name = 'Settings'
    table = None
    mode = 'homogeneous'
    icon = ''
    def execute(self, session, treeview, explorer,ids, tablename,  treedescription, **kargs):
        logger.debug("Settings --execute()")
        session = DM.getSession()
        if tablename.title() == "Well":
            if len(ids) > 1:
                logger.info("Settings for first well selected")
            rs = session.query(Well).filter(Well.id == ids[0])
            assert rs.count() == 1
            for well in rs:
                logger.debug("--plotLogs() well: "+str(well.name))
                dialog = WellSettingsDialog(well)
                dialog.exec_()
            session.close()
        explorer.refresh()
   
   
'''       
class ContextMenuPlotLogic(object):
    @classmethod
    def getWell(cls, session, ids):
        # gets well of given id from database 
        if len(ids) == 0:
            return None
        if len(ids) > 1:
                logger.info("Plotting first well selected")
        selectedWell = None
        rs = session.query(Well).filter(Well.id == ids[0])
        assert rs.count() == 1
        for well in rs:
            logger.debug("--getWell() well name: "+str(well.name))
            selectedWell = well 
        return selectedWell
    
    @classmethod
    def getLogSet(cls, session, ids):
        # gets logset of given id from database 
        if len(ids) == 0:
            return None
        if len(ids) > 1:
                logger.info("Plotting first log set selected")
        selectedLogSet = None
        rs = session.query(LogSet).filter(LogSet.id == ids[0])
        assert rs.count() == 1
        for logSet in rs:
            logger.debug("--getWell() well name: "+str(logSet.name))
            selectedLogSet = logSet 
        return selectedLogSet
    
    @classmethod
    def getWellLogs(cls, session, ids):
        # gets all logs from given well/log set from database 
        rs = session.query(Log).filter(Log.well_id == ids[0])
        logs = []
        for log in rs:
            logger.debug("--getWellLogs() log id: "+str(ids[0])+ " log: "+str(log.name))
            logs.append(log)
        return logs
       
    @classmethod     
    def getLogSetLogs(self, session, ids):
        # gets all logs from given log set from database 
        rs = session.query(Log).filter(Log.log_set_id == ids[0])
        logs = []
        for log in rs:
            logger.debug("--getLogSetLogs() log id: "+str(ids[0])+ " log: "+str(log.name))
            logs.append(log)
        return logs
'''
 

    

context_menu = [ WellPlot, Settings, ]  