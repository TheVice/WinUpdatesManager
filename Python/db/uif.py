import os
import re
import core.kb
import core.dates
import core.dirs
from core.versions import Versions
from core.types import Types
from core.languages import Languages


def prepareLineToParse(aLine):

    aLine = aLine.replace(', \'', ',\t\'')
    aLine = aLine.replace('\'}', '\'\t}')
    aLine = aLine.replace(')}', '),\t}')
    aLine = aLine.replace('\'KB\': ', '\'KB\': \'')
    aLine = aLine.replace('\'Date\': ', '\'Date\': \'')
    return aLine


def getValue(aText, aParameter):

    parameter = '(?<=' + aParameter + '\': \')(.+\t)'
    value = re.search(parameter, aText).group(0)

    value = value[:value.find('\'')]

    pos = value.rfind(',')
    if(pos != -1):
        value = value[:pos]

    return value


def getUpdateFromLine(aLine, aVersions, aTypes, aLanguages, aUpdates):

    aLine = prepareLineToParse(aLine)

    path = getValue(aLine, 'Path')
    path = path.replace(os.sep + os.sep, os.sep)

    kb = None
    try:
        kb = int(getValue(aLine, 'KB'))
    except:
        kb = core.kb.getKB(path)

    osVersion = None
    try:
        osVersion = getValue(aLine, 'Version')
    except:
        osVersion = aVersions.getVersion(aLine)

    osType = None
    try:
        osType = getValue(aLine, 'Type')
    except:
        osType = aTypes.getType(aLine)

    language = None
    try:
        language = getValue(aLine, 'Language')
    except:
        language = aLanguages.getLanguage(aLine)

    date = getValue(aLine, 'Date')

    aUpdates.append({'Path': path, 'KB': kb, 'Version': osVersion,
                     'Type': osType, 'Language': language,
                      'Date': core.dates.getDatesFromUIF_Recode(date)})


def getUpdatesFromFile(aFile, aUpdates):

    try:
        inputFile = open(aFile, 'r')

        versions = Versions()
        types = Types()
        languages = Languages()

        for line in inputFile:
            getUpdateFromLine(line, versions, types, languages, aUpdates)

        inputFile.close()
    except:
        raise Exception('Unexpected error while work with file:' + aFile)


def getUpdatesFromStorage(aPath):

    updates = []

    if os.path.isfile(aPath):
        getUpdatesFromFile(aPath, updates)
    elif os.path.isdir(aPath):
        files = core.dirs.getFilesInDirectory(aPath, '.uif')
        count = len(files)
        i = 1
        for f in files:
            getUpdatesFromFile(f, updates)
            print(str(i) + ' / ' + str(count) + ' ' + str(f))
            i += 1

    return updates
