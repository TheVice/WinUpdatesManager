import unittest
import db.storage


class TestSequenceFunctions(unittest.TestCase):

    def test_getStorage(self):

        self.assertTrue(isinstance(db.storage.getStorage(':memory:'), db.storage.SQLite))
        self.assertTrue(isinstance(db.storage.getStorage('mongodb://localhost:27017/'), db.storage.MongoDB))

    def test_get(self):

        storage = db.storage.getStorage('mongodb://localhost:27017/')
        self.assertLess(0, len(list(storage.get({}))))


if __name__ == '__main__':

    unittest.main()
