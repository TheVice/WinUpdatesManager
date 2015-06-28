import sys
import unittest
from core.languages import Languages
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        if 2 == sys.version_info[0]:
            self.mJsonHelper = JsonHelper(__file__.replace('.pyc', '.json'))
        else:
            self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))
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

    unittest.main()
