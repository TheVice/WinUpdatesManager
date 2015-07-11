import sys
import webUi
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_decodeQuery(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], webUi.Main.decodeQuery(testData[0]))

    def test_encodeQuery(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[0], webUi.Main.encodeQuery(testData[1]))

    def test_decodeSort(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], webUi.Main.decodeSort(testData[0]))

    def test_encodeSort(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[0], webUi.Main.encodeSort(testData[1]))

    def test_normalize(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            template = testData['template']
            parameterName = testData['parameterName']
            parameter = testData['parameter']
            expectedTemplate = testData['expectedTemplate']

            self.assertEqual(expectedTemplate, webUi.Main.normalize(template, parameterName, parameter))


if __name__ == '__main__':

    main()
