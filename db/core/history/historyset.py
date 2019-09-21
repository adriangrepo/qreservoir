'''
Created on 27 Jun 2015

@author: a
'''
from db.core.history.historysetbase import HistorySetBase
import logging

from db.databasemanager import DM

logger = logging.getLogger('console')

class HistorySet(HistorySetBase):
    '''
    Wrapper for HistorySetBase object
    '''

