import os
import sys
import unittest
import core.dirs
if 2 == sys.version_info[0]:
    from mock import MagicMock
else:
    from unittest.mock import MagicMock
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        if 2 == sys.version_info[0]:
            self.mJsonHelper = JsonHelper(__file__.replace('.pyc', '.json'))
        else:
            self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))

    def test_getSubDirectoryFiles(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            mock_return_value = []
            osWalkArray = testData['mockData']

            for p in osWalkArray:
                mock_return_value.append((p['root'], p['dirs'], p['files']))

            osWalk = os.walk
            os.walk = MagicMock(return_value=mock_return_value)

            files = core.dirs.getSubDirectoryFiles(osWalkArray[0]['root'])

            os.walk = osWalk

            expectedFiles = testData['expectedFiles']
            self.assertEqual(expectedFiles, files)


if __name__ == '__main__':

    unittest.main()
