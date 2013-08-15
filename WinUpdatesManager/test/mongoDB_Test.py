import unittest
import datetime
import core.updates
import db.mongoDB


class TestSequenceFunctions(unittest.TestCase):

    def test_complex(self):

        db.mongoDB.dropTableInDB()
        items = db.mongoDB.getFromDB()
        self.assertEqual(0, items.count())

        paths = ['E:\\1212\\2779030\\Windows8\\x86\\NEU\\' +
        'WINDOWS8-RT-KB2779030-X86.MSU']
        date = datetime.datetime(2012, 12, 11)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        db.mongoDB.insertToDB(aItems=updates)
        items = db.mongoDB.getFromDB()
        self.assertEqual(len(updates), items.count())

        for i in range(len(updates)):
            self.assertEqual(updates[i]['Path'], items[i]['Path'])
            self.assertEqual(updates[i]['KB'], items[i]['KB'])
            self.assertEqual(updates[i]['Version'], items[i]['Version'])
            self.assertEqual(updates[i]['Type'], items[i]['Type'])
            self.assertEqual(updates[i]['Language'], items[i]['Language'])
            self.assertEqual(updates[i]['Date'], items[i]['Date'])

        db.mongoDB.deleteFromDB(aItems=items)
        items = db.mongoDB.getFromDB()

        self.assertEqual(0, items.count())

        db.mongoDB.insertToDB(aItems=updates)
        items = db.mongoDB.getFromDB()
        self.assertEqual(len(updates), items.count())

        db.mongoDB.deleteFromDB(aItems=updates)
        items = db.mongoDB.getFromDB()
        self.assertEqual(0, items.count())

    def test_updateInDB(self):

        db.mongoDB.dropTableInDB()

        paths = ['E:\\0906\\WINDOWS\\WINDOWS2000\\920685\\' +
        'X86\\ENGLISH\\WINDOWS2000-KB920685-X86-ENU.EXE',
        'E:\\0906\\WINDOWS\\WINDOWS2000\\920685\\X86\\' +
        'RUSSIAN\\WINDOWS2000-KB920685-X86-RUS.EXE']
        date = datetime.datetime(2006, 9, 12)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        db.mongoDB.insertToDB(aItems=updates)
        items = db.mongoDB.getFromDB()
        self.assertEqual(len(updates), items.count())

        languages = ['Enu', 'Rus']
        ids = []

        updates = []

        #for it, language in zip(items, languages):
        for i in range(0, max(items.count(), len(languages))):
            updates.append(items[i])
            updates[i]['Language'] = languages[i]
            ids.append({'_id': updates[i]['_id']})

        db.mongoDB.updateInDB(aItems=updates)
        items = db.mongoDB.getFromDB()
        self.assertEqual(len(updates), items.count())

        for i in range(0, len(updates)):
            self.assertEqual(ids[i]['_id'], items[i]['_id'])
            self.assertEqual(languages[i], items[i]['Language'])

if __name__ == '__main__':

    unittest.main()
