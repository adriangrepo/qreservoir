#encoding : utf-8 



from db.databasemanager import DM
from db.core.well.well import Well


import logging

from gui.settings.wellsettingsdialog import WellSettingsDialog

logger = logging.getLogger('console')

class LayoutMenuItem(object):
    name = ''
    table = None # None  for alltable
    mode = 'all' # or all unique homogeneous empty
    icon = ''
    def execute(self, **kargs):
        logger.debug ('Not implemented', self.name)
        logger.debug (kargs)
            

class LayoutItemSettings(LayoutMenuItem):
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
   


    

context_menu = [ LayoutItemSettings, ]  