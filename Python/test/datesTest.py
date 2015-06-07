import os
import unittest
import core.dates
from test.jsonHelper import JsonHelper

def string2intList(aInput):

    output = []
    start = 0
    end = 1

    while start < end:

        end = aInput.find(',', start)
        if -1 == end:
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

        data = self.mJsonHelper.GetTestInputOutputData('test_getDayFromYearMonthAndWeek')
        for i in data:
            inputValue = string2intList(i[0])
            self.assertEqual(i[1], core.dates.getDayFromYearMonthAndWeek(inputValue[0], inputValue[1],
                                                                         inputValue[2], inputValue[3]))

    def test_getDatesForYearEdition(self):

        data = self.mJsonHelper.GetTestInputOutputData('test_getDatesForYearEdition')
        for i in data:
            self.assertEqual(i[1], core.dates.getDate(i[0]).day)


if __name__ == '__main__':

    unittest.main()
