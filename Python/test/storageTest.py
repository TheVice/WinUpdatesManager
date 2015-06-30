import sys
from unittest import main, TestCase
from test.jsonHelper import JsonHelper
from db.storage import Uif, SQLite, MongoDB, getStorage
if 2 == sys.version_info[0]:
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_getAvalibleVersions(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            pass

    def test_getAvalibleTypes(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            pass

    def test_getAvalibleLanguages(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            pass

    def test_get(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            pass
        # storage = db.storage.getStorage('mongodb://localhost:27017/')
        # self.assertLess(0, len(list(storage.get({}))))

    def test_uif2SQLiteDB(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            pass

    def test_uif2MongoDB(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            pass

    def test_getStorage(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            if testData[0] == '1.uif':
                with patch('db.storage.os.path.isfile'):
                    with patch('db.storage.os.path.exists'):
                        with patch('builtins.open'):
                            storageType = type(getStorage(testData[0]))
                            self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'UIFs':
                with patch('db.storage.os.path.isdir'):
                    with patch('db.storage.os.path.exists'):
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'base.sqlite':
                with patch('db.storage.os.path.isfile'):
                    with patch('db.storage.os.path.exists'):
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'wrong.File':
                with patch('db.storage.os.path.isfile'):
                    with self.assertRaises(OSError):
                        getStorage(testData[0])
            elif testData[0] == 'wrongFolder':
                with patch('db.storage.os.path.isdir'):
                    with self.assertRaises(OSError):
                        getStorage(testData[0])
            else:
                storageType = type(getStorage(testData[0]))
                self.assertEqual(eval(testData[1]), storageType)


if __name__ == '__main__':

    main()
