import os
import sys
# import json
import core.dates
import core.dirs
import core.updates


def printUpdates(aUpdates):

    for update in aUpdates['known']:
        print(update)

    for update in aUpdates['unKnown']:
        print(update)

    # print('-----------updateToPackage-----------')
    # paths = []
    # for update in aUpdates['unKnown']:
    #     if not isinstance(update['KB'], dict):
    #         paths.append(update['Path'])
    #
    # s = []
    # s.append('{\"Paths\": [')
    # s.append(os.linesep)
    # for path in paths:
    #     s.append(json.dumps(path))
    #     s.append(',')
    #     s.append(os.linesep)
    #
    # del s[len(s)-2:len(s)-1]
    # s.append(']}')
    # print(''.join(s))
    # print('-----------updateToPackage-----------')

if __name__ == '__main__':

    argc = len(sys.argv)

    if argc == 2:
        inputPath = os.path.abspath(sys.argv[1])
        subFolders = os.listdir(inputPath)
        updates = []

        for folder in subFolders:
            subInputPath = os.path.join(inputPath, folder)
            files = core.dirs.getSubDirectoryFiles(subInputPath)

            if 0 < len(files):
                date = core.dates.getDate(folder)
                updates.extend(core.updates.getUpdatesFromPackage(files, date))

        updates = core.updates.Updates.separateToKnownAndUnknown(updates)
        printUpdates(updates)

    elif argc == 3:
        inputPath = os.path.abspath(sys.argv[1])
        files = core.dirs.getSubDirectoryFiles(inputPath)

        if 0 < len(files):
            date = core.dates.getDate(sys.argv[2])
            updates = core.updates.getUpdatesFromPackage(files, date)

            updates = core.updates.Updates.separateToKnownAndUnknown(updates)
            printUpdates(updates)

    else:
        print('Using:{}{} <path to directory with updates>'
              '<date (MMYY), only for non year edition>'.format(os.linesep, sys.argv[0]))
