import unittest
import os
from core.unknownSubstance import UnknownSubstance


class TestSequenceFunctions(unittest.TestCase):

    def test_unknownSubstance(self):

        kb = 123
        lang = 'NEU'
        osType = 'x86'

        substance = UnknownSubstance.unknown('KB', kb)
        self.assertEqual({'KB': 123}, substance)
        substance = UnknownSubstance.unknown('Lang', lang)
        self.assertEqual({'Lang': 'NEU'}, substance)
        substance = UnknownSubstance.unknown('Type', osType)
        self.assertEqual({'Type': 'x86'}, substance)

    def test_getItemByPath(self):

        self.assertEqual(None, UnknownSubstance.getItemByPath({}, ''))
        d = {}
        d['kb'] = 123
        d['lang'] = 'NEU'
        d['osType'] = 'x86'
        d['path'] = 'Root'
        self.assertEqual('Root', UnknownSubstance.getItemByPath(d, 'path'))

    def test_getKeyPathByValue(self):

        self.assertEqual(os.sep + os.sep,
            UnknownSubstance.getKeyPathByValue({}, ''))
        d = {}
        d['kb'] = 123
        d['lang'] = 'NEU'
        d['osType'] = 'x86'
        d['path'] = 'Root'
        self.assertEqual('path',
            UnknownSubstance.getKeyPathByValue(d, 'Root'))

if __name__ == '__main__':

    unittest.main()
