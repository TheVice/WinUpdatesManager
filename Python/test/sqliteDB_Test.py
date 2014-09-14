import unittest
import datetime
import db.sqliteDB


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        self.dataBase = db.sqliteDB.connect(':memory:')
        self.assertNotEqual(None, self.dataBase)

        db.sqliteDB.createTableKBs(self.dataBase)
        db.sqliteDB.createTableDates(self.dataBase)
        db.sqliteDB.createTableVersions(self.dataBase)
        db.sqliteDB.createTableTypes(self.dataBase)
        db.sqliteDB.createTableLanguages(self.dataBase)
        db.sqliteDB.createTablePaths(self.dataBase)
        db.sqliteDB.createTableUpdates(self.dataBase)

    def test_complex(self):

        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase, 'KBs'))
        self.assertNotEqual(None,
                                db.sqliteDB.findTable(self.dataBase, 'Dates'))
        self.assertNotEqual(None,
                            db.sqliteDB.findTable(self.dataBase, 'Versions'))
        self.assertNotEqual(None,
                            db.sqliteDB.findTable(self.dataBase, 'Types'))
        self.assertNotEqual(None,
                            db.sqliteDB.findTable(self.dataBase, 'Languages'))
        self.assertNotEqual(None, db.sqliteDB.findTable(self.dataBase,
                                                        'Paths'))

        self.assertEqual(None, db.sqliteDB.getIDFrom(self.dataBase,
                                                    'KBs', 'id', 1))
        db.sqliteDB.insertInto(self.dataBase, 'KBs', 'id', 1)
        self.assertNotEqual(None, db.sqliteDB.getIDFrom(self.dataBase, 'KBs',
                                                        'id', 1))

        self.assertEqual(['Dates', 'KBs', 'Languages', 'Paths', 'Types',
                          'Updates', 'Versions', 'sqlite_sequence'],
                         db.sqliteDB.listTables(self.dataBase))

        update = {'Date': datetime.date(2011, 5, 10),
                 'Language': 'German',
                 'Type': 'IA64',
                 'KB': 2524426,
                 'Version': 'Windows Server 2003',
                 'Path': '\\2524426\\WindowsServer2003\\ia64\\DEU\\' +
                         'WINDOWSSERVER2003-KB2524426-IA64-DEU.EXE'}

        self.assertEqual([], db.sqliteDB.getUpdates(self.dataBase, update))
        db.sqliteDB.addUpdate(self.dataBase, update)
        self.assertNotEqual([],
                                db.sqliteDB.getUpdates(self.dataBase, update))
        update['Path'] = '?'
        self.assertEqual([], db.sqliteDB.getUpdates(self.dataBase, update))

        self.assertNotEqual(None,
            db.sqliteDB.getIDFrom(self.dataBase, 'KBs', 'id', update['KB']))
        self.assertEqual(None,
        db.sqliteDB.getIDFrom(self.dataBase, 'KBs', 'id', update['KB'] + 1))

        self.assertNotEqual(None, db.sqliteDB.getDateByID(self.dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getDateByID(self.dataBase, 2))

        self.assertNotEqual(None, db.sqliteDB.getPathByID(self.dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getPathByID(self.dataBase, 2))

        self.assertNotEqual(None, db.sqliteDB.getVersionByID(self.dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getVersionByID(self.dataBase, 2))

        self.assertNotEqual(None, db.sqliteDB.getTypeByID(self.dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getTypeByID(self.dataBase, 2))

        self.assertNotEqual(None,
                                db.sqliteDB.getLanguageByID(self.dataBase, 1))
        self.assertEqual(None, db.sqliteDB.getLanguageByID(self.dataBase, 2))

        update['Path'] = ('\\2524426\\WindowsServer2003\\ia64\\DEU\\' +
                         'WINDOWSSERVER2003-KB2524426-IA64-DEU.EXE')

        self.assertNotEqual([],
            db.sqliteDB.getUpdates(self.dataBase, update))
        update['KB'] += 1
        self.assertEqual([], db.sqliteDB.getUpdates(self.dataBase, update))

    def test_getUpdates(self):

        updates = [
            {'Type': 'x64',
            'Date': datetime.date(2014, 7, 8),
            'Language': 'Neutral', 'KB': 2974008,
            'Version': 'Windows Server 2012 R2',
            'Path': '\\2974008\\WindowsServer2012R2\\X64\\' +
            'NEU\\Windows8.1-KB2974008-x64.msu'},
            {'KB': 2966072,
            'Version': 'Windows Server 2012',
            'Date': datetime.date(2014, 6, 10),
            'Path': '\\2966072\\WindowsServer2012\\X64\\' +
            'NEU\\Windows8-RT-KB2966072-x64.msu',
            'Type': 'x64',
            'Language': 'Neutral'},
            {'Date': datetime.date(2014, 5, 13),
            'Path': '\\2953522\\WindowsServer2008R2\\X64' +
            '\\NEU\\IE9-Windows6.1-KB2953522-x64.msu',
            'Type': 'x64',
            'Version': 'Windows Server 2008 R2',
            'KB': 2953522,
            'Language': 'Neutral'},
            {'Date': datetime.date(2014, 5, 13),
            'Path': '\\2931354\\WindowsServer2008\\X64\\' +
            'NEU\\Windows6.0-KB980842-x64.msu',
            'Type': 'x64',
            'Version': 'Windows Server 2008',
            'KB': 980842,
            'Language': 'Neutral'},
            {'Version':
                {'UNKNOWN VERSION': '\\2916036\\X86\\' +
                'ENU\\WindowsServer2003-KB2916036-x86-ENU.exe'},
            'KB': 2916036,
            'Language': 'English',
            'Date': datetime.date(2014, 2, 11),
            'Path': '\\2916036\\X86' +
            '\\ENU\\WindowsServer2003-KB2916036-x86-ENU.exe',
            'Type': 'x86'},
            {'Language': 'English',
            'Type': 'x86',
            'KB': 2570947,
            'Date': datetime.date(2011, 9, 13),
            'Version': 'Windows 2000',
            'Path': '\\2570947\\Windows2000\\x86\\' +
            'ENU\\WINDOWS2000-KB2570947-X86-CUSTOM-ENU.EXE'}
        ]
        for update in updates:
            db.sqliteDB.addUpdate(self.dataBase, update)

        query = {'KB': 2966072}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(1, len(updates))

        query = {'Date': datetime.date(2014, 5, 13)}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(2, len(updates))

        query = {'Language': 'English'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(2, len(updates))

        query = {'Language': 'Neutral'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(4, len(updates))

        query = {'Version': 'UNKNOWN VERSION'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(1, len(updates))

        query = {'Type': 'x86'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(2, len(updates))

        query = {'Date': datetime.date(2014, 7, 8), 'Version': 'Windows 2000'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(0, len(updates))

        query = {'Date': datetime.date(2014, 8, 12)}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(0, len(updates))

        query = {'Version': 'Windows XP Embedded'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(0, len(updates))

        query = {'Type': 'IA64'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(0, len(updates))

        query = {'Language': 'NEU'}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(0, len(updates))

        query = {}
        updates = db.sqliteDB.getUpdates(self.dataBase, query)
        self.assertEqual(6, len(updates))

    def test_getUpdatesByKBInPath(self):

        updates = [
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Neutral',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2008 R2',
            'Path': '\\2524426\\WindowsServer2008R2\\x64' +
            '\\NEU\\WINDOWS6.1-KB2524426-X64.MSU'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Neutral',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2008',
            'Path': '\\2524426\\WindowsServer2008\\x86' +
            '\\NEU\\WINDOWS6.0-KB2524426-X86.MSU'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Neutral',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2008',
            'Path': '\\2524426\\WindowsServer2008\\x64' +
            '\\NEU\\WINDOWS6.0-KB2524426-X64.MSU'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Turkish',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\TRK\\WINDOWSSERVER2003-KB2524426-X86-TRK.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Swedish',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\SVE\\WINDOWSSERVER2003-KB2524426-X86-SVE.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Russian',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\RUS\\WINDOWSSERVER2003-KB2524426-X86-RUS.EXE'},
        {'Date': datetime.date(2011, 5, 10),
            'Language': 'Portuguese (Portugal)',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\PTG\\WINDOWSSERVER2003-KB2524426-X86-PTG.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Portuguese (Brazil)',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\PTB\\WINDOWSSERVER2003-KB2524426-X86-PTB.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Polish',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\PLK\\WINDOWSSERVER2003-KB2524426-X86-PLK.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Dutch',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\NLD\\WINDOWSSERVER2003-KB2524426-X86-NLD.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Korean',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\KOR\\WINDOWSSERVER2003-KB2524426-X86-KOR.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Japanese',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\JPN\\WINDOWSSERVER2003-KB2524426-X86-JPN.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Italian',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\ITA\\WINDOWSSERVER2003-KB2524426-X86-ITA.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Hungarian',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\HUN\\WINDOWSSERVER2003-KB2524426-X86-HUN.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'French',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\FRA\\WINDOWSSERVER2003-KB2524426-X86-FRA.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Spanish',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\ESN\\WINDOWSSERVER2003-KB2524426-X86-ESN.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'English',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\ENU\\WINDOWSSERVER2003-KB2524426-X86-ENU.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'German',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\DEU\\WINDOWSSERVER2003-KB2524426-X86-DEU.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Czech',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\CSY\\WINDOWSSERVER2003-KB2524426-X86-CSY.EXE'},
        {'Date': datetime.date(2011, 5, 10),
            'Language': 'Chinese (Traditional)',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\CHT\\WINDOWSSERVER2003-KB2524426-X86-CHT.EXE'},
        {'Date': datetime.date(2011, 5, 10),
            'Language': 'Chinese (Simplified)',
            'Type': 'x86', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x86' +
            '\\CHS\\WINDOWSSERVER2003-KB2524426-X86-CHS.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Russian',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\RUS\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-RUS.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Portuguese (Brazil)',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\PTB\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-PTB.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Korean',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\KOR\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-KOR.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Japanese',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\JPN\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-JPN.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Italian',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\ITA\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-ITA.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'French',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\FRA\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-FRA.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Spanish',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\ESN\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-ESN.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'English',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\ENU\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-ENU.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'German',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\DEU\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-DEU.EXE'},
        {'Date': datetime.date(2011, 5, 10),
            'Language': 'Chinese (Traditional)',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\CHT\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-CHT.EXE'},
        {'Date': datetime.date(2011, 5, 10),
            'Language': 'Chinese (Simplified)',
            'Type': 'x64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\x64' +
            '\\CHS\\WINDOWSSERVER2003.WINDOWSXP-KB2524426-X64-CHS.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'Japanese',
            'Type': 'IA64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\ia64' +
            '\\JPN\\WINDOWSSERVER2003-KB2524426-IA64-JPN.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'French',
            'Type': 'IA64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\ia64' +
            '\\FRA\\WINDOWSSERVER2003-KB2524426-IA64-FRA.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'English',
            'Type': 'IA64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\ia64' +
            '\\ENU\\WINDOWSSERVER2003-KB2524426-IA64-ENU.EXE'},
        {'Date': datetime.date(2011, 5, 10), 'Language': 'German',
            'Type': 'IA64', 'KB': 2524426, 'Version': 'Windows Server 2003',
            'Path': '\\2524426\\WindowsServer2003\\ia64' +
            '\\DEU\\WINDOWSSERVER2003-KB2524426-IA64-DEU.EXE'}
        ]

        for update in updates:
            db.sqliteDB.addUpdate(self.dataBase, update)

        updates = db.sqliteDB.getUpdatesByKBInPath(self.dataBase, 'JPN')
        self.assertEqual(3, len(updates))

        updates = db.sqliteDB.getUpdatesByKBInPath(self.dataBase, 'ia64')
        self.assertEqual(4, len(updates))

    def tearDown(self):

        db.sqliteDB.disconnect(self.dataBase)

if __name__ == '__main__':

    unittest.main()
