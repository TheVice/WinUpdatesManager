import os
import unittest
import datetime
import core.updates
from core.updates import Updates
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'updatesTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_addUpdates(self):

        data = self.mJsonHelper.GetTestRoot('test_addUpdates')
        for d in data:
            updates = d['updates']
            expectedCount = d['expectedCount']
            coreUpdates = Updates()
            coreUpdates.addUpdates(updates)
            self.assertEqual(expectedCount, len(coreUpdates))

    def test_addUpdate(self):

        data = self.mJsonHelper.GetTestRoot('test_addUpdate')
        for d in data:
            updates = d['updates']
            expectedCount = d['expectedCount']
            coreUpdates = Updates()
            for u in updates:
                coreUpdates.addUpdate(u['Path'], u['KB'], u['Version'], u['Type'], u['Language'], u['Date'])
            self.assertEqual(expectedCount, len(coreUpdates))

    def test_assignmentUp2Up(self):

        data = self.mJsonHelper.GetTestRoot('test_assignmentUp2Up')
        for d in data:
            ups = core.updates.Updates()
            ups.addUpdates(d['updates'])
            self.assertNotEqual(ups[0], ups[1])
            Updates.assignmentUp2Up(ups[0], ups[1])
            self.assertEqual(ups[0], ups[1])

    def test_exchangeUps(self):

       data = self.mJsonHelper.GetTestRoot('test_exchangeUps')
       for d in data:

           ups1 = Updates()
           ups1.addUpdates(d['updates'])
           ups2 = Updates()
           ups2.addUpdates(d['updates'])

           self.assertEqual(ups1[0], ups2[0])
           self.assertEqual(ups1[1], ups2[1])

           Updates.exchangeUps(ups1[0], ups1[1])

           self.assertNotEqual(ups1[0], ups2[0])
           self.assertNotEqual(ups1[1], ups2[1])
           self.assertEqual(ups1[0], ups2[1])
           self.assertEqual(ups1[1], ups2[0])

    def test_sortByFieldUpToDown(self):

        data = self.mJsonHelper.GetTestRoot('test_sortByFieldUpToDown')
        for d in data:
            inUpdates = d['inUpdates']
            outUpdates = d['outUpdates']
            sortField = d['sortField']
            if 'Date' == sortField:
                for u in inUpdates:
                    u['Date'] = JsonHelper.intList2Date(JsonHelper.string2intList(u['Date']))
                for u in outUpdates:
                    u['Date'] = JsonHelper.intList2Date(JsonHelper.string2intList(u['Date']))

            upIn = core.updates.Updates()
            upIn.addUpdates(inUpdates)
            upOut = core.updates.Updates()
            upOut.addUpdates(outUpdates)

            core.updates.Updates.sortByFieldUpToDown(upIn, sortField)

            self.assertEqual(len(upIn), len(upOut))
            for up1, up2 in zip(upIn, upOut):
                self.assertEqual(up1['Date'], up2['Date'])

    def test_sortByFieldDownToUp(self):

        data = self.mJsonHelper.GetTestRoot('test_sortByFieldDownToUp')
        for d in data:
            inUpdates = d['inUpdates']
            outUpdates = d['outUpdates']
            sortField = d['sortField']
            if 'Date' == sortField:
                for u in inUpdates:
                    u['Date'] = JsonHelper.intList2Date(JsonHelper.string2intList(u['Date']))
                for u in outUpdates:
                    u['Date'] = JsonHelper.intList2Date(JsonHelper.string2intList(u['Date']))

            upIn = core.updates.Updates()
            upIn.addUpdates(inUpdates)
            upOut = core.updates.Updates()
            upOut.addUpdates(outUpdates)

            core.updates.Updates.sortByFieldDownToUp(upIn, sortField)

            self.assertEqual(len(upIn), len(upOut))
            for up1, up2 in zip(upIn, upOut):
                self.assertEqual(up1['Date'], up2['Date'])

    def test_separateToKnownAndUnknown(self):

        data = self.mJsonHelper.GetTestRoot('test_separateToKnownAndUnknown')
        for d in data:
            updates = d['updates']
            unKnown = d['unKnown']
            known = d['known']
            self.assertEqual(unKnown, len(Updates.separateToKnownAndUnknown(updates).get('unKnown')))
            self.assertEqual(known, len(Updates.separateToKnownAndUnknown(updates).get('known')))

    def test_convertUifListIntoUpdates(self):

        data = self.mJsonHelper.GetTestRoot('test_convertUifListIntoUpdates')
        for d in data:
            updates = d['updates']
            expectedCount = d['expectedCount']
            self.assertEqual(expectedCount, len(Updates.convertUifListIntoUpdates(updates)))

    def test_getUpdatesFromPackage(self):

        data = self.mJsonHelper.GetTestRoot('test_getUpdatesFromPackage')
        for d in data:

            paths = d['paths']
            date = JsonHelper.string2intList(d['date'])
            date = datetime.datetime(date[0], date[1], date[2])
            updates = d['updates']
            for u in updates:
                u['Date'] = JsonHelper.string2intList(u['Date'])
                u['Date'] = datetime.datetime(u['Date'][0], u['Date'][1], u['Date'][2])
            self.assertEqual(updates, core.updates.getUpdatesFromPackage(paths, date))


if __name__ == '__main__':

    unittest.main()
