import os
import sys
import unittest
import datetime
from core.updates import Updates
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        if 2 == sys.version_info[0]:
            self.mJsonHelper = JsonHelper(__file__.replace('.pyc', '.json'))
        else:
            self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))

    def test_addUpdates(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            updates = Updates()
            updates.addUpdates(testData['updates'])
            self.assertEqual(len(testData['expectedUpdates']), len(updates))
            for refUp, up in zip(testData['expectedUpdates'], updates):
                self.assertEqual(refUp, up)

    def test_addUpdate(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            updates = Updates()
            for update in  testData['updates']:
                updates.addUpdate(update['Path'], update['KB'], update['Version'], update['Type'], update['Language'], update['Date'])
            self.assertEqual(len(testData['expectedUpdates']), len(updates))
            for refUp, up in zip(testData['expectedUpdates'], updates):
                self.assertEqual(refUp, up)

    def test_next(self):

        updates = Updates()
        updates.addUpdateDict({'KB': 1})
        updates.addUpdateDict({'KB': 2})

        self.assertEqual({'KB': 2}, updates.__next__())
        self.assertEqual({'KB': 1}, updates.next())

    def test___getitem__(self):

        updates = Updates()
        updates.addUpdateDict({})
        with self.assertRaises(IndexError):
            updates[-1]
        with self.assertRaises(IndexError):
            updates[len(updates)]

    def test___str__(self):

        updates = Updates()
        updates.addUpdateDict({})
        self.assertEqual('{}{}{}'.format('{', '}', os.linesep), '{}'.format(updates))

    def test_assignmentUp2Up(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            updates = Updates()
            updates.addUpdates(testData['updates'])
            self.assertNotEqual(updates[0], updates[1])
            Updates.assignmentUp2Up(updates[0], updates[1])
            self.assertEqual(updates[0], updates[1])

    def test_exchangeUps(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:

            updates1 = Updates()
            updates1.addUpdates(testData['updates'])
            updates2 = Updates()
            updates2.addUpdates(testData['updates'])

            self.assertEqual(updates1[0], updates2[0])
            self.assertEqual(updates1[1], updates2[1])
            self.assertNotEqual(updates1[0], updates2[1])
            self.assertNotEqual(updates1[1], updates2[0])

            Updates.exchangeUps(updates1[0], updates1[1])

            self.assertNotEqual(updates1[0], updates2[0])
            self.assertNotEqual(updates1[1], updates2[1])
            self.assertEqual(updates1[0], updates2[1])
            self.assertEqual(updates1[1], updates2[0])

    def test_sortByFieldUpToDown(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            updates = testData['updates']
            expectedUpdates = testData['expectedUpdates']
            sortField = testData['sortField']

            if 'Date' == sortField:
                for update in updates:
                    update['Date'] = datetime.datetime.strptime(update['Date'], '%Y, %m, %d')
                for update in expectedUpdates:
                    update['Date'] = datetime.datetime.strptime(update['Date'], '%Y, %m, %d')

            coreUpdates = Updates()
            coreUpdates.addUpdates(updates)
            coreExpectedUpdates = Updates()
            coreExpectedUpdates.addUpdates(expectedUpdates)

            Updates.sortByFieldUpToDown(coreUpdates, sortField)

            self.assertEqual(len(coreExpectedUpdates), len(coreUpdates))
            for refUp, up in zip(coreExpectedUpdates, coreUpdates):
                self.assertEqual(refUp['Date'], up['Date'])

    def test_sortByFieldDownToUp(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            updates = testData['updates']
            expectedUpdates = testData['expectedUpdates']
            sortField = testData['sortField']
            if 'Date' == sortField:
                for update in updates:
                    update['Date'] = datetime.datetime.strptime(update['Date'], '%Y, %m, %d')
                for update in expectedUpdates:
                    update['Date'] = datetime.datetime.strptime(update['Date'], '%Y, %m, %d')

            coreUpdates = Updates()
            coreUpdates.addUpdates(updates)
            coreExpectedUpdates = Updates()
            coreExpectedUpdates.addUpdates(expectedUpdates)

            Updates.sortByFieldDownToUp(coreUpdates, sortField)

            self.assertEqual(len(coreExpectedUpdates), len(coreUpdates))
            for refUp, up in zip(coreExpectedUpdates, coreUpdates):
                self.assertEqual(refUp['Date'], up['Date'])

    def test_separateToKnownAndUnknown(self):

        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            self.assertEqual(testData['unKnown'], len(Updates.separateToKnownAndUnknown(testData['updates']).get('unKnown')))
            self.assertEqual(testData['known'], len(Updates.separateToKnownAndUnknown(testData['updates']).get('known')))


if __name__ == '__main__':

    unittest.main()
