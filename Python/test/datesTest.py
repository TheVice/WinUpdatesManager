import os
import unittest
import datetime
import core.dates
from test.jsonHelper import JsonHelper


def string2intList(aInput):

    output = []
    start = 0
    end = 1

    while start < end:

        end = aInput.find(',', start)
        if (end == -1):
            output.append(int(aInput[start:]))
        else:
            output.append(int(aInput[start:end]))
            start = end + 1
            end = start + 1

    return output

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        path = '{}{}{}{}{}'.format(os.path.abspath(os.curdir), os.sep, 'test', os.sep, 'datesTest.json')
        self.mJsonHelper = JsonHelper(path)

    def test_getDayFromYearMonthAndWeek(self):

        inputData = self.mJsonHelper.GetTestRoot('test_getDayFromYearMonthAndWeek')
        for i in inputData:
            inputValue = list(i.keys())[0]
            outputValue = i[inputValue]
            inputValue = string2intList(inputValue)

            self.assertEqual(outputValue, core.dates.getDayFromYearMonthAndWeek(inputValue[0], inputValue[1],
                                                                                inputValue[2], inputValue[3]))

    def test_getDatesForYearEdition(self):

        files = self.mJsonHelper.GetStingArray('test_getDatesForYearEdition', 'files')
        dates = core.dates.getDatesOfUpdates(files)
        correctDays = self.mJsonHelper.GetIntegerArray('test_getDatesForYearEdition', 'correctDays')

        for correctDay, date in zip(correctDays, dates):
            self.assertEqual(correctDay, date.day)

    def test_getDatesFromUIF_Recode(self):

        inputData = self.mJsonHelper.GetTestRoot('test_getDatesFromUIF_Recode')
        for i in inputData:
            inputValue = list(i.keys())[0]
            outputValue = i[inputValue]
            outputValue = string2intList(outputValue)

            self.assertEqual(datetime.date(outputValue[0], outputValue[1], outputValue[2]),
                             core.dates.getDatesFromUIF_Recode(inputValue))

if __name__ == '__main__':

    unittest.main()
