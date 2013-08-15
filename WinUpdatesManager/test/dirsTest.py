import unittest
import os
import core.dirs


class TestSequenceFunctions(unittest.TestCase):

    def test_PathsClass(self):

        inputPaths = ['E:' + os.sep + '0112', 'E:' + os.sep + '0112' + os.sep,
            'E:' + os.sep + '2584146' + os.sep + 'Windows7' + os.sep + 'x64' +
            os.sep + 'NEU' + os.sep + 'WINDOWS6.1-KB2584146-X64.MSU',
            'E', 'E:' + os.sep + 'Addons']
        correctRootPaths = ['E:' + os.sep + '0112', 'E:' + os.sep + '2584146',
            'E', 'E:' + os.sep + 'Addons']
        correctRootObjects = ['0112', '2584146', 'E', 'Addons']

        paths = core.dirs.Paths(inputPaths)

        self.assertEqual(inputPaths, paths.getFullPaths())
        self.assertEqual(correctRootPaths, paths.getRootPaths())
        self.assertEqual(correctRootObjects, paths.getRootObjects())

        inputPaths = [
            'E:' + os.sep + '0112' + os.sep + '2584146' + os.sep + 'Windows7' +
            os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2584146-X64.MSU',
            'E:' + os.sep + '0212' + os.sep + '2633870' + os.sep + 'Windows7' +
            os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'MSIPATCHREGFIX-AMD64.EXE',
            'E:' + os.sep + '0212' + os.sep + '2633870' + os.sep + 'Windows7' +
            os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'NDP40-KB2633870-X64.EXE',
            'E:' + os.sep + '0312' + os.sep + '2621440' + os.sep + 'Windows7' +
            os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2621440-X64.MSU',
            'E:' + os.sep + '0312' + os.sep + '2621440' + os.sep + 'Windows7' +
            os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2621440-X86.MSU',
            'E:' + os.sep + '0312' + os.sep + '2621440' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2621440-X64-ENU.EXE',
            'E:' + os.sep + '0412' + os.sep + '2653956' + os.sep + 'Windows7' +
            os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2653956-X64.MSU',
            'E:' + os.sep + '0412' + os.sep + '2653956' + os.sep + 'Windows7'
            + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2653956-X86.MSU',
            'E:' + os.sep + '0412' + os.sep + '2653956' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2653956-X64-ENU.EXE',
            'E:' + os.sep + '0412' + os.sep + '2653956' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2653956-X64-RUS.EXE',
            'E:' + os.sep + '0512' + os.sep + '2604042' + os.sep +
            'WindowsXP' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'NDP1.0SP3-KB2604042-X86-OCM-ENU.EXE',
            'E:' + os.sep + '0512' + os.sep + '2604078' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003-KB2604078-X86-ENU.EXE',
            'E:' + os.sep + '0512' + os.sep + '2604092' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' +
            os.sep + 'MSIPATCHREGFIX-AMD64.EXE',
            'E:' + os.sep + '0512' + os.sep + '2604092' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' +
            os.sep + 'NDP20SP2-KB2604092-X64.EXE',
            'E:' + os.sep + '0512' + os.sep + '2604092' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'MSIPATCHREGFIX-X86.EXE',
            'E:' + os.sep + '0612' + os.sep + '2656368' + os.sep +
            'Windows7' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'MSIPATCHREGFIX-AMD64.EXE',
            'E:' + os.sep + '0612' + os.sep + '2656368' + os.sep +
            'Windows7' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'NDP40-KB2656368-V2-X64.EXE',
            'E:' + os.sep + '0612' + os.sep + '2656368' + os.sep +
            'Windows7' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'MSIPATCHREGFIX-X86.EXE',
            'E:' + os.sep + '0612' + os.sep + '2656368' + os.sep +
            'Windows7' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'NDP40-KB2656368-V2-X86.EXE',
            'E:' + os.sep + '0612' + os.sep + '2656368' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'MSIPATCHREGFIX-AMD64.EXE',
            'E:' + os.sep + '0612' + os.sep + '2656368' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'NDP40-KB2656368-V2-X64.EXE',
            'E:' + os.sep + '0712' + os.sep + '2655992' + os.sep +
            'Windows7' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2655992-X64.MSU',
            'E:' + os.sep + '0712' + os.sep + '2655992' + os.sep +
            'Windows7' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2655992-X86.MSU',
            'E:' + os.sep + '0712' + os.sep + '2655992' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2655992-X64-ENU.EXE',
            'E:' + os.sep + '0712' + os.sep + '2655992' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2655992-X64-RUS.EXE',
            'E:' + os.sep + '0712' + os.sep + '2655992' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003-KB2655992-X86-ENU.EXE',
            'E:' + os.sep + '0712' + os.sep + '2655992' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003-KB2655992-X86-RUS.EXE',
            'E:' + os.sep + '0712' + os.sep + '2655992' + os.sep +
            'WindowsServer2008' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2655992-X64.MSU',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep + 'Windows7' +
            os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2705219-X64.MSU',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep + 'Windows7' +
            os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2705219-X86.MSU',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2705219-X64-ENU.EXE',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2705219-X64-RUS.EXE',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003-KB2705219-X86-ENU.EXE',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003-KB2705219-X86-RUS.EXE',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep +
            'WindowsServer2008' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2705219-X64.MSU',
            'E:' + os.sep + '0812' + os.sep + '2705219' + os.sep +
            'WindowsServer2008' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2705219-X86.MSU',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep +
            'Windows2000' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWS2000-KB2570947-X86-CUSTOM-ENU.EXE',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep +
            'Windows2000' + os.sep + 'x86' + os.sep + 'RUS' + os.sep +
            'WINDOWS2000-KB2570947-X86-CUSTOM-RUS.EXE',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep + 'Windows7'
            + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2570947-X64.MSU',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep + 'Windows7' +
            os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2570947-X86.MSU',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWS6.0-KB2570947-X64-CUSTOM.MSU',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2570947-X64-ENU.EXE',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2570947-X64-RUS.EXE',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWS6.0-KB2570947-X86-CUSTOM.MSU',
            'E:' + os.sep + '0911' + os.sep + '2570947' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003-KB2570947-X86-ENU.EXE',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep + 'Windows7' +
            os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2705219-V2-X64.MSU',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep + 'Windows7' +
            os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2705219-V2-X86.MSU',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2705219-V2-X64-ENU.EXE',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2705219-V2-X64-RUS.EXE',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003-KB2705219-V2-X86-ENU.EXE',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003-KB2705219-V2-X86-RUS.EXE',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsServer2008' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2705219-V2-X64.MSU',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsServer2008' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2705219-V2-X86.MSU',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsServer2008R2' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2705219-V2-X64.MSU',
            'E:' + os.sep + '1012' + os.sep + '2705219' + os.sep +
            'WindowsVista' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2705219-V2-X64.MSU',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'MSIPATCHREGFIX-AMD64.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'NDP1.1SP1-KB2698023-X86.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsServer2008' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'MSIPATCHREGFIX-AMD64.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsServer2008' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'NDP1.1SP1-KB2698023-X86.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsServer2008' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'MSIPATCHREGFIX-X86.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsServer2008' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'NDP1.1SP1-KB2698023-X86.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsVista' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'MSIPATCHREGFIX-AMD64.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsVista' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'NDP1.1SP1-KB2698023-X86.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsVista' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'MSIPATCHREGFIX-X86.EXE',
            'E:' + os.sep + '1112' + os.sep + '2698023' + os.sep +
            'WindowsVista' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'NDP1.1SP1-KB2698023-X86.EXE',
            'E:' + os.sep + '1112' + os.sep + '2761451' + os.sep +
            'WindowsVista' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'IE9-WINDOWS6.0-KB2761451-X86.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'Windows7' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2753842-X64.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'Windows7' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2753842-X86.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'Windows8' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS8-RT-KB2753842-X64.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'Windows8' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS8-RT-KB2753842-X86.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsRT' + os.sep + 'arm' + os.sep + 'NEU' + os.sep +
            'WINDOWS8-RT-KB2753842-ARM.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2753842-X64-ENU.EXE',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsServer2003' + os.sep + 'x64' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003.WINDOWSXP-KB2753842-X64-RUS.EXE',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'ENU' + os.sep +
            'WINDOWSSERVER2003-KB2753842-X86-ENU.EXE',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsServer2003' + os.sep + 'x86' + os.sep + 'RUS' + os.sep +
            'WINDOWSSERVER2003-KB2753842-X86-RUS.EXE',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsServer2008' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2753842-X64.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsServer2008' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.0-KB2753842-X86.MSU',
            'E:' + os.sep + '1212' + os.sep + '2753842' + os.sep +
            'WindowsServer2008R2' + os.sep + 'x64' + os.sep + 'NEU' + os.sep +
            'WINDOWS6.1-KB2753842-X64.MSU',
            'E:' + os.sep + 'Addons' + os.sep + 'KB979099' + os.sep +
            'WindowsRightsManagementServicesSP2-KB979099-Client-amd64-ENU.exe',
            'E:' + os.sep + 'Addons' + os.sep + 'KB979099' + os.sep +
            'WindowsRightsManagementServicesSP2-KB979099-Client-amd64-RU.exe',
            'E:' + os.sep + 'Addons' + os.sep + 'KB979099' + os.sep +
            'WindowsRightsManagementServicesSP2-KB979099-Client-x86-ENU.exe',
            'E:' + os.sep + 'Addons' + os.sep + 'KB979099' + os.sep +
            'WindowsRightsManagementServicesSP2-KB979099-Client-x86-RU.exe',
            'E:' + os.sep + 'Addons' + os.sep + 'KB980248' + os.sep +
            'WINDOWS6.0-KB980248-X64.MSU',
            'E:' + os.sep + 'Addons' + os.sep + 'KB980248' + os.sep +
            'WINDOWS6.0-KB980248-X86.MSU',
            'E:' + os.sep + 'Addons' + os.sep + 'KB982551' + os.sep +
            'KB982551_INFO.ZIP',
            'E:' + os.sep + 'Addons' + os.sep + 'KB982551' + os.sep +
            'WINDOWSSERVER2003-KB982551-X64-ENU.EXE',
            'E:' + os.sep + 'Addons' + os.sep + 'KB982551' + os.sep +
            'WINDOWSSERVER2003-KB982551-X86-ENU.EXE',
            'E:' + os.sep + 'Addons' + os.sep + 'KB982551' + os.sep +
            'WINDOWSXP-KB982551-V2-X86-ENU.EXE',
            'E:' + os.sep + 'Addons' + os.sep + 'KB982551' + os.sep +
            'WINDOWSXP-KB982551-V2-X86-RUS.EXE',
            'E:' + os.sep + 'Addons' + os.sep + 'PowerShell' + os.sep +
            'KB928439 - v1' + os.sep + 'Windows6.0-KB928439-x64.msu',
            'E:' + os.sep + 'Addons' + os.sep + 'PowerShell' + os.sep +
            'KB928439 - v1' + os.sep + 'Windows6.0-KB928439-x86.msu']
        correctRootPaths = ['E:' + os.sep + '0112', 'E:' + os.sep + '0212',
            'E:' + os.sep + '0312', 'E:' + os.sep + '0412',
            'E:' + os.sep + '0512', 'E:' + os.sep + '0612',
            'E:' + os.sep + '0712', 'E:' + os.sep + '0812',
            'E:' + os.sep + '0911', 'E:' + os.sep + '1012',
            'E:' + os.sep + '1112', 'E:' + os.sep + '1212',
            'E:' + os.sep + 'Addons']
        correctRootObjects = ['0112', '0212', '0312', '0412', '0512', '0612',
            '0712', '0812', '0911', '1012', '1112', '1212', 'Addons']

        paths = core.dirs.Paths(inputPaths)

        self.assertEqual(inputPaths, paths.getFullPaths())
        self.assertEqual(correctRootPaths, paths.getRootPaths())
        self.assertEqual(correctRootObjects, paths.getRootObjects())

        for path, i in zip(correctRootPaths, range(len(correctRootPaths))):
            self.assertEqual(i + 1, len(paths.getSubObjects(path)))

        subObjects = paths.getSubObjects('E:' + os.sep + 'Addons')
        shift = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 + 12

        for i in range(0, len(subObjects)):
            self.assertEqual(inputPaths[i + shift], subObjects[i])

        subObjects = paths.getSubObjects('E:' + os.sep + 'Addons', True)
        for i in range(0, len(subObjects)):
            inputPath = inputPaths[i + shift]
            self.assertEqual(inputPath[len('E:' + os.sep + 'Addons'):],
                subObjects[i])

    #for writing next test MockObject required to use,
    #but no skill to do it right now
    #def test_getSubDirectoryFiles(self):

        #getSubDirectoryFiles()
        #self.assertEqual()

    def test_getRootPaths(self):

        paths = ['E:' + os.sep + '0112', 'E:' + os.sep + '0112' + os.sep,
            'E:' + os.sep + '2584146' + os.sep + 'Windows7' + os.sep + 'x64' +
            os.sep + 'NEU' + os.sep + 'WINDOWS6.1-KB2584146-X64.MSU',
            'E', os.sep, 'E:' + os.sep + '0112', os.sep + os.sep,
            os.sep, os.sep + os.sep + os.sep]
        correctRootPaths = ['E:' + os.sep + '0112',
            'E:' + os.sep + '2584146', 'E', os.sep,
            os.sep + os.sep, os.sep + os.sep + os.sep]

        rootPaths = core.dirs.getRootPaths(paths)

        for correctPath, path in zip(correctRootPaths, rootPaths):
            self.assertEqual(correctPath, path)

    def test_getRootObjects(self):

        paths = ['E:' + os.sep + '0112', 'E:' + os.sep + '0112' + os.sep,
            'E:' + os.sep + '2584146' + os.sep + 'Windows7' + os.sep + 'x64' +
            os.sep + 'NEU' + os.sep + 'WINDOWS6.1-KB2584146-X64.MSU',
            'E', 'E:' + os.sep + 'Addons']
        correctRootObjects = ['0112', '2584146', 'E', 'Addons']

        rootObjects = core.dirs.getRootObjects(paths)

        for correctPath, path in zip(correctRootObjects, rootObjects):
            self.assertEqual(correctPath, path)

if __name__ == '__main__':

    unittest.main()
