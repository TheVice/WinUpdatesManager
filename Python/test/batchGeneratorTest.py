import os
import unittest
import batchGenerator
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'batchGeneratorTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_batchTemplate(self):
        referenceTemplate = self.mJsonHelper.GetSting('test_batchTemplate', 'referenceTemplate')
        self.assertEqual(referenceTemplate, batchGenerator.batchTemplate('1.txt', str(2), ' /quit'))

    def test_generate(self):
        generate = self.mJsonHelper.GetSting('test_generate', 'generate1')
        self.assertEqual(generate, batchGenerator.generate(['update.exe'], None, ' /quit /nobackup'))

        generate = self.mJsonHelper.GetSting('test_generate', 'generate2')
        self.assertEqual(generate, batchGenerator.generate(['update.exe'], 'Z:\\', ' /quit /nobackup'))

if __name__ == '__main__':

    unittest.main()
