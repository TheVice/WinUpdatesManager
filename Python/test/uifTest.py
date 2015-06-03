import os
import unittest
import db.uif
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'uifTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_prepareLineToParse(self):

        inLine = self.mJsonHelper.GetTestVariable('test_prepareLineToParse', 'inLine')
        outLine = self.mJsonHelper.GetTestVariable('test_prepareLineToParse', 'outLine')
        self.assertEqual(outLine, db.uif.prepareLineToParse(inLine))

    def test_getValue(self):

        inLine = self.mJsonHelper.GetTestVariable('test_getValue', 'inLine')
        inLine = db.uif.prepareLineToParse(inLine)
        self.assertEqual(self.mJsonHelper.GetTestVariable('test_getValue', 'Path'), db.uif.getValue(inLine, 'Path'))
        self.assertEqual(self.mJsonHelper.GetTestVariable('test_getValue', 'KB'), int(db.uif.getValue(inLine, 'KB')))
        self.assertEqual(self.mJsonHelper.GetTestVariable('test_getValue', 'Version'), db.uif.getValue(inLine, 'Version'))
        self.assertEqual(self.mJsonHelper.GetTestVariable('test_getValue', 'Type'), db.uif.getValue(inLine, 'Type'))
        self.assertEqual(self.mJsonHelper.GetTestVariable('test_getValue', 'Language'), db.uif.getValue(inLine, 'Language'))
        self.assertEqual(self.mJsonHelper.GetTestVariable('test_getValue', 'Date'), db.uif.getValue(inLine, 'Date'))

    # def test_getUpdateFromLine(self):
    # def test_getUpdatesFromFile(self):
    # def test_getUpdatesFromStorage(self):
    # def test_get(self):
    # def test_showDubs(self):

if __name__ == '__main__':

    unittest.main()
