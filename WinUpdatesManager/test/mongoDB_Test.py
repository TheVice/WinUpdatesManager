import unittest
import datetime
import core.updates
import db.mongoDB


class TestSequenceFunctions(unittest.TestCase):

    def test_ComplexTest(self):

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

        #for up, it in zip(updates, items):
        for i in range(0, max(len(updates), items.count())):
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

if __name__ == '__main__':

    unittest.main()
