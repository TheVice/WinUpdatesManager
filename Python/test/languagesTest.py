import unittest
import os
from core.languages import Languages


class TestSequenceFunctions(unittest.TestCase):

    def test_Languages(self):

        languages = Languages()

        path = os.sep + 'middle' + os.sep + 'of' + os.sep + 'nowhere' + os.sep
        self.assertEqual({'UNKNOWN LANGUAGE': path},
                            languages.getLanguage(path))
        self.assertEqual(languages.Neutral,
                        languages.getLanguage(os.sep + 'NEU' + os.sep))

        self.assertEqual(os.sep + os.sep, languages.getPathKey(''))
        self.assertEqual(os.sep + 'Neutral' + os.sep,
                         languages.getPathKey(languages.Neutral))

if __name__ == '__main__':

    unittest.main()
