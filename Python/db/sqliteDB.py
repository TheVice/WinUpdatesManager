import re
import sys
import sqlite3
if 2 == sys.version_info[0]:
    import thread
else:
    import _thread as thread


def connect(aDataBase):

    return sqlite3.connect(aDataBase)


def disconnect(aConnection):

    aConnection.close()


def write(aDataBase, aStatement, aMutex=None):

    if isinstance(aDataBase, sqlite3.Connection):
        connection = aDataBase
    else:
        connection = connect(aDataBase)

    connection.executescript(aStatement)
    connection.commit()

    if not isinstance(aDataBase, sqlite3.Connection):
        disconnect(connection)

    if aMutex:
        aMutex.acquire()


def read(aDataBase, aStatement, aFetch, aMutex=None, aReturnData=None):

    if isinstance(aDataBase, sqlite3.Connection):
        connection = aDataBase
    else:
        connection = connect(aDataBase)

    cursor = connection.cursor()
    cursor.execute(aStatement)
    data = aFetch(cursor)

    if not isinstance(aDataBase, sqlite3.Connection):
        disconnect(connection)

    if aMutex:
        aReturnData.append(data)
        aMutex.acquire()
    else:
        return data


def writeAsync(aDataBase, aStatement):

    mutex = thread.allocate_lock()
    thread.start_new_thread(write, (aDataBase, aStatement, mutex))
    while not mutex.locked():
        pass


def readAsync(aDataBase, aStatement, aFetch):

    l = []
    mutex = thread.allocate_lock()
    thread.start_new_thread(read, (aDataBase, aStatement, aFetch, mutex, l))
    while not mutex.locked():
        pass
    return l[0]


def listTables(aDataBase):

    statement = ('SELECT name FROM sqlite_master'
                 ' WHERE type LIKE \'table\''
                 ' ORDER BY name')
    tables = read(aDataBase, statement, lambda l: l.fetchall())

    for i in range(0, len(tables)):
        tables[i] = tables[i][0]
    return tables


def isTableExist(aDataBase, aTable):

    statement = ('SELECT name FROM sqlite_master'
                 ' WHERE type LIKE \'table\''
                 ' AND name LIKE \'{}\''.format(aTable))
    return read(aDataBase, statement, lambda l: l.fetchone()) is not None


def listRows(aDataBase, aTable):

    statement = ('SELECT sql FROM sqlite_master'
        ' WHERE tbl_name LIKE \'{}\' AND type LIKE \'table\''.format(aTable))
    tableInfo = read(aDataBase, statement, lambda l: l.fetchone())

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


def isRowExist(aDataBase, aTable, aRow):

    statement = ('SELECT sql FROM sqlite_master'
        ' WHERE tbl_name LIKE \'{}\' AND type LIKE \'table\''.format(aTable))
    tableInfo = read(aDataBase, statement, lambda l: l.fetchone())

    if tableInfo is not None:
        tableInfo = tableInfo[0]

        if (-1 != tableInfo.find('({} '.format(aRow)) or
                -1 != tableInfo.find(',{} '.format(aRow)) or
                -1 != tableInfo.find(', {} '.format(aRow))):
            return True

    return False


def dropTable(aDataBase, aTable):

    statement = ('DROP TABLE {}'.format(aTable))
    write(aDataBase, statement)


def deleteFromTable(aDataBase, aTable, aRows=None, aItem=None):

    statement = ('DELETE FROM {}'.format(aTable))

    if aRows and aItem:
        l = []
        for row, item in zip(aRows, aItem):
            l.append('{} LIKE \'{}\''.format(row, item))
        l = '{}'.format(l)
        l = l.replace('[', '').replace(']', '')
        l = l.replace(',', ' AND')
        l = l.replace('"', '')
        statement = '{} WHERE {}'.format(statement, l)

    write(aDataBase, statement)


def updateAtTable(aDataBase, aTable, aRows, aItem, aCurrentItem):

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
        l.append('{} LIKE \'{}\''.format(row, currentItem))
    l = '{}'.format(l)
    l = l.replace('[', '').replace(']', '')
    l = l.replace(',', ' AND')
    l = l.replace('"', '')
    statement = '{} WHERE {}'.format(statement, l)

    write(aDataBase, statement)


def getFrom(aDataBase, aTable, aRows=None, aFilter=None):

    if aRows:
        aRows = '{}'.format(aRows)
        aRows = aRows.replace('[', '').replace(']', '')
        aRows = aRows.replace('\'', '')
        aRows = aRows.replace('"', '')
        statement = 'SELECT {} FROM {}'.format(aRows, aTable)
    else:
        statement = 'SELECT * FROM {}'.format(aTable)

    if aFilter:
        template = []

        for key in aFilter.keys():
            if isinstance(aFilter[key], int):
                template.append('{} LIKE {}'.format(key, aFilter[key]))
            elif isinstance(aFilter[key], str):
                template.append('{} LIKE \'{}\''.format(key, aFilter[key]))

        for i in range(0, len(template) - 1):
            template[i] = '{} AND '.format(template[i])

        template = ''.join(template)
        template = template.replace('\'\'', '\'')

        statement = '{} WHERE {}'.format(statement, template)

    items = read(aDataBase, statement, lambda l: l.fetchall())
    for i in range(0, len(items)):
        if 1 == len(items[i]):
            items[i] = items[i][0]
        else:
            items[i] = list(items[i])
    return items


def insertInto(aDataBase, aTable, aItems, aRows=None):

    if aRows:
        aRows = '{}'.format(aRows)
        aRows = aRows.replace('[', '').replace(']', '')
        aRows = aRows.replace('"', '')
        template = 'INSERT INTO {} (' + aRows + ') VALUES({});'
    else:
        template = 'INSERT INTO {} VALUES({});'

    statement = []
    for item in aItems:
        item = '{}'.format(item)
        item = item.replace('[', '').replace(']', '')
        statement.append(template.format(aTable, item))

    write(aDataBase, ''.join(statement))
