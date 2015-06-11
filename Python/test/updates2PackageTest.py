import os
import unittest
import updates2Package
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'updates2PackageTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_getPath(self):

        data = self.mJsonHelper.GetTestInputOutputData('test_getPath')
        for d in data:
            self.assertEqual(d[1], updates2Package.UpFile(d[0]).getPath())

if __name__ == '__main__':

    unittest.main()
