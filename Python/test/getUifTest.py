import os
import sys
import json
import getUif
import core.dates
from datetime import datetime
if 2 == sys.version_info[0]:
    from mock import patch, MagicMock
else:
    from unittest.mock import patch, MagicMock
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_getUpdatesFromPackage(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            paths = testData['paths']
            d = datetime.strptime(testData['date'], '%Y, %m, %d')
            expectedUpdates = testData['updates']

            updates = getUif.getUpdatesFromPackage(paths, d)

            for i in range(0, len(updates)):
                updates[i] = json.loads(updates[i])
            self.assertEqual(expectedUpdates, updates)

    def test_fromPath(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            osListDirReturn = []
            osWalkSideEffect = []

            for m in testData['mockData']:
                key = list(m.keys())[0]
                osListDirReturn.append(key)
                osWalkArray = m[key]
                osWalkReturnValue = []
                for p in osWalkArray:
                    osWalkReturnValue.append((p['root'], p['dirs'], p['files']))
                osWalkSideEffect.append(osWalkReturnValue)

            with patch('getUif.os.listdir') as osListDir:
                osListDir.return_value=osListDirReturn
                with patch('getUif.os.walk') as osWalk:
                    osWalk.side_effect=osWalkSideEffect

                    updates = getUif.fromPath('')
                    for i in range(0, len(updates)):
                        updates[i] = json.loads(updates[i])

                    expectedUpdates = testData['updates']
                    for i in range(0, len(expectedUpdates)):
                        d = expectedUpdates[i]['Date']
                        if 'datetime.now' in d:
                            d = eval(d)
                            expectedUpdates[i]['Date'] = core.dates.toString(d)
                    self.assertEqual(expectedUpdates, updates)

    def test_fromPathAndDate(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            mockData = testData['mockData']
            key = list(mockData.keys())[0]
            osWalkReturnValue = []
            for p in mockData[key]:
                osWalkReturnValue.append((p['root'], p['dirs'], p['files']))

            with patch('getUif.os.walk') as osWalk:
                osWalk.return_value=osWalkReturnValue

                updates = getUif.fromPathAndDate(key, key)

                for i in range(0, len(updates)):
                    updates[i] = json.loads(updates[i])

                expectedUpdates = testData['updates']
                self.assertEqual(expectedUpdates, updates)

    def test_getUpdates(self):
        sysArgvValues = [['getUif.py', ''], ['getUif.py', '', '0615']]
        updatesValues = [{'known': [{'Update': 'From Path'}], 'unKnown': []},
                         {'known': [{'Update': 'From Path and Date'}], 'unKnown': []}]

        for sysArgv, refUpdate in zip(sysArgvValues, updatesValues):
            with patch('getUif.fromPath') as getUifFromPath:
                getUifFromPath.return_value=[{'Update': 'From Path'}]
                with patch('getUif.fromPathAndDate') as getUifFromPathAndDate:
                    getUifFromPathAndDate.return_value=[{'Update': 'From Path and Date'}]
                    with patch('getUif.os.path.abspath') as osPathAbsPath:
                        osPathAbsPath.return_value=''

                        updates = getUif.getUpdates(sysArgv)

                        self.assertEqual(refUpdate, updates)


if __name__ == '__main__':

    main()
