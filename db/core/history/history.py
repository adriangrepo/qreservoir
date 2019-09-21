'''
Created on 27 Jun 2015

@author: a
'''
from db.core.history.historybase import HistoryBase
import logging

from db.databasemanager import DM

logger = logging.getLogger('console')

class History(HistoryBase):
    '''
    Wrapper for HistoryBase object
    '''

