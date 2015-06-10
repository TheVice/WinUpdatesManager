import os
import sys
import json
import core.kb
import core.dirs
import core.dates
from core.types import Types
from core.updates import Updates
from core.versions import Versions
from core.languages import Languages


def getUpdatesFromPackage(aFiles, aDate):

    updates = []
    versions = Versions()
    types = Types()
    languages = Languages()
    date = '{}, {}, {}'.format(aDate.year, aDate.month, aDate.day)

    for updateFile in aFiles:

        path = os.path.normpath(updateFile)
        kb = core.kb.getKB(updateFile)
        osVersion = versions.getVersion(updateFile)
        osType = types.getType(updateFile)
        language = languages.getLanguage(updateFile)

        updates.append(json.dumps({'Path': path,
                                   'KB': kb,
                                   'Version': osVersion,
                                   'Type': osType,
                                   'Language': language,
                                   'Date': date}))

    return updates


def fromPath(aPath):

    folders = os.listdir(aPath)
    updates = []

    for folder in folders:
        path = os.path.join(aPath, folder)
        updates.extend(fromPathAndDate(path, folder))

    return updates


def fromPathAndDate(aPath, aDate):

    files = core.dirs.getSubDirectoryFiles(aPath)
    updates = []

    if 0 < len(files):
        date = core.dates.getDate(aDate)
        updates.extend(getUpdatesFromPackage(files, date))

    return updates


def getUpdates(aSysArgv):

    updates = []
    argc = len(aSysArgv)
    path = os.path.abspath(aSysArgv[1])
    if argc == 3:
        updates.extend(fromPathAndDate(path, aSysArgv[2]))
    else:
        updates.extend(fromPath(path))
    updates = Updates.separateToKnownAndUnknown(updates)
    return updates


def printUpdates(aUpdates):

    for update in aUpdates['known']:
        print(update)

    for update in aUpdates['unKnown']:
        print(update)


if __name__ == '__main__':

    argc = len(sys.argv)

    if argc == 2 or argc == 3:
        printUpdates(getUpdates(sys.argv))
    else:
        print('Using:{}{} <path to directory with updates>'
              '<date (MMYY), only for non year edition>'.format(os.linesep,
                                                                sys.argv[0]))
