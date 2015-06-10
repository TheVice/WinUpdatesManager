import os
import json
import unittest
import datetime
import getUif
from unittest.mock import MagicMock
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'getUifTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_getUpdatesFromPackage(self):

        data = self.mJsonHelper.GetTestRoot('test_getUpdatesFromPackage')
        for d in data:
            paths = d['paths']
            date = datetime.datetime.strptime(d['date'], '%Y, %m, %d')
            expectedUpdates = d['updates']

            updates = getUif.getUpdatesFromPackage(paths, date)

            for i in range(0, len(updates)):
                updates[i] = json.loads(updates[i])
            self.assertEqual(expectedUpdates, updates)

    def test_fromPath(self):

        data = self.mJsonHelper.GetTestRoot('test_fromPath')
        for d in data:
            mockData = d['mockData']
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

            expectedUpdates = d['updates']
            self.assertEqual(expectedUpdates, updates)

    def test_fromPathAndDate(self):

        data = self.mJsonHelper.GetTestRoot('test_fromPath')
        for d in data:
            mockData = d['mockData']
            m = mockData[0]
            key = list(m.keys())[0]
            osWalkReturnValue = []
            for p in m[key]:
                osWalkReturnValue.append((p['root'], p['dirs'], p['files']))

            osWalk = os.walk
            os.walk = MagicMock(return_value=osWalkReturnValue)

            updates = getUif.fromPathAndDate('', key)

            os.walk = osWalk

            expectedUpdates = []
            refDate = d['updates'][0]['Date']
            for refUp in d['updates']:
                if refUp['Date'] == refDate:
                    refUp['Path'] = os.path.normpath('{}{}{}'.format(os.sep, key, refUp['Path']))
                    expectedUpdates.append(refUp)

            for i in range(0, len(updates)):
                updates[i] = json.loads(updates[i])

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

    unittest.main()
