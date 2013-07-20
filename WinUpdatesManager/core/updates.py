

def getKB(aPath):

    length = len(aPath)
    startKB = aPath.find('KB')

    if startKB != -1 and startKB + 2 < length:
        endKB = startKB + 2

        while endKB < length and aPath[endKB].isdigit():
            endKB += 1

        if endKB - startKB > 2:
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


def getUpdatesInfoFromPackage(aFiles, aStyle=0):

    updates = []

    for update_file in aFiles:
        kb = getKB(update_file)

        version = getVersion(update_file)
        osType = getOsType(update_file)
        language = getLanguage(update_file)

        for ver in version:
            ver = checkIsThisR2(ver, update_file)
            ver = checkIsThisARM(ver, osType)

            if aStyle == 0:
                if kb != 'UNKNOWN KB':
                    update_file = update_file[update_file.rfind('\\') + 1:]
                update = updateInfoInJSON(update_file, kb, ver, osType,
                        language)
            elif aStyle == 1:
                if kb != 'UNKNOWN KB':
                    kb = kb[2:]
                update = updateInfoInDirStyle(
                    update_file[0:update_file.find('\\') + 1],
                    update_file[update_file.rfind('\\') + 1:],
                    kb, ver, osType,
                    language)

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


def updateInfoInJSON(aFileName, aKB, aVersion, aType, aLanguage):

    return ('{' + 'Name = ' + aFileName + ', '
                + 'KB = ' + aKB + ', '
                + 'Version = ' + aVersion + ', '
                + 'Type = ' + aType + ', '
                + 'Language = ' + aLanguage
                + '}')


def updateInfoInDirStyle(aPath, aFileName, aKB, aVersion, aType, aLanguage):

    return (aPath
            + aKB
            + '\\' + aVersion
            + '\\' + aType
            + '\\' + aLanguage
            + '\\' + aFileName)


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

    upNum = 0
    while upNum < len(updates):
        shiftLen = len(updates[upNum]) - 1
        updates[upNum] = updates[upNum][:shiftLen] + ', ' + str(aDate) + '}'
        upNum += 1

    return updates
