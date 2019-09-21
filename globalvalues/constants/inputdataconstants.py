'''
Created on 1 Feb 2015

@author: a
'''

class InputDataConstants(object):
    #  las data Parameter variables - use as lower priority than Well vars
    Z_DOMAIN_SIGNIFICANT_PLACES = 4
    GEOGRAPHIC_SIGNIFICANT_PLACES = 2
    MISC_SIGNIFICANT_PLACES = 2
    TEMP_SIGNIFICANT_PLACES = 2
    RESIS_SIGNIFICANT_PLACES = 2
    PARAMETER_DATA_SIGNIFICANT_PLACES = 3
    #maximum number of places to take precision to from input step
    #ie if input step is 0.123456789011111 then precision defaults to
    #Z_DOMAIN_SIGNIFICANT_PLACES 
    LAS_READER_Z_DOMAIN_MAXIMUM_EPSILON = 10