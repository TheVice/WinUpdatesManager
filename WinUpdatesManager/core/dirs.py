import os


class Paths:

    def __init__(self, aPaths=''):

        self.mPaths = aPaths
        self.mRootPaths = getRootPaths(self.mPaths)
        self.mRootObjects = getRootObjects(self.mRootPaths, True)

    def getFullPaths(self):

        return self.mPaths

    def getRootPaths(self):

        return self.mRootPaths

    def getRootObjects(self):

        return self.mRootObjects

    def getSubObjects(self, aPath, aNoPath=False):

        files = []
        for path in self.mPaths:
            if 0 == path.find(aPath):
                if aNoPath:
                    files.append(path[len(aPath):])
                else:
                    files.append(path)

        return files


def getSubDirectoryFiles(aPath):

    files = []

    for dirPath, subDirList, fileList in os.walk(aPath):
        for fileName in fileList:
            fileFullPath = os.path.join(dirPath, fileName)
            files.append(fileFullPath)

    return files


def getRootPaths(aPaths):

    files = []

    for path in aPaths:
        if 0 != files.count(path):
            continue

        firstPosOfSlash = path.find('\\')

        if firstPosOfSlash == 2 and (firstPosOfSlash + 1) < len(path):
            secondPosIfSlash = path.find('\\', firstPosOfSlash + 1)

            if secondPosIfSlash < 0:
                files.append(path)
            else:
                newPath = path[0:secondPosIfSlash]
                if 0 != files.count(newPath):
                    continue

                files.append(newPath)

        else:
            files.append(path)

    return files


def getRootObjects(aPaths, aDataPrepared=False):

    files = []

    if False == aDataPrepared:
        files = getRootPaths(aPaths)
        return getRootObjects(files, True)

    for path in aPaths:
        posOfSlash = path.find('\\')

        if posOfSlash == 2:
            files.append(path[posOfSlash + 1:])
        else:
            files.append(path)

    return files
