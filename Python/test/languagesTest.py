import unittest
import os
from core.languages import Languages
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'languagesTest.json')
        self.mJsonHelper = JsonHelper(path)
        self.mLanguages = Languages()

    def test_getLanguage(self):

        testData = self.mJsonHelper.GetTestInputOutputData('test_getLanguage')
        for i in testData:
            self.assertEqual(i[1], self.mLanguages.getLanguage(i[0]))

    def test_getPathKey(self):

        testData = self.mJsonHelper.GetTestInputOutputData('test_getPathKey')
        for i in testData:
            self.assertEqual(i[1], self.mLanguages.getPathKey(i[0]))

if __name__ == '__main__':

    unittest.main()
