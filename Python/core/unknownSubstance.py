import os


class UnknownSubstance:

    @staticmethod
    def unknown(aSubstance, aValue):

        unknown = {}
        unknown[aSubstance] = aValue
        return unknown

    @staticmethod
    def getItemByPath(aDict, aKey):

        key = None

        for keyType in aDict.keys():
            if keyType in aKey:
                key = keyType
                break

        return aDict.get(key)

    @staticmethod
    def getKeyPathByValue(aDict, aValue):

        for key, value in aDict.items():
            if value == aValue:
                return key

        return '{0}{1}{0}'.format(os.sep, aValue)
