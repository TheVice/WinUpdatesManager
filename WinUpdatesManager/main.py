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


#def some_mock():
    #import data

    #print(data.one_month())
    #print(data.one_year())

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

        for monthUpdates in updates:
            for update in monthUpdates:
                print(update.toWinDirStyle())

    elif argc == 3:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        updates = core.updates.getUpdatesFromPackage(files,
            sys.argv[2])
        for update in updates:
            print(update.toWinDirStyle())

    #some_mock()

