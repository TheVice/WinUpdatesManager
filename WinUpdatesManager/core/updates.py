import os


class Updates:

    def __init__(self):

        self.mData = []
        self.mIndex = 0

    def addUpdate(self, aPath=None, aKB=None, aOsVersion=None,
        aOsType=None, aLanguage=None, aDate=None):

        update = {}

        update['Path'] = aPath
        update['KB'] = aKB
        update['Version'] = aOsVersion
        update['Type'] = aOsType
        update['Language'] = aLanguage
        update['Date'] = aDate

        self.addUpdateDict(update)

    def addUpdateDict(self, aUpdate):

        if 0 == self.mData.count(aUpdate):
            self.mData.append(aUpdate)
            self.mIndex += 1

    def __iter__(self):

        return self

    def __next__(self):

        if self.mIndex == 0:
            self.mIndex = len(self.mData)
            raise StopIteration

        self.mIndex -= 1
        return self.mData[self.mIndex]

    def next(self):

        return self.__next__()

    def __len__(self):

        return len(self.mData)

    def __getitem__(self, aKey):

        if aKey < 0 or self.mIndex <= aKey:
            raise IndexError

        return self.mData[aKey]


def toPathStyle(aUpdate):

    path = aUpdate['Path']
    date = aUpdate['Date']
    kb = aUpdate['KB']
    version = aUpdate['Version']
    osType = aUpdate['Type']
    language = aUpdate['Language']

    output = path[0:path.find(os.sep)]

    output += os.sep + dateToPathStyle(date)
    output += os.sep + str(kb)
    output += os.sep + version
    output += os.sep + osType
    output += os.sep + language

    output += path[path.rfind(os.sep):]

    return output


def dateToPathStyle(aDate):

    month = str(aDate.month)
    if len(month) == 1:
        month = '0' + month
    date = month + str(aDate.year)[2:4]
    return date


def getKB(aPath):

    length = len(aPath)
    startKB = aPath.find('KB')

    if startKB != -1 and startKB + 2 < length:
        startKB += 2
        endKB = startKB

        while endKB < length and aPath[endKB].isdigit():
            endKB += 1

        if endKB - startKB > 0:
            return int(aPath[startKB:endKB])

    return -1


def getVersion(aPath):

    versions = ['\\Windows2000\\', '\\WindowsXP\\', '\\WindowsServer2003\\',
                '\\WindowsVista\\', '\\WindowsServer2008\\', '\\Windows7\\',
                '\\WindowsServer2008R2\\', '\\Windows8\\',
                '\\WindowsServer2012\\', '\\Windows8dot1\\',
                '\\WindowsServer2012R2\\', '\\WindowsRT\\']

    for version in versions:
        if version in aPath or version.upper() in aPath:
            return version[1:len(version) - 1]

    return 'UNKNOWN VERSION'


def getOsType(aPath):

    osTypes = ['\\x86\\', '\\x64\\', '\\IA64\\', '\\ARM\\']

    for osType in osTypes:
        if (osType in aPath) or (osType.lower()
            in aPath) or (osType.upper() in aPath):
            return osType[1:len(osType) - 1]

    return 'UNKNOWN TYPE'


def getLanguage(aPath):

    languages = ['\\NEU\\', '\\ARA\\', '\\CHS\\', '\\CHT\\', '\\CSY\\',
                 '\\DAN\\', '\\DEU\\', '\\ELL\\', '\\ENU\\', '\\ESN\\',
                 '\\FIN\\', '\\FRA\\', '\\HEB\\', '\\HUN\\', '\\ITA\\',
                 '\\JPN\\', '\\KOR\\', '\\NLD\\', '\\NOR\\', '\\PLK\\',
                 '\\PTB\\', '\\PTG\\', '\\RUS\\', '\\SVE\\', '\\TRK\\']

    for language in languages:
        if language in aPath:
            return language[1:len(language) - 1]

    return 'UNKNOWN LANGUAGE'


def getUpdatesFromPackage(aFiles, aDate):

    updates = Updates()

    for updateFile in aFiles:
        kb = getKB(updateFile)
        osVersion = getVersion(updateFile)
        osType = getOsType(updateFile)
        language = getLanguage(updateFile)

        updates.addUpdate(updateFile, kb, osVersion, osType, language, aDate)

    return updates


def getKBsFromReport(aReport):

    KBs = []
    i = 0

    while i < len(aReport):

        KB = getKB(aReport[i:])
        if KB != -1 and 0 == KBs.count(KB):
            KBs.append(KB)

        strKB = 'KB'
        if KB != -1:
            strKB += str(KB)

        pos = aReport[i:].find(strKB)
        if pos < 1:
            i = len(aReport)
        else:
            i += pos + len(strKB)

    return KBs

