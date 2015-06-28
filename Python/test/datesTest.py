import sys
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
        if 2 == sys.version_info[0]:
            self.mJsonHelper = JsonHelper(__file__.replace('.pyc', '.json'))
        else:
            self.mJsonHelper = JsonHelper(__file__.replace('.py', '.json'))

    def test_getDayFromYearMonthAndWeek(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            inputValue = string2intList(testData[0])
            self.assertEqual(testData[1], core.dates.getDayFromYearMonthAndWeek(inputValue[0], inputValue[1],
                                                                                inputValue[2], inputValue[3]))

    def test_getDatesForYearEdition(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            try:
                self.assertEqual(testData[1], core.dates.getDate(testData[0]).day)
            except Exception:
                self.assertEqual(testData[1], str(sys.exc_info()[1]))


if __name__ == '__main__':

    unittest.main()
