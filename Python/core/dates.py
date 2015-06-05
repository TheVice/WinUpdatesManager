import datetime


def getDayFromYearMonthAndWeek(aYear, aMonth, aWeekOfMonth, aDayOfWeek):

    day = 1
    dayInMonth = 0

    while day <= 31:
        dayOfWeek = datetime.date.isoweekday(datetime.date(aYear, aMonth, day))

        if dayOfWeek == aDayOfWeek:
            dayInMonth += 1

        if aWeekOfMonth == dayInMonth:
            break

        day += 1

    return day


def getDate(aFolderName):

    if(len(aFolderName) != 4):
        return None

    year = '20{}'.format(aFolderName[2:4])
    month = aFolderName[0:2]

    if not year.isdigit() or not month.isdigit() or int(month) > 12:
        return None

    day = getDayFromYearMonthAndWeek(int(year), int(month), 2, 2)
    return datetime.date(int(year), int(month), day)
