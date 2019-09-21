'''
Created on 29 Dec 2014

@author: a
'''
import logging
import unittest
from db.databasemanager import DM
from db.core.well.well import Well

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('console')

class DatabaseManagerTest(unittest.TestCase):


    def test_init_db(self):
        logger.debug(">>test_init_db")
        #DM.getBase()
        DM.init_db()
        
    def test_getSession(self):
        logger.debug(">>test_getSession")
        DM.init_db()
        session = DM.getSession()
        session.close()
        
    def test_write(self):
        logger.debug("--test_write() ")
        DM.init_db()
        session = DM.getSession()
        well = Well()
        well.name = "Hampo"
        well.depth_reference = "MDKB"
        well.elevation_of_depth_reference = "24.0"
        session.add(well)
        session.commit()
        logger.debug("--test_write() id: "+str(well.id))
        dummy = session.query(Well).filter(Well.name == 'Hampo').one()
        logger.debug("--test_write() dummy: "+str(dummy.name)+" object: "+str(dummy))
        self.assertEqual("Hampo", dummy.name)
        session.close()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()