import os
import unittest
import datetime
import core.dates
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'datesTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_getDayFromYearMonthAndWeek(self):

        data = self.mJsonHelper.GetTestInputOutputData('test_getDayFromYearMonthAndWeek')
        for i in data:
            inputValue = JsonHelper.string2intList(i[0])
            self.assertEqual(i[1], core.dates.getDayFromYearMonthAndWeek(inputValue[0], inputValue[1],
                                                                         inputValue[2], inputValue[3]))

    def test_getDatesForYearEdition(self):

        files = self.mJsonHelper.GetStingArray('test_getDatesForYearEdition', 'files')
        dates = core.dates.getDatesOfUpdates(files)
        correctDays = self.mJsonHelper.GetIntegerArray('test_getDatesForYearEdition', 'correctDays')

        for correctDay, date in zip(correctDays, dates):
            self.assertEqual(correctDay, date.day)

    def test_getDatesFromUIF_Recode(self):

        data = self.mJsonHelper.GetTestInputOutputData('test_getDatesFromUIF_Recode')
        for i in data:
            outputValue = JsonHelper.string2intList(i[1])
            self.assertEqual(datetime.date(outputValue[0], outputValue[1], outputValue[2]),
                             core.dates.getDatesFromUIF_Recode(i[0]))

if __name__ == '__main__':

    unittest.main()
