#!/usr/bin/env python
""" generated source for module ParameterEntity """
# package: com.qgs.qreservoir.jpa.data.model.entity


import datetime

class ParameterDTO(object):
    """ Parameter list holder """
    def __init__(self):
        self.id = int()
        #self.history = str()
        self.creationDate = datetime.datetime.now()
        self.updateDate = datetime.datetime.now()
        self.well = int()
        self.logService = int()
        self.logSet = int()
        self.name = str()
        self.parameterList = []



