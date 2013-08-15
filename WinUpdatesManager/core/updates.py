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

        version = getItemByPath(self.mVersions, aPath)

        if version is not None:
            return version

        return unknownSubstance('UNKNOWN VERSION', aPath)

    def getPathKey(self, aValue):

        return getKeyPathByValue(self.mVersions, aValue)


class Types:

    def __init__(self):

        self.x86 = 'x86'
        self.x64 = 'x64'
        self.IA64 = 'IA64'
        self.ARM = 'ARM'

        types = {}

        types[os.sep + 'x86' + os.sep] = self.x86
        types[os.sep + 'x64' + os.sep] = self.x64
        types[os.sep + 'IA64' + os.sep] = self.IA64
        types[os.sep + 'ARM' + os.sep] = self.ARM

        types[os.sep + 'X86' + os.sep] = self.x86
        types[os.sep + 'X64' + os.sep] = self.x64

        self.mTypes = types

    def getType(self, aPath):

        osType = getItemByPath(self.mTypes, aPath)

        if osType is not None:
            return osType

        return unknownSubstance('UNKNOWN TYPE', aPath)

    def getPathKey(self, aValue):

        return getKeyPathByValue(self.mTypes, aValue)


class Languages:

    def __init__(self):

        self.Neutral = 'Neutral'
        self.Arabic = 'Arabic'
        self.Chinese_Simplified = 'Chinese (Simplified)'
        self.Chinese_Traditional = 'Chinese (Traditional)'
        self.Czech = 'Czech'
        self.Danish = 'Danish'
        self.Dutch = 'Dutch'
        self.English = 'English'
        self.Finnish = 'Finnish'
        self.French = 'French'
        self.German = 'German'
        self.Greek = 'Greek'
        self.Hebrew = 'Hebrew'
        self.Hungarian = 'Hungarian'
        self.Italian = 'Italian'
        self.Japanese = 'Japanese'
        self.Korean = 'Korean'
        self.Norwegian = 'Norwegian'
        self.Polish = 'Polish'
        self.Portuguese_Brazil = 'Portuguese (Brazil)'
        self.Portuguese_Portugal = 'Portuguese (Portugal)'
        self.Russian = 'Russian'
        self.Spanish = 'Spanish'
        self.Swedish = 'Swedish'
        self.Turkish = 'Turkish'

        languages = {}

        languages[os.sep + 'Neutral' + os.sep] = self.Neutral
        languages[os.sep + 'Arabic' + os.sep] = self.Arabic
        languages[os.sep + 'Chinese (Simplified)' + os.sep] = (
            self.Chinese_Simplified)
        languages[os.sep + 'Chinese (Traditional)' + os.sep] = (
            self.Chinese_Traditional)
        languages[os.sep + 'Czech' + os.sep] = self.Czech
        languages[os.sep + 'Danish' + os.sep] = self.Danish
        languages[os.sep + 'Dutch' + os.sep] = self.Dutch
        languages[os.sep + 'English' + os.sep] = self.English
        languages[os.sep + 'Finnish' + os.sep] = self.Finnish
        languages[os.sep + 'French' + os.sep] = self.French
        languages[os.sep + 'German' + os.sep] = self.German
        languages[os.sep + 'Greek' + os.sep] = self.Greek
        languages[os.sep + 'Hebrew' + os.sep] = self.Hebrew
        languages[os.sep + 'Hungarian' + os.sep] = self.Hungarian
        languages[os.sep + 'Italian' + os.sep] = self.Italian
        languages[os.sep + 'Japanese (Japan)' + os.sep] = self.Japanese
        languages[os.sep + 'Korean' + os.sep] = self.Korean
        languages[os.sep + 'Norwegian'] = self.Norwegian    # ()
        languages[os.sep + 'Polish' + os.sep] = self.Polish
        languages[os.sep + 'Portuguese (Brazil)' + os.sep] = (
            self.Portuguese_Brazil)
        languages[os.sep + 'Portuguese (Portugal)' + os.sep] = (
            self.Portuguese_Portugal)
        languages[os.sep + 'Russian' + os.sep] = self.Russian
        languages[os.sep + 'Spanish (Traditional Sort)' + os.sep] = (
            self.Spanish)
        languages[os.sep + 'Swedish' + os.sep] = self.Swedish
        languages[os.sep + 'Turkish' + os.sep] = self.Turkish

        languages[os.sep + 'NEU' + os.sep] = self.Neutral
        languages[os.sep + 'ARA' + os.sep] = self.Arabic
        languages[os.sep + 'CHS' + os.sep] = self.Chinese_Simplified
        languages[os.sep + 'CHT' + os.sep] = self.Chinese_Traditional
        languages[os.sep + 'CSY' + os.sep] = self.Czech
        languages[os.sep + 'DAN' + os.sep] = self.Danish
        languages[os.sep + 'NLD' + os.sep] = self.Dutch
        languages[os.sep + 'ENU' + os.sep] = self.English
        languages[os.sep + 'FIN' + os.sep] = self.Finnish
        languages[os.sep + 'FRA' + os.sep] = self.French
        languages[os.sep + 'DEU' + os.sep] = self.German
        languages[os.sep + 'ELL' + os.sep] = self.Greek
        languages[os.sep + 'HEB' + os.sep] = self.Hebrew
        languages[os.sep + 'HUN' + os.sep] = self.Hungarian
        languages[os.sep + 'ITA' + os.sep] = self.Italian
        languages[os.sep + 'JPN' + os.sep] = self.Japanese
        languages[os.sep + 'KOR' + os.sep] = self.Korean
        languages[os.sep + 'NOR' + os.sep] = self.Norwegian
        languages[os.sep + 'PLK' + os.sep] = self.Polish
        languages[os.sep + 'PTB' + os.sep] = self.Portuguese_Brazil
        languages[os.sep + 'PTG' + os.sep] = self.Portuguese_Portugal
        languages[os.sep + 'RUS' + os.sep] = self.Russian
        languages[os.sep + 'ESN' + os.sep] = self.Spanish
        languages[os.sep + 'SVE' + os.sep] = self.Swedish
        languages[os.sep + 'TRK' + os.sep] = self.Turkish

        self.mLanguages = languages

    def getLanguage(self, aPath):

        language = getItemByPath(self.mLanguages, aPath)

        if language is not None:
            return language

        return unknownSubstance('UNKNOWN LANGUAGE', aPath)

    def getPathKey(self, aValue):

        return getKeyPathByValue(self.mLanguages, aValue)


def getItemByPath(aDict, aKey):

    key = None

    for keyType in aDict.keys():
        if keyType in aKey:
            key = keyType
            break

    return aDict.get(key)


def getKeyPathByValue(aDict, aValue):

    for key, value in aDict.items():
        if value == aValue:
            return key

    return os.sep + aValue + os.sep


def unknownSubstance(aSubstance, aValue):

    unknown = {}
    unknown[aSubstance] = aValue
    return unknown


def toPathStyle(aUpdate, aVersions=None, aTypes=None, aLanguages=None):

    if aVersions is None:
        aVersions = Versions()
    if aTypes is None:
        aTypes = Types()
    if aLanguages is None:
        aLanguages = Languages()

    path = aUpdate['Path']
    date = aUpdate['Date']
    kb = aUpdate['KB']

    version = aVersions.getPathKey(aUpdate['Version'])
    osType = aTypes.getPathKey(aUpdate['Type'])
    language = aLanguages.getPathKey(aUpdate['Language'])

    output = path[0:path.find(os.sep)]

    output += os.sep + dateToPathStyle(date)
    output += os.sep + str(kb)
    output += version
    output += osType[1:]
    output += language[1:]

    output += path[path.rfind(os.sep) + 1:]

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


def getUpdatesFromPackage(aFiles, aDate):

    updates = Updates()
    versions = Versions()
    types = Types()
    languages = Languages()

    for updateFile in aFiles:
        kb = getKB(updateFile)
        osVersion = versions.getVersion(updateFile)
        osType = types.getType(updateFile)
        language = languages.getLanguage(updateFile)

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

