import sqlite3
from core.unknownSubstance import UnknownSubstance


def connect(aDbName):

    db = sqlite3.connect(aDbName)
    return db


def disconnect(aDb):

    aDb.close()


def writeToDataBase(aDb, aStatement):

    cursor = aDb.cursor()
    cursor.execute(aStatement)
    aDb.commit()


def readFromDataBase(aDb, aStatement):

    cursor = aDb.cursor()
    cursor.execute(aStatement)
    return cursor


def insertInto(aDb, aTable, aRowName, aItem):

    writeToDataBase(aDb,
        '''INSERT INTO {} ({}) VALUES({})'''.format
        (aTable, aRowName, aItem))


def getIDFrom(aDb, aTable, aRowName, aItem):

    fields = readFromDataBase(aDb,
        '''SELECT id FROM {} WHERE {} LIKE {}'''.format
        (aTable, aRowName, aItem)).fetchone()
    return fields[0] if fields is not None else None


def getSomethingByIDFrom(aDb, aTable, aRowName, aId):

    fields = readFromDataBase(aDb,
        '''SELECT {} FROM {} WHERE id LIKE {}'''.format
        (aRowName, aTable, aId)).fetchone()
    return fields[0] if fields is not None else None


def findTable(aDb, aTable):

    return readFromDataBase(aDb, '''SELECT name FROM
        (SELECT * FROM sqlite_master UNION ALL
         SELECT * FROM sqlite_temp_master)
         WHERE type LIKE 'table' AND name LIKE '{}'
         ORDER BY name
         '''.format(aTable)).fetchone()


def listTables(aDb):

    rawTables = readFromDataBase(aDb, '''SELECT name FROM
       (SELECT * FROM sqlite_master UNION ALL
        SELECT * FROM sqlite_temp_master)
        WHERE type LIKE 'table'
        ORDER BY name''')

    tables = []
    for table in rawTables:
        tables.append(table[0])
    return tables


def listCollections(aDb, aTable):

    query = '''SELECT * FROM {}'''.format(aTable)
    rawData = readFromDataBase(aDb, query).fetchall()
    items = []

    if 'KBs' == aTable:
        for d in rawData:
            if -1 != d[1]:
                items.append(d[1])
            else:
                items.append(UnknownSubstance.unknown('UNKNOWN KB', -1))
    elif 'Versions' == aTable:
        for d in rawData:
            if 'UNKNOWN VERSION' != d[1]:
                items.append(d[1])
            else:
                items.append(UnknownSubstance.unknown('UNKNOWN VERSION', ''))
    elif 'Types' == aTable:
        for d in rawData:
            if 'UNKNOWN TYPE' != d[1]:
                items.append(d[1])
            else:
                items.append(UnknownSubstance.unknown('UNKNOWN TYPE', ''))
    elif 'Languages' == aTable:
        for d in rawData:
            if 'UNKNOWN LANGUAGE' != d[1]:
                items.append(d[1])
            else:
                items.append(UnknownSubstance.unknown('UNKNOWN LANGUAGE', ''))
    else:
        for d in rawData:
            items.append(d[1])

    return items


def createTableKBs(aDb):

    writeToDataBase(aDb, '''CREATE TABLE KBs (
        id INTEGER PRIMARY KEY NOT NULL)''')


def createTableDates(aDb):

    writeToDataBase(aDb, '''CREATE TABLE Dates (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Date TEXT UNIQUE NOT NULL)''')


def createTablePaths(aDb):

    writeToDataBase(aDb, '''CREATE TABLE Paths (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Path TEXT UNIQUE NOT NULL)''')


def createTableVersions(aDb):

    writeToDataBase(aDb, '''CREATE TABLE Versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Version TEXT UNIQUE NOT NULL)''')


def createTableTypes(aDb):

    writeToDataBase(aDb, '''CREATE TABLE Types (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Type TEXT UNIQUE NOT NULL)''')


def createTableLanguages(aDb):

    writeToDataBase(aDb, '''CREATE TABLE Languages (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Language TEXT UNIQUE NOT NULL)''')


def createTableUpdates(aDb):

    writeToDataBase(aDb, '''CREATE TABLE Updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        kb_id INTEGER NOT NULL,
        date_id INTEGER NOT NULL,
        path_id INTEGER NOT NULL,
        version_id INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        language_id INTEGER NOT NULL,
        FOREIGN KEY(kb_id) REFERENCES KBs(id),
        FOREIGN KEY(date_id) REFERENCES Dates(id),
        FOREIGN KEY(path_id) REFERENCES Paths(id),
        FOREIGN KEY(version_id) REFERENCES Versions(id),
        FOREIGN KEY(type_id) REFERENCES Types(id),
        FOREIGN KEY(language_id) REFERENCES Languages(id))''')


def getDateByID(aDb, aId):

    return getSomethingByIDFrom(aDb, 'Dates', 'Date', aId)


def getPathByID(aDb, aId):

    return getSomethingByIDFrom(aDb, 'Paths', 'Path', aId)


def getVersionByID(aDb, aId):

    return getSomethingByIDFrom(aDb, 'Versions', 'Version', aId)


def getTypeByID(aDb, aId):

    return getSomethingByIDFrom(aDb, 'Types', 'Type', aId)


def getLanguageByID(aDb, aId):

    return getSomethingByIDFrom(aDb, 'Languages', 'Language', aId)


def getSetSubstanceID(aDb, aTable, aRowName, aItem):

    substanceID = getIDFrom(aDb, aTable, aRowName, aItem)

    if substanceID is not None:
        return substanceID

    insertInto(aDb, aTable, aRowName, aItem)
    return getIDFrom(aDb, aTable, aRowName, aItem)


def addUpdate(aDb, aUpdate):

    kb = aUpdate['KB'] if not isinstance(aUpdate['KB'], dict) else -1
    kb_id = getSetSubstanceID(aDb, 'KBs', 'id', kb)

    osVersion = (aUpdate['Version']
            if not isinstance(aUpdate['Version'], dict) else 'UNKNOWN VERSION')
    version_id = getSetSubstanceID(aDb, 'Versions', 'Version',
                                   '\'{}\''.format(osVersion))

    osType = (
        aUpdate['Type'] if not isinstance(aUpdate['Type'], dict) else
            'UNKNOWN TYPE')
    type_id = getSetSubstanceID(aDb, 'Types', 'Type', '\'{}\''.format(osType))

    language = (
        aUpdate['Language'] if not isinstance(aUpdate['Language'], dict) else
            'UNKNOWN LANGUAGE')
    language_id = getSetSubstanceID(aDb, 'Languages', 'Language',
                                    '\'{}\''.format(language))

    date_id = getSetSubstanceID(aDb, 'Dates', 'Date',
                                '\'{}\''.format(aUpdate['Date']))
    path_id = getSetSubstanceID(aDb, 'Paths', 'Path',
                                '\'{}\''.format(aUpdate['Path']))

    writeToDataBase(aDb, '''INSERT INTO Updates
                           (kb_id, date_id, path_id, version_id,
                            type_id, language_id)
                           VALUES ({}, {}, {}, {}, {}, {})'''.format
                (kb_id, date_id, path_id, version_id, type_id, language_id))


def addUpdates(aDb, aUpdates):

    i = 1
    count = len(aUpdates)
    cursor = aDb.cursor()

    for update in aUpdates:
        kb = update['KB'] if not isinstance(update['KB'], dict) else -1
        kb_id = getSetSubstanceID(aDb, 'KBs', 'id', kb)

        osVersion = (update['Version']
            if not isinstance(update['Version'], dict) else 'UNKNOWN VERSION')
        version_id = getSetSubstanceID(aDb, 'Versions', 'Version',
                                       '\'{}\''.format(osVersion))

        osType = (
            update['Type'] if not isinstance(update['Type'], dict) else
                'UNKNOWN TYPE')
        type_id = getSetSubstanceID(aDb, 'Types', 'Type',
            '\'{}\''.format(osType))

        language = (
            update['Language'] if not isinstance(update['Language'], dict) else
                'UNKNOWN LANGUAGE')
        language_id = getSetSubstanceID(aDb, 'Languages', 'Language',
                                        '\'{}\''.format(language))

        date_id = getSetSubstanceID(aDb, 'Dates', 'Date',
                                    '\'{}\''.format(update['Date']))
        path_id = getSetSubstanceID(aDb, 'Paths', 'Path',
                                    '\'{}\''.format(update['Path']))

        cursor.execute('''INSERT INTO Updates
                       (kb_id, date_id, path_id, version_id,
                       type_id, language_id)
                       VALUES ({}, {}, {}, {}, {}, {})'''.format
               (kb_id, date_id, path_id, version_id, type_id, language_id))

        print('{} / {}'.format(i, count))
        i += 1

    aDb.commit()


def rawUpdatesToUpdates(aDb, aRawUpdates):

    updates = []

    for rawUpdate in aRawUpdates:

        update = {}

        update['Path'] = getPathByID(aDb, rawUpdate[2])

        kb = rawUpdate[0]
        if -1 != kb:
            update['KB'] = kb
        else:
            update['KB'] = UnknownSubstance.unknown('UNKNOWN KB',
                                                    update['Path'])

        version = getVersionByID(aDb, rawUpdate[3])
        if 'UNKNOWN VERSION' != version:
            update['Version'] = version
        else:
            update['Version'] = UnknownSubstance.unknown('UNKNOWN VERSION',
                                                         update['Path'])

        osType = getTypeByID(aDb, rawUpdate[4])
        if 'UNKNOWN TYPE' != osType:
            update['Type'] = osType
        else:
            update['Type'] = UnknownSubstance.unknown('UNKNOWN TYPE',
                                                      update['Path'])

        osLanguage = getLanguageByID(aDb, rawUpdate[5])
        if 'UNKNOWN LANGUAGE' != osLanguage:
            update['Language'] = osLanguage
        else:
            update['Language'] = UnknownSubstance.unknown('UNKNOWN LANGUAGE',
                                                          update['Path'])

        update['Date'] = getDateByID(aDb, rawUpdate[1])

        updates.append(update)

    return updates


def getUpdates(aDb, aQuery):

    query = None
    if aQuery == {}:
        query = '''SELECT kb_id, date_id, path_id, version_id,
                   type_id, language_id FROM Updates'''
    else:
        query = '''SELECT kb_id, date_id, path_id, version_id,
                   type_id, language_id FROM Updates WHERE'''

        andNead = False
        for key in aQuery.keys():

            if(andNead):
                query += ''' AND'''

            if('KB' == key):
                kb_id = getIDFrom(aDb, 'KBs', 'id', aQuery[key])
                if kb_id is None:
                    return []

                query += ''' kb_id LIKE {}'''.format(kb_id)
                andNead = True

            elif('Date' == key):
                date_id = getIDFrom(aDb, 'Dates',
                                    'Date', '\'{}\''.format(aQuery[key]))
                if date_id is None:
                    return []

                query += ''' date_id LIKE {}'''.format(date_id)
                andNead = True

            elif('Version' == key):
                version_id = getIDFrom(aDb, 'Versions', 'Version',
                                       '\'{}\''.format(aQuery[key]))
                if version_id is None:
                    return []

                query += ''' version_id LIKE {}'''.format(version_id)
                andNead = True

            elif('Type' == key):
                type_id = getIDFrom(aDb, 'Types',
                                    'Type', '\'{}\''.format(aQuery[key]))
                if type_id is None:
                    return []

                query += ''' type_id LIKE {}'''.format(type_id)
                andNead = True

            elif('Language' == key):
                language_id = getIDFrom(aDb, 'Languages', 'Language',
                                        '\'{}\''.format(aQuery[key]))
                if language_id is None:
                    return []

                query += ''' language_id LIKE {}'''.format(language_id)
                andNead = True

            elif('Path' == key):
                path_id = getIDFrom(aDb, 'Paths',
                                    'Path', '\'{}\''.format(aQuery[key]))
                if path_id is None:
                    return []

                query += ''' path_id LIKE {}'''.format(path_id)
                andNead = True

    rawUpdates = readFromDataBase(aDb, query)
    return rawUpdatesToUpdates(aDb, rawUpdates)


def getUpdatesByKBInPath(aDb, aKb):

    path_ids = None
    try:

        path_ids = readFromDataBase(aDb, '''SELECT id FROM Paths
                                            WHERE Path REGEXP '{}' '''.format
                                            (aKb))
    except:

        aDb.create_function('REGEXP', 2, lambda kb, path: kb in path)
        path_ids = readFromDataBase(aDb, '''SELECT id FROM Paths
                                            WHERE Path REGEXP '{}' '''.format
                                            (aKb))

    updates = []
    for path_id in path_ids:

        path = getPathByID(aDb, path_id[0])
        query = {'Path': path}
        ups = getUpdates(aDb, query)

        for up in ups:
            updates.append(up)

    return updates
