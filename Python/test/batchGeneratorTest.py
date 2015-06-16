import sys
import unittest
import batchGenerator
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))

    def test_batchTemplate(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            path = testData['path']
            strNumber = testData['strNumber']
            switch = testData['switch']
            copyRequired = testData['copyRequired']
            referenceTemplate = testData['referenceTemplate']
            self.assertEqual(referenceTemplate, batchGenerator.batchTemplate(path, strNumber, switch, copyRequired))

    def test_generate(self):
        testsData = self.mJsonHelper.GetTestRoot(sys._getframe().f_code.co_name)
        for testData in testsData:
            lines = testData['lines']
            root = testData['root']
            switch = testData['switch']
            copyRequired = testData['copyRequired']
            referenceGenerate = testData['referenceGenerate']
            self.assertEqual(referenceGenerate, batchGenerator.generate(lines, root, switch, copyRequired))


if __name__ == '__main__':

    unittest.main()
