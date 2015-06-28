import sys
import core.kb
import updates4Target
from db.storage import Uif
if 2 == sys.version_info[0]:
    from mock import MagicMock
else:
    from unittest.mock import MagicMock
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class StorageFromUpdates(Uif):

    def __init__(self, aUpdates):

        self.mUpdates = aUpdates


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

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

    main()
