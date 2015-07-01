import sys
import json
import db.sqliteDB
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
                                    date = updates[i]['Date']
                                    updates[i]['Date'] = '{}, {}, {}'.format(date.year, date.month, date.day)
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
                        date = updates[i]['Date']
                        updates[i]['Date'] = '{}, {}, {}'.format(date.year, date.month, date.day)
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
                        date = updates[i]['Date']
                        updates[i]['Date'] = '{}, {}, {}'.format(date.year, date.month, date.day)
                        del updates[i]['_id']
                    for up in expectedUpdates:
                        self.assertTrue(up in updates)

                    testData['updates'] = updates

                else:
                    storage = Storage(storageType)
                    storage.get({})
                    storage.correctDate(None)

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
