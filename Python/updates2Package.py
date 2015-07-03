import os
import sys
import core.dirs
from db.storage import Uif
from core.types import Types
from core.updates import Updates
from core.versions import Versions
from core.languages import Languages

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

        return os.path.join(
            versions.getPathKey(self.mVersion).replace(os.sep, ''),
            types.getPathKey(self.mType).replace(os.sep, ''),
            languages.getPathKey(self.mLanguage))


def moveUp(aSrc, aDest):

    try:
        os.renames(aSrc, aDest)
        print('{} -> {}'.format(aSrc, aDest))
    except FileExistsError if 2 < sys.version_info[0] else OSError:
        print('Cannot move {} to {} because file already exists'.format(aSrc,
                                                                        aDest))


def moveFilesToNewLocations(aSourcePaths):

    for src in aSourcePaths:

        try:
            uf = UpFile(src)
        except:
            print(sys.exc_info()[1])
            continue

        dest = os.path.split(src)
        dest = os.path.join(dest[0], uf.getPath(), dest[1])
        moveUp(src, dest)


def getFullPath2UnknownUpdatesAtFolder(aFolderPath):

    files = []

    objects = os.listdir(aFolderPath)
    for o in objects:
        path = os.path.normpath('{}{}{}'.format(aFolderPath, os.path.sep, o))
        if os.path.isfile(path):
            files.append(path)

    return files


def relPaths2Full(aRoot, aPaths):

    files = []

    updatesFiles = core.dirs.getSubDirectoryFiles(aRoot)
    for p in aPaths:
        for uf in updatesFiles:
            if p in uf:
                files.append(os.path.normpath('{}{}'.format(aRoot, uf)))

    return files


def getFullPath2UnknownUpdatesAtList(aPathToUifFile,
                                     aPathToRootFolderWihtUpdates):

    updates = Uif.getUpdatesFromStorage(aPathToUifFile)
    updates = Updates.separateToKnownAndUnknown(updates)

    files = []
    for up in updates['unKnown']:
        if not isinstance(up['KB'], dict):
            files.append(up['Path'])

    if 0 < len(files):
        return relPaths2Full(aPathToRootFolderWihtUpdates, files)

    return []


if __name__ == '__main__':

    argc = len(sys.argv)

    if argc == 2 or argc == 3:
        paths = None

        if argc == 2:
            folderPath = sys.argv[1]
            if os.path.isdir(folderPath):
                paths = getFullPath2UnknownUpdatesAtFolder(folderPath)
        elif argc == 3:
            filePath = sys.argv[1]
            folderPath = sys.argv[2]
            if os.path.isfile(filePath) and os.path.isdir(folderPath):
                paths = getFullPath2UnknownUpdatesAtList(filePath, folderPath)

        if None != paths and 0 < len(paths):
            moveFilesToNewLocations(paths)
        else:
            print('No operation performed')
    else:
        print('Using {0}'
              ' <folder with updates>{1}'
              'Using {0}'
              ' <path to Uif file with updates contain unknown field(s)>'
              ' <root of updates storage>'.format(sys.argv[0], os.linesep))
