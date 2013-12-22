import os
import re
import core.dates


class Updates:

    def __init__(self):

        self.mData = []
        self.mIndex = 0

    def addUpdates(self, aUpdates):

        for up in aUpdates:
            self.addUpdate(up['Path'], up['KB'], up['Version'],
                           up['Type'], up['Language'], up['Date'])

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
        self.EightDotOne = 'Windows 8.1'
        self.Win2k12R2 = 'Windows Server 2012 R2'

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
        versions[os.sep + 'Windows8.1' + os.sep] = self.EightDotOne
        versions[os.sep + 'WindowsServer2012R2' + os.sep] = self.Win2k12R2

        versions[os.sep + 'WindowsRT' + os.sep] = self.WinRT

        self.mCalligraphicVersions = dict(versions)

        versions[os.sep + 'windows2000' + os.sep] = self.Win2k
        versions[os.sep + 'windowsxp' + os.sep] = self.WinXP
        versions[os.sep + 'windowsserver2003' + os.sep] = self.Win2k3
        versions[os.sep + 'windowsvista' + os.sep] = self.Vista
        versions[os.sep + 'windowsserver2008' + os.sep] = self.Win2k8
        versions[os.sep + 'windows7' + os.sep] = self.Seven
        versions[os.sep + 'windowsserver2008r2' + os.sep] = self.Win2k8R2
        versions[os.sep + 'windows8' + os.sep] = self.Eight
        versions[os.sep + 'windowsserver2012' + os.sep] = self.Win2k12
        versions[os.sep + 'windows8.1' + os.sep] = self.EightDotOne
        versions[os.sep + 'windowswerver2012r2' + os.sep] = self.Win2k12R2

        versions[os.sep + 'windowsrt' + os.sep] = self.WinRT

        versions[os.sep + 'WINDOWS2000' + os.sep] = self.Win2k
        versions[os.sep + 'WINDOWSXP' + os.sep] = self.WinXP
        versions[os.sep + 'WINDOWSSERVER2003' + os.sep] = self.Win2k3
        versions[os.sep + 'WINDOWSVISTA' + os.sep] = self.Vista
        versions[os.sep + 'WINDOWSSERVER2008' + os.sep] = self.Win2k8
        versions[os.sep + 'WINDOWS7' + os.sep] = self.Seven
        versions[os.sep + 'WINDOWSSERVER2008R2' + os.sep] = self.Win2k8R2
        versions[os.sep + 'WINDOWS8' + os.sep] = self.Eight
        versions[os.sep + 'WINDOWSSERVER2012' + os.sep] = self.Win2k12
        versions[os.sep + 'WINDOWS8.1' + os.sep] = self.EightDotOne
        versions[os.sep + 'WINDOWSSERVER2012R2' + os.sep] = self.Win2k12R2

        versions[os.sep + 'WINDOWSRT' + os.sep] = self.WinRT

        self.mVersions = versions

    def getVersion(self, aPath):

        version = getItemByPath(self.mVersions, aPath)

        if version is not None:
            return version

        return unknownSubstance('UNKNOWN VERSION', aPath)

    def getPathKey(self, aValue):

        return getKeyPathByValue(self.mCalligraphicVersions, aValue)


class Types:

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

        osType = getItemByPath(self.mTypes, aPath)

        if osType is not None:
            return osType

        return unknownSubstance('UNKNOWN TYPE', aPath)

    def getPathKey(self, aValue):

        return getKeyPathByValue(self.mCalligraphicTypes, aValue)


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
        languages[os.sep + 'Norwegian'] = self.Norwegian
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

        self.mCalligraphicLanguages = dict(languages)

        languages[os.sep + 'neutral' + os.sep] = self.Neutral
        languages[os.sep + 'arabic' + os.sep] = self.Arabic
        languages[os.sep + 'chinese (simplified)' + os.sep] = (
            self.Chinese_Simplified)
        languages[os.sep + 'chinese (traditional)' + os.sep] = (
            self.Chinese_Traditional)
        languages[os.sep + 'czech' + os.sep] = self.Czech
        languages[os.sep + 'danish' + os.sep] = self.Danish
        languages[os.sep + 'dutch' + os.sep] = self.Dutch
        languages[os.sep + 'english' + os.sep] = self.English
        languages[os.sep + 'finnish' + os.sep] = self.Finnish
        languages[os.sep + 'french' + os.sep] = self.French
        languages[os.sep + 'german' + os.sep] = self.German
        languages[os.sep + 'greek' + os.sep] = self.Greek
        languages[os.sep + 'hebrew' + os.sep] = self.Hebrew
        languages[os.sep + 'hungarian' + os.sep] = self.Hungarian
        languages[os.sep + 'italian' + os.sep] = self.Italian
        languages[os.sep + 'japanese (japan)' + os.sep] = self.Japanese
        languages[os.sep + 'japanese' + os.sep] = self.Japanese
        languages[os.sep + 'korean' + os.sep] = self.Korean
        languages[os.sep + 'norwegian'] = self.Norwegian
        languages[os.sep + 'polish' + os.sep] = self.Polish
        languages[os.sep + 'portuguese (brazil)' + os.sep] = (
            self.Portuguese_Brazil)
        languages[os.sep + 'portuguese (portugal)' + os.sep] = (
            self.Portuguese_Portugal)
        languages[os.sep + 'russian' + os.sep] = self.Russian
        languages[os.sep + 'spanish (traditional sort)' + os.sep] = (
            self.Spanish)
        languages[os.sep + 'swedish' + os.sep] = self.Swedish
        languages[os.sep + 'turkish' + os.sep] = self.Turkish

        languages[os.sep + 'NEUTRAL' + os.sep] = self.Neutral
        languages[os.sep + 'ARABIC' + os.sep] = self.Arabic
        languages[os.sep + 'CHINESE (SIMPLIFIED)' + os.sep] = (
            self.Chinese_Simplified)
        languages[os.sep + 'CHINESE (TRADITIONAL)' + os.sep] = (
            self.Chinese_Traditional)
        languages[os.sep + 'CZECH' + os.sep] = self.Czech
        languages[os.sep + 'DANISH' + os.sep] = self.Danish
        languages[os.sep + 'DUTCH' + os.sep] = self.Dutch
        languages[os.sep + 'ENGLISH' + os.sep] = self.English
        languages[os.sep + 'FINNISH' + os.sep] = self.Finnish
        languages[os.sep + 'FRENCH' + os.sep] = self.French
        languages[os.sep + 'GERMAN' + os.sep] = self.German
        languages[os.sep + 'GREEK' + os.sep] = self.Greek
        languages[os.sep + 'HEBREW' + os.sep] = self.Hebrew
        languages[os.sep + 'HUNGARIAN' + os.sep] = self.Hungarian
        languages[os.sep + 'ITALIAN' + os.sep] = self.Italian
        languages[os.sep + 'JAPANESE (JAPAN)' + os.sep] = self.Japanese
        languages[os.sep + 'KOREAN' + os.sep] = self.Korean
        languages[os.sep + 'NORWEGIAN'] = self.Norwegian
        languages[os.sep + 'POLISH' + os.sep] = self.Polish
        languages[os.sep + 'PORTUGUESE (BRAZIL)' + os.sep] = (
            self.Portuguese_Brazil)
        languages[os.sep + 'PORTUGUESE (PORTUGAL)' + os.sep] = (
            self.Portuguese_Portugal)
        languages[os.sep + 'RUSSIAN' + os.sep] = self.Russian
        languages[os.sep + 'SPANISH (TRADITIONAL SORT)' + os.sep] = (
            self.Spanish)
        languages[os.sep + 'SWEDISH' + os.sep] = self.Swedish
        languages[os.sep + 'TURKISH' + os.sep] = self.Turkish

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

        languages[os.sep + 'neu' + os.sep] = self.Neutral
        languages[os.sep + 'ara' + os.sep] = self.Arabic
        languages[os.sep + 'chs' + os.sep] = self.Chinese_Simplified
        languages[os.sep + 'cht' + os.sep] = self.Chinese_Traditional
        languages[os.sep + 'csy' + os.sep] = self.Czech
        languages[os.sep + 'dan' + os.sep] = self.Danish
        languages[os.sep + 'nld' + os.sep] = self.Dutch
        languages[os.sep + 'enu' + os.sep] = self.English
        languages[os.sep + 'fin' + os.sep] = self.Finnish
        languages[os.sep + 'fra' + os.sep] = self.French
        languages[os.sep + 'deu' + os.sep] = self.German
        languages[os.sep + 'ell' + os.sep] = self.Greek
        languages[os.sep + 'heb' + os.sep] = self.Hebrew
        languages[os.sep + 'hun' + os.sep] = self.Hungarian
        languages[os.sep + 'ita' + os.sep] = self.Italian
        languages[os.sep + 'jpn' + os.sep] = self.Japanese
        languages[os.sep + 'kor' + os.sep] = self.Korean
        languages[os.sep + 'nor' + os.sep] = self.Norwegian
        languages[os.sep + 'plk' + os.sep] = self.Polish
        languages[os.sep + 'ptb' + os.sep] = self.Portuguese_Brazil
        languages[os.sep + 'ptg' + os.sep] = self.Portuguese_Portugal
        languages[os.sep + 'rus' + os.sep] = self.Russian
        languages[os.sep + 'esn' + os.sep] = self.Spanish
        languages[os.sep + 'sve' + os.sep] = self.Swedish
        languages[os.sep + 'trk' + os.sep] = self.Turkish

        self.mLanguages = languages

    def getLanguage(self, aPath):

        language = getItemByPath(self.mLanguages, aPath)

        if language is not None:
            return language

        return unknownSubstance('UNKNOWN LANGUAGE', aPath)

    def getPathKey(self, aValue):

        return getKeyPathByValue(self.mCalligraphicLanguages, aValue)


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

    return os.sep + str(aValue) + os.sep


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

    date = ''

    try:
        month = str(aDate.month)
        if len(month) == 1:
            month = '0' + month
        date = month + str(aDate.year)[2:4]
    except:
        date = aDate

    return date


def getKB(aPath):

    length = len(aPath)
    startKB = aPath.find('KB')

    if startKB == -1:
        startKB = aPath.find('kb')

    if startKB != -1 and startKB + 2 < length:
        startKB += 2
        endKB = startKB

        while endKB < length and aPath[endKB].isdigit():
            endKB += 1

        if endKB - startKB > 0:
            return int(aPath[startKB:endKB])

    return unknownSubstance('UNKNOWN KB', aPath)


def getUpdatesFromPackage(aFiles, aDate):

    updates = Updates()
    versions = Versions()
    types = Types()
    languages = Languages()

    for updateFile in aFiles:

        updateFile = updateFile[updateFile.find(os.sep):]

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
        if not isinstance(KB, dict) and 0 == KBs.count(KB):
            KBs.append(KB)

        strKB = 'KB'
        if not isinstance(KB, dict):
            strKB += str(KB)

        pos = aReport[i:].find(strKB)
        if pos < 1:
            i = len(aReport)
        else:
            i += pos + len(strKB)

    return KBs


def getKBsFromReportFile(aFileName):

    report = None
    try:
        inputFile = open(aFileName, 'r')
        report = inputFile.read()
        inputFile.close()
    except:
        raise('Unable to read from file', aFileName)

    return getKBsFromReport(report)


def prepareLineToParse(aLine):

    aLine = aLine.replace(', \'', ',\t\'')
    aLine = aLine.replace('\'}', '\'\t}')
    aLine = aLine.replace(')}', '),\t}')
    aLine = aLine.replace('\'KB\': ', '\'KB\': \'')
    aLine = aLine.replace('\'Date\': ', '\'Date\': \'')
    return aLine


def getJSONvalue(aText, aJSON_Parameter):

    parameter = '(?<=' + aJSON_Parameter + '\': \')(.+\t)'
    value = re.search(parameter, aText).group(0)

    value = value[:value.find('\'')]

    pos = value.rfind(',')
    if(pos != -1):
        value = value[:pos]

    return value


def getUpdatesFromJSONfile(aFile):

    updates = Updates()
    try:
        inputFile = open(aFile, 'r')

        versions = Versions()
        types = Types()
        languages = Languages()

        for line in inputFile:
            line = prepareLineToParse(line)

            path = getJSONvalue(line, 'Path')
            path = path.replace(os.sep + os.sep, os.sep)

            kb = None
            try:
                kb = int(getJSONvalue(line, 'KB'))
            except:
                kb = getKB(path)

            osVersion = None
            try:
                osVersion = getJSONvalue(line, 'Version')
            except:
                osVersion = versions.getVersion(line)

            osType = None
            try:
                osType = getJSONvalue(line, 'Type')
            except:
                osType = types.getType(line)

            language = None
            try:
                language = getJSONvalue(line, 'Language')
            except:
                language = languages.getLanguage(line)

            date = getJSONvalue(line, 'Date')

            updates.addUpdate(path, kb, osVersion, osType, language,
                              core.dates.getDatesFromJSON_Recode(date))

        inputFile.close()
    except:
        raise Exception('Unexpected error while work with file:' + aFile)

    return updates


def separateToKnownAndUnknown(aUpdates):

    updates = {'known': [], 'unKnown': []}

    for up in aUpdates:
        if (isinstance(up['KB'], dict) or isinstance(up['Version'], dict) or
            isinstance(up['Type'], dict) or isinstance(up['Language'], dict)):

            updates['unKnown'].append(up)
        else:
            updates['known'].append(up)

    return updates
