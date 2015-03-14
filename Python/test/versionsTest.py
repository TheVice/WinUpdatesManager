import unittest
import os
from core.versions import Versions


class TestSequenceFunctions(unittest.TestCase):

    def test_Versions(self):

        versions = Versions()

        path = os.sep + 'middle' + os.sep + 'of' + os.sep + 'nowhere' + os.sep
        self.assertEqual({'UNKNOWN VERSION': path}, versions.getVersion(path))
        self.assertEqual(versions.Win2k,
                        versions.getVersion(os.sep + 'Windows2000' + os.sep))

        self.assertEqual(os.sep + os.sep, versions.getPathKey(''))
        self.assertEqual(os.sep + 'Windows2000' + os.sep,
                         versions.getPathKey(versions.Win2k))

if __name__ == '__main__':

    unittest.main()
