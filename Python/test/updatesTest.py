import unittest
import os
import datetime
import core.updates
import db.uif
from core.versions import Versions
from core.types import Types
from core.languages import Languages


class TestSequenceFunctions(unittest.TestCase):

    def test_AddUpdates(self):

        items = []
        items.append({'_id': 'ObjectId(\'52a8e53ef1b5a171803d4163\')',
                      'Language': 'Neutral',
                      'Type': 'x64',
                      'KB': 2795944,
                      'Date': 'ISODate(\'2013-02-12T00:00:00Z\')',
                      'Version': 'Windows 8',
                      'Path': '\\2795944\\Windows8\\NEU\\x64' +
                      '\\Windows8-RT-KB2795944-x64.msu'})
        items.append({'_id': 'ObjectId(\'52ac66c0f1b5a1372437be3c\')',
                      'Language': 'Neutral',
                      'Type': 'x64',
                      'KB': 2795944,
                      'Date': 'ISODate(\'2013-02-12T00:00:00Z\')',
                      'Version': 'Windows 8',
                      'Path': '\\2795944\\Windows8\\NEU\\x64' +
                      '\\Windows8-RT-KB2795944-x64.msu'})
        items.append({'_id': 'ObjectId(\'52ac6deff1b5a1b01096772d\')',
                      'Language': 'Neutral',
                      'Type': 'x64',
                      'KB': 2795944,
                      'Date': 'ISODate(\'2013-02-12T00:00:00Z\')',
                      'Version': 'Windows 8',
                      'Path': '\\2795944\\Windows8\\NEU\\x64' +
                      '\\Windows8-RT-KB2795944-x64.msu'})
        updates = core.updates.Updates()
        updates.addUpdates(items)
        self.assertEqual(1, len(updates))

    def test_Updates(self):

        updates = core.updates.Updates()

        self.assertEqual(0, len(updates))
        self.assertRaises(IndexError, updates.__getitem__, -1)
        self.assertRaises(IndexError, updates.__getitem__, 0)
        self.assertRaises(IndexError, updates.__getitem__, 1)

        for update in updates:
            self.fail('Actually there are no updates! ', update)

        updates.addUpdate('Some' + os.sep + 'Path', 123,
                'Win32', '80x86', 'English', datetime.datetime(1970, 1, 1))
        updates.addUpdate('Some' + os.sep + 'Path', 123,
                'Win32', '80x86', 'English', datetime.datetime(1970, 1, 1))
        updates.addUpdate('Some' + os.sep + 'Path2', 456,
                'Win64', 'x86-64', 'Russian', datetime.datetime(2008, 12, 11))
        updates.addUpdate('Some' + os.sep + 'Path2', 456,
                'Win64', 'x86-64', 'Russian', datetime.datetime(2008, 12, 11))

        items = []
        items.append({'Path': 'Some' + os.sep + 'Path', 'KB': 123,
                      'Version': 'Win32', 'Type': '80x86',
                      'Language': 'English',
                      'Date': datetime.datetime(1970, 1, 1)})
        items.append({'Path': 'Some' + os.sep + 'Path', 'KB': 123,
                      'Version': 'Win32', 'Type': '80x86',
                      'Language': 'English',
                      'Date': datetime.datetime(1970, 1, 1)})
        items.append({'Path': 'Some' + os.sep + 'Path2', 'KB': 456,
                      'Version': 'Win64', 'Type': 'x86-64',
                      'Language': 'Russian',
                      'Date': datetime.datetime(2008, 12, 11)})

        updates.addUpdates(items)

        self.assertEqual(2, len(updates))
        self.assertRaises(IndexError, updates.__getitem__, -1)
        try:
            self.assertEqual(updates.__getitem__(0)['Type'], '80x86')
            self.assertEqual(updates.__getitem__(1)['Language'], 'Russian')
        except:
            self.fail('Actually there are present updates!')
        self.assertRaises(IndexError, updates.__getitem__, 3)

        versions = ['Win64', 'Win32']
        for update, version in zip(updates, versions):
            self.assertEqual(version, update['Version'])

        versions = ['Win32', 'Win64']
        for i in range(0, 2):
            self.assertEqual(updates[i]['Version'], versions[i])

        self.assertEqual('Win32', updates[0]['Version'])
        self.assertEqual('Win64', updates[1]['Version'])

    def test_QueryUpdates(self):

        items = []
        items.append({'_id': 'ObjectId(\'52a8e53ef1b5a171803d4163\')',
                      'Language': 'Neutral',
                      'Type': 'x64',
                      'KB': 2795944,
                      'Date': 'ISODate(\'2013-02-12T00:00:00Z\')',
                      'Version': 'Windows 8',
                      'Path': '\\2795944\\Windows8\\NEU\\x64' +
                      '\\Windows8-RT-KB2795944-x64.msu'})
        items.append({'_id': 'ObjectId(\'52ac66c0f1b5a1372437be3c\')',
                      'Language': 'Neutral',
                      'Type': 'x64',
                      'KB': 2795945,
                      'Date': 'ISODate(\'2013-02-12T00:00:00Z\')',
                      'Version': 'Windows 8',
                      'Path': '\\2795945\\Windows8\\NEU\\x64' +
                      '\\Windows8-RT-KB2795944-x64.msu'})
        items.append({'_id': 'ObjectId(\'52ac6deff1b5a1b01096772d\')',
                      'Language': 'Neutral',
                      'Type': 'x64',
                      'KB': 2795946,
                      'Date': 'ISODate(\'2013-02-12T00:00:00Z\')',
                      'Version': 'Windows 8',
                      'Path': '\\2795946\\Windows8\\NEU\\x64' +
                      '\\Windows8-RT-KB2795944-x64.msu'})

        updates = core.updates.Updates()
        updates.addUpdates(items)
        query = {}
        query['Path'] = ('\\2795944\\Windows8\\NEU\\' +
                         'x64\\Windows8-RT-KB2795944-x64.msu')
        query['KB'] = 2795944
        query['Version'] = 'Windows 8'
        query['Type'] = 'x64'
        query['Language'] = 'Neutral'
        query['Date'] = 'ISODate(\'2013-02-12T00:00:00Z\')'
        up2 = updates.getUpdates(dict(query))
        self.assertEqual(1, len(up2))

        query = {}
        query['Type'] = 'x64'
        up2 = updates.getUpdates(dict(query))
        self.assertEqual(3, len(up2))

        query = {}
        query['Language'] = 'Neutral'
        up2 = updates.getUpdates(dict(query))
        self.assertEqual(3, len(up2))

        query = {}
        query['Language'] = ''
        up2 = updates.getUpdates(dict(query))
        self.assertEqual(0, len(up2))

        query = {}
        up2 = updates.getUpdates(dict(query))
        self.assertEqual(3, len(up2))

    def test_QueryUpdates2(self):

        lines = []
        lines.append('{\'Date\': datetime.date(2014, 5, 13), \'Path\': \'\\2920189\\WindowsServer2012R2\\X64\\NEU\\Windows8.1-KB2920189-x64.msu\', \'Type\': \'x64\', \'Version\': \'Windows Server 2012 R2\', \'KB\': 2920189, \'Language\': \'Neutral\'}')
        lines.append('{\'Date\': datetime.date(2014, 5, 13), \'Path\': \'\\2920189\\WindowsServer2012\\X64\\NEU\\Windows8-RT-KB2920189-x64.msu\', \'Type\': \'x64\', \'Version\': \'Windows Server 2012\', \'KB\': 2920189, \'Language\': \'Neutral\'}')
        lines.append('{\'Date\': datetime.date(2014, 5, 13), \'Path\': \'\\2920189\\Windows8.1\\X86\\NEU\\Windows8.1-KB2920189-x86.msu\', \'Type\': \'x86\', \'Version\': \'Windows 8.1\', \'KB\': 2920189, \'Language\': \'Neutral\'}')
        lines.append('{\'Date\': datetime.date(2014, 5, 13), \'Path\': \'\\2920189\\Windows8.1\\X64\\NEU\\Windows8.1-KB2920189-x64.msu\', \'Type\': \'x64\', \'Version\': \'Windows 8.1\', \'KB\': 2920189, \'Language\': \'Neutral\'}')
        lines.append('{\'Date\': datetime.date(2014, 5, 13), \'Path\': \'\\2920189\\Windows8\\X86\\NEU\\Windows8-RT-KB2920189-x86.msu\', \'Type\': \'x86\', \'Version\': \'Windows 8\', \'KB\': 2920189, \'Language\': \'Neutral\'}')
        lines.append('{\'Date\': datetime.date(2014, 5, 13), \'Path\': \'\\2920189\\Windows8\\X64\\NEU\\Windows8-RT-KB2920189-x64.msu\', \'Type\': \'x64\', \'Version\': \'Windows 8\', \'KB\': 2920189, \'Language\': \'Neutral\'}')

        updates = []
        versions = Versions()
        types = Types()
        languages = Languages()

        for line in lines:
            db.uif.getUpdateFromLine(line, versions,
                types, languages, updates)

        self.assertEqual(len(lines), len(updates))
        query = {}
        query['Version'] = 'Windows 8'
        query['Type'] = 'x64'
        query['Language'] = 'Neutral'
        updates2 = core.updates.Updates()
        updates2.addUpdates(updates)
        updates = updates2
        up = updates.getUpdates(dict(query))
        self.assertEqual(1, len(up))

    def test_getUpdatesFromPackage(self):

        paths = ['E:' + os.sep + '1212' + os.sep + '2761465' + os.sep +
            'WindowsServer2003' + os.sep + 'X64' + os.sep + 'ENU' +
            os.sep + 'IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE',
           'E:' + os.sep + '1212' + os.sep + '2761465' + os.sep +
           'WindowsServer2003' + os.sep + 'X64' + os.sep + 'ENU' + os.sep +
           'IE7-WINDOWSSERVER2003.WINDOWSXP-KB2761465-X64-ENU.EXE']
        date = datetime.datetime(2012, 12, 1)
        updates = core.updates.getUpdatesFromPackage(paths, date)

        self.assertEqual(1, len(updates))

        kbs = [2761465]
        versions = [core.updates.Versions().Win2k3]
        types = ['x64']
        languages = ['English']

        for i in range(0, len(updates)):
            self.assertEqual(paths[i][2:], updates[i]['Path'])
            self.assertEqual(kbs[i], updates[i]['KB'])
            self.assertEqual(versions[i], updates[i]['Version'])
            self.assertEqual(types[i], updates[i]['Type'])
            self.assertEqual(languages[i], updates[i]['Language'])
            self.assertEqual(date, updates[i]['Date'])

    def test_separateToKnownAndUnknown(self):

        updates = [{'KB': {}, 'Version': {}, 'Type': {}, 'Language': {}}]
        data = core.updates.separateToKnownAndUnknown(updates)

        self.assertEqual(1, len(data.get('unKnown')))
        self.assertEqual(0, len(data.get('known')))

        updates = [{'KB': 123, 'Version': {}, 'Type': {}, 'Language': {}}]
        data = core.updates.separateToKnownAndUnknown(updates)

        self.assertEqual(1, len(data.get('unKnown')))
        self.assertEqual(0, len(data.get('known')))

        updates = [{'KB': 123, 'Version': 'Windows',
                    'Type': {}, 'Language': {}}]
        data = core.updates.separateToKnownAndUnknown(updates)

        self.assertEqual(1, len(data.get('unKnown')))
        self.assertEqual(0, len(data.get('known')))

        updates = [{'KB': 123, 'Version': 'Windows',
                    'Type': 'x86', 'Language': {}}]
        data = core.updates.separateToKnownAndUnknown(updates)

        self.assertEqual(1, len(data.get('unKnown')))
        self.assertEqual(0, len(data.get('known')))

        updates = [{'KB': 123, 'Version': 'Windows',
                    'Type': 'x86', 'Language': 'Neutral'}]
        data = core.updates.separateToKnownAndUnknown(updates)

        self.assertEqual(0, len(data.get('unKnown')))
        self.assertEqual(1, len(data.get('known')))

    def test_assignmentUp2Up(self):

        ups = core.updates.Updates()
        ups.addUpdateDict({'Date': datetime.date(2014, 7, 11), 'KB': 324189})
        ups.addUpdateDict({'Date': datetime.date(2014, 5, 13), 'KB': 292189})

        core.updates.assignmentUp2Up(ups[0], ups[1])

        self.assertEqual(ups[0], ups[1])

    def test_exchangeUps(self):

        ups = core.updates.Updates()
        ups.addUpdateDict({'Date': datetime.date(2014, 7, 11), 'KB': 324189})
        ups.addUpdateDict({'Date': datetime.date(2014, 5, 13), 'KB': 292189})

        core.updates.exchangeUps(ups[0], ups[1])

        self.assertNotEqual(ups[0], ups[1])

    def test_sort_by_date(self):

        upIn = core.updates.Updates()
        upIn.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 35764})
        upIn.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 52515})
        upIn.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 69413})
        upIn.addUpdateDict({'Date': datetime.date(2014, 3, 28), 'KB': 43915})
        upIn.addUpdateDict({'Date': datetime.date(2014, 6, 20), 'KB': 63237})
        upIn.addUpdateDict({'Date': datetime.date(2014, 1, 1), 'KB': 29068})
        upIn.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 56402})
        upIn.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 53064})
        upIn.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 42119})
        upIn.addUpdateDict({'KB': 72550, 'Date': datetime.date(2014, 6, 25)})
        upIn.addUpdateDict({'KB': 65153, 'Date': datetime.date(2014, 3, 3)})
        upIn.addUpdateDict({'KB': 64589, 'Date': datetime.date(2014, 3, 3)})
        upIn.addUpdateDict({'KB': 32858, 'Date': datetime.date(2014, 3, 3)})
        upIn.addUpdateDict({'KB': 75060, 'Date': datetime.date(2014, 5, 5)})
        upIn.addUpdateDict({'KB': 52820, 'Date': datetime.date(2014, 3, 18)})
        upIn.addUpdateDict({'KB': 52570, 'Date': datetime.date(2014, 3, 18)})
        upIn.addUpdateDict({'KB': 61927, 'Date': datetime.date(2014, 3, 18)})
        upIn.addUpdateDict({'KB': 26868, 'Date': datetime.date(2014, 3, 18)})
        upIn.addUpdateDict({'KB': 83810, 'Date': datetime.date(2014, 3, 18)})
        upIn.addUpdateDict({'KB': 31790, 'Date': datetime.date(2014, 2, 27)})
        upIn.addUpdateDict({'KB': 84359, 'Date': datetime.date(2014, 2, 27)})
        upIn.addUpdateDict({'KB': 19907, 'Date': datetime.date(2014, 2, 27)})
        upIn.addUpdateDict({'KB': 61161, 'Date': datetime.date(2014, 2, 27)})
        upIn.addUpdateDict({'Date': datetime.date(2014, 7, 11), 'KB': 324189})
        upIn.addUpdateDict({'Date': datetime.date(2014, 5, 13), 'KB': 292189})

        upRef = core.updates.Updates()
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 1), 'KB': 29068})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 42119})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 53064})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 56402})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 35764})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 52515})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 69413})
        upRef.addUpdateDict({'KB': 19907, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'KB': 31790, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'KB': 61161, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'KB': 84359, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'KB': 32858, 'Date': datetime.date(2014, 3, 3)})
        upRef.addUpdateDict({'KB': 64589, 'Date': datetime.date(2014, 3, 3)})
        upRef.addUpdateDict({'KB': 65153, 'Date': datetime.date(2014, 3, 3)})
        upRef.addUpdateDict({'KB': 26868, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 52570, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 52820, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 61927, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 83810, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'Date': datetime.date(2014, 3, 28), 'KB': 43915})
        upRef.addUpdateDict({'KB': 75060, 'Date': datetime.date(2014, 5, 5)})
        upRef.addUpdateDict({'Date': datetime.date(2014, 5, 13), 'KB': 292189})
        upRef.addUpdateDict({'Date': datetime.date(2014, 6, 20), 'KB': 63237})
        upRef.addUpdateDict({'KB': 72550, 'Date': datetime.date(2014, 6, 25)})
        upRef.addUpdateDict({'Date': datetime.date(2014, 7, 11), 'KB': 324189})

        core.updates.sortByFieldUpToDown(upIn, 'Date')

        self.assertEqual(len(upIn), len(upRef))
        for up, rf in zip(upIn, upRef):
            self.assertEqual(up['Date'], rf['Date'])

        upRef = core.updates.Updates()
        upRef.addUpdateDict({'Date': datetime.date(2014, 7, 11), 'KB': 324189})
        upRef.addUpdateDict({'KB': 72550, 'Date': datetime.date(2014, 6, 25)})
        upRef.addUpdateDict({'Date': datetime.date(2014, 6, 20), 'KB': 63237})
        upRef.addUpdateDict({'Date': datetime.date(2014, 5, 13), 'KB': 292189})
        upRef.addUpdateDict({'KB': 75060, 'Date': datetime.date(2014, 5, 5)})
        upRef.addUpdateDict({'Date': datetime.date(2014, 3, 28), 'KB': 43915})
        upRef.addUpdateDict({'KB': 83810, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 61927, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 52820, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 52570, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 26868, 'Date': datetime.date(2014, 3, 18)})
        upRef.addUpdateDict({'KB': 65153, 'Date': datetime.date(2014, 3, 3)})
        upRef.addUpdateDict({'KB': 64589, 'Date': datetime.date(2014, 3, 3)})
        upRef.addUpdateDict({'KB': 32858, 'Date': datetime.date(2014, 3, 3)})
        upRef.addUpdateDict({'KB': 84359, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'KB': 61161, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'KB': 31790, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'KB': 19907, 'Date': datetime.date(2014, 2, 27)})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 69413})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 52515})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 25), 'KB': 35764})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 56402})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 53064})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 19), 'KB': 42119})
        upRef.addUpdateDict({'Date': datetime.date(2014, 1, 1), 'KB': 29068})

        core.updates.sortByFieldDownToUp(upIn, 'Date')

        self.assertEqual(len(upIn), len(upRef))
        for up, rf in zip(upIn, upRef):
            self.assertEqual(up['Date'], rf['Date'])

    def test_sort_by_path(self):

        upIn = core.updates.Updates()
        upIn.addUpdateDict({'Path': 'B'})
        upIn.addUpdateDict({'Path': 'C'})
        upIn.addUpdateDict({'Path': 'A'})

        upRef = core.updates.Updates()
        upRef.addUpdateDict({'Path': 'A'})
        upRef.addUpdateDict({'Path': 'B'})
        upRef.addUpdateDict({'Path': 'C'})

        core.updates.sortByFieldUpToDown(upIn, 'Path')

        self.assertEqual(len(upIn), len(upRef))
        for up, rf in zip(upIn, upRef):
            self.assertEqual(up['Path'], rf['Path'])


if __name__ == '__main__':

    unittest.main()
