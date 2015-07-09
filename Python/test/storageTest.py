import sys
import json
import core.dates
import db.sqliteDB
from datetime import datetime, date
from core.updates import Updates
from unittest import main, TestCase
from db.mongoDB import MongoDBClient
from test.jsonHelper import JsonHelper
from core.storage import Storage, Uif, SQLite, MongoDB, getStorage
if 2 == sys.version_info[0]:
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock


class MockFile(Updates):

    def __init__(self, aData):

        self.mData = []
        for d in aData:
            self.mData.append(json.dumps(d))
        self.mIndex = len(self.mData)

    @staticmethod
    def close():
        pass


class TestSequenceFunctions(TestCase):

    storages = ['Uif', 'SQLite', 'MongoDB', 'Storage']

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

        if 'SQLite' in TestSequenceFunctions.storages:
            dataBase = self.mJsonHelper.GetTestRoot('sqliteDB')['fileName']
            tables = self.mJsonHelper.GetTestRoot('sqliteDB')['tables']
            self.mSqliteDB = db.sqliteDB.connect(dataBase, False)
            for table in tables:
                if db.sqliteDB.isTableExist(self.mSqliteDB, table):
                    db.sqliteDB.dropTable(self.mSqliteDB, table)

        if 'MongoDB' in TestSequenceFunctions.storages:
            self.mMongoDataBase = self.mJsonHelper.GetTestRoot('MongoClient')['dataBase']
            self.mMongoTable = self.mJsonHelper.GetTestRoot('MongoClient')['table']
            self.mMongoHostAndPort = self.mJsonHelper.GetTestRoot('MongoClient')['HostAndPort']
            ServerSelectionTimeoutMS = self.mJsonHelper.GetTestRoot('MongoClient')['ServerSelectionTimeoutMS']
            self.mMongoDB = MongoDBClient(self.mMongoHostAndPort, ServerSelectionTimeoutMS)
            self.mMongoDB.dropCollectionsInDB(self.mMongoDataBase, self.mMongoTable)

    def tearDown(self):
        if 'SQLite' in TestSequenceFunctions.storages:
            db.sqliteDB.disconnect(self.mSqliteDB)

    def test_getAvalibleVersions(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in TestSequenceFunctions.storages:
                if 'Uif' == storageType:
                    with patch('core.storage.os.path.isfile'):
                        with patch('core.storage.os.path.exists'):
                            patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                            with patch(patchName) as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                versions = storage.getAvalibleVersions()
                                expectedVersions = testData['expectedVersions']
                                self.assertEqual(expectedVersions, versions)

                elif 'SQLite' == storageType:
                    SQLite.uif2SQLiteDB(self.mSqliteDB.cursor(), testData['updates'])
                    self.mSqliteDB.commit()

                    storage = SQLite(self.mSqliteDB)
                    versions = storage.getAvalibleVersions()
                    expectedVersions = testData['expectedVersions']
                    self.assertEqual(expectedVersions, versions)

                elif 'MongoDB' == storageType:
                    MongoDB.uif2MongoDB(testData['updates'], self.mMongoDataBase,
                                        self.mMongoTable, self.mMongoHostAndPort)

                    storage = MongoDB(self.mMongoHostAndPort, self.mMongoDataBase, self.mMongoTable)
                    versions = storage.getAvalibleVersions()
                    expectedVersions = testData['expectedVersions']
                    self.assertEqual(expectedVersions, versions)

                else:
                    storage = Storage(storageType)
                    storage.getAvalibleVersions()

    def test_getAvalibleTypes(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in TestSequenceFunctions.storages:
                if 'Uif' == storageType:
                    with patch('core.storage.os.path.isfile'):
                        with patch('core.storage.os.path.exists'):
                            patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                            with patch(patchName) as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                types = storage.getAvalibleTypes()
                                expectedTypes = testData['expectedTypes']
                                self.assertEqual(expectedTypes, types)

                elif 'SQLite' == storageType:
                    SQLite.uif2SQLiteDB(self.mSqliteDB.cursor(), testData['updates'])
                    self.mSqliteDB.commit()

                    storage = SQLite(self.mSqliteDB)
                    types = storage.getAvalibleTypes()
                    expectedTypes = testData['expectedTypes']
                    self.assertEqual(expectedTypes, types)

                elif 'MongoDB' == storageType:
                    MongoDB.uif2MongoDB(testData['updates'], self.mMongoDataBase,
                                        self.mMongoTable, self.mMongoHostAndPort)

                    storage = MongoDB(self.mMongoHostAndPort, self.mMongoDataBase, self.mMongoTable)
                    types = storage.getAvalibleTypes()
                    expectedTypes = testData['expectedTypes']
                    self.assertEqual(expectedTypes, types)

                else:
                    storage = Storage(storageType)
                    storage.getAvalibleTypes()

    def test_getAvalibleLanguages(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in TestSequenceFunctions.storages:
                if 'Uif' == storageType:
                    with patch('core.storage.os.path.isfile'):
                        with patch('core.storage.os.path.exists'):
                            patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                            with patch(patchName) as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                languages = storage.getAvalibleLanguages()
                                expectedLanguages = testData['expectedLanguages']
                                self.assertEqual(expectedLanguages, languages)

                elif 'SQLite' == storageType:
                    SQLite.uif2SQLiteDB(self.mSqliteDB.cursor(), testData['updates'])
                    self.mSqliteDB.commit()

                    storage = SQLite(self.mSqliteDB)
                    languages = storage.getAvalibleLanguages()
                    expectedLanguages = testData['expectedLanguages']
                    self.assertEqual(expectedLanguages, languages)

                elif 'MongoDB' == storageType:
                    MongoDB.uif2MongoDB(testData['updates'], self.mMongoDataBase,
                                        self.mMongoTable, self.mMongoHostAndPort)

                    storage = MongoDB(self.mMongoHostAndPort, self.mMongoDataBase, self.mMongoTable)
                    languages = storage.getAvalibleLanguages()
                    expectedLanguages = testData['expectedLanguages']
                    self.assertEqual(expectedLanguages, languages)

                else:
                    storage = Storage(storageType)
                    storage.getAvalibleLanguages()

    def test_get(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in TestSequenceFunctions.storages:
                self.tearDown()
                self.setUp()
                if 'Uif' == storageType:
                    with patch('core.storage.os.path.isfile'):
                        with patch('core.storage.os.path.exists'):
                            patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                            with patch(patchName) as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                getQuery = testData['getQuery']
                                limit = testData['limit']
                                skip = testData['skip']
                                sort = testData['sort']
                                try:
                                    updates = storage.get(getQuery, limit, skip, sort)
                                    for i in range(0, len(updates)):
                                        self.assertTrue(isinstance(updates[i]['Date'], date))
                                        updates[i]['Date'] = core.dates.toString(updates[i]['Date'])
                                    expectedUpdates = testData['expectedUpdates']

                                    if sort:
                                        self.assertEqual(expectedUpdates, updates)
                                    else:
                                        self.assertEqual(len(expectedUpdates), len(updates))
                                        for up in expectedUpdates:
                                            self.assertTrue(up in updates)
                                except:
                                    self.assertEqual(testData['expectedUpdates'], '{}'.format(sys.exc_info()[1]))

                elif 'SQLite' == storageType:
                    SQLite.uif2SQLiteDB(self.mSqliteDB.cursor(), testData['updates'])
                    self.mSqliteDB.commit()

                    storage = SQLite(self.mSqliteDB)
                    getQuery = testData['getQuery']
                    limit = testData['limit']
                    skip = testData['skip']
                    sort = testData['sort']
                    try:
                        updates = storage.get(getQuery, limit, skip, sort)
                        for i in range(0, len(updates)):
                            self.assertTrue(isinstance(updates[i]['Date'], date))
                            updates[i]['Date'] = core.dates.toString(updates[i]['Date'])
                        expectedUpdates = testData['expectedUpdates']

                        if sort:
                            self.assertEqual(expectedUpdates, updates)
                        else:
                            self.assertEqual(len(expectedUpdates), len(updates))
                            for up in expectedUpdates:
                                self.assertTrue(up in updates)
                    except:
                        self.assertEqual(testData['expectedUpdates'], '{}'.format(sys.exc_info()[1]))

                elif 'MongoDB' == storageType:
                    MongoDB.uif2MongoDB(testData['updates'], self.mMongoDataBase,
                                        self.mMongoTable, self.mMongoHostAndPort)

                    storage = MongoDB(self.mMongoHostAndPort, self.mMongoDataBase, self.mMongoTable)
                    getQuery = testData['getQuery']
                    limit = testData['limit']
                    skip = testData['skip']
                    sort = testData['sort']
                    try:
                        updates = storage.get(getQuery, limit, skip, sort)
                        for i in range(0, len(updates)):
                            self.assertTrue(isinstance(updates[i]['Date'], datetime))
                            updates[i]['Date'] = core.dates.toString(updates[i]['Date'])
                        expectedUpdates = testData['expectedUpdates']
                        if sort:
                            self.assertEqual(expectedUpdates, updates)
                        else:
                            self.assertEqual(len(expectedUpdates), len(updates))
                            for up in expectedUpdates:
                                self.assertTrue(up in updates)
                    except:
                        self.assertEqual(testData['expectedUpdates'], '{}'.format(sys.exc_info()[1]))

                else:
                    storage = Storage(storageType)
                    storage.get({})

    def test_getCount(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in TestSequenceFunctions.storages:
                self.tearDown()
                self.setUp()
                if 'Uif' == storageType:
                    with patch('core.storage.os.path.isfile'):
                        with patch('core.storage.os.path.exists'):
                            patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                            with patch(patchName) as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                getQuery = testData['getQuery']
                                try:
                                    count = storage.getCount(getQuery)
                                    expectedCount = testData['expectedCount']
                                    self.assertEqual(expectedCount, count)
                                except:
                                    self.assertEqual(testData['expectedCount'], '{}'.format(sys.exc_info()[1]))

                elif 'SQLite' == storageType:
                    SQLite.uif2SQLiteDB(self.mSqliteDB.cursor(), testData['updates'])
                    self.mSqliteDB.commit()

                    storage = SQLite(self.mSqliteDB)
                    getQuery = testData['getQuery']
                    try:
                        count = storage.getCount(getQuery)
                        expectedCount = testData['expectedCount']
                        self.assertEqual(expectedCount, count)
                    except:
                        self.assertEqual(testData['expectedCount'], '{}'.format(sys.exc_info()[1]))

                elif 'MongoDB' == storageType:
                    MongoDB.uif2MongoDB(testData['updates'], self.mMongoDataBase,
                                        self.mMongoTable, self.mMongoHostAndPort)

                    storage = MongoDB(self.mMongoHostAndPort, self.mMongoDataBase, self.mMongoTable)
                    getQuery = testData['getQuery']
                    try:
                        count = storage.getCount(getQuery)
                        expectedCount = testData['expectedCount']
                        self.assertEqual(expectedCount, count)
                    except:
                        self.assertEqual(testData['expectedCount'], '{}'.format(sys.exc_info()[1]))

                else:
                    storage = Storage(storageType)
                    storage.getCount({})

    def test_uif2SQLiteDB(self):
        if 'SQLite' not in TestSequenceFunctions.storages:
            return
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            SQLite.uif2SQLiteDB(self.mSqliteDB.cursor(), testData['updates'])
            self.mSqliteDB.commit()

            storage = SQLite(self.mSqliteDB)
            updates = storage.get({})
            for i in range(0, len(updates)):
                updates[i]['Date'] = core.dates.toString(updates[i]['Date'])
            self.assertEqual(testData['updates'], updates)

    def test_uif2MongoDB(self):
        if 'MongoDB' not in TestSequenceFunctions.storages:
            return
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            MongoDB.uif2MongoDB(testData['updates'], self.mMongoDataBase,
                                self.mMongoTable, self.mMongoHostAndPort)

            storage = MongoDB(self.mMongoHostAndPort, self.mMongoDataBase, self.mMongoTable)
            updates = storage.get({})
            for i in range(0, len(updates)):
                updates[i]['Date'] = core.dates.toString(updates[i]['Date'])
            for i in range(0, len(testData['updates'])):
                testData['updates'][i]['Date'] = core.dates.toString(testData['updates'][i]['Date'])
                del testData['updates'][i]['_id']

            self.assertEqual(len(testData['updates']), len(updates))
            for up in testData['updates']:
                self.assertTrue(up in updates)

    def test_getStorage(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            if testData[0] == '1.uif':
                with patch('core.storage.os.path.isfile'):
                    with patch('core.storage.os.path.exists'):
                        patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                        with patch(patchName):
                            storageType = type(getStorage(testData[0]))
                            self.assertEqual(eval(testData[1]), storageType)
                            self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                            if 2 != sys.version_info[0]:
                                with patch('core.storage.sys.version_info') as mock_pyVer:
                                    mock_pyVer.__getitem__ = MagicMock(return_value=2)
                                    storageType = type(getStorage(testData[0]))
                                    self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'UIFs':
                with patch('core.storage.os.path.isdir'):
                    with patch('core.storage.os.path.exists'):
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)
                        self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                        if 2 != sys.version_info[0]:
                            with patch('core.storage.sys.version_info') as mock_pyVer:
                                mock_pyVer.__getitem__ = MagicMock(return_value=2)
                                storageType = type(getStorage(testData[0]))
                                self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'base.sqlite':
                with patch('core.storage.os.path.isfile'):
                    with patch('core.storage.os.path.exists'):
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)
                        self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                        if 2 != sys.version_info[0]:
                            with patch('core.storage.sys.version_info') as mock_pyVer:
                                mock_pyVer.__getitem__ = MagicMock(return_value=2)
                                storageType = type(getStorage(testData[0]))
                                self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'wrong.File':
                with patch('core.storage.os.path.isfile'):
                    with self.assertRaises(OSError):
                        getStorage(testData[0])
            elif testData[0] == 'wrongFolder':
                with patch('core.storage.os.path.isdir'):
                    with self.assertRaises(OSError):
                        getStorage(testData[0])
            else:
                storageType = type(getStorage(testData[0]))
                self.assertEqual(eval(testData[1]), storageType)
                self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                if 2 != sys.version_info[0]:
                    with patch('core.storage.sys.version_info') as mock_pyVer:
                        mock_pyVer.__getitem__ = MagicMock(return_value=2)
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)

    def test_getUpdatesFromFile(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('core.storage.os.path.isfile'):
                with patch('core.storage.os.path.exists'):
                    patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                    with patch(patchName) as mock_open:
                        mock_open.return_value = MockFile(testData['updates'])
                        try:
                            updates = Uif.getUpdatesFromFile(testData['fileName'])
                            for i in range(0, len(updates)):
                                updates[i]['Date'] = core.dates.toString(updates[i]['Date'])
                            expectedUpdates = testData['updates']
                            self.assertEqual(len(expectedUpdates), len(updates))
                            for update in expectedUpdates:
                                self.assertTrue(update in updates)
                        except:
                            self.assertEqual(testData['exception'], '{}'.format(sys.exc_info()[1]))

    def test_getUpdatesFromStorage(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('core.storage.os.path.isdir'):
                with patch('core.storage.os.path.exists'):
                    with patch('core.dirs.getSubDirectoryFiles') as mock_dir_files:
                        mock_dir_files.return_value = testData['files']
                        patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                        with patch(patchName) as mock_open:
                            mock_open.return_value = MockFile(testData['updates'])

                            updates = Uif.getUpdatesFromStorage(testData['path'])
                            for i in range(0, len(updates)):
                                updates[i]['Date'] = core.dates.toString(updates[i]['Date'])
                            expectedUpdates = testData['updates']
                            self.assertEqual(len(expectedUpdates), len(updates))
                            for update in expectedUpdates:
                                self.assertTrue(update in updates)


if __name__ == '__main__':

    main()
