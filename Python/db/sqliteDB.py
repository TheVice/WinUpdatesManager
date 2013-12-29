import sqlite3
import datetime


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
    return cursor.fetchone()


def insertInto(db, table, rowName, item):
    writeToDataBase(db, '''INSERT INTO %s (%s) VALUES(%s)'''
        % (table, rowName, item))


def getIDFrom(db, table, rowName, item):
    fields = readFromDataBase(db, '''SELECT id FROM %s WHERE %s=%s'''
        % (table, rowName, item))
    return fields[0] if fields is not None else None


def findTable(db, table):
    return readFromDataBase(db, '''SELECT name FROM
        (SELECT * FROM sqlite_master UNION ALL
         SELECT * FROM sqlite_temp_master)
         WHERE type='table' AND name='%s'
         ORDER BY name
         ''' % table)


def listTables(db):
    return readFromDataBase(db, '''SELECT name FROM
       (SELECT * FROM sqlite_master UNION ALL
        SELECT * FROM sqlite_temp_master)
        WHERE type='table'
        ORDER BY name''')


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


def getSetSubstanceID(db, table, rowName, item):
    substanceID = getIDFrom(db, table, rowName, item)
    if substanceID is not None:
        return substanceID
    insertInto(db, table, rowName, item)
    return getIDFrom(db, table, rowName, item)


def addUpdate(db, update):
    kb_id = getSetSubstanceID(db, 'KBs', 'id', update['KB'])
    date_id = getSetSubstanceID(db, 'Dates', 'Date', update['Date'])
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
    date_id = getIDFrom(db, 'Dates', 'Date', update['Date'])
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
    return readFromDataBase(db, '''SELECT kb_id, date_id, path_id, version_id,
                            type_id, language_id
                            FROM Updates
                            WHERE kb_id=%s AND date_id=%s AND path_id=%s AND
                            version_id=%s AND type_id=%s AND language_id=%s
                            ''' % (kb_id, date_id, path_id, version_id,
                                type_id, language_id))


if __name__ == '__main__':
    db = connect(':memory:')

    if findTable(db, 'KBs') is None:
        createTableKBs(db)
    if findTable(db, 'Dates') is None:
        createTableDates(db)
    if findTable(db, 'Paths') is None:
        createTablePaths(db)
    if findTable(db, 'Versions') is None:
        createTableVersions(db)
    if findTable(db, 'Types') is None:
        createTableTypes(db)
    if findTable(db, 'Languages') is None:
        createTableLanguages(db)
    if findTable(db, 'Updates') is None:
        createTableUpdates(db)
    if getIDFrom(db, 'KBs', 'id', 1) is None:
        insertInto(db, 'KBs', 'id', 1)

    update = {'KB': 1,
              'Date': datetime.date(2013, 2, 1),
              'Path': 'D:\\SQLite\\sqlite3.exe',
              'Version': 'SQLite',
              'Type': 'x86',
              'Language': 'Neutral'}

    if findUpdate(db, update) is None:
        addUpdate(db, update)

    update['Path'] = '?'

    print(findUpdate(db, update))

    db.close()
