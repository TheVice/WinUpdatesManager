import os
import unittest
from core.unknownSubstance import UnknownSubstance
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'unknownSubstanceTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_unknownSubstance(self):

        data = self.mJsonHelper.GetTestRoot('test_unknownSubstance')
        for d in data:
            key = list(d.keys())[0]
            self.assertEqual(d, UnknownSubstance.unknown(key, d[key]))

    def test_getItemByPath(self):

        data = self.mJsonHelper.GetTestRoot('test_getItemByPath')
        for d in data:
            self.assertEqual(d['output'], UnknownSubstance.getItemByPath(d['update'], d['input']))

    def test_getKeyPathByValue(self):

        data = self.mJsonHelper.GetTestRoot('test_getKeyPathByValue')
        for d in data:
            self.assertEqual(d['output'], UnknownSubstance.getKeyPathByValue(d['update'], d['input']))


if __name__ == '__main__':

    unittest.main()
