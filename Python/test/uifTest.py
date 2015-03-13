import unittest
import db.uif


class TestSequenceFunctions(unittest.TestCase):

    def test_prepareLineToParse(self):

        line = ('{\'Type\': \'x86\', \'Date\': datetime.date(2013, 2, 12),' +
            ' \'KB\': 2802968, \'Language\': \'Turkish\', \'Path\':' +
            ' \'\\2802968\\WindowsXP\\x86\\TRK\\' +
            'WINDOWSXP-KB2802968-X86-TRK.EXE\', \'Version\': \'Windows XP\'}')

        line = db.uif.prepareLineToParse(line)
        newLine = ('{\'Type\': \'x86\',' +
            '\t\'Date\': \'datetime.date(2013, 2, 12),' +
            '\t\'KB\': \'2802968,\t\'Language\': \'Turkish\',\t\'Path\':' +
            ' \'\\2802968\\WindowsXP\\x86\\TRK\\' +
            'WINDOWSXP-KB2802968-X86-TRK.EXE\',' +
            '\t\'Version\': \'Windows XP\'\t}')
        self.assertEqual(newLine, line)

    def test_getUIFvalue(self):

        line = ('{\'Type\': \'x86\', \'Date\': datetime.date(2013, 2, 12),' +
            ' \'KB\': 2802968, \'Language\': \'Turkish\', \'Path\':' +
            ' \'\\2802968\\WindowsXP\\x86\\TRK\\' +
            'WINDOWSXP-KB2802968-X86-TRK.EXE\', \'Version\': \'Windows XP\'}')

        line = db.uif.prepareLineToParse(line)

        self.assertEqual('\\2802968\\WindowsXP\\x86\\TRK\\' +
            'WINDOWSXP-KB2802968-X86-TRK.EXE',
            db.uif.getValue(line, 'Path'))
        self.assertEqual(2802968, int(db.uif.getValue(line, 'KB')))
        self.assertEqual('Windows XP',
            db.uif.getValue(line, 'Version'))
        self.assertEqual('x86', db.uif.getValue(line, 'Type'))
        self.assertEqual('Turkish',
            db.uif.getValue(line, 'Language'))
        self.assertEqual('datetime.date(2013, 2, 12)',
            db.uif.getValue(line, 'Date'))

if __name__ == '__main__':

    unittest.main()
