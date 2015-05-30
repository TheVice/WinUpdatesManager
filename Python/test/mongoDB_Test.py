import unittest
import os
import datetime
import core.updates
import db.mongoDB

dbClient = db.mongoDB.MongoDBClient()
gHostAndPort = None


class TestSequenceFunctions(unittest.TestCase):

    def test_complex(self):

        paths = ['E:' + os.sep + '1212' + os.sep + '2779030' + os.sep +
            'Windows8' + os.sep + 'x86' + os.sep + 'NEU' + os.sep +
            'WINDOWS8-RT-KB2779030-X86.MSU']
        date = datetime.datetime(2012, 12, 11)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        dbClient.dropTableInDB('win32', 'updates', gHostAndPort)
        dbClient.insertToDB('win32', 'updates', gHostAndPort, updates)
        items = dbClient.getItemsFromDB('win32', 'updates', gHostAndPort)
        self.assertEqual(len(updates), items.count())

        for i in range(len(updates)):
            self.assertEqual(updates[i]['Path'], items[i]['Path'])
            self.assertEqual(updates[i]['KB'], items[i]['KB'])
            self.assertEqual(updates[i]['Version'], items[i]['Version'])
            self.assertEqual(updates[i]['Type'], items[i]['Type'])
            self.assertEqual(updates[i]['Language'], items[i]['Language'])
            self.assertEqual(updates[i]['Date'], items[i]['Date'])

        dbClient.deleteFromDB('win32', 'updates', gHostAndPort, items)
        items = dbClient.getItemsFromDB('win32', 'updates', gHostAndPort)

        self.assertEqual(0, items.count())

        dbClient.insertToDB('win32', 'updates', gHostAndPort, updates)
        items = dbClient.getItemsFromDB('win32', 'updates', gHostAndPort)
        self.assertEqual(len(updates), items.count())

        dbClient.deleteFromDB('win32', 'updates',
                                   gHostAndPort, updates)
        items = dbClient.getItemsFromDB('win32', 'updates', gHostAndPort)
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

        dbClient.insertToDB('win32', 'updates', gHostAndPort, updates)
        items = dbClient.getItemsFromDB('win32', 'updates', gHostAndPort)
        self.assertEqual(len(updates), items.count())

        languages = ['Enu', 'Rus']
        ids = []

        updates = []

        for i in range(0, max(items.count(), len(languages))):
            updates.append(items[i])
            updates[i]['Language'] = languages[i]
            ids.append({'_id': updates[i]['_id']})

        dbClient.updateInDB('win32', 'updates', gHostAndPort, updates)
        items = dbClient.getItemsFromDB('win32', 'updates', gHostAndPort)
        self.assertEqual(len(updates), items.count())

        for i in range(0, len(updates)):
            self.assertEqual(ids[i]['_id'], items[i]['_id'])
            self.assertEqual(languages[i], items[i]['Language'])

        dbClient.dropTableInDB('win32', 'updates', gHostAndPort)
        items = dbClient.getItemsFromDB('win32', 'updates', gHostAndPort)
        self.assertEqual(0, items.count())

    def test_getDBsAndCollections(self):

        dbClient.insertToDB('win16',
                            'updates1',
                            gHostAndPort,
                            [{'item1': 1}, {'item2': 2}])
        dbClient.insertToDB('win16',
                            'updates2',
                            gHostAndPort,
                            [{'item3': 3}, {'item4': 4}])
        dbClient.insertToDB('win64',
                            'updates3',
                            gHostAndPort,
                            [{'item5': 5}, {'item6': 6}])

        dbs = dbClient.getDBs(gHostAndPort)

        db1 = False
        db2 = False
        for dataBase in dbs:
            if(dataBase == 'win32'):
                db1 = True
            elif(dataBase == 'win64'):
                db2 = True

        self.assertTrue(db1)
        self.assertEqual(db1, db2)

        collections = dbClient.getCollections('win16', gHostAndPort)
        self.assertEqual(3, len(collections))
        self.assertEqual(['system.indexes', 'updates1', 'updates2'],
            collections)

        collections = dbClient.getCollections('win64', gHostAndPort)
        self.assertEqual(2, len(collections))
        self.assertEqual(['system.indexes', 'updates3'], collections)

        dbClient.dropTableInDB('win16', 'updates1', gHostAndPort)
        dbClient.dropTableInDB('win16', 'updates2', gHostAndPort)
        dbClient.dropTableInDB('win64', 'updates3', gHostAndPort)

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

    def test_addObjectIdField(self):

        updates = []
        updates.append({'KB': 3002657,
                        'Path': '\\3002657\\WindowsServer2003\\X64\\DEU\\'
                        'WindowsServer2003-KB3002657-x64-DEU.exe',
                        'Version': 'Windows Server 2003',
                        'Language': 'German',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x64'})
        updates.append({'KB': 3002657,
                        'Path': '\\3002657\\WindowsServer2003\\X64\\CHT\\'
                        'WindowsServer2003-KB3002657-x64-CHT.exe',
                        'Version': 'Windows Server 2003',
                        'Language': 'Chinese (Traditional)',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x64'})
        updates.append({'KB': 3002657,
                        'Path': '\\3002657\\WindowsServer2003\\X64\\CHS\\'
                        'WindowsServer2003-KB3002657-x64-CHS.exe',
                        'Version': 'Windows Server 2003',
                        'Language': 'Chinese (Simplified)',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x64'})
        updates.append({'KB': 3002657,
                        'Path': '\\3002657\\WindowsServer2003\\IA64\\JPN\\'
                        'WindowsServer2003-KB3002657-ia64-JPN.exe',
                        'Version': 'Windows Server 2003',
                        'Language': 'Japanese',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'IA64'})
        updates.append({'KB': 3002657,
                        'Path': '\\3002657\\WindowsServer2003\\IA64\\FRA\\'
                        'WindowsServer2003-KB3002657-ia64-FRA.exe',
                        'Version': 'Windows Server 2003',
                        'Language': 'French',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'IA64'})
        updates.append({'KB': 3002657,
                        'Path': '\\3002657\\WindowsServer2003\\IA64\\ENU\\'
                        'WindowsServer2003-KB3002657-ia64-ENU.exe',
                        'Version': 'Windows Server 2003',
                        'Language': 'English',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'IA64'})

        updates = db.mongoDB.addObjectIdField(updates)

        for up1 in updates:
            objectId1 = up1['_id']
            for up2 in updates:
                if up1 is not up2:
                    objectId2 = up2['_id']
                    self.assertNotEquals(objectId1, objectId2)

    def test_removeDubsByObjectId(self):

        updates = []
        updates.append({'KB': 3030377,
                        'Path': '\\3030377\\Windows8.1\\X86\\NEU\\'
                        'Windows8.1-KB3030377-x86.msu',
                        'Version': 'Windows 8.1',
                        'Language': 'Neutral',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x86'})
        updates.append({'KB': 3030377,
                        'Path': '\\3030377\\Windows8.1\\X64\\NEU\\'
                        'Windows8.1-KB3030377-x64.msu',
                        'Version': 'Windows 8.1',
                        'Language': 'Neutral',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x64'})
        updates.append({'KB': 3030377,
                        'Path': '\\3030377\\Windows8.1\\ARM\\NEU\\'
                        'Windows8.1-KB3030377-arm.msu',
                        'Version': 'Windows 8.1',
                        'Language': 'Neutral',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'ARM'})
        updates.append({'KB': 3030377,
                        'Path': '\\3030377\\Windows8\\X86\\NEU\\'
                        'Windows8-RT-KB3030377-x86.msu',
                        'Version': 'Windows 8',
                        'Language': 'Neutral',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x86'})
        updates.append({'KB': 3030377,
                        'Path': '\\3030377\\Windows8\\X64\\NEU\\'
                        'Windows8-RT-KB3030377-x64.msu',
                        'Version': 'Windows 8',
                        'Language': 'Neutral',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x64'})
        updates.append({'KB': 3030377,
                        'Path': '\\3030377\\Windows8\\ARM\\NEU\\'
                        'Windows8-RT-KB3030377-arm.msu',
                        'Version': 'Windows 8',
                        'Language': 'Neutral',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'ARM'})

        updates = db.mongoDB.pymongoDate2DateTime(updates, 'Date')
        updates = db.mongoDB.addObjectIdField(updates)
        dbClient.dropTableInDB('win64', 'updates3', gHostAndPort)
        dbClient.insertToDB('win64', 'updates3', gHostAndPort, updates)

        items = dbClient.getItemsFromDB('win64', 'updates3', gHostAndPort)

        updatesCount = len(updates)
        self.assertEquals(updatesCount, items.count())

        updates.append({'KB': 3030398,
                        'Path': '\\3030398\\WindowsVista\\X86\\NEU\\'
                        'Windows6.0-KB3030398-x86.msu',
                        'Version': 'Windows Vista',
                        'Language': 'Neutral',
                        'Date': datetime.date(2015, 3, 10),
                        'Type': 'x86'})

        updates = db.mongoDB.pymongoDate2DateTime(updates, 'Date')
        updates = db.mongoDB.addObjectIdField(updates)
        updates = db.mongoDB.removeDubsByObjectId('win64', 'updates3',
                                                  gHostAndPort, updates)

        self.assertEquals(1, len(updates))
        updatesCount += 1

        dbClient.insertToDB('win64', 'updates3', gHostAndPort, updates)
        items = dbClient.getItemsFromDB('win64', 'updates3', gHostAndPort)
        self.assertEquals(updatesCount, items.count())
        dbClient.dropTableInDB('win64', 'updates3', gHostAndPort)


if __name__ is '__main__':

    unittest.main()
