import sys
import core
import core.dates
import core.dirs
import core.updates


def getUpdatesFromPackage(aFiles, aDate):

    updates = core.updates.getUpdatesInfoFromPackage(aFiles)

    for up in updates:
        up = up[:len(up) - 1] + ', ' + str(aDate) + '}'
        print(up)


def getFromYearEditionPackage(aPaths, aDates):

    if len(aDates) == 0 or len(aPaths) == 0:
        return

    i = 0
    for path in aPaths:
        files = core.dirs.getSubDirectoryFiles(path)
        getUpdatesFromPackage(files, aDates[min(i, len(aDates) - 1)])
        i += 1


if __name__ == '__main__':

    argc = len(sys.argv)
    if argc == 1 or argc > 3:

        print('Bad using.\n'
              'Correct will be ' + sys.argv[0] +
              ' <path to directory with updates> <date for non Year edition>')
    elif argc == 2:

        print('One ' + sys.argv[1])
        #rootFolders = core.dirs.getSubFolderOnly(sys.argv[1])
        #dates = core.dates.getDatesOfUpdates(rootFolders)
        #if len(dates) == 0:
        #    return
        #rootFolders = core.dirs.getSubFolderOnly(sys.argv[1], True)
        #getFromYearEditionPackage(rootFolders, dates)

    elif argc == 3:
        print('Two ' + sys.argv[1] + ' ' + sys.argv[2])
        #getUpdatesFromPackage(sys.argv[1], sys.argv[2])
