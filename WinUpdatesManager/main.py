import sys
import core
import core.dates
import core.dirs
import core.updates

if __name__ == '__main__':

    argc = len(sys.argv)
    updates = []

    if argc == 1 or argc > 3:
        print('Bad using.\n'
              'Correct will be ' + sys.argv[0] +
              ' <path to directory with updates> <date for non year edition>')

    elif argc == 2:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        paths = core.dirs.Paths(files)
        dates = core.dates.getDatesOfUpdates(paths.getRootObjects())

        for path, date in zip(paths.getRootPaths(), dates):
            files = paths.getSubObjects(path, True)
            monthUpdates = core.updates.getUpdatesFromPackage(files, date)
            updates.append(monthUpdates)

        for monthUpdates in updates:
            for update in monthUpdates:
                print(core.updates.toWinDirStyle(update))

    elif argc == 3:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        updates = core.updates.getUpdatesFromPackage(files, sys.argv[2])

        for update in updates:
            print(core.updates.toWinDirStyle(update))
