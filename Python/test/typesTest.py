import unittest
import os
from core.types import Types


class TestSequenceFunctions(unittest.TestCase):

    def test_Types(self):

        types = Types()

        path = os.sep + 'middle' + os.sep + 'of' + os.sep + 'nowhere' + os.sep
        self.assertEqual({'UNKNOWN TYPE': path}, types.getType(path))
        self.assertEqual(types.x86,
                        types.getType(os.sep + 'x86' + os.sep))

        self.assertEqual(os.sep + os.sep, types.getPathKey(''))
        self.assertEqual(os.sep + 'x86' + os.sep,
                         types.getPathKey(types.x86))

if __name__ == '__main__':

    unittest.main()
