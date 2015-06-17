import os
import unittest
from core.types import Types
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'typesTest.json')
        self.mJsonHelper = JsonHelper(path)
        self.mTypes = Types()

    def test_getType(self):

        testData = self.mJsonHelper.GetTestInputOutputData('test_getType')
        for i in testData:
            self.assertEqual(i[1], self.mTypes.getType(i[0]))

    def test_getPathKey(self):

        testData = self.mJsonHelper.GetTestInputOutputData('test_getPathKey')
        for i in testData:
            self.assertEqual(i[1], self.mTypes.getPathKey(i[0]))


if __name__ == '__main__':

    unittest.main()
