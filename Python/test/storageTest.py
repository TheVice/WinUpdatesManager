import sys
import json
import db.sqliteDB
from datetime import datetime
from core.updates import Updates
from unittest import main, TestCase
from db.mongoDB import MongoDBClient
from test.jsonHelper import JsonHelper
from db.storage import Storage, Uif, SQLite, MongoDB, getStorage
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

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_getAvalibleVersions(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in testData['storages']:
                if 'Uif' == storageType:
                    with patch('db.storage.os.path.isfile'):
                        with patch('db.storage.os.path.exists'):
                            with patch('builtins.open') as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                versions = storage.getAvalibleVersions()
                                expectedVersions = testData['expectedVersions']
                                self.assertEqual(expectedVersions, versions)

                elif 'SQLite' == storageType:
                    updates = testData['updates']
                    dataBase = testData['sqliteDB']
                    tables = testData['tables']
                    dataBase = db.sqliteDB.connect(dataBase, False)
                    for table in tables:
                        if db.sqliteDB.isTableExist(dataBase, table):
                            db.sqliteDB.dropTable(dataBase, table)
                    SQLite.uif2SQLiteDB(dataBase.cursor(), updates)
                    dataBase.commit()

                    storage = SQLite(dataBase)
                    versions = storage.getAvalibleVersions()
                    expectedVersions = testData['expectedVersions']
                    self.assertEqual(expectedVersions, versions)

                    db.sqliteDB.disconnect(dataBase)

                elif 'MongoDB' == storageType:
                    updates = testData['updates']
                    MongoClient = testData['MongoClient']
                    dataBase = MongoClient['dataBase']
                    table = MongoClient['table']
                    HostAndPort = MongoClient['HostAndPort']
                    ServerSelectionTimeoutMS = MongoClient['ServerSelectionTimeoutMS']

                    client = MongoDBClient(HostAndPort, ServerSelectionTimeoutMS)
                    client.dropCollectionsInDB(dataBase, table)
                    MongoDB.uif2MongoDB(updates, dataBase, table, HostAndPort)

                    storage = MongoDB(HostAndPort, dataBase, table)
                    versions = storage.getAvalibleVersions()
                    expectedVersions = testData['expectedVersions']
                    self.assertEqual(expectedVersions, versions)

                    for i in range(0, len(updates)):
                        del updates[i]['_id']
                        d = updates[i]['Date']
                        updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)

                    testData['updates'] = updates

                else:
                    storage = Storage(storageType)
                    storage.getAvalibleVersions()

    def test_getAvalibleTypes(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in testData['storages']:
                if 'Uif' == storageType:
                    with patch('db.storage.os.path.isfile'):
                        with patch('db.storage.os.path.exists'):
                            with patch('builtins.open') as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                types = storage.getAvalibleTypes()
                                expectedTypes = testData['expectedTypes']
                                self.assertEqual(expectedTypes, types)

                elif 'SQLite' == storageType:
                    updates = testData['updates']
                    dataBase = testData['sqliteDB']
                    tables = testData['tables']
                    dataBase = db.sqliteDB.connect(dataBase, False)
                    for table in tables:
                        if db.sqliteDB.isTableExist(dataBase, table):
                            db.sqliteDB.dropTable(dataBase, table)
                    SQLite.uif2SQLiteDB(dataBase.cursor(), updates)
                    dataBase.commit()

                    storage = SQLite(dataBase)
                    types = storage.getAvalibleTypes()
                    expectedTypes = testData['expectedTypes']
                    self.assertEqual(expectedTypes, types)

                    db.sqliteDB.disconnect(dataBase)

                elif 'MongoDB' == storageType:
                    updates = testData['updates']
                    MongoClient = testData['MongoClient']
                    dataBase = MongoClient['dataBase']
                    table = MongoClient['table']
                    HostAndPort = MongoClient['HostAndPort']
                    ServerSelectionTimeoutMS = MongoClient['ServerSelectionTimeoutMS']

                    client = MongoDBClient(HostAndPort, ServerSelectionTimeoutMS)
                    client.dropCollectionsInDB(dataBase, table)
                    MongoDB.uif2MongoDB(updates, dataBase, table, HostAndPort)

                    storage = MongoDB(HostAndPort, dataBase, table)
                    types = storage.getAvalibleTypes()
                    expectedTypes = testData['expectedTypes']
                    self.assertEqual(expectedTypes, types)

                    for i in range(0, len(updates)):
                        del updates[i]['_id']
                        d = updates[i]['Date']
                        updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)

                    testData['updates'] = updates

                else:
                    storage = Storage(storageType)
                    storage.getAvalibleTypes()

    def test_getAvalibleLanguages(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in testData['storages']:
                if 'Uif' == storageType:
                    with patch('db.storage.os.path.isfile'):
                        with patch('db.storage.os.path.exists'):
                            with patch('builtins.open') as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                languages = storage.getAvalibleLanguages()
                                expectedLanguages = testData['expectedLanguages']
                                self.assertEqual(expectedLanguages, languages)

                elif 'SQLite' == storageType:
                    updates = testData['updates']
                    dataBase = testData['sqliteDB']
                    tables = testData['tables']
                    dataBase = db.sqliteDB.connect(dataBase, False)
                    for table in tables:
                        if db.sqliteDB.isTableExist(dataBase, table):
                            db.sqliteDB.dropTable(dataBase, table)
                    SQLite.uif2SQLiteDB(dataBase.cursor(), updates)
                    dataBase.commit()

                    storage = SQLite(dataBase)
                    languages = storage.getAvalibleLanguages()
                    expectedLanguages = testData['expectedLanguages']
                    self.assertEqual(expectedLanguages, languages)

                    db.sqliteDB.disconnect(dataBase)

                elif 'MongoDB' == storageType:
                    updates = testData['updates']
                    MongoClient = testData['MongoClient']
                    dataBase = MongoClient['dataBase']
                    table = MongoClient['table']
                    HostAndPort = MongoClient['HostAndPort']
                    ServerSelectionTimeoutMS = MongoClient['ServerSelectionTimeoutMS']

                    client = MongoDBClient(HostAndPort, ServerSelectionTimeoutMS)
                    client.dropCollectionsInDB(dataBase, table)
                    MongoDB.uif2MongoDB(updates, dataBase, table, HostAndPort)

                    storage = MongoDB(HostAndPort, dataBase, table)
                    languages = storage.getAvalibleLanguages()
                    expectedLanguages = testData['expectedLanguages']
                    self.assertEqual(expectedLanguages, languages)

                    for i in range(0, len(updates)):
                        del updates[i]['_id']
                        d = updates[i]['Date']
                        updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)

                    testData['updates'] = updates

                else:
                    storage = Storage(storageType)
                    storage.getAvalibleLanguages()

    def test_get(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            for storageType in testData['storages']:
                if 'Uif' == storageType:
                    with patch('db.storage.os.path.isfile'):
                        with patch('db.storage.os.path.exists'):
                            with patch('builtins.open') as mock_open:
                                mock_open.return_value = MockFile(testData['updates'])

                                storage = getStorage('file.uif')
                                getQuery = testData['getQuery']
                                updates = storage.get(getQuery)
                                expectedUpdates = testData['expectedUpdates']
                                self.assertEqual(len(expectedUpdates), len(updates))
                                for i in range(0, len(updates)):
                                    d = updates[i]['Date']
                                    updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)
                                for up in expectedUpdates:
                                    self.assertTrue(up in updates)

                elif 'SQLite' == storageType:
                    updates = testData['updates']
                    dataBase = testData['sqliteDB']
                    tables = testData['tables']
                    dataBase = db.sqliteDB.connect(dataBase, False)
                    for table in tables:
                        if db.sqliteDB.isTableExist(dataBase, table):
                            db.sqliteDB.dropTable(dataBase, table)
                    SQLite.uif2SQLiteDB(dataBase.cursor(), updates)
                    dataBase.commit()

                    storage = SQLite(dataBase)
                    getQuery = testData['getQuery']
                    updates = storage.get(getQuery)
                    expectedUpdates = testData['expectedUpdates']
                    self.assertEqual(len(expectedUpdates), len(updates))
                    for i in range(0, len(updates)):
                        d = updates[i]['Date']
                        updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)
                    for up in expectedUpdates:
                        self.assertTrue(up in updates)

                    db.sqliteDB.disconnect(dataBase)

                elif 'MongoDB' == storageType:
                    updates = testData['updates']
                    MongoClient = testData['MongoClient']
                    dataBase = MongoClient['dataBase']
                    table = MongoClient['table']
                    HostAndPort = MongoClient['HostAndPort']
                    ServerSelectionTimeoutMS = MongoClient['ServerSelectionTimeoutMS']

                    client = MongoDBClient(HostAndPort, ServerSelectionTimeoutMS)
                    client.dropCollectionsInDB(dataBase, table)
                    MongoDB.uif2MongoDB(updates, dataBase, table, HostAndPort)

                    storage = MongoDB(HostAndPort, dataBase, table)
                    getQuery = testData['getQuery']
                    updates = storage.get(getQuery)
                    expectedUpdates = testData['expectedUpdates']
                    self.assertEqual(len(expectedUpdates), len(updates))
                    for i in range(0, len(updates)):
                        d = updates[i]['Date']
                        updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)
                        del updates[i]['_id']
                    for up in expectedUpdates:
                        self.assertTrue(up in updates)

                    testData['updates'] = updates

                else:
                    storage = Storage(storageType)
                    storage.get({})

    def test_uif2SQLiteDB(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            updates = testData['updates']
            dataBase = testData['sqliteDB']
            tables = testData['tables']

            dataBase = db.sqliteDB.connect(dataBase, False)

            for table in tables:
                if db.sqliteDB.isTableExist(dataBase, table):
                    db.sqliteDB.dropTable(dataBase, table)

            SQLite.uif2SQLiteDB(dataBase.cursor(), updates)
            dataBase.commit()
            db.sqliteDB.disconnect(dataBase)

    def test_uif2MongoDB(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            updates = testData['updates']
            MongoClient = testData['MongoClient']
            dataBase = MongoClient['dataBase']
            table = MongoClient['table']
            HostAndPort = MongoClient['HostAndPort']
            ServerSelectionTimeoutMS = MongoClient['ServerSelectionTimeoutMS']

            client = MongoDBClient(HostAndPort, ServerSelectionTimeoutMS)
            client.dropCollectionsInDB(dataBase, table)
            MongoDB.uif2MongoDB(updates, dataBase, table, HostAndPort)
            mongoDB_updates = client.getItemsFromDB(dataBase, table)
            self.assertEqual(len(updates), len(mongoDB_updates))
            for up in updates:
                self.assertTrue(up in mongoDB_updates)

    def test_getStorage(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            if testData[0] == '1.uif':
                with patch('db.storage.os.path.isfile'):
                    with patch('db.storage.os.path.exists'):
                        with patch('builtins.open'):
                            storageType = type(getStorage(testData[0]))
                            self.assertEqual(eval(testData[1]), storageType)
                            self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                            if 2 != sys.version_info[0]:
                                with patch('db.storage.sys.version_info') as mock_pyVer:
                                    mock_pyVer.__getitem__ = MagicMock(return_value=2)
                                    storageType = type(getStorage(testData[0]))
                                    self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'UIFs':
                with patch('db.storage.os.path.isdir'):
                    with patch('db.storage.os.path.exists'):
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)
                        self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                        if 2 != sys.version_info[0]:
                            with patch('db.storage.sys.version_info') as mock_pyVer:
                                mock_pyVer.__getitem__ = MagicMock(return_value=2)
                                storageType = type(getStorage(testData[0]))
                                self.assertEqual(eval(testData[1]), storageType)
            elif testData[0] == 'base.sqlite':
                with patch('db.storage.os.path.isfile'):
                    with patch('db.storage.os.path.exists'):
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)
                        self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                        if 2 != sys.version_info[0]:
                            with patch('db.storage.sys.version_info') as mock_pyVer:
                                mock_pyVer.__getitem__ = MagicMock(return_value=2)
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
                self.assertEqual(testData[1], '{}'.format(getStorage(testData[0])))
                if 2 != sys.version_info[0]:
                    with patch('db.storage.sys.version_info') as mock_pyVer:
                        mock_pyVer.__getitem__ = MagicMock(return_value=2)
                        storageType = type(getStorage(testData[0]))
                        self.assertEqual(eval(testData[1]), storageType)

    def test_getUpdatesFromFile(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('db.storage.os.path.isfile'):
                with patch('db.storage.os.path.exists'):
                    with patch('builtins.open') as mock_open:
                        mock_open.return_value = MockFile(testData['updates'])
                        try:
                            updates = Uif.getUpdatesFromFile(testData['fileName'])
                            for i in range(0, len(updates)):
                                d = updates[i]['Date']
                                updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)
                            expectedUpdates = testData['updates']
                            self.assertEqual(len(expectedUpdates), len(updates))
                            for update in expectedUpdates:
                                self.assertTrue(update in updates)
                        except:
                            self.assertEqual(testData['exception'], '{}'.format(sys.exc_info()[1]))

    def test_getUpdatesFromStorage(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            with patch('db.storage.os.path.isdir'):
                with patch('db.storage.os.path.exists'):
                    with patch('core.dirs.getSubDirectoryFiles') as mock_dir_files:
                        mock_dir_files.return_value = testData['files']
                        with patch('builtins.open') as mock_open:
                            mock_open.return_value = MockFile(testData['updates'])

                            updates = Uif.getUpdatesFromStorage(testData['path'])
                            for i in range(0, len(updates)):
                                d = updates[i]['Date']
                                updates[i]['Date'] = '{}, {}, {}'.format(d.year, d.month, d.day)
                            expectedUpdates = testData['updates']
                            self.assertEqual(len(expectedUpdates), len(updates))
                            for update in expectedUpdates:
                                self.assertTrue(update in updates)


if __name__ == '__main__':

    main()
