import os
import json
import unittest
import datetime
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
            ups = Updates()
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
                    u['Date'] = datetime.datetime.strptime(u['Date'], '%Y, %m, %d')
                for u in outUpdates:
                    u['Date'] = datetime.datetime.strptime(u['Date'], '%Y, %m, %d')

            upIn = Updates()
            upIn.addUpdates(inUpdates)
            upOut = Updates()
            upOut.addUpdates(outUpdates)

            Updates.sortByFieldUpToDown(upIn, sortField)

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
                    u['Date'] = datetime.datetime.strptime(u['Date'], '%Y, %m, %d')
                for u in outUpdates:
                    u['Date'] = datetime.datetime.strptime(u['Date'], '%Y, %m, %d')

            upIn = Updates()
            upIn.addUpdates(inUpdates)
            upOut = Updates()
            upOut.addUpdates(outUpdates)

            Updates.sortByFieldDownToUp(upIn, sortField)

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

    def test_getUpdatesFromPackage(self):

        data = self.mJsonHelper.GetTestRoot('test_getUpdatesFromPackage')
        for d in data:

            paths = d['paths']
            date = datetime.datetime.strptime(d['date'], '%Y, %m, %d')
            expectedUpdates = d['updates']
            updates = Updates.getUpdatesFromPackage(paths, date)
            for i in range(0, len(updates)):
                updates[i] = json.loads(updates[i])
            self.assertEqual(expectedUpdates, updates)


if __name__ == '__main__':

    unittest.main()
