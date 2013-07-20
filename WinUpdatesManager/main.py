import sys
import core
import core.dates
import core.dirs
import core.updates


def getYearUpdates(aPaths, aDates):

    updates = []

    if len(aDates) == 0 or len(aPaths) == 0:
        return updates

    dateNum = 0
    for path in aPaths:
        files = core.dirs.getSubDirectoryFiles(path)

        fileNum = 0
        shiftLen = len(path)
        while fileNum < len(files):
            files[fileNum] = files[fileNum][shiftLen:]
            fileNum += 1

        monthUpdates = core.updates.getUpdatesFromPackage(files,
                                        aDates[min(dateNum, len(aDates) - 1)])
        updates.append(monthUpdates)
        dateNum += 1

    return updates


if __name__ == '__main__':

    argc = len(sys.argv)

    updates = []

    if argc == 1 or argc > 3:
        print('Bad using.\n'
              'Correct will be ' + sys.argv[0] +
              ' <path to directory with updates> <date for non year edition>')

    elif argc == 2:
        rootDirectories = core.dirs.getSubDirectoryOnly(sys.argv[1])
        dates = core.dates.getDatesOfUpdates(rootDirectories)

        if len(dates) != 0:
            rootDirectories = core.dirs.getSubDirectoryOnly(sys.argv[1], True)
            updates = getYearUpdates(rootDirectories, dates)
        else:
            print('In selected folder ' + sys.argv[1] + ' no date folder')

    elif argc == 3:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        updates = core.dirs.updates.getUpdatesFromPackage(files,
            sys.argv[2])

    for update in updates:
        print(update)

    #files = core.dirs.getSubDirectoryFiles('E:\\0112\\')
    #updates = core.updates.getUpdatesInfoFromPackage(files, 1)
    #updatesUN = core.updates.getUpdatesSerriesSeparate(updates, 'KNOW', True)
    #updatesKNOW = core.updates.getUpdatesSerriesSeparate(updates, 'KNOW')

    #for update in updatesKNOW:
        #update = 'E:\\0112\\' + update[3:]
        #print(update)

    #for update in updatesUN:
        #print(update)
