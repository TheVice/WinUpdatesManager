import sys
import core.kb
import unittest
import updates4Target
from db.storage import Uif
from unittest.mock import MagicMock
from test.jsonHelper import JsonHelper


class StorageFromUpdates(Uif):

    def __init__(self, aUpdates):

        self.mUpdates = aUpdates


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))

    def test_updates4Target(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            storage = StorageFromUpdates(testData['Storage'])
            version = testData['Version']
            platform = testData['Platform']
            language = testData['Language']
            pathToReport = testData['PathToReport']

            coreKbGetKBsFromReportFile = None
            if None != pathToReport:
                coreKbGetKBsFromReportFile = core.kb.getKBsFromReportFile
                core.kb.getKBsFromReportFile = MagicMock(return_value=pathToReport)

            updates, version, platform, language, KBs = updates4Target.updates4Target(storage, version, platform, language, pathToReport)
            self.assertEqual(testData['ExpectedUpdates'], updates)
            self.assertEqual(testData['ExpectedVersion'], version)
            self.assertEqual(testData['ExpectedPlatform'], platform)
            self.assertEqual(testData['ExpectedLanguage'], language)
            self.assertEqual(testData['ExpectedKBs'], KBs)

            if None != pathToReport:
                core.kb.getKBsFromReportFile = coreKbGetKBsFromReportFile


if __name__ == '__main__':

    unittest.main()
