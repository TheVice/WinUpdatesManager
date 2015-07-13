import sys
from datetime import datetime, date


def getDayFromYearMonthAndWeek(aYear, aMonth, aWeekOfMonth, aDayOfWeek):

    day = 1
    dayOfWeek = date.isoweekday(date(aYear, aMonth, day))
    if dayOfWeek == aDayOfWeek:
        day = day + (aWeekOfMonth - 1) * 7
    elif dayOfWeek > aDayOfWeek:
        if aWeekOfMonth == 1:
            raise Exception('Bad input: Week of month is incorrect')
        day = day + 7 - (dayOfWeek - aDayOfWeek) + (aWeekOfMonth - 1) * 7
    elif dayOfWeek < aDayOfWeek:
        day = day + aDayOfWeek - dayOfWeek + (aWeekOfMonth - 1) * 7
    return day


def getDate(aFolderName):

    if(len(aFolderName) != 4):
        raise Exception('Length of folder name \'{}\' not equal to 4'.format(aFolderName))

    year = '20{}'.format(aFolderName[2:4])
    month = aFolderName[0:2]

    if not year.isdigit() or not month.isdigit() or int(month) > 12:
        raise Exception('Year \'{}\' or month \'{}\' not digital or month is great than 12'.format(year, month))

    day = getDayFromYearMonthAndWeek(int(year), int(month), 2, 2)
    return date(int(year), int(month), day)


def toDate(aDate):

    if isinstance(aDate, list):
        for i in range(0, len(aDate)):
            aDate[i] = toDate(aDate[i])
    elif isinstance(aDate, str):
        return datetime.strptime(aDate, '%Y, %m, %d').date()
    elif 2 == sys.version_info[0] and isinstance(aDate, unicode):
        aDate = toDate(aDate.encode('utf-8'))
    elif isinstance(aDate, datetime):
        return aDate.date()
    return aDate


def toString(aDate):

    if isinstance(aDate, list):
        for i in range(0, len(aDate)):
            aDate[i] = toString(aDate[i])
    elif isinstance(aDate, date) or isinstance(aDate, datetime):
        return '{}, {}, {}'.format(aDate.year, aDate.month, aDate.day)
    elif 2 == sys.version_info[0] and isinstance(aDate, unicode):
        aDate = toString(aDate.encode('utf-8'))
    return aDate


def toDateTime(aDate):

    if isinstance(aDate, list):
        for i in range(0, len(aDate)):
            aDate[i] = toDateTime(aDate[i])
    elif isinstance(aDate, str):
        return datetime.strptime(aDate, '%Y, %m, %d')
    elif 2 == sys.version_info[0] and isinstance(aDate, unicode):
        aDate = toDateTime(aDate.encode('utf-8'))
    elif isinstance(aDate, date):
        return datetime(aDate.year, aDate.month, aDate.day)
    return aDate
