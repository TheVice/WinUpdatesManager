import unittest
import core.dirs


class TestSequenceFunctions(unittest.TestCase):

    def test_PathsClass(self):

        inputPaths = ['E:\\0112', 'E:\\0112\\',
            'E:\\2584146\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2584146-X64.MSU',
            'E', 'E:\\Addons']
        correctRootPaths = ['E:\\0112', 'E:\\2584146', 'E', 'E:\\Addons']
        correctRootObjects = ['0112', '2584146', 'E', 'Addons']

        paths = core.dirs.Paths(inputPaths)

        self.assertEqual(inputPaths, paths.getFullPaths())
        self.assertEqual(correctRootPaths, paths.getRootPaths())
        self.assertEqual(correctRootObjects, paths.getRootObjects())

        inputPaths = [
'E:\\0112\\2584146\\Windows7\\x64\\NEU\\' +
'WINDOWS6.1-KB2584146-X64.MSU',
'E:\\0212\\2633870\\Windows7\\x64\\NEU\\MSIPATCHREGFIX-AMD64.EXE',
'E:\\0212\\2633870\\Windows7\\x64\\NEU\\NDP40-KB2633870-X64.EXE',
'E:\\0312\\2621440\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2621440-X64.MSU',
'E:\\0312\\2621440\\Windows7\\x86\\NEU\\WINDOWS6.1-KB2621440-X86.MSU',
'E:\\0312\\2621440\\WindowsServer2003\\x64\\ENU\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2621440-X64-ENU.EXE',
'E:\\0412\\2653956\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2653956-X64.MSU',
'E:\\0412\\2653956\\Windows7\\x86\\NEU\\WINDOWS6.1-KB2653956-X86.MSU',
'E:\\0412\\2653956\\WindowsServer2003\\x64\\ENU\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2653956-X64-ENU.EXE',
'E:\\0412\\2653956\\WindowsServer2003\\x64\\RUS\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2653956-X64-RUS.EXE',
'E:\\0512\\2604042\\WindowsXP\\x86\\ENU\\NDP1.0SP3-KB2604042-X86-OCM-ENU.EXE',
'E:\\0512\\2604078\\WindowsServer2003\\x86\\ENU\\' +
'WINDOWSSERVER2003-KB2604078-X86-ENU.EXE',
'E:\\0512\\2604092\\WindowsServer2003\\x64\\ENU\\MSIPATCHREGFIX-AMD64.EXE',
'E:\\0512\\2604092\\WindowsServer2003\\x64\\ENU\\NDP20SP2-KB2604092-X64.EXE',
'E:\\0512\\2604092\\WindowsServer2003\\x86\\ENU\\MSIPATCHREGFIX-X86.EXE',
'E:\\0612\\2656368\\Windows7\\x64\\NEU\\MSIPATCHREGFIX-AMD64.EXE',
'E:\\0612\\2656368\\Windows7\\x64\\NEU\\NDP40-KB2656368-V2-X64.EXE',
'E:\\0612\\2656368\\Windows7\\x86\\NEU\\MSIPATCHREGFIX-X86.EXE',
'E:\\0612\\2656368\\Windows7\\x86\\NEU\\NDP40-KB2656368-V2-X86.EXE',
'E:\\0612\\2656368\\WindowsServer2003\\x64\\ENU\\MSIPATCHREGFIX-AMD64.EXE',
'E:\\0612\\2656368\\WindowsServer2003\\x64\\ENU\\NDP40-KB2656368-V2-X64.EXE',
'E:\\0712\\2655992\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2655992-X64.MSU',
'E:\\0712\\2655992\\Windows7\\x86\\NEU\\WINDOWS6.1-KB2655992-X86.MSU',
'E:\\0712\\2655992\\WindowsServer2003\\x64\\ENU\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2655992-X64-ENU.EXE',
'E:\\0712\\2655992\\WindowsServer2003\\x64\\RUS\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2655992-X64-RUS.EXE',
'E:\\0712\\2655992\\WindowsServer2003\\x86\\ENU\\' +
'WINDOWSSERVER2003-KB2655992-X86-ENU.EXE',
'E:\\0712\\2655992\\WindowsServer2003\\x86\\RUS\\' +
'WINDOWSSERVER2003-KB2655992-X86-RUS.EXE',
'E:\\0712\\2655992\\WindowsServer2008\\x64\\NEU\\WINDOWS6.0-KB2655992-X64.MSU',
'E:\\0812\\2705219\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2705219-X64.MSU',
'E:\\0812\\2705219\\Windows7\\x86\\NEU\\WINDOWS6.1-KB2705219-X86.MSU',
'E:\\0812\\2705219\\WindowsServer2003\\x64\\ENU\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2705219-X64-ENU.EXE',
'E:\\0812\\2705219\\WindowsServer2003\\x64\\RUS\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2705219-X64-RUS.EXE',
'E:\\0812\\2705219\\WindowsServer2003\\x86\\ENU\\' +
'WINDOWSSERVER2003-KB2705219-X86-ENU.EXE',
'E:\\0812\\2705219\\WindowsServer2003\\x86\\RUS\\' +
'WINDOWSSERVER2003-KB2705219-X86-RUS.EXE',
'E:\\0812\\2705219\\WindowsServer2008\\x64\\NEU\\WINDOWS6.0-KB2705219-X64.MSU',
'E:\\0812\\2705219\\WindowsServer2008\\x86\\NEU\\WINDOWS6.0-KB2705219-X86.MSU',
'E:\\0911\\2570947\\Windows2000\\x86\\ENU\\' +
'WINDOWS2000-KB2570947-X86-CUSTOM-ENU.EXE',
'E:\\0911\\2570947\\Windows2000\\x86\\RUS\\' +
'WINDOWS2000-KB2570947-X86-CUSTOM-RUS.EXE',
'E:\\0911\\2570947\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2570947-X64.MSU',
'E:\\0911\\2570947\\Windows7\\x86\\NEU\\WINDOWS6.1-KB2570947-X86.MSU',
'E:\\0911\\2570947\\WindowsServer2003\\x64\\ENU\\' +
'WINDOWS6.0-KB2570947-X64-CUSTOM.MSU',
'E:\\0911\\2570947\\WindowsServer2003\\x64\\ENU\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2570947-X64-ENU.EXE',
'E:\\0911\\2570947\\WindowsServer2003\\x64\\RUS\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2570947-X64-RUS.EXE',
'E:\\0911\\2570947\\WindowsServer2003\\x86\\ENU\\' +
'WINDOWS6.0-KB2570947-X86-CUSTOM.MSU',
'E:\\0911\\2570947\\WindowsServer2003\\x86\\ENU\\' +
'WINDOWSSERVER2003-KB2570947-X86-ENU.EXE',
'E:\\1012\\2705219\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2705219-V2-X64.MSU',
'E:\\1012\\2705219\\Windows7\\x86\\NEU\\WINDOWS6.1-KB2705219-V2-X86.MSU',
'E:\\1012\\2705219\\WindowsServer2003\\x64\\ENU' +
'\\WINDOWSSERVER2003.WINDOWSXP-KB2705219-V2-X64-ENU.EXE',
'E:\\1012\\2705219\\WindowsServer2003\\x64\\RUS' +
'\\WINDOWSSERVER2003.WINDOWSXP-KB2705219-V2-X64-RUS.EXE',
'E:\\1012\\2705219\\WindowsServer2003\\x86\\ENU\\' +
'WINDOWSSERVER2003-KB2705219-V2-X86-ENU.EXE',
'E:\\1012\\2705219\\WindowsServer2003\\x86\\RUS\\' +
'WINDOWSSERVER2003-KB2705219-V2-X86-RUS.EXE',
'E:\\1012\\2705219\\WindowsServer2008\\x64\\NEU\\' +
'WINDOWS6.0-KB2705219-V2-X64.MSU',
'E:\\1012\\2705219\\WindowsServer2008\\x86\\NEU\\' +
'WINDOWS6.0-KB2705219-V2-X86.MSU',
'E:\\1012\\2705219\\WindowsServer2008R2\\x64\\NEU\\' +
'WINDOWS6.1-KB2705219-V2-X64.MSU',
'E:\\1012\\2705219\\WindowsVista\\x64\\NEU\\WINDOWS6.0-KB2705219-V2-X64.MSU',
'E:\\1112\\2698023\\WindowsServer2003\\x64\\ENU\\MSIPATCHREGFIX-AMD64.EXE',
'E:\\1112\\2698023\\WindowsServer2003\\x64\\ENU\\NDP1.1SP1-KB2698023-X86.EXE',
'E:\\1112\\2698023\\WindowsServer2008\\x64\\NEU\\MSIPATCHREGFIX-AMD64.EXE',
'E:\\1112\\2698023\\WindowsServer2008\\x64\\NEU\\NDP1.1SP1-KB2698023-X86.EXE',
'E:\\1112\\2698023\\WindowsServer2008\\x86\\NEU\\MSIPATCHREGFIX-X86.EXE',
'E:\\1112\\2698023\\WindowsServer2008\\x86\\NEU\\NDP1.1SP1-KB2698023-X86.EXE',
'E:\\1112\\2698023\\WindowsVista\\x64\\NEU\\MSIPATCHREGFIX-AMD64.EXE',
'E:\\1112\\2698023\\WindowsVista\\x64\\NEU\\NDP1.1SP1-KB2698023-X86.EXE',
'E:\\1112\\2698023\\WindowsVista\\x86\\NEU\\MSIPATCHREGFIX-X86.EXE',
'E:\\1112\\2698023\\WindowsVista\\x86\\NEU\\NDP1.1SP1-KB2698023-X86.EXE',
'E:\\1112\\2761451\\WindowsVista\\x86\\NEU\\IE9-WINDOWS6.0-KB2761451-X86.MSU',
'E:\\1212\\2753842\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2753842-X64.MSU',
'E:\\1212\\2753842\\Windows7\\x86\\NEU\\WINDOWS6.1-KB2753842-X86.MSU',
'E:\\1212\\2753842\\Windows8\\x64\\NEU\\WINDOWS8-RT-KB2753842-X64.MSU',
'E:\\1212\\2753842\\Windows8\\x86\\NEU\\WINDOWS8-RT-KB2753842-X86.MSU',
'E:\\1212\\2753842\\WindowsRT\\arm\\NEU\\WINDOWS8-RT-KB2753842-ARM.MSU',
'E:\\1212\\2753842\\WindowsServer2003\\x64\\ENU\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2753842-X64-ENU.EXE',
'E:\\1212\\2753842\\WindowsServer2003\\x64\\RUS\\' +
'WINDOWSSERVER2003.WINDOWSXP-KB2753842-X64-RUS.EXE',
'E:\\1212\\2753842\\WindowsServer2003\\x86\\ENU\\' +
'WINDOWSSERVER2003-KB2753842-X86-ENU.EXE',
'E:\\1212\\2753842\\WindowsServer2003\\x86\\RUS\\' +
'WINDOWSSERVER2003-KB2753842-X86-RUS.EXE',
'E:\\1212\\2753842\\WindowsServer2008\\x64\\NEU\\WINDOWS6.0-KB2753842-X64.MSU',
'E:\\1212\\2753842\\WindowsServer2008\\x86\\NEU\\WINDOWS6.0-KB2753842-X86.MSU',
'E:\\1212\\2753842\\WindowsServer2008R2\\x64\\NEU\\' +
'WINDOWS6.1-KB2753842-X64.MSU',
'E:\\Addons\\KB979099\\' +
'WindowsRightsManagementServicesSP2-KB979099-Client-amd64-ENU.exe',
'E:\\Addons\\KB979099\\' +
'WindowsRightsManagementServicesSP2-KB979099-Client-amd64-RU.exe',
'E:\\Addons\\KB979099\\' +
'WindowsRightsManagementServicesSP2-KB979099-Client-x86-ENU.exe',
'E:\\Addons\\KB979099\\' +
'WindowsRightsManagementServicesSP2-KB979099-Client-x86-RU.exe',
'E:\\Addons\\KB980248\\WINDOWS6.0-KB980248-X64.MSU',
'E:\\Addons\\KB980248\\WINDOWS6.0-KB980248-X86.MSU',
'E:\\Addons\\KB982551\\KB982551_INFO.ZIP',
'E:\\Addons\\KB982551\\WINDOWSSERVER2003-KB982551-X64-ENU.EXE',
'E:\\Addons\\KB982551\\WINDOWSSERVER2003-KB982551-X86-ENU.EXE',
'E:\\Addons\\KB982551\\WINDOWSXP-KB982551-V2-X86-ENU.EXE',
'E:\\Addons\\KB982551\\WINDOWSXP-KB982551-V2-X86-RUS.EXE',
'E:\\Addons\\PowerShell\\KB928439 - v1\\Windows6.0-KB928439-x64.msu',
'E:\\Addons\\PowerShell\\KB928439 - v1\\Windows6.0-KB928439-x86.msu']
        correctRootPaths = ['E:\\0112', 'E:\\0212', 'E:\\0312', 'E:\\0412',
        'E:\\0512', 'E:\\0612', 'E:\\0712', 'E:\\0812', 'E:\\0911', 'E:\\1012',
        'E:\\1112', 'E:\\1212', 'E:\\Addons']
        correctRootObjects = ['0112', '0212', '0312', '0412', '0512', '0612',
            '0712', '0812', '0911', '1012', '1112', '1212', 'Addons']

        paths = core.dirs.Paths(inputPaths)

        self.assertEqual(inputPaths, paths.getFullPaths())
        self.assertEqual(correctRootPaths, paths.getRootPaths())
        self.assertEqual(correctRootObjects, paths.getRootObjects())

        for path, i in zip(correctRootPaths, range(len(correctRootPaths))):
            self.assertEqual(i + 1, len(paths.getSubObjects(path)))

        subObjects = paths.getSubObjects('E:\\Addons')
        shift = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10 + 11 + 12

        for i in range(0, len(subObjects)):
            self.assertEqual(inputPaths[i + shift], subObjects[i])

        subObjects = paths.getSubObjects('E:\\Addons', True)
        for i in range(0, len(subObjects)):
            inputPath = inputPaths[i + shift]
            self.assertEqual(inputPath[len('E:\\Addons'):], subObjects[i])

    #for writing next test MockObject required to use,
    #but no skill to do it right now
    #def test_getSubDirectoryFiles(self):

        #getSubDirectoryFiles()
        #self.assertEqual()

    def test_getRootPaths(self):

        paths = ['E:\\0112', 'E:\\0112\\',
        'E:\\2584146\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2584146-X64.MSU',
        'E', '\\', 'E:\\0112', '\\\\', '\\', '\\\\\\']
        correctRootPaths = ['E:\\0112', 'E:\\2584146', 'E', '\\', '\\\\', '\\\\\\']

        rootPaths = core.dirs.getRootPaths(paths)

        for correctPath, path in zip(correctRootPaths, rootPaths):
            self.assertEqual(correctPath, path)

    def test_getRootObjects(self):

        paths = ['E:\\0112', 'E:\\0112\\',
        'E:\\2584146\\Windows7\\x64\\NEU\\WINDOWS6.1-KB2584146-X64.MSU',
        'E', 'E:\\Addons']
        correctRootObjects = ['0112', '2584146', 'E', 'Addons']

        rootObjects = core.dirs.getRootObjects(paths)

        for correctPath, path in zip(correctRootObjects, rootObjects):
            self.assertEqual(correctPath, path)

if __name__ == '__main__':

    unittest.main()
