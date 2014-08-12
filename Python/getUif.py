import sys
import core.dates
import core.dirs
import core.updates


if __name__ == '__main__':

    argc = len(sys.argv)

    if argc == 2:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        #TODO: check return
        paths = core.dirs.Paths(files)
        dates = core.dates.getDatesOfUpdates(paths.getRootObjects())
        updates = {'known': [], 'unKnown': []}

        for path, date in zip(paths.getRootPaths(), dates):
            files = paths.getSubObjects(path, True)
            monthUpdates = core.updates.getUpdatesFromPackage(files, date)
            monthUpdates = core.updates.separateToKnownAndUnknown(monthUpdates)
            updates['known'].append(monthUpdates['known'])
            updates['unKnown'].append(monthUpdates['unKnown'])

        for monthUpdates in updates['known']:
            for update in monthUpdates:
                print(update)

        for monthUpdates in updates['unKnown']:
            for update in monthUpdates:
                print(update)

    elif argc == 3:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        #TODO: check return
        updates = core.updates.getUpdatesFromPackage(files,
                  core.dates.getDatesOfUpdates([sys.argv[2]])[0])
        updates = core.updates.separateToKnownAndUnknown(updates)

        for update in updates['known']:
            print(update)

        for update in updates['unKnown']:
            print(update)

    else:
        print('Using:')
        print(sys.argv[0] + ' <path to directory with updates>' +
                            ' <date (MMYY), only for non year edition>')
