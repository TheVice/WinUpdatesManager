import unittest
import os
import core.kb
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'kbTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_getKB(self):

        testData = self.mJsonHelper.GetTestInputOutputData('test_getKB')
        for i in testData:
            self.assertEqual(i[1], core.kb.getKB(i[0]))

    def test_getKBsFromReport(self):

        testData = self.mJsonHelper.GetTestInputOutputData('test_getKBsFromReport')
        for i in testData:
            self.assertEqual(i[1], core.kb.getKBsFromReport(i[0]))


if __name__ == '__main__':

    unittest.main()
