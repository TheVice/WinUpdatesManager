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


def getDatesOfUpdates(aFolders):

    dates = []

    for folder in aFolders:
        if len(folder) != 4 or not folder.isdigit():
            continue

        year = '20' + folder[2:]
        month = folder[0:2]

        day = getDayFromYearMonthAndWeek(int(year), int(month), 2, 2)
        dates.append(datetime.date(int(year), int(month), day))

    return dates

