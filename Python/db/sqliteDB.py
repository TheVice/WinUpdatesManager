import re
import sqlite3


def connect(aDbName):

    return sqlite3.connect(aDbName)


def disconnect(aConnection):

    aConnection.close()


def writeToDataBase(aConnection, aStatement):

    aConnection.executescript(aStatement)
    aConnection.commit()


def readFromDataBase(aConnection, aStatement, aFetch):

    cursor = aConnection.cursor()
    cursor.execute(aStatement)
    return aFetch(cursor)


def listTables(aConnection):

    statement = ('SELECT name FROM sqlite_master'
                 ' WHERE type LIKE \'table\''
                 ' ORDER BY name')
    tables = readFromDataBase(aConnection,
                              statement, lambda l: l.fetchall())

    for i in range(0, len(tables)):
        tables[i] = tables[i][0]
    return tables


def isTableExist(aConnection, aTable):

    statement = ('SELECT name FROM sqlite_master'
                 ' WHERE type LIKE \'table\''
                 ' AND name LIKE \'{}\''.format(aTable))
    return readFromDataBase(aConnection,
                            statement, lambda l: l.fetchone()) is not None


def listRows(aConnection, aTable):

    statement = ('SELECT sql FROM sqlite_master'
        ' WHERE tbl_name = \'{}\' AND type = \'table\''.format(aTable))
    tableInfo = readFromDataBase(aConnection,
                                 statement, lambda l: l.fetchone())

    if tableInfo is not None:
        tableInfo = tableInfo[0]

        rows = []
        rows.append(re.search('\([A-Za-z]\w+', tableInfo).group(0)[1:])

        while -1 != tableInfo.find(','):
            row = re.search(',[A-Za-z ]\w+', tableInfo).group(0)
            row = re.search('[A-Za-z]\w+', row).group(0)
            tableInfo = tableInfo[tableInfo.find(row) + len(row):]
            rows.append(row)

        tableInfo = rows

    return tableInfo


def isRowExist(aConnection, aTable, aRow):

    statement = ('SELECT sql FROM sqlite_master'
        ' WHERE tbl_name = \'{}\' AND type = \'table\''.format(aTable))
    tableInfo = readFromDataBase(aConnection,
                                 statement, lambda l: l.fetchone())

    if tableInfo is not None:
        tableInfo = tableInfo[0]

        if (-1 != tableInfo.find('({} '.format(aRow)) or
                -1 != tableInfo.find(',{} '.format(aRow)) or
                -1 != tableInfo.find(', {} '.format(aRow))):
            return True

    return False


def dropTable(aConnection, aTable):

    statement = ('DROP TABLE {}'.format(aTable))
    writeToDataBase(aConnection, statement)


def deleteFromTable(aConnection, aTable, aRows=None, aItem=None):

    statement = ('DELETE FROM {}'.format(aTable))

    if aRows and aItem:
        l = []
        for row, item in zip(aRows, aItem):
            l.append('{} = \'{}\''.format(row, item))
        l = '{}'.format(l)
        l = l.replace('[', '').replace(']', '')
        l = l.replace(',', ' AND')
        l = l.replace('"', '')
        statement = '{} WHERE {}'.format(statement, l)

    writeToDataBase(aConnection, statement)


def updateAtTable(aConnection, aTable, aRows, aItem, aCurrentItem):

    statement = ('UPDATE {}'.format(aTable))
    l = []
    for row, item in zip(aRows, aItem):
        l.append('{} = \'{}\''.format(row, item))
    l = '{}'.format(l)
    l = l.replace('[', '').replace(']', '')
    l = l.replace('"', '')
    statement = '{} SET {}'.format(statement, l)

    l = []
    for row, currentItem in zip(aRows, aCurrentItem):
        l.append('{} = \'{}\''.format(row, currentItem))
    l = '{}'.format(l)
    l = l.replace('[', '').replace(']', '')
    l = l.replace(',', ' AND')
    l = l.replace('"', '')
    statement = '{} WHERE {}'.format(statement, l)

    writeToDataBase(aConnection, statement)


def getFrom(aConnection, aTable, aRows=None):

    if aRows:
        aRows = '{}'.format(aRows)
        aRows = aRows.replace('[', '').replace(']', '')
        aRows = aRows.replace('\'', '')
        template = 'SELECT {} FROM {}'.format(aRows, aTable)
    else:
        template = 'SELECT * FROM {}'.format(aTable)

    items = readFromDataBase(aConnection, template, lambda l: l.fetchall())
    for i in range(0, len(items)):
        if 1 == len(items[i]):
            items[i] = items[i][0]
        else:
            items[i] = list(items[i])
    return items


def insertInto(aConnection, aTable, aItems, aRows=None):

    if aRows:
        aRows = '{}'.format(aRows)
        aRows = aRows.replace('[', '').replace(']', '')
        template = 'INSERT INTO {} (' + aRows + ') VALUES({});'
    else:
        template = 'INSERT INTO {} VALUES({});'

    statement = []
    for item in aItems:
        item = '{}'.format(item)
        item = item.replace('[', '').replace(']', '')
        statement.append(template.format(aTable, item))

    writeToDataBase(aConnection, ''.join(statement))
