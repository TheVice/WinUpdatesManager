import unittest
import os
import datetime
import core.updates
import db.mongoDB


class TestSequenceFunctions(unittest.TestCase):

    def test_complex(self):

        paths = ['E:' + os.sep + '1212' + os.sep + '2779030' + os.sep +
            'Windows8' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS8-RT-KB2779030-X86.MSU']
        date = datetime.datetime(2012, 12, 11)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        db.mongoDB.dropTableInDB(aDB='win32', aTable='updates')
        db.mongoDB.insertToDB(aDB='win32', aTable='updates', aItems=updates)
        items = db.mongoDB.getItemsFromDB(aDB='win32', aTable='updates')
        self.assertEqual(len(updates), items.count())

        for i in range(len(updates)):
            self.assertEqual(updates[i]['Path'], items[i]['Path'])
            self.assertEqual(updates[i]['KB'], items[i]['KB'])
            self.assertEqual(updates[i]['Version'], items[i]['Version'])
            self.assertEqual(updates[i]['Type'], items[i]['Type'])
            self.assertEqual(updates[i]['Language'], items[i]['Language'])
            self.assertEqual(updates[i]['Date'], items[i]['Date'])

        db.mongoDB.deleteFromDB(aDB='win32', aTable='updates', aItems=items)
        items = db.mongoDB.getItemsFromDB(aDB='win32', aTable='updates')

        self.assertEqual(0, items.count())

        db.mongoDB.insertToDB(aDB='win32', aTable='updates', aItems=updates)
        items = db.mongoDB.getItemsFromDB(aDB='win32', aTable='updates')
        self.assertEqual(len(updates), items.count())

        db.mongoDB.deleteFromDB(aDB='win32', aTable='updates', aItems=updates)
        items = db.mongoDB.getItemsFromDB(aDB='win32', aTable='updates')
        self.assertEqual(0, items.count())

        paths = ['E:' + os.sep + '0906' + os.sep + 'WINDOWS' + os.sep +
                'WINDOWS2000' + os.sep + '920685' + os.sep +
                'X86' + os.sep + 'ENGLISH' + os.sep +
                'WINDOWS2000-KB920685-X86-ENU.EXE',
                'E:' + os.sep + '0906' + os.sep + 'WINDOWS' + os.sep +
                'WINDOWS2000' + os.sep + '920685' + os.sep + 'X86' + os.sep +
                'RUSSIAN' + os.sep + 'WINDOWS2000-KB920685-X86-RUS.EXE']
        date = datetime.datetime(2006, 9, 12)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        db.mongoDB.insertToDB(aDB='win32', aTable='updates', aItems=updates)
        items = db.mongoDB.getItemsFromDB(aDB='win32', aTable='updates')
        self.assertEqual(len(updates), items.count())

        languages = ['Enu', 'Rus']
        ids = []

        updates = []

        for i in range(0, max(items.count(), len(languages))):
            updates.append(items[i])
            updates[i]['Language'] = languages[i]
            ids.append({'_id': updates[i]['_id']})

        db.mongoDB.updateInDB(aDB='win32', aTable='updates', aItems=updates)
        items = db.mongoDB.getItemsFromDB(aDB='win32', aTable='updates')
        self.assertEqual(len(updates), items.count())

        for i in range(0, len(updates)):
            self.assertEqual(ids[i]['_id'], items[i]['_id'])
            self.assertEqual(languages[i], items[i]['Language'])

        db.mongoDB.dropTableInDB(aDB='win32', aTable='updates')
        items = db.mongoDB.getItemsFromDB(aDB='win32', aTable='updates')
        self.assertEqual(0, items.count())

    def test_getDBsAndCollections(self):

        db.mongoDB.insertToDB(aDB='win16',
                              aTable='updates1',
                              aItems=[{'item1': 1}, {'item2': 2}])
        db.mongoDB.insertToDB(aDB='win16',
                              aTable='updates2',
                              aItems=[{'item3': 3}, {'item4': 4}])
        db.mongoDB.insertToDB(aDB='win64',
                              aTable='updates3',
                              aItems=[{'item5': 5}, {'item6': 6}])

        dbs = db.mongoDB.getDBs()

        db1 = False
        db2 = False
        for dataBase in dbs:
            if(dataBase == 'win32'):
                db1 = True
            elif(dataBase == 'win64'):
                db2 = True

        self.assertTrue(db1)
        self.assertEqual(db1, db2)

        collections = db.mongoDB.getCollections('win16')
        self.assertEqual(3, len(collections))
        self.assertEqual(['system.indexes', 'updates1', 'updates2'],
            collections)

        collections = db.mongoDB.getCollections('win64')
        self.assertEqual(2, len(collections))
        self.assertEqual(['system.indexes', 'updates3'], collections)

        db.mongoDB.dropTableInDB(aDB='win16', aTable='updates1')
        db.mongoDB.dropTableInDB(aDB='win16', aTable='updates2')
        db.mongoDB.dropTableInDB(aDB='win64', aTable='updates3')

    def test_pymongoDate2DateTime(self):
        updates = []

        for i in range(1, 31):
            data = {}
            data['date'] = datetime.date(2013, 12, i)
            updates.append(data)

        updates = db.mongoDB.pymongoDate2DateTime(updates, 'date')

        i = 1
        for update in updates:
            self.assertEqual(datetime.datetime(2013, 12, i), update['date'])
            i += 1

if __name__ == '__main__':

    unittest.main()
