import sys
import os
import core.dirs
from test.jsonHelper import JsonHelper

class UpFile:

    def __init__(self, aUpFile):

        versions = {}
        #versions['Windows2000'] = self.Win2k
        versions['WindowsXP'] = 'WindowsXP'
        versions['WindowsServer2003'] = 'WindowsServer2003'
        versions['WindowsVista'] = 'Windows6.0'
        #versions['WindowsServer2008'] = self.Win2k8
        versions['Windows7'] = 'Windows6.1'
        #versions['WindowsServer2008R2'] = self.Win2k8R2
        versions['Windows8'] = 'Windows8-RT'
        #versions['WindowsServer2012'] = self.Win2k12
        versions['Windows8.1'] = 'Windows8.1'
        #versions['WindowsServer2012R2'] = self.Win2k12R2
        #versions['WindowsRT'] = self.WinRT

        self.mVersion = self.getValue(versions, aUpFile)
        if self.mVersion is None:
            raise Exception('Version is None', aUpFile)

        types = {}
        types['x86'] = 'x86'
        types['x64'] = 'x64'
        types['arm'] = 'arm'
        types['ia64'] = 'ia64'

        self.mType = self.getValue(types, aUpFile)
        if self.mType is None:
            raise Exception('Type is None', aUpFile)

        languages = {}
        #languages['NEU'] = 'NEU'
        #languages[os.sep + 'ARA' + os.sep] = self.Arabic
        #languages[os.sep + 'CHS' + os.sep] = self.Chinese_Simplified
        #languages[os.sep + 'CHT' + os.sep] = self.Chinese_Traditional
        #languages[os.sep + 'CSY' + os.sep] = self.Czech
        #languages[os.sep + 'DAN' + os.sep] = self.Danish
        #languages[os.sep + 'NLD' + os.sep] = self.Dutch
        languages['ENU'] = 'ENU'
        #languages[os.sep + 'FIN' + os.sep] = self.Finnish
        #languages[os.sep + 'FRA' + os.sep] = self.French
        #languages[os.sep + 'DEU' + os.sep] = self.German
        #languages[os.sep + 'ELL' + os.sep] = self.Greek
        #languages[os.sep + 'HEB' + os.sep] = self.Hebrew
        #languages[os.sep + 'HUN' + os.sep] = self.Hungarian
        #languages[os.sep + 'ITA' + os.sep] = self.Italian
        #languages[os.sep + 'JPN' + os.sep] = self.Japanese
        #languages[os.sep + 'KOR' + os.sep] = self.Korean
        #languages[os.sep + 'NOR' + os.sep] = self.Norwegian
        #languages[os.sep + 'PLK' + os.sep] = self.Polish
        #languages[os.sep + 'PTB' + os.sep] = self.Portuguese_Brazil
        #languages[os.sep + 'PTG' + os.sep] = self.Portuguese_Portugal
        languages['RUS'] = 'RUS'
        #languages[os.sep + 'ESN' + os.sep] = self.Spanish
        #languages[os.sep + 'SVE' + os.sep] = self.Swedish
        #languages[os.sep + 'TRK' + os.sep] = self.Turkish

        if (self.mVersion is 'WindowsVista' or
            self.mVersion is 'Windows7' or
            self.mVersion is 'Windows8' or
            self.mVersion is 'Windows8.1'):
            self.mLanguage = 'NEU'
        else:
            self.mLanguage = self.getValue(languages, aUpFile)
        if self.mLanguage is None:
            raise Exception('Language is None', aUpFile)

    def getValue(self, aDictionary, aValue):

        for key, value in aDictionary.items():
            if aValue.find(value) != -1:
                return key

        return None

    def getPath(self):

        return os.path.join(self.mVersion, self.mType, self.mLanguage)


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


if __name__ == '__main__':

    argc = len(sys.argv)
    if argc == 2:

        folderPath = sys.argv[1]
        if os.path.isdir(folderPath):

            dPath = None
            upList = None

            for dirPath, subDirList, fileList in os.walk(folderPath):
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

    elif argc == 3:
        filePath = sys.argv[1]
        folderPath = sys.argv[2]
        if os.path.isfile(filePath) and os.path.isdir(folderPath):

            jsonHelper = JsonHelper(filePath)
            paths = jsonHelper.GetTestRoot('Paths')
            sourcePaths = relPaths2Full(folderPath, paths)
            for src in sourcePaths:
                try:
                    uf = UpFile(src)
                except:
                    print(sys.exc_info()[1])
                    continue
                dest = os.path.split(src)
                dest = os.path.join(dest[0], uf.getPath(), dest[1])
                moveUp(src, dest)

    else:
        print('Using:{}{} <path to dir with updates>{}'
              '{} <path to json file with paths to updates> <root of updates storage>'.format(os.linesep,
                                                                                              sys.argv[0], os.linesep,
                                                                                              sys.argv[0]))
