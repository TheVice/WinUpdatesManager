import unittest
import datetime
import db.sqliteDB


class TestSequenceFunctions(unittest.TestCase):

    def test_complex(self):

        dataBase = db.sqliteDB.connect(':memory:')
        self.assertNotEqual(None, dataBase)

        self.assertEqual([],
                         db.sqliteDB.listTables(dataBase))

        self.assertEqual(None, db.sqliteDB.findTable(dataBase, 'KBs'))
        db.sqliteDB.createTableKBs(dataBase)
        self.assertNotEqual(None, db.sqliteDB.findTable(dataBase, 'KBs'))

        self.assertEqual(None, db.sqliteDB.findTable(dataBase, 'Dates'))
        db.sqliteDB.createTableDates(dataBase)
        self.assertNotEqual(None, db.sqliteDB.findTable(dataBase, 'Dates'))

        self.assertEqual(None, db.sqliteDB.findTable(dataBase, 'Paths'))
        db.sqliteDB.createTablePaths(dataBase)
        self.assertNotEqual(None, db.sqliteDB.findTable(dataBase, 'Paths'))

        self.assertEqual(None, db.sqliteDB.findTable(dataBase, 'Versions'))
        db.sqliteDB.createTableVersions(dataBase)
        self.assertNotEqual(None, db.sqliteDB.findTable(dataBase, 'Versions'))

        self.assertEqual(None, db.sqliteDB.findTable(dataBase, 'Types'))
        db.sqliteDB.createTableTypes(dataBase)
        self.assertNotEqual(None, db.sqliteDB.findTable(dataBase, 'Types'))

        self.assertEqual(None, db.sqliteDB.findTable(dataBase, 'Languages'))
        db.sqliteDB.createTableLanguages(dataBase)
        self.assertNotEqual(None, db.sqliteDB.findTable(dataBase, 'Languages'))

        self.assertEqual(None, db.sqliteDB.findTable(dataBase, 'Updates'))
        db.sqliteDB.createTableUpdates(dataBase)
        self.assertNotEqual(None, db.sqliteDB.findTable(dataBase, 'Updates'))

        self.assertEqual(None, db.sqliteDB.getIDFrom(dataBase, 'KBs', 'id', 1))
        db.sqliteDB.insertInto(dataBase, 'KBs', 'id', 1)
        self.assertNotEqual(None, db.sqliteDB.getIDFrom(dataBase, 'KBs',
                                                        'id', 1))

        self.assertEqual(['Dates', 'KBs', 'Languages', 'Paths', 'Types',
                          'Updates', 'Versions', 'sqlite_sequence'],
                         db.sqliteDB.listTables(dataBase))

        update = {'Date': datetime.date(2011, 5, 10),
                 'Language': 'German',
                 'Type': 'IA64',
                 'KB': 2524426,
                 'Version': 'Windows Server 2003',
                 'Path': '\\2524426\\WindowsServer2003\\ia64\\DEU\\' +
                         'WINDOWSSERVER2003-KB2524426-IA64-DEU.EXE'}

        self.assertEqual(None, db.sqliteDB.getUpdates(dataBase, update))
        db.sqliteDB.addUpdate(dataBase, update)
        self.assertNotEqual(None, db.sqliteDB.getUpdates(dataBase, update))
        update['Path'] = '?'
        self.assertEqual(None, db.sqliteDB.getUpdates(dataBase, update))

        self.assertNotEqual(None, db.sqliteDB.getIDFrom(dataBase, 'KBs', 'id',
                                                        update['KB']))
        self.assertEqual(None, db.sqliteDB.getIDFrom(dataBase, 'KBs', 'id',
                                                     update['KB'] + 1))

        self.assertNotEqual(None, db.sqliteDB.getDateByID(dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getDateByID(dataBase, 2))

        self.assertNotEqual(None, db.sqliteDB.getPathByID(dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getPathByID(dataBase, 2))

        self.assertNotEqual(None, db.sqliteDB.getVersionByID(dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getVersionByID(dataBase, 2))

        self.assertNotEqual(None, db.sqliteDB.getTypeByID(dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getTypeByID(dataBase, 2))

        self.assertNotEqual(None, db.sqliteDB.getLanguageByID(dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getLanguageByID(dataBase, 2))

        update['Path'] = ('\\2524426\\WindowsServer2003\\ia64\\DEU\\' +
                         'WINDOWSSERVER2003-KB2524426-IA64-DEU.EXE')

        self.assertNotEqual(None, db.sqliteDB.getUpdates(dataBase, update))
        update['KB'] += 1
        self.assertEqual(None, db.sqliteDB.getUpdates(dataBase, update))

        dataBase.close()


if __name__ == '__main__':

    unittest.main()
