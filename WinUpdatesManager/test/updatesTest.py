import unittest
import datetime
import core
import core.updates


class TestSequenceFunctions(unittest.TestCase):

    def test_UpdateClass(self):

        paths = ['E:\\1212\\2761465\\WindowsServer2003' +
           '\\X64\\ENU\\IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE']
        date = datetime.datetime(2012, 12, 1)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        self.assertEqual(2, len(updates))

        versions = ['WindowsXP', 'WindowsServer2003']
        checkPaths = ['E:\\1212\\2761465\\WindowsXP' +
           '\\x64\\ENU\\IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE',
           'E:\\1212\\2761465\\WindowsServer2003' +
           '\\x64\\ENU\\IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE']

        for i in range(0, len(updates)):
            #self.assertEqual(checkPaths[i], updates[i]['Path'])
            print(updates[i]['Path'])
            self.assertEqual(2761465, updates[i]['KB'])
            self.assertEqual(versions[i], updates[i]['Version'])
            self.assertEqual('x64', updates[i]['Type'])
            self.assertEqual('ENU', updates[i]['Language'])
            self.assertEqual(datetime.datetime(2012, 12, 1),
                            updates[i]['Date'])
            self.assertEqual(checkPaths[i],
                                        core.updates.toWinDirStyle(updates[i]))

    def test_getKB(self):

        files = ['\\dotNetFW_4.X\\dotNetFx40_Full_x86_x64.exe']
        correctKBs = [-1]

        for KB, updateFile in zip(correctKBs, files):
            self.assertEqual(KB, core.updates.getKB(updateFile))


if __name__ == '__main__':

    unittest.main()
