import sys
import core
import core.dates
import core.dirs
import core.updates


def getYearUpdates(aPaths, aDates):

    updates = []

    for path, date in zip(aPaths, aDates):

        files = core.dirs.getSubDirectoryFiles(path)

        shiftLen = len(path)
        fileNum = 0
        while fileNum < len(files):
            files[fileNum] = files[fileNum][shiftLen:]
            fileNum += 1

        monthUpdates = core.updates.getUpdatesFromPackage(files, date)
        updates.append(monthUpdates)

    return updates


if __name__ == '__main__':

    argc = len(sys.argv)

    if argc == 1 or argc > 3:
        print('Bad using.\n'
              'Correct will be ' + sys.argv[0] +
              ' <path to directory with updates> <date for non year edition>')

    elif argc == 2:
        rootDirectories = core.dirs.getSubDirectoryOnly(sys.argv[1])
        dates = core.dates.getDatesOfUpdates(rootDirectories)

        if len(rootDirectories) != 0 and len(dates) != 0:
            rootDirectories = core.dirs.getSubDirectoryOnly(sys.argv[1], True)
            updates = getYearUpdates(rootDirectories, dates)
        else:
            print('In selected folder ' + sys.argv[1] + ' no date folder')

        for monthUpdates in updates:
            for update in monthUpdates:
                print(update.toWinDirStyle())

    elif argc == 3:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        updates = core.updates.getUpdatesFromPackage(files, sys.argv[2])
        for update in updates:
            print(update.toWinDirStyle())

