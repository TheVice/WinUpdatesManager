import sys
import datetime
import unittest
from bson import ObjectId
from unittest.mock import patch, MagicMock
from db.mongoDB import MongoDBClient
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))
        self.mHostAndPort = self.mJsonHelper.GetSting('MongoClient', 'HostAndPort')
        self.mServerSelectionTimeoutMS = self.mJsonHelper.GetInteger('MongoClient', 'ServerSelectionTimeoutMS')
        self.mDataBase = self.mJsonHelper.GetSting('MongoClient', 'dataBase')
        self.mTable = self.mJsonHelper.GetSting('MongoClient', 'table')
        self.mItemsForTest = self.mJsonHelper.GetArray('MongoClient', 'itemsForTest')
        self.mItemsForTest = MongoDBClient.addObjectIdFieldAtCollection(self.mItemsForTest)

        self.mDbClient = MongoDBClient(self.mHostAndPort)
        self.mDbClient.dropDB(self.mDataBase)

    def test_changeServer(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            try:
                self.assertEqual(testData[1], self.mDbClient.changeServer(testData[0], self.mServerSelectionTimeoutMS))
            except Exception:
                exceptionText = '{}'.format(sys.exc_info()[1])
                self.assertLess(0, testData[1].count(exceptionText))

    def test_getItemsFromDB(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)

        self.mDbClient.insertToDB(self.mDataBase, self.mTable, self.mItemsForTest)

        for testData in testsData:

            sort = []
            if testData['sort'] is None:
                sort = None
            else:
                for s in testData['sort']:
                    key = list(s.keys())[0]
                    sort.append((key, s[key]))

            try:
                items = self.mDbClient.getItemsFromDB(self.mDataBase, self.mTable, testData['query'],
                                                      testData['projection'], testData['skip'],
                                                      testData['limit'], sort)
                expectedItems = testData['expectedItems']
                for i in range(0, len(expectedItems)):
                    if list(expectedItems[i].keys()).count('_id'):
                        expectedItems[i]['_id'] = ObjectId(expectedItems[i]['_id'])

                self.assertEqual(expectedItems, items)
            except:
                self.assertEqual(testData['expectedItems'], '{}'.format(sys.exc_info()[1]))

    def test_insertToDB(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        usePymongo3rdVersion = True
        for testData in testsData:
            self.mDbClient.dropCollectionsInDB(self.mDataBase, self.mTable)
            items = self.mDbClient.getItemsFromDB(self.mDataBase, self.mTable)
            if [] != testData[1]:
                self.assertNotEqual(testData[1], items)

            try:
                if usePymongo3rdVersion:
                    self.mDbClient.insertToDB(self.mDataBase, self.mTable, testData[1])
                else:
                    with patch('db.mongoDB.version_tuple') as mock_obj:
                        mock_obj.__ge__ = MagicMock(return_value=False)
                        self.mDbClient.insertToDB(self.mDataBase, self.mTable, testData[1])
            except:
                self.assertEqual(testData[0], '{}'.format(sys.exc_info()[1]))

            items = self.mDbClient.getItemsFromDB(self.mDataBase, self.mTable)
            if not isinstance(testData[1], list):
                self.assertEqual(1, len(items))
                self.assertEqual(testData[1], items[0])
            else:
                self.assertEqual(testData[1], items)

            usePymongo3rdVersion = not usePymongo3rdVersion

    def test_updateInDB(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        usePymongo3rdVersion = True
        for testData in testsData:
            self.mDbClient.dropCollectionsInDB(self.mDataBase, self.mTable)
            self.mDbClient.insertToDB(self.mDataBase, self.mTable, testData['itemsToInsert'])
            itemsToUpdate = testData['itemsToUpdate']

            query = {}
            for itu in itemsToUpdate:
                for key in itu[0].keys():
                    if 0 == list(query.keys()).count(key):
                        query[key] = []
                    query[key].append(itu[0][key])

            for key in query.keys():
                if 1 < len(query[key]):
                    query[key] = {key: {'$in': query[key]}}
                else:
                    query[key] = query[key][0]

            if len(query.keys()) > 1:
                newQuery = {}
                newQuery['$or'] = []
                for key in query.keys():
                    newQuery['$or'].append({key: query[key]})

                query = newQuery

            existItems = self.mDbClient.getItemsFromDB(self.mDataBase, self.mTable, query)
            self.assertEqual(len(itemsToUpdate), len(existItems))

            for i in range(0, len(itemsToUpdate)):
                for j in range(0, len(existItems)):
                    itemsToUpdate[i][0]['_id'] = existItems[j]['_id']
                    if itemsToUpdate[i][0] == existItems[j]:
                        modifiedItems = itemsToUpdate[i][1]
                        if not isinstance(modifiedItems, list):
                            for key in modifiedItems.keys():
                                existItems[j][key] = modifiedItems[key]
                        else:
                            existItems[j]['_id'] = modifiedItems

            if 1 == len(existItems):
                existItems = existItems[0]

            expectedItems = testData['expectedItems']

            try:
                if usePymongo3rdVersion:
                    self.mDbClient.updateInDB(self.mDataBase, self.mTable, existItems)
                else:
                    with patch('db.mongoDB.version_tuple') as mock_obj:
                        mock_obj.__ge__ = MagicMock(return_value=False)
                        self.mDbClient.updateInDB(self.mDataBase, self.mTable, existItems)

                items = self.mDbClient.getItemsFromDB(self.mDataBase, self.mTable, aProjection={'_id': 0})
                self.assertEqual(expectedItems, items)
            except Exception:
                self.assertEqual(expectedItems, '{}'.format(sys.exc_info()[1]))

            usePymongo3rdVersion = not usePymongo3rdVersion

    def test_deleteFromDB(self):

        self.test_insertToDB()

    def test_dropDB(self):

        dbs = self.mDbClient.getDBs()
        self.assertEqual(0, dbs.count('win16'))
        self.mDbClient.insertToDB('win16', 'updates2', [{}])
        dbs = self.mDbClient.getDBs()
        self.assertEqual(1, dbs.count('win16'))

        self.mDbClient.dropDB('win16')

        dbs = self.mDbClient.getDBs()
        self.assertEqual(0, dbs.count('win16'))

    def test_droCollectionsInDB(self):

        tables = self.mDbClient.getCollectionsFromDB('win32')
        self.assertEqual(0, list(tables).count('updates2'))
        self.mDbClient.insertToDB('win32', 'updates2', [{}])
        tables = self.mDbClient.getCollectionsFromDB('win32')
        self.assertEqual(1, list(tables).count('updates2'))

        self.mDbClient.dropCollectionsInDB('win32', 'updates2')

        tables = self.mDbClient.getCollectionsFromDB('win32')
        self.assertEqual(0, list(tables).count('updates2'))

    def test_getDBs(self):

        self.test_dropDB()

    def test_getCollectionsFromDB(self):

        self.test_droCollectionsInDB()

    # def test_aggregate(self):

    def test_removeDubsFromCollectionByObjectId(self):

        updates = self.mJsonHelper.GetArray('test_removeDubsByObjectId', 'updates')
        for update in updates:
            update['Date'] = datetime.datetime.strptime(update['Date'], '%Y, %m, %d')

        updates = MongoDBClient.addObjectIdFieldAtCollection(updates)

        self.mDbClient.dropDB('win16')
        self.mDbClient.insertToDB('win16', 'updates2', updates)

        updatesCount = len(updates)
        items = self.mDbClient.getItemsFromDB('win16', 'updates2')
        self.assertEquals(updatesCount, len(items))

        uniqueUpdates = self.mJsonHelper.GetArray('test_removeDubsByObjectId', 'uniqueUpdates')
        for update in uniqueUpdates:
            update['Date'] = datetime.datetime.strptime(update['Date'], '%Y, %m, %d')

        uniqueUpdates = MongoDBClient.addObjectIdFieldAtCollection(uniqueUpdates)
        updatesCount += len(uniqueUpdates)

        updates.extend(uniqueUpdates)
        updates = self.mDbClient.removeDubsFromCollectionByObjectId('win16', 'updates2', updates)
        self.assertEqual(uniqueUpdates, updates)
        self.mDbClient.insertToDB('win16', 'updates2', updates)
        items = self.mDbClient.getItemsFromDB('win16', 'updates2')
        self.assertEquals(updatesCount, len(items))

        self.mDbClient.dropDB('win16')

    # def test_deleteUpdateDubsFromTable(self):

    # def test_getUpdateDubsFromTable(self):

    def test_addObjectIdFieldAtCollection(self):

        updates = self.mJsonHelper.GetArray('test_addObjectIdFieldAtCollection', 'updates')
        for update in updates:
            update['Date'] = datetime.datetime.strptime(update['Date'], '%Y, %m, %d').date()

        updates = MongoDBClient.addObjectIdFieldAtCollection(updates)
        hashes = self.mJsonHelper.GetArray('test_addObjectIdFieldAtCollection', 'hashes')

        for i in zip(updates, hashes):
            self.assertEquals(str(i[1]), str(i[0]['_id']))


if __name__ == '__main__':

    unittest.main()
