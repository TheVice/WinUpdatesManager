import unittest
import datetime
import core.updates
import db.mongoDB


class TestSequenceFunctions(unittest.TestCase):

    def test_ComplexTest(self):

        items = db.mongoDB.getFromDB()
        self.assertEqual(0, items.count())

        ups = []

        paths = ['E:\\1212\\2779030\\Windows8\\x86\\NEU\\' +
        'WINDOWS8-RT-KB2779030-X86.MSU']

        for path in paths:
            update = core.updates.Update()
            update.mFullName = path
            update.mKB = core.updates.getKB(path)
            update.mVersion = core.updates.getVersion(path)[0]
            update.mOsType = core.updates.getOsType(path)
            update.mLanguage = core.updates.getLanguage(path)
            update.mDate = datetime.datetime(2012, 12, 11)
            ups.append(update)

        db.mongoDB.insertToDB(aItems=ups)
        items = db.mongoDB.getFromDB()

        self.assertEqual(len(ups), items.count())

        gettedItems = []

        for up, item in zip(ups, items):
            self.assertEqual(up.mFullName, item['Name'])
            self.assertEqual(up.mKB, item['KB'])
            self.assertEqual(up.mVersion, item['Version'])
            self.assertEqual(up.mOsType, item['Type'])
            self.assertEqual(up.mLanguage, item['Language'])
            self.assertEqual(up.mDate, item['Date'])
            gettedItems.append(item)

        db.mongoDB.deleteFromDB(aItems=gettedItems, aRawItems=True)
        items = db.mongoDB.getFromDB()
        self.assertEqual(0, items.count())

        db.mongoDB.insertToDB(aItems=ups)
        items = db.mongoDB.getFromDB()
        self.assertEqual(len(ups), items.count())

        db.mongoDB.deleteFromDB(aItems=ups)
        items = db.mongoDB.getFromDB()
        self.assertEqual(0, items.count())

if __name__ == '__main__':

    unittest.main()
