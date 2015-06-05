import os
import unittest
import core.dirs
from unittest.mock import MagicMock
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'dirsTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_getSubDirectoryFiles(self):

        data = self.mJsonHelper.GetTestRoot('test_getSubDirectoryFiles')
        for d in data:
            mock_return_value = []
            osWalkArray = d['mockData']

            for p in osWalkArray:
                mock_return_value.append((p['root'], p['dirs'], p['files']))

            os.walk = MagicMock(return_value=mock_return_value )

            files = core.dirs.getSubDirectoryFiles(osWalkArray[0]['root'])

            expectedFiles = d['expectedFiles']
            self.assertEqual(expectedFiles, files)

if __name__ == '__main__':

    unittest.main()
