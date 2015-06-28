import sys
from unittest import main, TestCase
from core.unknownSubstance import UnknownSubstance
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):

        self.mJsonHelper = JsonHelper(__file__)

    def test_unknownSubstance(self):

        data = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for d in data:
            key = list(d.keys())[0]
            self.assertEqual(d, UnknownSubstance.unknown(key, d[key]))

    def test_getItemByPath(self):

        data = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for d in data:
            self.assertEqual(d['output'], UnknownSubstance.getItemByPath(d['update'], d['input']))

    def test_getKeyPathByValue(self):

        data = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for d in data:
            self.assertEqual(d['output'], UnknownSubstance.getKeyPathByValue(d['update'], d['input']))


if __name__ == '__main__':

    main()
