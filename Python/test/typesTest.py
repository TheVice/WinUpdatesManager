import sys
from core.types import Types
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):

        self.mJsonHelper = JsonHelper(__file__)
        self.mTypes = Types()

    def test_getType(self):

        testData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for i in testData:
            self.assertEqual(i[1], self.mTypes.getType(i[0]))

    def test_getPathKey(self):

        testData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for i in testData:
            self.assertEqual(i[1], self.mTypes.getPathKey(i[0]))


if __name__ == '__main__':

    main()
