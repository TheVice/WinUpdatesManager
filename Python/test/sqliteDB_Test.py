import os
import unittest
import datetime
import db.sqliteDB
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'sqliteDB_Test.json')
        self.mJsonHelper = JsonHelper(path)
        self.dataBase = db.sqliteDB.connect(':memory:')
        self.assertNotEqual(None, self.dataBase)

        db.sqliteDB.createTableKBs(self.dataBase)
        db.sqliteDB.createTableDates(self.dataBase)
        db.sqliteDB.createTableVersions(self.dataBase)
        db.sqliteDB.createTableTypes(self.dataBase)
        db.sqliteDB.createTableLanguages(self.dataBase)
        db.sqliteDB.createTablePaths(self.dataBase)
        db.sqliteDB.createTableUpdates(self.dataBase)

    def tearDown(self):

        db.sqliteDB.disconnect(self.dataBase)

    def test_connect(self):

        pass # see setUp

    def test_disconnect(self):

        pass # see tearDown

    def test_insertInto(self):

        self.assertEqual(None, db.sqliteDB.getIDFrom(self.dataBase, 'KBs', 'id', 1))
        db.sqliteDB.insertInto(self.dataBase, 'KBs', 'id', 1)
        self.assertNotEqual(None, db.sqliteDB.getIDFrom(self.dataBase, 'KBs', 'id', 1))

    def test_getIDFrom(self):

        self.test_insertInto()

    # def test_getSomethingByIDFrom(self):

    def test_findTable(self):

        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'KBs'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'Dates'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'Versions'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'Types'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'Languages'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'Paths'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'Updates'))

    def test_listTables(self):

        self.assertEqual(['Dates', 'KBs', 'Languages', 'Paths', 'Types', 'Updates', 'Versions', 'sqlite_sequence'],
                         db.sqliteDB.listTables(self.dataBase))

    def test_getDateByID(self):

        self.assertEqual(None, db.sqliteDB.getDateByID(self.dataBase, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getDateByID(self.dataBase, 1))

    def test_getPathByID(self):

        self.assertEqual(None, db.sqliteDB.getPathByID(self.dataBase, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getPathByID(self.dataBase, 1))

    def test_getVersionByID(self):

        self.assertEqual(None, db.sqliteDB.getVersionByID(self.dataBase, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getVersionByID(self.dataBase, 1))

    def test_getTypeByID(self):

        self.assertEqual(None, db.sqliteDB.getTypeByID(self.dataBase, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getTypeByID(self.dataBase, 1))

    def test_getLanguageByID(self):

        self.assertEqual(None, db.sqliteDB.getLanguageByID(self.dataBase, 1))
        self.test_addUpdate()
        self.assertNotEqual(None, db.sqliteDB.getLanguageByID(self.dataBase, 1))

    # def test_getSetSubstanceID(self):

    def test_addUpdate(self):

        update = self.mJsonHelper.GetDictionary('test_addUpdate', 'update')
        self.assertEqual([], db.sqliteDB.getUpdates(self.dataBase, update))
        db.sqliteDB.addUpdate(self.dataBase, update)
        updates = db.sqliteDB.getUpdates(self.dataBase, update)
        self.assertEqual([update], updates)

    # def test_rawUpdatesToUpdates(self):

    def test_getUpdates(self):

        self.assertEqual(0, len(db.sqliteDB.getUpdates(self.dataBase, {})))

        updates = self.mJsonHelper.GetArray('test_getUpdates', 'updates')
        for up in updates:
            up['Date'] = JsonHelper.intList2Date(JsonHelper.string2intList(up['Date']))

        db.sqliteDB.addUpdates(self.dataBase, updates)

        self.assertEqual(len(updates), len(db.sqliteDB.getUpdates(self.dataBase, {})))

        queryAndAnswer = self.mJsonHelper.GetArray('test_getUpdates', 'queryAndAnswer')
        for qa in queryAndAnswer:
            self.assertEqual(qa['answer'], len(db.sqliteDB.getUpdates(self.dataBase, qa['query'])))

    def test_getUpdatesByKBInPath(self):

        updates = self.mJsonHelper.GetArray('test_getUpdatesByKBInPath', 'updates')
        for up in updates:
            up['Date'] = JsonHelper.intList2Date(JsonHelper.string2intList(up['Date']))

        db.sqliteDB.addUpdates(self.dataBase, updates)

        queryAndAnswer = self.mJsonHelper.GetArray('test_getUpdatesByKBInPath', 'queryAndAnswer')
        for qa in queryAndAnswer:
            inputValue = list(qa.keys())[0]
            self.assertEqual(qa[inputValue], len(db.sqliteDB.getUpdatesByKBInPath(self.dataBase, inputValue)))


if __name__ == '__main__':

    unittest.main()
