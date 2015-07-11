import os
import sys
import webUi
from core.storage import getStorage
if 2 == sys.version_info[0]:
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock
from unittest import main, TestCase
from test.jsonHelper import JsonHelper
from test.storageTest import MockFile


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_index(self):
        storage = MagicMock()
        mainPage = webUi.Main(storage)
        template = mainPage.index()
        referenceTemplate = (
            '<!DOCTYPE html><html><head><meta charset=\'utf-8\'>'
            '<title>Windows Updates Getter</title></head><body>'
            '<a href=\'/view_updates\'>Go to view updates</a><br>'
            '<a href=\'/report_submit\'>Go to report submit</a><br>'
            '<a href=\'/batch_generator\'>Go to batch generator</a><br>'
            '</body></html>'
        )
        self.assertEqual(referenceTemplate, template)

    def test_report_submit(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            storage = MagicMock()
            storage.getAvalibleVersions = MagicMock(return_value = testData['versions'])
            storage.getAvalibleTypes = MagicMock(return_value = testData['types'])
            storage.getAvalibleLanguages = MagicMock(return_value = testData['languages'])

            mainPage = webUi.Main(storage)
            template = mainPage.report_submit()
            referenceTemplate = testData['referenceTemplate']

            self.assertEqual(referenceTemplate, template)

    def test_process_report(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            report = testData['report']
            version = testData['version']
            platform = testData['platform']
            language = testData['language']
            referenceTemplate = testData['referenceTemplate']

            with patch('core.storage.os.path.isfile'):
                with patch('core.storage.os.path.exists'):
                    patchName = '__builtin__.open' if 2 == sys.version_info[0] else 'builtins.open'
                    with patch(patchName) as mock_open:
                        mock_open.return_value = MockFile(testData['updates'])

                        storage = getStorage('file.uif')
                        mainPage = webUi.Main(storage)
                        template = mainPage.process_report(report, version, platform, language)
                        self.assertEqual(referenceTemplate, template)

    def test_batch_generator(self):
        getStorage = MagicMock()
        mainPage = webUi.Main(getStorage())
        template = mainPage.batch_generator()
        referenceTemplate = (
            '<!DOCTYPE html>'
            '<html><head>'
            '<meta charset=\'utf-8\'>'
            '<title>Windows Updates Getter</title>'
            '</head><body>'
            '<form action=\'process_generation\' method=\'post\'>'
            '<p><label>Root path (if req): <input list=\'Roots\''
            ' name=aRoot type=\'text\'></label>'
            '<datalist id=\'Roots\'>'
            '<option value=\'\\\\192.168.56.1\\0\'></option>'
            '<option value=\'Z:\\\'></option>'
            '</datalist>'
            '</p>'
            '<p><label>Switch: <input list=\'Switchs\''
            ' name=aSwitch type=\'text\'></label>'
            '<datalist id=\'Switchs\'>'
            '<option value=\'/quiet /norestart\'></option>'
            '<option value=\'-u -q -norestart\'></option>'
            '</datalist>'
            '</p>'
            '<p>'
            '<input type="checkbox" name="aCopyRequired">Copy updates into %TEMP% before installing<br>'
            '</p>'
            '<p><label><u>List of paths</u><br><br>'
            '<textarea name=aReport cols=100 rows=25 required></textarea>'
            '</label></p>'
            '<p><input type=submit value=\'Generate\'></p>'
            '</form>'
            '</body></html>'
        )
        self.assertEqual(referenceTemplate, template)

    def test_process_generation(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            lines = testData['lines']
            root = testData['root']
            switch = testData['switch']
            copyRequired = testData['copyRequired']
            referenceGenerate = testData['referenceGenerate']
            referenceGenerate = referenceGenerate.replace('os.linesep', os.linesep)
            getStorage = MagicMock()
            mainPage = webUi.Main(getStorage())
            generate = mainPage.process_generation(lines, root, switch, copyRequired)
            self.assertEqual(referenceGenerate, generate)

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
