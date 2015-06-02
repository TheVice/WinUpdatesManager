import os
import unittest
import core.dirs
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'dirsTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_Paths(self):

        inputPaths = self.mJsonHelper.GetStingArray('test_Paths', 'inputPaths')
        correctRootPaths = self.mJsonHelper.GetStingArray('test_Paths', 'correctRootPaths')
        correctRootObjects = self.mJsonHelper.GetStingArray('test_Paths', 'correctRootObjects')

        paths = core.dirs.Paths(inputPaths)

        self.assertEqual(inputPaths, paths.getFullPaths())
        self.assertEqual(correctRootPaths, paths.getRootPaths())
        self.assertEqual(correctRootObjects, paths.getRootObjects())

    def test_getRootPaths(self):

        paths = self.mJsonHelper.GetStingArray('test_getRootPaths', 'paths')
        correctRootPaths = self.mJsonHelper.GetStingArray('test_getRootPaths', 'correctRootPaths')

        rootPaths = core.dirs.getRootPaths(paths)

        for correctPath, path in zip(correctRootPaths, rootPaths):
            self.assertEqual(correctPath, path)

    def test_getRootObjects(self):

        paths = self.mJsonHelper.GetStingArray('test_getRootObjects', 'paths')
        correctRootObjects = self.mJsonHelper.GetStingArray('test_getRootObjects', 'correctRootObjects')

        rootObjects = core.dirs.getRootObjects(paths)

        for correctPath, path in zip(correctRootObjects, rootObjects):
            self.assertEqual(correctPath, path)


if __name__ == '__main__':

    unittest.main()
