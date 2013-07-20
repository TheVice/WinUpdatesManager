

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


def getType(aPath):

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

        if kb == 'UNKNOWN KB':
            digitStart = 0

            while (digitStart < len(update_file)
                   and not update_file[digitStart].isdigit()):
                digitStart += 1

            if digitStart >= len(update_file):
                continue

            newFile = 'KB' + update_file[digitStart:]
            kb = getKB(newFile)

        version = getVersion(update_file)
        osType = getType(update_file)
        language = getLanguage(update_file)

        for ver in version:
            ver = checkIsThisR2(ver, update_file)
            ver = checkIsThisARM(ver, osType)
            if aStyle == 0:
                update = updateInfoInJSON(update_file, kb, ver, osType,
                    language)
            elif aStyle == 1:
                update = updateInfoInDirStyle(update_file, kb, ver, osType,
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

    return ('{' + 'Name = ' + aFileName[aFileName.rfind('\\') + 1:] + ', '
                + 'KB = ' + aKB + ', '
                + 'Version = ' + aVersion + ', '
                + 'Type = ' + aType + ', '
                + 'Language = ' + aLanguage
                + '}')


def updateInfoInDirStyle(aFileName, aKB, aVersion, aType, aLanguage):

    return (aFileName[0:aFileName.find('\\') + 1]
            + aKB[2:]
            + '\\' + aVersion
            + '\\' + aType
            + '\\' + aLanguage
            + '\\' + aFileName[aFileName.rfind('\\') + 1:])


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
