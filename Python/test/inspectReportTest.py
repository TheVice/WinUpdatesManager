import os
import unittest
import inspectReport
from db.storage import Uif
from test.jsonHelper import JsonHelper


class UpdatesWithGetMethod(Uif):

    def __init__(self, aData):

        self.mUpdates = aData


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'inspectReportTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_items2KBs(self):

        items = self.mJsonHelper.GetArray('test_items2KBs', 'items')
        refKbList = self.mJsonHelper.GetIntegerArray('test_items2KBs', 'refKbList')
        kbList = inspectReport.items2KBs(items)

        self.assertEqual(refKbList, kbList)

    def test_getData(self):

        updates = self.mJsonHelper.GetArray('test_getData', 'updates')
        coreUpdates = UpdatesWithGetMethod(updates)
        kbsToFind = self.mJsonHelper.GetIntegerArray('test_getData', 'kbsToFind')
        data = inspectReport.getData(coreUpdates, kbsToFind, {})
        updates = data.get('Updates')
        expectedCount = self.mJsonHelper.GetInteger('test_getData', 'ExpectedCount')
        self.assertEqual(expectedCount, len(updates))


if __name__ == '__main__':

    unittest.main()
