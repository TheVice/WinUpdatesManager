import os
import sys
import json
import getUif
import datetime
if 2 == sys.version_info[0]:
    from mock import MagicMock
else:
    from unittest.mock import MagicMock
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_getUpdatesFromPackage(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            paths = testData['paths']
            date = datetime.datetime.strptime(testData['date'], '%Y, %m, %d')
            expectedUpdates = testData['updates']

            updates = getUif.getUpdatesFromPackage(paths, date)

            for i in range(0, len(updates)):
                updates[i] = json.loads(updates[i])
            self.assertEqual(expectedUpdates, updates)

    def test_fromPath(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            mockData = testData['mockData']
            osListDirReturn = []
            osWalkSideEffect = []
            for m in mockData:
                key = list(m.keys())[0]
                osListDirReturn.append(key)
                osWalkArray = m[key]
                osWalkReturnValue = []
                for p in osWalkArray:
                    osWalkReturnValue.append((p['root'], p['dirs'], p['files']))
                osWalkSideEffect.append(osWalkReturnValue)

            osListDir = os.listdir
            os.listdir = MagicMock(return_value=osListDirReturn)
            osWalk = os.walk
            os.walk = MagicMock(side_effect=osWalkSideEffect)

            updates = getUif.fromPath('')

            os.listdir = osListDir
            os.walk = osWalk

            for i in range(0, len(updates)):
                updates[i] = json.loads(updates[i])

            expectedUpdates = testData['updates']
            self.assertEqual(expectedUpdates, updates)

    def test_fromPathAndDate(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            mockData = testData['mockData']
            key = list(mockData.keys())[0]
            osWalkReturnValue = []
            for p in mockData[key]:
                osWalkReturnValue.append((p['root'], p['dirs'], p['files']))

            osWalk = os.walk
            os.walk = MagicMock(return_value=osWalkReturnValue)

            updates = getUif.fromPathAndDate(key, key)

            os.walk = osWalk

            for i in range(0, len(updates)):
                updates[i] = json.loads(updates[i])

            expectedUpdates = testData['updates']
            self.assertEqual(expectedUpdates, updates)

    def test_getUpdates(self):

        sysArgvValues = [['getUif.py', ''], ['getUif.py', '', '0615']]
        updatesValues = [{'known': [{'Update': 'From Path'}], 'unKnown': []},
                         {'known': [{'Update': 'From Path and Date'}], 'unKnown': []}]

        for sysArgv, refUpdate in zip(sysArgvValues, updatesValues):

            getUifFromPath = getUif.fromPath
            getUifFromPathAndDate = getUif.fromPathAndDate
            osPathAbsPath = os.path.abspath

            getUif.fromPath = MagicMock(return_value=[{'Update': 'From Path'}])
            getUif.fromPathAndDate = MagicMock(return_value=[{'Update': 'From Path and Date'}])
            os.path.abspath = MagicMock(return_value='')

            updates = getUif.getUpdates(sysArgv)

            getUif.fromPath = getUifFromPath
            getUif.fromPathAndDate = getUifFromPathAndDate
            os.path.abspath = osPathAbsPath

            self.assertEqual(refUpdate, updates)


if __name__ == '__main__':

    main()
