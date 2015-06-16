import sys
from core.unknownSubstance import UnknownSubstance


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

    return UnknownSubstance.unknown('UNKNOWN KB', aPath)


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

    try:
        inputFile = open(aFileName, 'r')
        report = inputFile.read()
        inputFile.close()
        return getKBsFromReport(report)
    except:
        raise Exception('Unexpected error while work with file {} {}'.format(aFileName, sys.exc_info[1]))
