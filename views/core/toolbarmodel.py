'''
Created on 4 Mar 2015

@author: a
'''

from PyQt4 import QtGui

class MainWindowModel(object):

    #### properties for value of Qt model contents ####

    def __init__(self):
        self._update_funcs = []
        self.config_section = 'settings'
        self.config_options = (
            ('importFile', 'getboolean'),
            ('saveProject', 'getboolean'),
            ('newProject', 'getboolean'),
            ('openProject', 'getboolean'),
            ('saveProjectAs', 'getboolean'),
        )

        #### create Qt models for compatible widget types ####

        #### model variables ####
        self.importFile = None
        self.saveProject = None
        self.newProject = None
        self.openProject = None
        self.saveProjectAs = None

    def subscribe_update_func(self, func):
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    def unsubscribe_update_func(self, func):
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    def announce_update(self):
        for func in self._update_funcs:
            func()