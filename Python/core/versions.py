import os
from core.unknownSubstance import UnknownSubstance


class Versions(UnknownSubstance):

    def __init__(self):

        self.Win2k = 'Windows 2000'
        self.WinXP = 'Windows XP'
        self.WinXPEmbedded = 'Windows XP Embedded'
        self.Win2k3 = 'Windows Server 2003'
        self.Vista = 'Windows Vista'
        self.Win2k8 = 'Windows Server 2008'
        self.Seven = 'Windows 7'
        self.Win2k8R2 = 'Windows Server 2008 R2'
        self.Eight = 'Windows 8'
        self.Win2k12 = 'Windows Server 2012'
        self.EightDotOne = 'Windows 8.1'
        self.Win2k12R2 = 'Windows Server 2012 R2'

        self.WinRT = 'Windows RT'

        versions = {}

        versions[os.sep + 'Windows2000' + os.sep] = self.Win2k
        versions[os.sep + 'WindowsXP' + os.sep] = self.WinXP
        versions[os.sep + 'WindowsXPEmbedded' + os.sep] = self.WinXPEmbedded
        versions[os.sep + 'WindowsServer2003' + os.sep] = self.Win2k3
        versions[os.sep + 'WindowsVista' + os.sep] = self.Vista
        versions[os.sep + 'WindowsServer2008' + os.sep] = self.Win2k8
        versions[os.sep + 'Windows7' + os.sep] = self.Seven
        versions[os.sep + 'WindowsServer2008R2' + os.sep] = self.Win2k8R2
        versions[os.sep + 'Windows8' + os.sep] = self.Eight
        versions[os.sep + 'WindowsServer2012' + os.sep] = self.Win2k12
        versions[os.sep + 'Windows8.1' + os.sep] = self.EightDotOne
        versions[os.sep + 'WindowsServer2012R2' + os.sep] = self.Win2k12R2

        versions[os.sep + 'WindowsRT' + os.sep] = self.WinRT

        self.mCalligraphicVersions = dict(versions)

        versions[os.sep + 'windows2000' + os.sep] = self.Win2k
        versions[os.sep + 'windowsxp' + os.sep] = self.WinXP
        versions[os.sep + 'windowsserver2003' + os.sep] = self.Win2k3
        versions[os.sep + 'windowsvista' + os.sep] = self.Vista
        versions[os.sep + 'windowsserver2008' + os.sep] = self.Win2k8
        versions[os.sep + 'windows7' + os.sep] = self.Seven
        versions[os.sep + 'windowsserver2008r2' + os.sep] = self.Win2k8R2
        versions[os.sep + 'windows8' + os.sep] = self.Eight
        versions[os.sep + 'windowsserver2012' + os.sep] = self.Win2k12
        versions[os.sep + 'windows8.1' + os.sep] = self.EightDotOne
        versions[os.sep + 'windowswerver2012r2' + os.sep] = self.Win2k12R2

        versions[os.sep + 'windowsrt' + os.sep] = self.WinRT

        versions[os.sep + 'WINDOWS2000' + os.sep] = self.Win2k
        versions[os.sep + 'WINDOWSXP' + os.sep] = self.WinXP
        versions[os.sep + 'WINDOWSSERVER2003' + os.sep] = self.Win2k3
        versions[os.sep + 'WINDOWSVISTA' + os.sep] = self.Vista
        versions[os.sep + 'WINDOWSSERVER2008' + os.sep] = self.Win2k8
        versions[os.sep + 'WINDOWS7' + os.sep] = self.Seven
        versions[os.sep + 'WINDOWSSERVER2008R2' + os.sep] = self.Win2k8R2
        versions[os.sep + 'WINDOWS8' + os.sep] = self.Eight
        versions[os.sep + 'WINDOWSSERVER2012' + os.sep] = self.Win2k12
        versions[os.sep + 'WINDOWS8.1' + os.sep] = self.EightDotOne
        versions[os.sep + 'WINDOWSSERVER2012R2' + os.sep] = self.Win2k12R2

        versions[os.sep + 'WINDOWSRT' + os.sep] = self.WinRT

        self.mVersions = versions

    def getVersion(self, aPath):

        version = UnknownSubstance.getItemByPath(self.mVersions, aPath)

        if version is not None:
            return version

        return UnknownSubstance.unknown('UNKNOWN VERSION', aPath)

    def getPathKey(self, aValue):

        return UnknownSubstance.getKeyPathByValue(
            self.mCalligraphicVersions, aValue)

    def isLanguageCanBeNeutral(self, aVersion):

        return (aVersion == self.Vista or
                aVersion == self.Win2k8 or
                aVersion == self.Seven or
                aVersion == self.Win2k8R2 or
                aVersion == self.Eight or
                aVersion == self.Win2k12 or
                aVersion == self.EightDotOne or
                aVersion == self.Win2k12R2)
