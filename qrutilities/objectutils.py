'''
Created on 29 Mar 2015

@author: a
'''

class ObjectUtils(object):
    '''
    classdocs
    '''

    @classmethod
    def cmp(cls, a, b):
        ''' The Python 2 builtin cmp() has been removed in Python 3 '''
        return (a > b) - (a < b)
    
    @classmethod
    def shallowCopy (cls, destination, source):
        ''' copy all the properties between two (already present) instances'''
        #see http://stackoverflow.com/questions/243836/how-to-copy-all-properties-of-an-object-to-another-object-in-python
        destination.__dict__.update(source.__dict__)
        return destination