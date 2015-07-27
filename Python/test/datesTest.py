import sys
import core.dates
from datetime import datetime
from unittest import main, TestCase
from test.jsonHelper import JsonHelper


class TestSequenceFunctions(TestCase):

    def setUp(self):
        self.mJsonHelper = JsonHelper(__file__)

    def test_getDayFromYearMonthAndWeek(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            inputValue = eval(testData[0])
            try:
                self.assertEqual(testData[1], core.dates.getDayFromYearMonthAndWeek(inputValue[0], inputValue[1],
                                                                                    inputValue[2], inputValue[3]))
            except:
                self.assertEqual(testData[1], '{}'.format(sys.exc_info()[1]))

    def test_getDatesForYearEdition(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            try:
                self.assertEqual(testData[1], core.dates.getDate(testData[0]).day)
            except Exception:
                self.assertEqual(testData[1], '{}'.format(sys.exc_info()[1]))

    def test_toDate(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            inputDate = eval(testData[0])
            expectedDate = eval(testData[1])
            correctedDate = core.dates.toDate(inputDate)
            self.assertEqual(expectedDate, correctedDate)
            correctedDate = core.dates.toDate([inputDate])
            self.assertEqual([expectedDate], correctedDate)
            if 2 == sys.version_info[0] and isinstance(inputDate, str):
                inputDate = unicode(inputDate)
                correctedDate = core.dates.toDate(inputDate)
                self.assertEqual(expectedDate, correctedDate)
                correctedDate = core.dates.toDate([inputDate])
                self.assertEqual([expectedDate], correctedDate)

    def test_toString(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            inputDate = eval(testData[0])
            expectedDate = eval(testData[1])
            correctedDate = core.dates.toString(inputDate)
            self.assertEqual(expectedDate, correctedDate)
            correctedDate = core.dates.toString([inputDate])
            self.assertEqual([expectedDate], correctedDate)
            if 2 == sys.version_info[0] and isinstance(inputDate, str):
                inputDate = unicode(inputDate)
                correctedDate = core.dates.toString(inputDate)
                self.assertEqual(expectedDate, correctedDate)
                correctedDate = core.dates.toString([inputDate])
                self.assertEqual([expectedDate], correctedDate)

    def test_toDateTime(self):
        testsData = self.mJsonHelper.GetTestInputOutputData(sys._getframe().f_code.co_name)
        for testData in testsData:
            inputDate = eval(testData[0])
            expectedDate = eval(testData[1])
            correctedDate = core.dates.toDateTime(inputDate)
            self.assertEqual(expectedDate, correctedDate)
            correctedDate = core.dates.toDateTime([inputDate])
            self.assertEqual([expectedDate], correctedDate)
            if 2 == sys.version_info[0] and isinstance(inputDate, str):
                inputDate = unicode(inputDate)
                correctedDate = core.dates.toDateTime(inputDate)
                self.assertEqual(expectedDate, correctedDate)
                correctedDate = core.dates.toDateTime([inputDate])
                self.assertEqual([expectedDate], correctedDate)


if __name__ == '__main__':

    main()
