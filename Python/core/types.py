import os
from core.unknownSubstance import UnknownSubstance


class Types(UnknownSubstance):

    def __init__(self):

        self.x86 = 'x86'
        self.x64 = 'x64'
        self.IA64 = 'IA64'
        self.ARM = 'ARM'

        types = {}

        types[os.sep + 'x86' + os.sep] = self.x86
        types[os.sep + 'x64' + os.sep] = self.x64
        types[os.sep + 'ARM' + os.sep] = self.ARM
        types[os.sep + 'IA64' + os.sep] = self.IA64

        self.mCalligraphicTypes = dict(types)

        types[os.sep + 'X86' + os.sep] = self.x86
        types[os.sep + 'X64' + os.sep] = self.x64
        types[os.sep + 'arm' + os.sep] = self.ARM
        types[os.sep + 'ia64' + os.sep] = self.IA64

        types['-X86-'] = self.x86
        types['-X64-'] = self.x64
        types['-IA64-'] = self.IA64

        types['-x86-'] = self.x86
        types['-x64-'] = self.x64
        types['-ia64-'] = self.IA64

        self.mTypes = types

    def getType(self, aPath):

        osType = UnknownSubstance.getItemByPath(self.mTypes, aPath)

        if osType is not None:
            return osType

        return UnknownSubstance.unknown('UNKNOWN TYPE', aPath)

    def getPathKey(self, aValue):

        return UnknownSubstance.getKeyPathByValue(
            self.mCalligraphicTypes, aValue)
