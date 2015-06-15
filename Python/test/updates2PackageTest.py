import os
import sys
import unittest
import core.dirs
import updates2Package
from db.storage import Uif
from unittest.mock import MagicMock
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'updates2PackageTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_getPath(self):

        testsData = self.mJsonHelper.GetTestInputOutputData('test_getPath')
        for testInputOutput in testsData:
            try:
                upFile = updates2Package.UpFile(testInputOutput[0])
                self.assertEqual(testInputOutput[1], upFile.getPath())
            except Exception:
                self.assertEqual(testInputOutput[1], str(sys.exc_info()[1]))

    def test_moveUp(self):

        side_effect=[None, FileExistsError]

        osRenames = os.renames
        os.renames = MagicMock(side_effect=side_effect)

        for i in range(0, len(side_effect)):
            self.assertRaises(None, updates2Package.moveUp('source', 'destination'))

        os.renames = osRenames

    def test_moveFilesToNewLocations(self):

        updates2PackageMoveUp = updates2Package.moveUp
        updates2Package.moveUp = MagicMock(retur_value=None)

        paths = []
        testsData = self.mJsonHelper.GetTestInputOutputData('test_getPath')
        for testInputOutput in testsData:
            paths.append(testInputOutput[0])
        self.assertRaises(None, updates2Package.moveFilesToNewLocations(paths))

        updates2Package.moveUp = updates2PackageMoveUp

    def test_getFullPath2UnknownUpdatesAtFolder(self):

        files = []
        expectedPaths = []
        testsData = self.mJsonHelper.GetTestInputOutputData('test_getPath')
        for testInputOutput in testsData:
            files.append(testInputOutput[0])
            expectedPaths.append('A:\\{}'.format(testInputOutput[0]))

        osListDir = os.listdir
        os.listdir = MagicMock(return_value=files)
        osPathIsfile = os.path.isfile
        os.path.isfile = MagicMock(return_value=True)

        self.assertEqual(expectedPaths, updates2Package.getFullPath2UnknownUpdatesAtFolder('A:\\'))

        os.path.isfile = osPathIsfile
        os.listdir = osListDir

    def test_relPaths2Full(self):

        testsData = self.mJsonHelper.GetTestRoot('test_relPaths2Full')
        for testData in testsData:
            coreDirsGetSubDirectoryFiles = core.dirs.getSubDirectoryFiles
            core.dirs.getSubDirectoryFiles = MagicMock(return_value=testData['getSubDirectoryFiles'])

            paths = updates2Package.relPaths2Full(testData['RootPath'], testData['Paths'])
            self.assertEqual(testData['expectedPaths'], paths)

            core.dirs.getSubDirectoryFiles = coreDirsGetSubDirectoryFiles

    def test_getFullPath2UnknownUpdatesAtList(self):

        testsData = self.mJsonHelper.GetTestRoot('test_getFullPath2UnknownUpdatesAtList')
        for testData in testsData:
            UifGetUpdatesFromStorage = Uif.getUpdatesFromStorage
            Uif.getUpdatesFromStorage = MagicMock(return_value=testData['updates'])

            coreDirsGetSubDirectoryFiles = core.dirs.getSubDirectoryFiles
            core.dirs.getSubDirectoryFiles = MagicMock(return_value=testData['getSubDirectoryFiles'])

            paths = updates2Package.getFullPath2UnknownUpdatesAtList(None, testData['RootPath'])
            self.assertEqual(testData['expectedPaths'], paths)

            core.dirs.getSubDirectoryFiles = coreDirsGetSubDirectoryFiles
            Uif.getUpdatesFromStorage = UifGetUpdatesFromStorage


if __name__ == '__main__':

    unittest.main()
