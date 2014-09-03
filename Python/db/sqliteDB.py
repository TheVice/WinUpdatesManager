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

    fields = readFromDataBase(aDb, '''SELECT %s FROM %s
        WHERE id LIKE %s''' % (aRowName, aTable, aId)).fetchone()
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


def addUpdate(db, update):
    kb_id = getSetSubstanceID(db, 'KBs', 'id', update['KB'])
    date_id = getSetSubstanceID(db, 'Dates', 'Date', '\'%s\'' % update['Date'])
    path_id = getSetSubstanceID(db, 'Paths', 'Path', '\'%s\'' % update['Path'])
    version_id = getSetSubstanceID(db, 'Versions', 'Version',
                                   '\'%s\'' % update['Version'])
    type_id = getSetSubstanceID(db, 'Types', 'Type', '\'%s\'' % update['Type'])
    language_id = getSetSubstanceID(db, 'Languages', 'Language',
                                    '\'%s\'' % update['Language'])
    writeToDataBase(db, '''INSERT INTO Updates
                           (kb_id, date_id, path_id, version_id,
                            type_id, language_id)
                           VALUES (%s, %s, %s, %s, %s, %s)'''
                    % (kb_id, date_id, path_id, version_id, type_id,
                       language_id))


def findUpdate(db, update):
    kb_id = getIDFrom(db, 'KBs', 'id', update['KB'])
    if kb_id is None:
        return None
    date_id = getIDFrom(db, 'Dates', 'Date', '\'%s\'' % update['Date'])
    if date_id is None:
        return None
    path_id = getIDFrom(db, 'Paths', 'Path', '\'%s\'' % update['Path'])
    if path_id is None:
        return None
    version_id = getIDFrom(db, 'Versions', 'Version',
                                   '\'%s\'' % update['Version'])
    if version_id is None:
        return None
    type_id = getIDFrom(db, 'Types', 'Type', '\'%s\'' % update['Type'])
    if type_id is None:
        return None
    language_id = getIDFrom(db, 'Languages', 'Language',
                                    '\'%s\'' % update['Language'])
    if language_id is None:
        return None

    if None is readFromDataBase(db, '''SELECT kb_id, date_id, path_id,
                            version_id, type_id, language_id
                            FROM Updates
                            WHERE kb_id LIKE %s AND date_id LIKE %s AND
                            path_id LIKE %s AND version_id LIKE %s AND
                            type_id LIKE %s AND language_id LIKE %s
                            ''' % (kb_id, date_id, path_id, version_id,
                                type_id, language_id)).fetchone():
        return None

    update = {}
    update['KB'] = kb_id
    update['Date'] = getDateByID(db, date_id)
    update['Path'] = getPathByID(db, path_id)
    update['Version'] = getVersionByID(db, version_id)
    update['Type'] = getTypeByID(db, type_id)
    update['Language'] = getLanguageByID(db, language_id)

    return update


def getUpdatesByKB(aDb, aKB):

    kb_id = getIDFrom(aDb, 'KBs', 'id', aKB)
    if kb_id is None:
        return None

    rawUpdates = readFromDataBase(aDb, '''SELECT kb_id, date_id, path_id,
                                  version_id, type_id, language_id
                                  FROM Updates
                                  WHERE kb_id LIKE %s''' % kb_id)

    updates = []
    for rawUpdate in rawUpdates:

        update = {}
        update['KB'] = rawUpdate[0]
        update['Date'] = getDateByID(aDb, rawUpdate[1])
        update['Path'] = getPathByID(aDb, rawUpdate[2])
        update['Version'] = getVersionByID(aDb, rawUpdate[3])
        update['Type'] = getTypeByID(aDb, rawUpdate[4])
        update['Language'] = getLanguageByID(aDb, rawUpdate[5])

        updates.append(update)

    return updates
