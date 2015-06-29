import sys
import sqlite3
import db.sqliteDB
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)
        self.mDataBase = self.mJsonHelper.GetSting('Connection', 'dataBase')

    def test_connect(self):
        self.assertIsNotNone(db.sqliteDB.connect(self.mDataBase))

    def test_disconnect(self):
        connection = db.sqliteDB.connect(self.mDataBase)
        self.assertNotEqual(None, connection)
        db.sqliteDB.disconnect(connection)

    def test_write(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']

            db.sqliteDB.write(connection, writeStatement)

            readStatement = testData['readStatement']
            readResult = db.sqliteDB.read(connection, readStatement, lambda l: l.fetchall())
            expectedReadResult = testData['expectedReadResult']
            for i in range(0, len(expectedReadResult)):
                expectedReadResult[i] = (expectedReadResult[i],)
            self.assertEqual(expectedReadResult, readResult)

            db.sqliteDB.disconnect(connection)

            db.sqliteDB.write(self.mDataBase, writeStatement)

            connection = db.sqliteDB.connect(self.mDataBase)
            db.sqliteDB.write(connection.cursor(), writeStatement)
            db.sqliteDB.disconnect(connection)

    def test_writeAsync(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = sqlite3.connect(self.mDataBase, check_same_thread=False)

            writeStatement = testData['writeStatement']

            db.sqliteDB.writeAsync(connection, writeStatement)

            readStatement = testData['readStatement']
            readResult = db.sqliteDB.readAsync(connection, readStatement, lambda l: l.fetchall())
            expectedReadResult = testData['expectedReadResult']
            for i in range(0, len(expectedReadResult)):
                expectedReadResult[i] = (expectedReadResult[i],)
            self.assertEqual(expectedReadResult, readResult)

            connection.close()

    def test_read(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            expectedReadResult = testData['expectedReadResult']
            for i in range(0, len(expectedReadResult)):
                expectedReadResult[i] = (expectedReadResult[i],)

            readStatement = testData['readStatement']
            readResult = db.sqliteDB.read(connection, readStatement, lambda l: l.fetchall())
            self.assertNotEqual(expectedReadResult, readResult)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)
            readResult = db.sqliteDB.read(connection, readStatement, lambda l: l.fetchall())
            self.assertEqual(expectedReadResult, readResult)

            db.sqliteDB.disconnect(connection)

            db.sqliteDB.read(self.mDataBase, readStatement, lambda l: l.fetchall())

            connection = db.sqliteDB.connect(self.mDataBase)
            db.sqliteDB.read(connection.cursor(), readStatement, lambda l: l.fetchall())
            db.sqliteDB.disconnect(connection)

    def test_readAsync(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = sqlite3.connect(self.mDataBase, check_same_thread=False)

            expectedReadResult = testData['expectedReadResult']
            for i in range(0, len(expectedReadResult)):
                expectedReadResult[i] = (expectedReadResult[i],)

            readStatement = testData['readStatement']
            readResult = db.sqliteDB.readAsync(connection, readStatement, lambda l: l.fetchall())
            self.assertNotEqual(expectedReadResult, readResult)

            writeStatement = testData['writeStatement']
            db.sqliteDB.writeAsync(connection, writeStatement)
            readResult = db.sqliteDB.readAsync(connection, readStatement, lambda l: l.fetchall())
            self.assertEqual(expectedReadResult, readResult)

            connection.close()

    def test_listTables(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            expectedReadResult = testData['expectedReadResult']
            readResult = db.sqliteDB.listTables(connection)
            self.assertEqual(expectedReadResult, readResult)

            db.sqliteDB.disconnect(connection)

    def test_isTableExist(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            tables = testData['tables']
            expectedResults = testData['expectedResults']

            for table, expectedResult in zip(tables, expectedResults):
                self.assertEqual(expectedResult, db.sqliteDB.isTableExist(connection, table))

            db.sqliteDB.disconnect(connection)

    def test_listRows(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            tables = testData['tables']
            expectedResults = testData['expectedResults']

            for table, expectedResult in zip(tables, expectedResults):
                self.assertEqual(expectedResult, db.sqliteDB.listRows(connection, table))

            db.sqliteDB.disconnect(connection)

    def test_isRowExist(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            inputData = testData['inputData']
            expectedResults = testData['expectedResults']
            for i, expectedResult in zip(inputData, expectedResults):
                table = list(i.keys())[0]
                rows = i[table]
                results = []
                for r in rows:
                    results.append(db.sqliteDB.isRowExist(connection, table, r))

                self.assertEqual(expectedResult, results)

            db.sqliteDB.disconnect(connection)

    def test_dropTable(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            table = testData['table']

            self.assertTrue(db.sqliteDB.isTableExist(connection, table))
            db.sqliteDB.dropTable(connection, table)
            self.assertFalse(db.sqliteDB.isTableExist(connection, table))

            db.sqliteDB.disconnect(connection)

    def test_deleteFromTable(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            table = testData['table']
            rows = testData['rows']
            items = testData['items']
            expectedResults = testData['expectedResults']

            result = db.sqliteDB.getFrom(connection, table, rows)
            self.assertEqual(expectedResults, result)

            for item in items:
                db.sqliteDB.deleteFromTable(connection, table, rows, item)

            result = db.sqliteDB.getFrom(connection, table, rows)
            self.assertNotEqual(expectedResults, result)

            db.sqliteDB.disconnect(connection)

    def test_updateAtTable(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            table = testData['table']
            rows = testData['rows']
            currentItems = testData['currentItems']
            items = testData['items']

            result = db.sqliteDB.getFrom(connection, table, rows)
            self.assertNotEqual(items, result)

            for item, currentItem in zip(items, currentItems):
                db.sqliteDB.updateAtTable(connection, table, rows, item, currentItem)

            expectedResults = testData['expectedResults']
            result = db.sqliteDB.getFrom(connection, table, rows)
            self.assertEqual(expectedResults, result)

            db.sqliteDB.disconnect(connection)

    def test_getFrom(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            table = testData['table']
            rows = testData['rows']
            getFilter = testData['filter']

            expectedResult = testData['expectedResult']
            result = db.sqliteDB.getFrom(connection, table, rows, getFilter)

            self.assertEqual(expectedResult, result)

            db.sqliteDB.disconnect(connection)

    def test_insertInto(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            connection = db.sqliteDB.connect(self.mDataBase)

            writeStatement = testData['writeStatement']
            db.sqliteDB.write(connection, writeStatement)

            table = testData['table']
            rows = testData['rows']
            items = testData['items']

            self.assertNotEqual(items, db.sqliteDB.getFrom(connection, table))
            self.assertNotEqual(items, db.sqliteDB.getFrom(connection, table, rows))

            db.sqliteDB.insertInto(connection, table, items)

            self.assertEqual(items, db.sqliteDB.getFrom(connection, table))
            self.assertEqual(items, db.sqliteDB.getFrom(connection, table, rows))

            db.sqliteDB.deleteFromTable(connection, table)

            self.assertNotEqual(items, db.sqliteDB.getFrom(connection, table))
            self.assertNotEqual(items, db.sqliteDB.getFrom(connection, table, rows))

            db.sqliteDB.insertInto(connection, table, items, rows)

            self.assertEqual(items, db.sqliteDB.getFrom(connection, table))
            self.assertEqual(items, db.sqliteDB.getFrom(connection, table, rows))

            db.sqliteDB.disconnect(connection)


if __name__ == '__main__':

    main()
