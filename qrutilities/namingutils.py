

class NamingUtils(object):
    '''
    Utilities related to object naming
    '''

    @classmethod
    def createUniqueMnemonic(cls, mnem, unitMap):
        """ If mnemonic exists in dict appends a _x where x is an int """
        result = mnem
        if mnem in unitMap:
            suffix = 1
            while (mnem + "_" + str(suffix)) in unitMap:
                suffix += 1
            result = mnem + "_" + str(suffix)
        return result