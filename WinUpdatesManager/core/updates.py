

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

    def __len__(self):

        return len(self.mData)

    def __getitem__(self, aKey):

        if aKey < 0 or self.mIndex <= aKey:
            raise IndexError

        return self.mData[aKey]


def toWinDirStyle(aUpdate):

    path = aUpdate['Path']
    date = aUpdate['Date']
    kb = aUpdate['KB']
    version = aUpdate['Version']
    osType = aUpdate['Type']
    language = aUpdate['Language']

    output = path[0:path.find('\\')]

    output += '\\' + dateToWinDirStyle(date)
    output += '\\' + str(kb)
    output += '\\' + version
    output += '\\' + osType
    output += '\\' + language

    output += path[path.rfind('\\'):]

    return output


def dateToWinDirStyle(aDate):

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

    versions = ['Windows2000', 'WindowsXP', 'WindowsServer2003',
                'WindowsVista', 'WindowsServer2008', 'Windows7',
                'WindowsServer2008R2', 'Windows8', 'WindowsServer2012',
                'Windows8dot1', 'WindowsServer2012R2', 'WindowsRT']
    version = []

    for ver in versions:
        if ver in aPath or ver.upper() in aPath:
            version.append(ver)

    if len(version) == 0:
        version.append('UNKNOWN VERSION')

    return version


def getOsType(aPath):

    osTypes = ['x86', 'x64', 'IA64', 'ARM']

    for osType in osTypes:
        if osType in aPath:
            return osType
        elif osType.lower() in aPath:
            return osType
        elif osType.upper() in aPath:
            return osType

    return 'UNKNOWN TYPE'


def getLanguage(aPath):

    languages = ['NEU', 'ARA', 'CHS', 'CHT', 'CSY', 'DAN',
                 'DEU', 'ELL', 'ENU', 'ESN', 'FIN', 'FRA',
                 'HEB', 'HUN', 'ITA', 'JPN', 'KOR', 'NLD',
                 'NOR', 'PLK', 'PTB', 'PTG', 'RUS', 'SVE',
                 'TRK']

    for language in languages:
        if language in aPath:
            return language

    return 'UNKNOWN LANGUAGE'


def getUpdatesFromPackage(aFiles, aDate):

    updates = Updates()

    for updateFile in aFiles:
        kb = getKB(updateFile)

        osVersion = getVersion(updateFile)
        osType = getOsType(updateFile)
        language = getLanguage(updateFile)

        for osVer in osVersion:
            osVer = checkIsThisR2(osVer, updateFile)
            osVer = checkIsThisARM(osVer, osType)

            updates.addUpdate(updateFile, kb, osVer, osType, language, aDate)

    return updates


def getKBsFromReport(aReport):

    KBs = []

    while 1:
        KB = getKB(aReport)

        if KB != -1 and 0 == KBs.count(KB):
            KBs.append(KB)

        pos = aReport.find(KB)
        if pos < 1 or pos + len(KB) > len(aReport):
            return KBs

        aReport = aReport[pos + len(KB):]

    return KBs


def checkIsThisR2(aVersion, aFileName):

    if not 'WindowsServer' in aVersion:
        return aVersion

    if ('Windows6.1' in aFileName
        or 'WINDOWS6.1' in aFileName) and not 'R2' in aVersion:
        return aVersion + 'R2'

    if ('Windows6.3' in aFileName
        or 'WINDOWS6.3' in aFileName) and not 'R2' in aVersion:
        return aVersion + 'R2'

    return aVersion


def checkIsThisARM(aVersion, aType):

    if not 'ARM' in aType:
        return aVersion

    return 'WindowsRT'

