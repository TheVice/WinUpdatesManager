import os
import unittest
import updateToPackage


class TestSequenceFunctions(unittest.TestCase):

    def test_UpFile(self):

        upFile = updateToPackage.UpFile('Windows8.1-KB2904266-x64.msu')
        path = upFile.getPath()
        self.assertEqual(os.path.join('Windows8.1', 'x64', 'NEU'), path)

        upFile = updateToPackage.UpFile('Windows8.1-KB2904266-x86.msu')
        path = upFile.getPath()
        self.assertEqual(os.path.join('Windows8.1', 'x86', 'NEU'), path)

if __name__ == '__main__':
    unittest.main()
