import os


class UnknownSubstance:

    def unknown(self, aSubstance, aValue):

        unknown = {}
        unknown[aSubstance] = aValue
        return unknown

    def getItemByPath(self, aDict, aKey):

        key = None

        for keyType in aDict.keys():
            if keyType in aKey:
                key = keyType
                break

        return aDict.get(key)

    def getKeyPathByValue(self, aDict, aValue):

        for key, value in aDict.items():
            if value == aValue:
                return key

        return os.sep + str(aValue) + os.sep
