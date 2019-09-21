
import db.core.log.log as log
import db.core.logset.logset as logset
import db.core.parameterset.parameterset as parameterset
import db.core.well.well as well
import logging

logger = logging.getLogger('console')

class ClassMapper(object):
    mapped_classes = {}
    
    
    """ A python singleton see http://code.activestate.com/recipes/52558/ """
    class __impl:
        """ Implementation of the singleton interface """
        def spam(self):
            """ Test method, return singleton id """
            return id(self)
    # storage for the instance reference
    __instance = None


    def __init__(self):
        super(ClassMapper, self).__init__()
        """ Create singleton instance """
        # Check whether we already have an instance
        if ClassMapper.__instance is None:
            # Create and remember instance
            ClassMapper.__instance = ClassMapper.__impl()
        # Store instance reference as the only member in the handle
        self.__dict__['_ClassMapper__instance'] = ClassMapper.__instance
        
        #Classes used in main tree
        self.mapped_classes["log"] = log.Log
        self.mapped_classes["log_set"] = logset.LogSet
        self.mapped_classes["parameter_set"] = parameterset.ParameterSet
        self.mapped_classes["well"] = well.Well

        
    def getMappedClasses(self):
        return self.mapped_classes


        
        