import unittest
import core.dates


class TestSequenceFunctions(unittest.TestCase):

    def test_getDayFromYearMonthAndWeek(self):

        self.assertEqual(9,
            core.dates.getDayFromYearMonthAndWeek(2013, 7, 2, 2))

    def test_getDatesForYearEdition(self):

        files = ['0112', '0212', '0312', 'abcd', '0412', 'Addons', '0512',
                 '12qw','0612', '0', '0211-1', 'af64']
        correctDays = [10, 14, 13, 10, 8, 12, 8]
        dates = core.dates.getDatesOfUpdates(files)

        for correctDay, date in zip(correctDays, dates):
            self.assertEqual(correctDay, date.day)


if __name__ == '__main__':

    unittest.main()
