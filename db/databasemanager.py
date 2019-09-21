import logging
import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from PyQt4.QtCore import QObject, pyqtSignal
#from sqlalchemy.ext.declarative import declarative_base
from db.base import Base
from globalvalues.appsettings import AppSettings
from db.base import Base



logger = logging.getLogger('console')

Session = scoped_session(sessionmaker(autoflush=True))


#see http://stackoverflow.com/questions/9486345/is-it-ok-to-execute-code-when-a-module-imports
#TODO SQLAlchemy raises a warning when you try to configure an engine for the second time. - need to fix this

class DatabaseManager(QObject):
    """
    The top level database manager used by all the SQLAlchemy classes to fetch their session / declarative base.
    """
    engine = None
    base = None
    host= AppSettings.DATABASE_PROTOCOL + AppSettings.QR_DATABASE_NAME
    
    #connected to tree refresh slot
    databaseModifiedSignal  = pyqtSignal()

    def init_db(self):
        ''' Create the database and tables, returns without creating anything if db exists and can't delete it'''
        # initialisation required for object inheritance
        QObject.__init__(self) 
        if self.checkDBExists():
            if not self.deleteDB():
                return False
            
        import db.core.history.history
        import db.core.history.historyset
        import db.core.depthdata.depthdata
        import db.core.log.log
        import db.core.logdomain.logdomain
        import db.core.logservice.logservice
        import db.core.logset.logset
        import db.core.marker.marker
        import db.core.parameter.parameter
        import db.core.parameterset.parameterset
        import db.core.well.well
        import db.windows.logcurvepreferences.logcurvepreferences

        import db.windows.wellplot.zaxistrackdata.zaxisdata
        import db.windows.wellplot.wellplotdata.wellplotdata
        import db.windows.wellplot.logtrackdata.logtrackdata
        import db.windows.wellplot.template.wellplottemplate
        
        self.engine = create_engine(self.host, echo=False)
        self.base = Base()
        self.base.metadata.create_all(bind=self.engine)    
        logger.debug("Database "+str(self.host)+" created")
         
        return True
        
    def checkDBExists(self):
        ''' Returns True if db exists '''
        try:

            open(AppSettings.QR_DATABASE_NAME)
            logger.debug("Database: "+str(self.host)+" already exists")
            return True
        except IOError as e:
            if e.errno == 2: # No such file or directory
                logger.debug("No database named: "+str(self.host))
                return False
            else: # permission denied or something else?
                logger.error(str(e))
                return False
            
    def deleteDB(self):
        ''' Deletes db given in DatabaseProtocols '''

        try:
            os.remove(AppSettings.QR_DATABASE_NAME)
            logger.debug("Datbase "+str(AppSettings.QR_DATABASE_NAME)+" removed")
            return True
        except IOError as e:
            logger.error("Could not delete database "+str(AppSettings.QR_DATABASE_NAME)+" check file permissions")
            return False

    def ready(self):
        """Determines if the SQLAlchemy engine and base have been set, and if not, initializes them."""
        
        if self.engine and self.base:
            return True
        else:
            try:
                #self.engine = create_engine(host, pool_recycle=3600)
                #self.base = declarative_base(bind=self.engine)
                self.engine = create_engine(self.host, echo=True)
                self.base = Base()
                return True
            except:
                return False

    def getSession(self):
        """Returns the active SQLAlchemy session."""
        if self.ready():
            #session = Session()
            #session.configure(bind=self.engine)
            Session.configure(bind=self.engine)
            session = Session()
            return session
        else:
            return None

    def getBase(self):
        """Returns the active SQLAlchemy base."""
        logger.debug(">>getBase()")
        if self.ready():
            return self.base
        else:
            return None

    def getEngine(self):
        """Returns the active SQLAlchemy engine."""
        if self.ready():
            return self.engine
        else:
            return None
        
    
    def databaseModified(self):
        logger.debug(">>databaseModified()")
        self.databaseModifiedSignal.emit()

DM = DatabaseManager()