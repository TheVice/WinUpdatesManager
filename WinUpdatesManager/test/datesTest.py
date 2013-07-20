import unittest
import core
import core.dates


class TestSequenceFunctions(unittest.TestCase):

    def test_getDayFromYearMonthAndWeek(self):
        self.assertEqual(9,
            core.dates.getDayFromYearMonthAndWeek(2013, 7, 2, 2))

    def test_getDatesForYearEdition(self):
        files = ['0112', '0212', '0312', '0412', '0512', '0612']
        correctDays = [10, 14, 13, 10, 8, 12]
        dates = core.dates.getDatesOfUpdates(files)
        i = 0
        for date in dates:
            self.assertEqual(correctDays[i], date.day)
            i += 1


if __name__ == '__main__':
    unittest.main()
