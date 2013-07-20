import core


def getUpdatesFromPackage(aFiles, aDate):

    print('\n' + str(aDate) + '\n')
    updates = core.updates.getUpdatesInfoFromPackage(aFiles)

    for up in updates:
        up = up[:len(up) - 1] + str(aDate) + '}'
        print(up)


def getFromYearEditionPackage(aPaths, aDates):

    i = 0
    for path in aPaths:
        files = core.updates.getSubDirectoryFiles(path)

        for fileName in files:
            fileName = fileName[fileName.find('KB'):]

        core.updates.getUpdatesFromPackageToJSON(files,
            aDates[min(i, len(aDates) - 1)])
        i += 1


#getFromYearEditionPackage(getSubFolderOnly('D:\\', True),
#getDatesForYearEdition(getSubFolderOnly('D:\\')))
