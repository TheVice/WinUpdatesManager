import sys
import os


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

    dest = os.path.join(os.getcwd(), aDest, os.path.basename(aSrc))
    print('Source -', aSrc)
    print('Destination -', dest)

    os.renames(aSrc, dest)

if __name__ == '__main__':

    argc = len(sys.argv)
    if argc > 1:

        dPath = None
        upList = None
        for dirPath, subDirList, fileList in os.walk(sys.argv[1]):
            dPath = dirPath
            upList = fileList
            break

        if upList is not None:
            for up in upList:

                try:
                    src = os.path.join(dPath, up)
                    uf = UpFile(src)
                    moveUp(src, uf.getPath())
                except:
                    print('Skipping', up)
    else:
        print('Using', sys.argv[0], '<path to dir with updates>')
