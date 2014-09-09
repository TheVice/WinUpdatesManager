import sqlite3


def connect(dbName):
    db = sqlite3.connect(dbName)
    return db


def writeToDataBase(db, statement):
    cursor = db.cursor()
    cursor.execute(statement)
    db.commit()


def readFromDataBase(db, statement):
    cursor = db.cursor()
    cursor.execute(statement)
    return cursor


def insertInto(db, table, rowName, item):
    writeToDataBase(db, '''INSERT INTO %s (%s) VALUES(%s)'''
        % (table, rowName, item))


def getIDFrom(db, table, rowName, item):
    fields = readFromDataBase(db, '''SELECT id FROM %s WHERE %s LIKE %s'''
        % (table, rowName, item)).fetchone()
    return fields[0] if fields is not None else None


def getSomethingByIDFrom(aDb, aTable, aRowName, aId):

    fields = readFromDataBase(aDb, '''SELECT %s FROM %s WHERE id LIKE %s'''
        % (aRowName, aTable, aId)).fetchone()
    return fields[0] if fields is not None else None


def findTable(db, table):
    return readFromDataBase(db, '''SELECT name FROM
        (SELECT * FROM sqlite_master UNION ALL
         SELECT * FROM sqlite_temp_master)
         WHERE type LIKE 'table' AND name LIKE '%s'
         ORDER BY name
         ''' % table).fetchone()


def listTables(db):
    rawTables = readFromDataBase(db, '''SELECT name FROM
       (SELECT * FROM sqlite_master UNION ALL
        SELECT * FROM sqlite_temp_master)
        WHERE type LIKE 'table'
        ORDER BY name''')

    tables = []
    for table in rawTables:
        tables.append(table[0])
    return tables


def createTableKBs(db):
    writeToDataBase(db, '''CREATE TABLE KBs (
        id INTEGER PRIMARY KEY NOT NULL)''')


def createTableDates(db):
    writeToDataBase(db, '''CREATE TABLE Dates (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Date TEXT UNIQUE NOT NULL)''')


def createTablePaths(db):
    writeToDataBase(db, '''CREATE TABLE Paths (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Path TEXT UNIQUE NOT NULL)''')


def createTableVersions(db):
    writeToDataBase(db, '''CREATE TABLE Versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Version TEXT UNIQUE NOT NULL)''')


def createTableTypes(db):
    writeToDataBase(db, '''CREATE TABLE Types (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Type TEXT UNIQUE NOT NULL)''')


def createTableLanguages(db):
    writeToDataBase(db, '''CREATE TABLE Languages (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        Language TEXT UNIQUE NOT NULL)''')


def createTableUpdates(db):
    writeToDataBase(db, '''CREATE TABLE Updates (
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


def getSetSubstanceID(db, table, rowName, item):
    substanceID = getIDFrom(db, table, rowName, item)
    if substanceID is not None:
        return substanceID
    insertInto(db, table, rowName, item)
    return getIDFrom(db, table, rowName, item)


def addUpdate(aDb, aUpdate):

    kb = aUpdate['KB'] if not isinstance(aUpdate['KB'], dict) else -1
    kb_id = getSetSubstanceID(aDb, 'KBs', 'id', kb)

    osVersion = (aUpdate['Version']
            if not isinstance(aUpdate['Version'], dict) else 'UNKNOWN VERSION')
    version_id = getSetSubstanceID(aDb, 'Versions', 'Version',
                                   '\'%s\'' % osVersion)

    osType = (
        aUpdate['Type'] if not isinstance(aUpdate['Type'], dict) else
            'UNKNOWN TYPE')
    type_id = getSetSubstanceID(aDb, 'Types', 'Type', '\'%s\'' % osType)

    language = (
        aUpdate['Language'] if not isinstance(aUpdate['Language'], dict) else
            'UNKNOWN LANGUAGE')
    language_id = getSetSubstanceID(aDb, 'Languages', 'Language',
                                    '\'%s\'' % language)

    date_id = getSetSubstanceID(aDb, 'Dates', 'Date',
                                '\'%s\'' % aUpdate['Date'])
    path_id = getSetSubstanceID(aDb, 'Paths', 'Path',
                                '\'%s\'' % aUpdate['Path'])

    writeToDataBase(aDb, '''INSERT INTO Updates
                           (kb_id, date_id, path_id, version_id,
                            type_id, language_id)
                           VALUES (%s, %s, %s, %s, %s, %s)'''
                    % (kb_id, date_id, path_id, version_id, type_id,
                       language_id))


def rawUpdatesToUpdates(aDb, aRawUpdates):

    updates = []
    for rawUpdate in aRawUpdates:

        update = {}
        update['KB'] = rawUpdate[0]
        update['Date'] = getDateByID(aDb, rawUpdate[1])
        update['Path'] = getPathByID(aDb, rawUpdate[2])
        update['Version'] = getVersionByID(aDb, rawUpdate[3])
        update['Type'] = getTypeByID(aDb, rawUpdate[4])
        update['Language'] = getLanguageByID(aDb, rawUpdate[5])

        updates.append(update)

    return updates


def getUpdates(aDb, aQuery):

    query = None
    if(aQuery == {}):
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

                query += ''' kb_id LIKE %s''' % kb_id
                andNead = True

            elif('Date' == key):
                date_id = getIDFrom(aDb, 'Dates',
                                    'Date', '\'%s\'' % aQuery[key])
                if date_id is None:
                    return []

                query += ''' date_id LIKE %s''' % date_id
                andNead = True

            elif('Version' == key):
                version_id = getIDFrom(aDb, 'Versions', 'Version',
                                       '\'%s\'' % aQuery[key])
                if version_id is None:
                    return []

                query += ''' version_id LIKE %s''' % version_id
                andNead = True

            elif('Type' == key):
                type_id = getIDFrom(aDb, 'Types',
                                    'Type', '\'%s\'' % aQuery[key])
                if type_id is None:
                    return []

                query += ''' type_id LIKE %s''' % type_id
                andNead = True

            elif('Language' == key):
                language_id = getIDFrom(aDb, 'Languages', 'Language',
                                        '\'%s\'' % aQuery[key])
                if language_id is None:
                    return []

                query += ''' language_id LIKE %s''' % language_id
                andNead = True

            elif('Path' == key):
                path_id = getIDFrom(aDb, 'Paths',
                                    'Path', '\'%s\'' % aQuery[key])
                if path_id is None:
                    return []

                query += ''' path_id LIKE %s''' % path_id
                andNead = True

    rawUpdates = readFromDataBase(aDb, query)
    return rawUpdatesToUpdates(aDb, rawUpdates)


def regexp(aKb, aPath):

    return aKb in aPath


def getUpdatesByKBInPath(aDb, aKb):

    aDb.create_function('REGEXP', 2, regexp)
    path_ids = readFromDataBase(aDb, '''SELECT id FROM Paths
                                        WHERE Path REGEXP '%s' ''' % aKb)

    updates = []
    for path_id in path_ids:

        path = getPathByID(aDb, path_id[0])
        query = {'Path': path}
        ups = getUpdates(aDb, query)

        for up in ups:
            updates.append(up)

    return updates
