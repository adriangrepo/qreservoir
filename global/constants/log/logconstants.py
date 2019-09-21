#!/usr/bin/env python
""" generated source for module LogConstants """
# package: com.qgs.qreservoir.global_.constants.log
class LogConstants(object):
    """ generated source for class LogConstants """
    LOG_NULL_VALUE = -999.25
    LOG_NAME_DEFAULT_DUPLICATE_POSTFIX = "_1"
    MAX_LOG_NAME_LENGTH = 100

    #  just using MAX_LOG_NAME_LENGTH -2 as a rough guide 
    #      * actual name length after postfix could be invalid
    #      * which should be handled by MAX_LOG_NAME_LENGTH
    #      
    MAX_POSTFIX_LENGTH = 98
    MAX_LOG_SAMPLES = 999999

    #  original was 1x10^6

