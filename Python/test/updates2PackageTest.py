import sys
import updates2Package
if 2 == sys.version_info[0]:
    from mock import patch
else:
    from unittest.mock import patch
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):

        self.mJsonHelper = JsonHelper(__file__)

    def test_getPath(self):

        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            try:
                upFile = updates2Package.UpFile(testData[0])
                self.assertEqual(testData[1], upFile.getPath())
            except Exception:
                self.assertEqual(testData[1], '{}'.format(sys.exc_info()[1]))

    def test_moveUp(self):

        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:

            if testData[0] == 'FileExistsError' and 2 == sys.version_info[0]:
                continue
            elif testData[0] == 'OSError' and 2 != sys.version_info[0]:
                continue

            with patch('updates2Package.os.renames') as mock_rename:
                mock_rename.side_effect=eval(testData[0])
                with patch('sys.stdout') as mock_stdout:
                    updates2Package.moveUp(testData[1]['source'], testData[1]['destination'])
                    result = []
                    for i in mock_stdout.method_calls:
                        result.append(i[1][0])

                    self.assertEqual(testData[1]['expectedResult'], result)

    def test_moveFilesToNewLocations(self):

        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('updates2Package.moveUp'):
                with patch('sys.stdout') as mock_stdout:
                    updates2Package.moveFilesToNewLocations([testData[0]])
                    result = []
                    for i in mock_stdout.method_calls:
                        result.append(i[1][0])

                    self.assertEqual(testData[1], result)

    def test_getFullPath2UnknownUpdatesAtFolder(self):

        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('updates2Package.os.listdir') as mock_listdir:
                mock_listdir.return_value=[testData[0]]
                with patch('updates2Package.os.path.isfile') as mock_isfile:
                    mock_isfile.return_value=True

                    rootPath = self.mJsonHelper.GetTestRoot('rootPath')
                    self.assertEqual([testData[1]], updates2Package.getFullPath2UnknownUpdatesAtFolder(rootPath))

    def test_relPaths2Full(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('updates2Package.core.dirs.getSubDirectoryFiles') as mock_subDirectoryFiles:
                mock_subDirectoryFiles.return_value=testData['getSubDirectoryFiles']

                paths = updates2Package.relPaths2Full(testData['RootPath'], testData['Paths'])
                self.assertEqual(testData['expectedPaths'], paths)

    def test_getFullPath2UnknownUpdatesAtList(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('updates2Package.Uif.getUpdatesFromStorage') as mock_updatesFromStorage:
                mock_updatesFromStorage.return_value=testData['updates']
                with patch('updates2Package.core.dirs.getSubDirectoryFiles') as mock_subDirectoryFiles:
                    mock_subDirectoryFiles.return_value=testData['getSubDirectoryFiles']

                    paths = updates2Package.getFullPath2UnknownUpdatesAtList(None, testData['RootPath'])
                    self.assertEqual(testData['expectedPaths'], paths)


if __name__ == '__main__':

    main()
