import re
import sys
import sqlite3
if 2 == sys.version_info[0]:
    import thread
else:
    import _thread as thread


def connect(aDataBase, aCheckSameThread=True):

    return sqlite3.connect(aDataBase, check_same_thread=aCheckSameThread)


def disconnect(aConnection):

    aConnection.close()


def write(aDataBase, aStatement, aMutex=None):

    if isinstance(aDataBase, sqlite3.Connection):
        aDataBase.executescript(aStatement)
        aDataBase.commit()
    elif isinstance(aDataBase, sqlite3.Cursor):
        aDataBase.executescript(aStatement)
    else:
        connection = connect(aDataBase)
        connection.executescript(aStatement)
        connection.commit()
        disconnect(connection)

    if aMutex:
        aMutex.acquire()


def read(aDataBase, aStatement, aFetch, aMutex=None, aReturnData=None):

    if isinstance(aDataBase, sqlite3.Connection):
        cursor = aDataBase.cursor()
        cursor.execute(aStatement)
        data = aFetch(cursor)
    elif isinstance(aDataBase, sqlite3.Cursor):
        aDataBase.execute(aStatement)
        data = aFetch(aDataBase)
    else:
        connection = connect(aDataBase)
        cursor = connection.cursor()
        cursor.execute(aStatement)
        data = aFetch(cursor)
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
    tables = readAsync(aDataBase, statement, lambda l: l.fetchall())

    for i in range(0, len(tables)):
        tables[i] = tables[i][0]
    return tables


def isTableExist(aDataBase, aTable):

    statement = ('SELECT name FROM sqlite_master'
                 ' WHERE type LIKE \'table\''
                 ' AND name LIKE \'{}\''.format(aTable))
    return readAsync(aDataBase, statement, lambda l: l.fetchone()) is not None


def listRows(aDataBase, aTable):

    statement = ('SELECT sql FROM sqlite_master'
        ' WHERE tbl_name LIKE \'{}\' AND type LIKE \'table\''.format(aTable))
    tableInfo = readAsync(aDataBase, statement, lambda l: l.fetchone())

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
    tableInfo = readAsync(aDataBase, statement, lambda l: l.fetchone())

    if tableInfo is not None:
        tableInfo = tableInfo[0]

        if (-1 != tableInfo.find('({} '.format(aRow)) or
                -1 != tableInfo.find(',{} '.format(aRow)) or
                -1 != tableInfo.find(', {} '.format(aRow))):
            return True

    return False


def dropTable(aDataBase, aTable):

    statement = ('DROP TABLE {}'.format(aTable))
    writeAsync(aDataBase, statement)


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

    writeAsync(aDataBase, statement)


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

    writeAsync(aDataBase, statement)


def getFrom(aDataBase, aTable, aRows=None, aFilter=None, aOrderBy=None):

    if aRows:
        if isinstance(aRows, list):
            statement = '{}'.format(aRows[0])
            for i in range(1, len(aRows)):
                statement = '{}, {}'.format(statement, aRows[i])
            statement = 'SELECT {} FROM {}'.format(statement, aTable)
        else:
            statement = 'SELECT {} FROM {}'.format(aRows, aTable)
    else:
        statement = 'SELECT * FROM {}'.format(aTable)

    if aFilter and isinstance(aFilter, dict):
        filterStatement = ''

        for key in aFilter.keys():
            value = aFilter[key]

            if isinstance(value, list) and len(value):
                if isinstance(value[0], int):
                    subFilterStatement = '{} LIKE {}'.format(key, value[0])
                elif isinstance(value[0], str):
                    subFilterStatement = '{} LIKE \'{}\''.format(key, value[0])
                for i in range(1, len(value)):
                    if isinstance(value[i], int):
                        subFilterStatement = '{} OR {} LIKE {}'.format(subFilterStatement, key, value[i])
                    elif isinstance(value[i], str):
                        subFilterStatement = '{} OR {} LIKE \'{}\''.format(subFilterStatement, key, value[i])

            elif isinstance(value, int):
                subFilterStatement = '{} LIKE {}'.format(key, value)

            elif isinstance(value, str):
                subFilterStatement = '{} LIKE \'{}\''.format(key, value)

            if filterStatement == '':
                filterStatement = '{}'.format(subFilterStatement)
            else:
                filterStatement = '{} AND {}'.format(filterStatement, subFilterStatement)

        statement = '{} WHERE {}'.format(statement, filterStatement)

    if aOrderBy and isinstance(aOrderBy, dict):
        orderStatement = []
        for key in aOrderBy.keys():
            value = aOrderBy[key]
            if isinstance(value, int):
                if value < 0:
                    value = 'DESC'
                else:
                    value = 'ASC'
            else:
                value = 'ASC'
            orderStatement.append('{} {}'.format(key, value))

        orderStatement = ''.join(orderStatement)
        orderStatement = orderStatement.replace('ASC', 'ASC,')
        orderStatement = orderStatement.replace('DESC', 'DESC,')
        orderStatement = orderStatement[:len(orderStatement)-1]

        statement = '{} ORDER BY {}'.format(statement, orderStatement)

    items = readAsync(aDataBase, statement, lambda l: l.fetchall())
    for i in range(0, len(items)):
        if 1 == len(items[i]):
            items[i] = items[i][0]
        else:
            items[i] = list(items[i])
    return items


def getItemsCount(aDataBase, aTable):

    statement = 'SELECT COUNT (*) FROM {}'.format(aTable)
    return readAsync(aDataBase, statement, lambda l: l.fetchone())[0]


def insertInto(aDataBase, aTable, aRows, aItems):

    if aRows:
        if isinstance(aRows, list):
            rowsStatement = '{}'.format(aRows[0])
            for i in range(1, len(aRows)):
                rowsStatement = '{}, {}'.format(rowsStatement, aRows[i])
            rowsStatement = 'INSERT INTO {} ({})'.format(aTable, rowsStatement)
        else:
            rowsStatement = 'INSERT INTO {} ({})'.format(aTable, aRows)
    else:
        rowsStatement = 'INSERT INTO {}'.format(aTable)

    if aItems:
        statement = []
        if not isinstance(aItems, list):
            aItems = [aItems]
        for item in aItems:
            if isinstance(item, list) or isinstance(item, int):
                item = '{}'.format(item)
                item = item.replace('[', '').replace(']', '')
            elif isinstance(item, str):
                item = '\'{}\''.format(item)
            statement.append('{} VALUES({});'.format(rowsStatement, item))

        writeAsync(aDataBase, ''.join(statement))
