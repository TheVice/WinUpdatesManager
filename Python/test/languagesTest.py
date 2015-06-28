import sys
from unittest import main, TestCase
from core.languages import Languages
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)
        self.mLanguages = Languages()

    def test_getLanguage(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], self.mLanguages.getLanguage(testData[0]))

    def test_getPathKey(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], self.mLanguages.getPathKey(testData[0]))


if __name__ == '__main__':

    main()
