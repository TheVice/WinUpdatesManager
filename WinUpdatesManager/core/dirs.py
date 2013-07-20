import os


def getSubDirectoryFiles(aPath):

    files = []

    for dirPath, subDirList, fileList in os.walk(aPath):
        for fileName in fileList:
            fileFullPath = os.path.join(dirPath, fileName)
            files.append(fileFullPath)

    return files


def getSubDirectoryOnly(aPath, aFullPath=False):

    subFolders = []

    for dirPath, subDirList, fileList in os.walk(aPath):
        for curDir in subDirList:
            if 1 < os.path.join(dirPath, curDir).count('\\'):
                return subFolders

            if aFullPath:
                subFolders.append(os.path.join(dirPath, curDir))
            else:
                subFolders.append(curDir)

    return subFolders

