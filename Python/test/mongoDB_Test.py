import os
import datetime
import unittest
from db.mongoDB import MongoDBClient
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'mongoDB_Test.json')
        self.mJsonHelper = JsonHelper(path)
        self.mHostAndPort = self.mJsonHelper.GetSting('MongoClient', 'HostAndPort')
        self.mDbClient = MongoDBClient(self.mHostAndPort)

    def test_changeServer(self):

        self.mDbClient.changeServer(self.mHostAndPort, 500)

    def test_getItemsFromDB(self):

        items = self.mDbClient.getItemsFromDB('win32', 'updates')
        self.assertLess(0, items.count())

    def test_insertToDB(self):

        itemToInsert = {'_id': MongoDBClient.generateObjectId('{}{}'.format('test', 'insertToDB')),
                        'test': 'insertToDB'}
        items = self.mDbClient.getItemsFromDB('win32', 'updates', itemToInsert)
        self.assertEquals(0, items.count())

        self.mDbClient.insertToDB('win32', 'updates', [itemToInsert])

        items = self.mDbClient.getItemsFromDB('win32', 'updates', itemToInsert)
        self.assertEquals(1, items.count())
        self.mDbClient.deleteFromDB('win32', 'updates', [itemToInsert])

    def test_updateInDB(self):

        itemToInsert = {'_id': MongoDBClient.generateObjectId('{}{}'.format('test', 'insertToDB')),
                        'test': 'insertToDB'}
        items = self.mDbClient.getItemsFromDB('win32', 'updates', itemToInsert)
        self.assertEquals(0, items.count())
        self.mDbClient.insertToDB('win32', 'updates', [itemToInsert])
        items = self.mDbClient.getItemsFromDB('win32', 'updates', itemToInsert)
        self.assertEquals(1, items.count())
        itemToUpdate = items[0]
        itemToUpdate['test'] = 'updateInDB'
        items = self.mDbClient.getItemsFromDB('win32', 'updates', itemToUpdate)
        self.assertEquals(0, items.count())

        self.mDbClient.updateInDB('win32', 'updates', [itemToUpdate])

        items = self.mDbClient.getItemsFromDB('win32', 'updates', itemToInsert)
        self.assertEquals(0, items.count())
        items = self.mDbClient.getItemsFromDB('win32', 'updates', itemToUpdate)
        self.assertEquals(1, items.count())
        self.mDbClient.deleteFromDB('win32', 'updates', [itemToUpdate])

    def test_deleteFromDB(self):

        self.test_insertToDB()

    def test_dropDB(self):

        dbs = self.mDbClient.getDBs()
        self.assertEqual(0, list(dbs).count('win16'))
        self.mDbClient.insertToDB('win16', 'updates2', [{}])
        dbs = self.mDbClient.getDBs()
        self.assertEqual(1, list(dbs).count('win16'))

        self.mDbClient.dropDB('win16')

        dbs = self.mDbClient.getDBs()
        self.assertEqual(0, list(dbs).count('win16'))

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
        self.assertEquals(updatesCount, items.count())

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
        self.assertEquals(updatesCount, items.count())

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
