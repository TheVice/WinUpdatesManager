import sys
from core.versions import Versions
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)
        self.mTypes = Versions()

    def test_getVersion(self):

        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], self.mTypes.getVersion(testData[0]))

    def test_getPathKey(self):

        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], self.mTypes.getPathKey(testData[0]))

    def test_isLanguageCanBeNeutral(self):

        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], self.mTypes.isLanguageCanBeNeutral(testData[0]))


if __name__ == '__main__':

    main()
