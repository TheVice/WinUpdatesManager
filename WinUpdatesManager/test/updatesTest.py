import unittest
import datetime
import core
import core.updates


class TestSequenceFunctions(unittest.TestCase):

    def test_UpdateClass(self):

        path = ('E:\\1212\\2761465\\WindowsServer2003' +
           '\\X64\\ENU\\IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE')

        update = core.updates.Update(path)

        self.assertEqual('E:\\', update.getRootOfFullName())
        self.assertEqual('1212\\2761465\\WindowsServer2003' +
                         '\\X64\\ENU\\', update.getPathWithOutRoot())
        self.assertEqual('IE7-WINDOWSSERVER2003.' +
                    'WINDOWSXP-KB2761465-X64-ENU.EXE', update.getShortName())
        self.assertEqual('2761465', core.updates.getKB(path))
        update.mKB = core.updates.getKB(path)
        self.assertEqual(['WindowsXP', 'WindowsServer2003'],
                          core.updates.getVersion(path))
        update.mVersion = core.updates.getVersion(path)[1]
        self.assertEqual('X64', core.updates.getOsType(path))
        update.mOsType = core.updates.getOsType(path)
        self.assertEqual('ENU', core.updates.getLanguage(path))
        update.mLanguage = core.updates.getLanguage(path)
        update.mDate = datetime.date(2012, 12, 1)
        self.assertEqual(path, update.toWinDirStyle())

        update = core.updates.Update('dotNetFx40_Full_x86_x64.exe')
        self.assertEqual('', update.getRootOfFullName())
        self.assertEqual('', update.getPathWithOutRoot())
        self.assertEqual('dotNetFx40_Full_x86_x64.exe', update.getShortName())
        self.assertEqual('dotNetFx40_Full_x86_x64.exe', update.toWinDirStyle())

        update = core.updates.Update('update')
        update.mDate = '1212'
        self.assertEqual('1212\update', update.toWinDirStyle())

    def test_getKB(self):

        files = ['\\dotNetFW_4.X\\dotNetFx40_Full_x86_x64.exe']
        correctKBs = ['UNKNOWN KB']

        for KB, update_file in zip(correctKBs, files):
            self.assertEqual(KB, core.updates.getKB(update_file))

    def test_getUpdatesSerriesSeparate(self):

        updates = ['someUpdate', 'someUpdate, UNKNOWN LANGUAGE']
        self.assertNotIn('UNKNOWN',
            core.updates.getUpdatesSerriesSeparate(updates, 'UNKNOWN'))

if __name__ == '__main__':

    unittest.main()
