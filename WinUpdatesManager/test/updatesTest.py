import unittest
import core
import core.updates


class TestSequenceFunctions(unittest.TestCase):

    def test_getKB(self):

        files = ['\\dotNetFW_4.X\\dotNetFx40_Full_x86_x64.exe']
        correctAnswer = ['UNKNOWN KB']

        i = 0
        for update_file in files:
            self.assertEqual(correctAnswer[i], core.updates.getKB(update_file))
            i += 1

#def getVersion(aPath):
#def getType(aPath):
#def getLanguage(aPath):
#def getUpdatesInfoFromPackage(aFiles, aStyle=0):
#def getKBsFromReport(aReport):
#def updateInfoInJSON(aFileName, aKB, aVersion, aType, aLanguage):
#def updateInfoInDirStyle(aFileName, aKB, aVersion, aType, aLanguage):
#def checkIsThisR2(aVersion, aFileName):
#def checkIsThisARM(aVersion, aType):
#...
#def getUpdatesFromPackage

    def test_getUpdatesSerriesSeparate(self):

        updates = ['someUpdate', 'someUpdate, UNKNOWN LANGUAGE']
        self.assertNotIn('UNKNOWN',
            core.updates.getUpdatesSerriesSeparate(updates, 'UNKNOWN'))

if __name__ == '__main__':

    unittest.main()
