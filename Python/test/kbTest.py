import os
import sys
import core.kb
import unittest
import builtins
from unittest.mock import MagicMock
from test.jsonHelper import JsonHelper


class MockReport():

    mReport = None

    def __init__(self, aInit):
        if aInit is not None:
            MockReport.mReport = ''.join(aInit)
        else:
            MockReport.mReport = None

    @staticmethod
    def read():
        if MockReport.mReport is not None:
            return MockReport.mReport
        else:
            raise Exception('Report is empty')

    @staticmethod
    def close():
        pass


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))

    def test_getKB(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], core.kb.getKB(testData[0]))

    def test_getKBsFromReport(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData[1], core.kb.getKBsFromReport(testData[0]))

    def test_getKBsFromReportFile(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            builtinsOpen = builtins.open
            builtins.open = MagicMock(return_value=MockReport(testData['mockData']))

            try:
                self.assertEqual(testData['expectedUpdates'], core.kb.getKBsFromReportFile('reportFile'))
            except Exception:
                self.assertEqual('Unexpected error while work with file \'reportFile\' Report is empty',
                                 '{}'.format(sys.exc_info()[1]))

            builtins.open = builtinsOpen


if __name__ == '__main__':

    unittest.main()
