import sys
import datetime
import db.sqliteDB
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))
        self.mDataBase = self.mJsonHelper.GetSting('Connection', 'dataBase')
        self.mConnection = db.sqliteDB.connect(self.mDataBase)
        self.assertNotEqual(None, self.mConnection)

        db.sqliteDB.createTableKBs(self.mConnection)
        db.sqliteDB.createTableDates(self.mConnection)
        db.sqliteDB.createTableVersions(self.mConnection)
        db.sqliteDB.createTableTypes(self.mConnection)
        db.sqliteDB.createTableLanguages(self.mConnection)
        db.sqliteDB.createTablePaths(self.mConnection)
        db.sqliteDB.createTableUpdates(self.mConnection)

    def tearDown(self):
        db.sqliteDB.disconnect(self.mConnection)

    def test_connect(self):
        self.assertNotEqual(None, db.sqliteDB.connect(self.mDataBase))

    def test_disconnect(self):
        connection = db.sqliteDB.connect(self.mDataBase)
        self.assertNotEqual(None, connection)
        db.sqliteDB.disconnect(connection)

    def test_writeToDataBase(self):
        db.sqliteDB.disconnect(self.mConnection)
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.mConnection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']

            db.sqliteDB.writeToDataBase(self.mConnection, writeStatement)

            readStatement = testData['readStatement']
            readResult = db.sqliteDB.readFromDataBase(self.mConnection, readStatement).fetchall()
            expectedReadResult = testData['expectedReadResult']
            for i in range(0, len(expectedReadResult)):
                expectedReadResult[i] = (expectedReadResult[i],)
            self.assertEqual(expectedReadResult, readResult)

            db.sqliteDB.disconnect(self.mConnection)

    def test_readFromDataBase(self):
        db.sqliteDB.disconnect(self.mConnection)
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.mConnection = db.sqliteDB.connect(self.mDataBase)

            expectedReadResult = testData['expectedReadResult']
            for i in range(0, len(expectedReadResult)):
                expectedReadResult[i] = (expectedReadResult[i],)

            readStatement = testData['readStatement']
            readResult = db.sqliteDB.readFromDataBase(self.mConnection, readStatement).fetchall()
            self.assertNotEqual(expectedReadResult, readResult)

            writeStatement = testData['writeStatement']
            db.sqliteDB.writeToDataBase(self.mConnection, writeStatement)
            readResult = db.sqliteDB.readFromDataBase(self.mConnection, readStatement).fetchall()
            self.assertEqual(expectedReadResult, readResult)

            db.sqliteDB.disconnect(self.mConnection)

    def test_insertInto(self):
    
        self.assertEqual(None, db.sqliteDB.getIDFrom(self.mConnection, 'KBs', 'id', 1))
        db.sqliteDB.insertInto(self.mConnection, 'KBs', 'id', 1)
        self.assertNotEqual(None, db.sqliteDB.getIDFrom(self.mConnection, 'KBs', 'id', 1))
    
    def test_getIDFrom(self):
    
        self.test_insertInto()
    
    # def test_getSomethingByIDFrom(self):
    
    def test_findTable(self):
    
        self.assertNotEqual(None, db.sqliteDB.findTable(self.mConnection, 'KBs'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.mConnection, 'Dates'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.mConnection, 'Versions'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.mConnection, 'Types'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.mConnection, 'Languages'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.mConnection, 'Paths'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.mConnection, 'Updates'))
    
    def test_listTables(self):
    
        self.assertEqual(['Dates', 'KBs', 'Languages', 'Paths', 'Types', 'Updates', 'Versions', 'sqlite_sequence'],
                         db.sqliteDB.listTables(self.mConnection))
    
    def test_getDateByID(self):
    
        self.assertEqual(None, db.sqliteDB.getDateByID(self.mConnection, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getDateByID(self.mConnection, 1))
    
    def test_getPathByID(self):
    
        self.assertEqual(None, db.sqliteDB.getPathByID(self.mConnection, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getPathByID(self.mConnection, 1))
    
    def test_getVersionByID(self):
    
        self.assertEqual(None, db.sqliteDB.getVersionByID(self.mConnection, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getVersionByID(self.mConnection, 1))
    
    def test_getTypeByID(self):
    
        self.assertEqual(None, db.sqliteDB.getTypeByID(self.mConnection, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getTypeByID(self.mConnection, 1))
    
    def test_getLanguageByID(self):
    
        self.assertEqual(None, db.sqliteDB.getLanguageByID(self.mConnection, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getLanguageByID(self.mConnection, 1))
    
    # def test_getSetSubstanceID(self):
    
    def test_addUpdate(self):
    
        update = self.mJsonHelper.GetDictionary('test_addUpdate', 'update')
        self.assertEqual([], db.sqliteDB.getUpdates(self.mConnection, update))
        db.sqliteDB.addUpdate(self.mConnection, update)
        updates = db.sqliteDB.getUpdates(self.mConnection, update)
        self.assertEqual([update], updates)
    
    # def test_rawUpdatesToUpdates(self):
    
    def test_getUpdates(self):
    
        self.assertEqual(0, len(db.sqliteDB.getUpdates(self.mConnection, {})))
        updates = self.mJsonHelper.GetArray('test_getUpdates', 'updates')
    
        db.sqliteDB.addUpdates(self.mConnection, updates)
    
        self.assertEqual(len(updates), len(db.sqliteDB.getUpdates(self.mConnection, {})))
    
        queryAndAnswer = self.mJsonHelper.GetArray('test_getUpdates', 'queryAndAnswer')
        for qa in queryAndAnswer:
            self.assertEqual(qa['answer'], len(db.sqliteDB.getUpdates(self.mConnection, qa['query'])))
    
    def test_getUpdatesByKBInPath(self):
    
        updates = self.mJsonHelper.GetArray('test_getUpdatesByKBInPath', 'updates')
    
        db.sqliteDB.addUpdates(self.mConnection, updates)
    
        queryAndAnswer = self.mJsonHelper.GetArray('test_getUpdatesByKBInPath', 'queryAndAnswer')
        for qa in queryAndAnswer:
            inputValue = list(qa.keys())[0]
            self.assertEqual(qa[inputValue], len(db.sqliteDB.getUpdatesByKBInPath(self.mConnection, inputValue)))


if __name__ == '__main__':

    main()
