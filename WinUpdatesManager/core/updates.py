

class Update:

    def __init__(self, aPath='', aKB='', aVersion='',
        aOsType='', aLanguage='', aDate=''):

        self.mFullName = aPath
        self.mKB = aKB
        self.mVersion = aVersion
        self.mOsType = aOsType
        self.mLanguage = aLanguage
        self.mDate = aDate

    def toJSON(self):

        output = {}

        if self.mFullName != '':
            output['Name'] = self.mFullName
        if self.mKB != '':
            output['KB'] = self.mKB
        if self.mVersion != '':
            output['Version'] = self.mVersion
        if self.mOsType != '':
            output['Type'] = self.mOsType
        if self.mLanguage != '':
            output['Language'] = self.mLanguage
        if self.mDate != '':
            output['Date'] = self.mDate

        return output

    def toWinDirStyle(self):

        output = ''

        if self.mFullName == '':
            return output

        output = self.getRootOfFullName()

        if self.mDate != '':
            output += self.getDate() + '\\'
        if self.mKB != '':
            output += self.mKB + '\\'
        if self.mVersion != '':
            output += self.mVersion + '\\'
        if self.mOsType != '':
            output += self.mOsType + '\\'
        if self.mLanguage != '':
            output += self.mLanguage + '\\'

        output += self.getShortName()

        return output

    def getPathWithOutRoot(self):

        return self.mFullName[self.mFullName.find('\\') + 1:
               self.mFullName.rfind('\\') + 1]

    def getShortName(self):

        return self.mFullName[self.mFullName.rfind('\\') + 1:]

    def getRootOfFullName(self):

        return self.mFullName[0:self.mFullName.find('\\') + 1]

    def getDate(self):

        try:
            month = str(self.mDate.month)
            if len(month) == 1:
                month = '0' + month
            date = month + str(self.mDate.year)[2:4]
            return date
        except:
            return self.mDate

    def __str__(self):

        return self.toWinDirStyle()


def getKB(aPath):

    length = len(aPath)
    startKB = aPath.find('KB')

    if startKB != -1 and startKB + 2 < length:
        startKB += 2
        endKB = startKB

        while endKB < length and aPath[endKB].isdigit():
            endKB += 1

        if endKB - startKB > 0:
            return aPath[startKB:endKB]

    return 'UNKNOWN KB'


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

    osTypes = ['X86', 'X64', 'IA64', 'ARM']

    for osType in osTypes:
        if osType in aPath or osType.lower() in aPath:
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


def getUpdatesInfoFromPackage(aFiles):

    updates = []

    for update_file in aFiles:
        kb = getKB(update_file)

        version = getVersion(update_file)
        osType = getOsType(update_file)
        language = getLanguage(update_file)

        for ver in version:
            ver = checkIsThisR2(ver, update_file)
            ver = checkIsThisARM(ver, osType)

            update = Update(update_file, kb, ver, osType, language)

            if 0 == updates.count(update):
                updates.append(update)

    return updates


def getKBsFromReport(aReport):

    KBs = []

    while 1:
        KB = getKB(aReport)

        if KB != 'UNKNOWN KB' and 0 == KBs.count(KB):
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


def getUpdatesSerriesSeparate(aUpdates, aSeparator, aWithSeparator=False):

    updates = []

    if aWithSeparator:
        for update in aUpdates:
            if aSeparator in update:
                updates.append(update)
    else:
        for update in aUpdates:
            if aSeparator not in update:
                updates.append(update)

    return updates


def getUpdatesFromPackage(aFiles, aDate):

    updates = getUpdatesInfoFromPackage(aFiles)

    for update in updates:
        update.mDate = aDate

    return updates
