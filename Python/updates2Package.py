import sys
import os
import core.dirs
from core.versions import Versions
from core.types import Types
from core.languages import Languages
from db.storage import Uif
from core.updates import Updates

versions = Versions()
types = Types()
languages = Languages()

versions.mVersions['WindowsXP'] = versions.WinXP
versions.mVersions['WindowsServer2003'] = versions.Win2k3
versions.mVersions['Windows6.0'] = versions.Vista
versions.mVersions['Windows6.1'] = versions.Seven
versions.mVersions['Windows8-RT'] = versions.Eight
versions.mVersions['Windows8.1'] = versions.EightDotOne

types.mTypes['x86'] = types.x86
types.mTypes['x64'] = types.x64
types.mTypes['arm'] = types.ARM
types.mTypes['ia64'] = types.IA64

languages.mLanguages = {}
languages.mLanguages['NEU'] = languages.Neutral
languages.mLanguages['ARA'] = languages.Arabic
languages.mLanguages['CHS'] = languages.Chinese_Simplified
languages.mLanguages['CHT'] = languages.Chinese_Traditional
languages.mLanguages['CSY'] = languages.Czech
languages.mLanguages['DAN'] = languages.Danish
languages.mLanguages['NLD'] = languages.Dutch
languages.mLanguages['ENU'] = languages.English
languages.mLanguages['FIN'] = languages.Finnish
languages.mLanguages['FRA'] = languages.French
languages.mLanguages['DEU'] = languages.German
languages.mLanguages['ELL'] = languages.Greek
languages.mLanguages['HEB'] = languages.Hebrew
languages.mLanguages['HUN'] = languages.Hungarian
languages.mLanguages['ITA'] = languages.Italian
languages.mLanguages['JPN'] = languages.Japanese
languages.mLanguages['KOR'] = languages.Korean
languages.mLanguages['NOR'] = languages.Norwegian
languages.mLanguages['PLK'] = languages.Polish
languages.mLanguages['PTB'] = languages.Portuguese_Brazil
languages.mLanguages['PTG'] = languages.Portuguese_Portugal
languages.mLanguages['RUS'] = languages.Russian
languages.mLanguages['ESN'] = languages.Spanish
languages.mLanguages['SVE'] = languages.Swedish
languages.mLanguages['TRK'] = languages.Turkish
languages.mCalligraphicLanguages = languages.mLanguages

class UpFile:

    def __init__(self, aPath):

        self.mVersion = versions.getVersion(aPath)
        if isinstance(self.mVersion, dict):
            raise Exception('Unable to detect version: {}'.format(aPath))

        self.mType = types.getType(aPath)
        if isinstance(self.mType, dict):
            raise Exception('Unable to detect type: {}'.format(aPath))

        if versions.isLanguageCanBeNeutral(self.mVersion):
            self.mLanguage = languages.Neutral
        else:
            self.mLanguage = languages.getLanguage(aPath)
        if isinstance(self.mLanguage, dict):
            raise Exception('Unable to detect language: {}'.format(aPath))

    def getPath(self):

        return os.path.join(versions.getPathKey(self.mVersion).replace(os.sep, ''),
                            types.getPathKey(self.mType).replace(os.sep, ''),
                            languages.getPathKey(self.mLanguage))


def moveUp(aSrc, aDest):

    try:
        os.renames(aSrc, aDest)
        print('{} -> {}'.format(aSrc, aDest))
    except FileExistsError:
        print('Cannot move {} to {} because file already exists'.format(aSrc, aDest))

def relPaths2Full(aRoot, aPaths):

    retFiles = []

    files = core.dirs.getSubDirectoryFiles(aRoot)
    for p in aPaths:
        for f in files:
            if -1 != f.find(p):
                retFiles.append(os.path.normpath('{}{}'.format(aRoot, f)))

    return retFiles


def processFolder(aFolderPath):

    dPath = None
    upList = None

    for dirPath, subDirList, fileList in os.walk(aFolderPath):
        dPath = dirPath
        upList = fileList
        break

    if upList is not None:
        for up in upList:

            try:
                src = os.path.join(dPath, up)
                uf = UpFile(src)
                moveUp(src, os.path.join(os.getcwd(), uf.getPath(), os.path.basename(src)))

            except:
                print(sys.exc_info()[1])


def processFolderViaListFromFile(aFilePath, aFolderPath):

    updates = Uif.getUpdatesFromStorage(aFilePath)
    updates = Updates.separateToKnownAndUnknown(updates)

    paths = []
    for up in updates['unKnown']:
        if not isinstance(up['KB'], dict):
            paths.append(up['Path'])

    sourcePaths = relPaths2Full(aFolderPath, paths)
    for src in sourcePaths:
        try:
            uf = UpFile(src)
        except:
            print('Cannot move: {}'.format(sys.exc_info()[1]))
            continue
        dest = os.path.split(src)
        dest = os.path.join(dest[0], uf.getPath(), dest[1])
        moveUp(src, dest)


if __name__ == '__main__':

    argc = len(sys.argv)
    if argc == 2:
        folderPath = sys.argv[1]

        if os.path.isdir(folderPath):
            processFolder(folderPath)


    elif argc == 3:
        filePath = sys.argv[1]
        folderPath = sys.argv[2]

        if os.path.isfile(filePath) and os.path.isdir(folderPath):
            processFolderViaListFromFile(filePath, folderPath)

    else:
        print('Using {0}'
              ' <folder with updates>{1}'
              'Using {0}'
              ' <path to Uif file with updates contain unknown field(s)>'
              ' <root of updates storage>'.format(sys.argv[0], os.linesep))
