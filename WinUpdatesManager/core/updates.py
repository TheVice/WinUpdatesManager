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


class Versions:

    def __init__(self):

        self.Win2k = 'Windows 2000'
        self.WinXP = 'Windows XP'
        self.Win2k3 = 'Windows Server 2003'
        self.Vista = 'Windows Vista'
        self.Win2k8 = 'Windows Server 2008'
        self.Seven = 'Windows 7'
        self.Win2k8R2 = 'Windows Server 2008 R2'
        self.Eight = 'Windows 8'
        self.Win2k12 = 'Windows Server 2012'

        self.WinRT = 'Windows RT'

        versions = {}

        versions[os.sep + 'Windows2000' + os.sep] = self.Win2k
        versions[os.sep + 'WindowsXP' + os.sep] = self.WinXP
        versions[os.sep + 'WindowsServer2003' + os.sep] = self.Win2k3
        versions[os.sep + 'WindowsVista' + os.sep] = self.Vista
        versions[os.sep + 'WindowsServer2008' + os.sep] = self.Win2k8
        versions[os.sep + 'Windows7' + os.sep] = self.Seven
        versions[os.sep + 'WindowsServer2008R2' + os.sep] = self.Win2k8R2
        versions[os.sep + 'Windows8' + os.sep] = self.Eight
        versions[os.sep + 'WindowsServer2012' + os.sep] = self.Win2k12

        versions[os.sep + 'WindowsRT' + os.sep] = self.WinRT

        self.mVersions = versions

    def getVersion(self, aPath):

        key = None

        for keyVersion in self.mVersions.keys():
            if keyVersion in aPath:
                key = keyVersion
                break

        if key is not None:
            return self.mVersions.get(key)

        unknown = {}
        unknown['UNKNOWN VERSION'] = aPath
        return unknown

    def getPathKey(self, aValue):

        for key, value in self.mVersions.items():
            if value == aValue:
                return key

        return os.sep + aValue + os.sep


def toPathStyle(aUpdate):

    path = aUpdate['Path']
    date = aUpdate['Date']
    kb = aUpdate['KB']
    version = Versions().getPathKey(aUpdate['Version'])
    osType = aUpdate['Type']
    language = aUpdate['Language']

    output = path[0:path.find(os.sep)]

    output += os.sep + dateToPathStyle(date)
    output += os.sep + str(kb)
    output += version
    output += osType
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
    versions = Versions()

    for updateFile in aFiles:
        kb = getKB(updateFile)
        osVersion = versions.getVersion(updateFile)
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

