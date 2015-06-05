import os

def getSubDirectoryFiles(aPath):

    files = []

    for dirPath, subDirList, fileList in os.walk(aPath):
        for fileName in fileList:
            filePath = os.path.join(dirPath, fileName)
            filePath = os.path.relpath(filePath, aPath)
            filePath = os.path.join(os.path.sep, filePath)
            files.append(filePath)

    return files
