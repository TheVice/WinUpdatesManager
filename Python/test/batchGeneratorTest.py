import os
import unittest
import batchGenerator


class TestSequenceFunctions(unittest.TestCase):

    def test_batchTemplate(self):
        ref = (':UP2' +
              os.linesep +
              'IF NOT EXIST "1.txt" GOTO N2' +
              os.linesep +
              os.linesep +
              'echo Installing 1.txt UP2' +
              os.linesep +
              'copy "1.txt" "%TEMP%\\1.txt" /Y' +
              os.linesep +
              '"%TEMP%\\1.txt" /quit' +
              os.linesep +
              'GOTO Y2' +
              os.linesep +
              os.linesep +
              ':N2' +
              os.linesep +
              'echo File 1.txt not present.' +
              os.linesep +
              'echo Please change media and press any key...' +
              os.linesep +
              'PAUSE > nul:' +
              os.linesep +
              'GOTO UP2' +
              os.linesep +
              ':Y2' +
              os.linesep)
        self.assertEqual(ref,
            batchGenerator.batchTemplate('1.txt', str(2), ' /quit'))

    def test_generate(self):
        ref = ('@echo off' +
              os.linesep +
              'if [%1] == [] GOTO UP1' +
              os.linesep +
              'GOTO %1' +
              os.linesep +
              os.linesep +
              ':UP1' +
              os.linesep +
              'IF NOT EXIST "update.exe" GOTO N1' +
              os.linesep +
              os.linesep +
              'echo Installing update.exe UP1' +
              os.linesep +
              'copy "update.exe" "%TEMP%\\update.exe" /Y' +
              os.linesep +
              '"%TEMP%\\update.exe" /quit /nobackup' +
              os.linesep +
              'GOTO Y1' +
              os.linesep +
              os.linesep +
              ':N1' +
              os.linesep +
              'echo File update.exe not present.' +
              os.linesep +
              'echo Please change media and press any key...' +
              os.linesep +
              'PAUSE > nul:' +
              os.linesep +
              'GOTO UP1' +
              os.linesep +
              ':Y1' +
              os.linesep)
        self.assertEqual(ref,
            batchGenerator.generate(['update.exe'], None, ' /quit /nobackup'))
 
        ref = ('@echo off' +
              os.linesep +
              'if [%1] == [] GOTO UP1' +
              os.linesep +
              'GOTO %1' +
              os.linesep +
              os.linesep +
              ':UP1' +
              os.linesep +
              'IF NOT EXIST "Z:' + os.sep + 'update.exe" GOTO N1' +
              os.linesep +
              os.linesep +
              'echo Installing Z:' + os.sep + 'update.exe UP1' +
              os.linesep +
              'copy "Z:\\update.exe" "%TEMP%\\update.exe" /Y' +
              os.linesep +
              '"%TEMP%\\update.exe" /quit /nobackup' +
              os.linesep +
              'GOTO Y1' +
              os.linesep +
              os.linesep +
              ':N1' +
              os.linesep +
              'echo File Z:' + os.sep + 'update.exe not present.' +
              os.linesep +
              'echo Please change media and press any key...' +
              os.linesep +
              'PAUSE > nul:' +
              os.linesep +
              'GOTO UP1' +
              os.linesep +
              ':Y1' +
              os.linesep)
        self.assertEqual(ref,
            batchGenerator.generate(['update.exe'], 'Z:' + os.sep,
                                    ' /quit /nobackup'))

if __name__ == '__main__':
    unittest.main()
