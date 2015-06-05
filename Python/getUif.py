import os
import sys
import core.dates
import core.dirs
from core.updates import Updates


def printUpdates(aUpdates):

    for update in aUpdates['known']:
        print(update)

    for update in aUpdates['unKnown']:
        print(update)


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
                updates.extend(Updates.getUpdatesFromPackage(files, date))

        updates = Updates.separateToKnownAndUnknown(updates)
        printUpdates(updates)

    elif argc == 3:
        inputPath = os.path.abspath(sys.argv[1])
        files = core.dirs.getSubDirectoryFiles(inputPath)

        if 0 < len(files):
            date = core.dates.getDate(sys.argv[2])
            updates = Updates.getUpdatesFromPackage(files, date)

            updates = Updates.separateToKnownAndUnknown(updates)
            printUpdates(updates)

    else:
        print('Using:{}{} <path to directory with updates>'
              '<date (MMYY), only for non year edition>'.format(os.linesep, sys.argv[0]))
