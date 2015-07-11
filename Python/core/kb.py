import sys
from core.unknownSubstance import UnknownSubstance


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

    return UnknownSubstance.unknown('UNKNOWN KB', aPath)


def getKBsFromReport(aReport):

    i = 0
    KBs = set()
    length = len(aReport)

    while i < length:

        KB = getKB(aReport[i:])
        if not isinstance(KB, dict):
            KBs.add(KB)

        strKB = 'KB'
        if not isinstance(KB, dict):
            strKB = '{}{}'.format(strKB, KB)

        pos = aReport[i:].find(strKB)
        if pos < 0:
            i = length
        else:
            i += pos + len(strKB)

    return list(KBs)


def getKBsFromReportFile(aFileName):

    try:
        inputFile = open(aFileName, 'r')
        report = inputFile.read()
        inputFile.close()
        return getKBsFromReport(report)
    except:
        raise Exception('Unexpected error while work with file \'{}\' {}'.format(
            aFileName, sys.exc_info()[1]))
