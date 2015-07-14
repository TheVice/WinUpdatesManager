import sys
import core.dirs
if 2 == sys.version_info[0]:
    from mock import patch
else:
    from unittest.mock import patch
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_getSubDirectoryFiles(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            mock_return_value = []
            osWalkArray = testData['mockData']

            for p in osWalkArray:
                mock_return_value.append((p['root'], p['dirs'], p['files']))

            with patch('core.dirs.os.walk') as mock_walk:
                mock_walk.return_value=mock_return_value

                files = core.dirs.getSubDirectoryFiles(osWalkArray[0]['root'])

                expectedFiles = testData['expectedFiles']
                self.assertEqual(expectedFiles, files)


if __name__ == '__main__':

    main()
