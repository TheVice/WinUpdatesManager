import sys
import json
if 2 == sys.version_info[0]:
    import thread
else:
    import _thread as thread
import os.path
import core.dirs
import db.mongoDB
import db.sqliteDB
from core.unknownSubstance import UnknownSubstance


class Storage:

    def __init__(self, aType):

        self.mType = aType

    def getAvalibleVersions(self):

        pass

    def getAvalibleTypes(self):

        pass

    def getAvalibleLanguages(self):

        pass

    def get(self, aQuery):

        pass

    def __str__(self):

        return str(self.mType)


class Uif(Storage):

    def __init__(self, aInit):

        if 2 == sys.version_info[0]:
            Storage.__init__(self, 'Uif')
        else:
            super(Uif, self).__init__('Uif')
        self.mUpdates = Uif.getUpdatesFromStorage(aInit)

    def getAvalibleVersions(self):

        return Uif.makeAvalibleList(self.mUpdates, 'Version')

    def getAvalibleTypes(self):

        return Uif.makeAvalibleList(self.mUpdates, 'Type')

    def getAvalibleLanguages(self):

        return Uif.makeAvalibleList(self.mUpdates, 'Language')

    def get(self, aQuery):

        updates = []

        for update in self.mUpdates:
            match = True

            for key in aQuery.keys():
                if isinstance(aQuery.get(key), list):
                    if 0 == aQuery.get(key).count(update[key]):
                        match = False
                        break
                elif not update[key] == aQuery.get(key):
                    match = False
                    break

            if match:
                updates.append(update)

        return updates

    @staticmethod
    def getUpdatesFromFile(aFile):

        updates = []

        try:
            inputFile = open(aFile, 'r')

            for line in inputFile:
                updates.append(json.loads(line))

            inputFile.close()
        except:
            raise Exception('Unexpected error while work with file {} {}'.format(aFile, sys.exc_info[1]))

        return updates

    @staticmethod
    def getUpdatesFromStorage(aPath):

        updates = []
        if os.path.isfile(aPath):
            updates.extend(Uif.getUpdatesFromFile(aPath))
        elif os.path.isdir(aPath):
            files = core.dirs.getSubDirectoryFiles(aPath)
            for f in files:
                if -1 != f.rfind('.uif'):
                    f = os.path.normpath('{}{}'.format(aPath, f))
                    updates.extend(Uif.getUpdatesFromFile(f))

        return updates

    @staticmethod
    def makeAvalibleList(aUpdates, aKey):

        items = set()
        for update in aUpdates:
            if isinstance(update, dict) and aKey in update:
                if not isinstance(update[aKey], dict):
                    items.add(update[aKey])
        return list(items)


class SQLite(Storage):

    def __init__(self, aInit):

        if 2 == sys.version_info[0]:
            Storage.__init__(self, 'SQLite')
        else:
            super(SQLite, self).__init__('SQLite')
        self.mInit = aInit

    @staticmethod
    def _getAvalibleVersions(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(SQLite.listCollections(sqlite, 'Versions'))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _getAvalibleTypes(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(SQLite.listCollections(sqlite, 'Types'))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _getAvalibleLanguages(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(SQLite.listCollections(sqlite, 'Languages'))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _get(aMutex, aPath, aQuery, aUpdates):

        sqlite = db.sqliteDB.connect(aPath)
        aUpdates.extend(SQLite.getUpdates(sqlite, aQuery))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def getIDFrom(aDb, aTable, aRowName, aItem):

        fields = db.sqliteDB.readFromDataBase(aDb,
            '''SELECT id FROM {} WHERE {} LIKE {}'''.format
            (aTable, aRowName, aItem), lambda l: l.fetchone())
        return fields[0] if fields is not None else None

    @staticmethod
    def getSomethingByIDFrom(aDb, aTable, aRowName, aId):

        fields = db.sqliteDB.readFromDataBase(aDb,
            '''SELECT {} FROM {} WHERE id LIKE {}'''.format
            (aRowName, aTable, aId), lambda l: l.fetchone())
        return fields[0] if fields is not None else None

    @staticmethod
    def getUpdates(aDb, aQuery):

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
                    kb_id = SQLite.getIDFrom(aDb, 'KBs', 'id', aQuery[key])
                    if kb_id is None:
                        return []

                    query += ''' kb_id LIKE {}'''.format(kb_id)
                    andNead = True

                elif('Date' == key):
                    date_id = SQLite.getIDFrom(aDb, 'Dates',
                                        'Date', '\'{}\''.format(aQuery[key]))
                    if date_id is None:
                        return []

                    query += ''' date_id LIKE {}'''.format(date_id)
                    andNead = True

                elif('Version' == key):
                    version_id = SQLite.getIDFrom(aDb, 'Versions', 'Version',
                                           '\'{}\''.format(aQuery[key]))
                    if version_id is None:
                        return []

                    query += ''' version_id LIKE {}'''.format(version_id)
                    andNead = True

                elif('Type' == key):
                    type_id = SQLite.getIDFrom(aDb, 'Types',
                                        'Type', '\'{}\''.format(aQuery[key]))
                    if type_id is None:
                        return []

                    query += ''' type_id LIKE {}'''.format(type_id)
                    andNead = True

                elif('Language' == key):
                    language_id = SQLite.getIDFrom(aDb, 'Languages', 'Language',
                                            '\'{}\''.format(aQuery[key]))
                    if language_id is None:
                        return []

                    query += ''' language_id LIKE {}'''.format(language_id)
                    andNead = True

                elif('Path' == key):
                    path_id = SQLite.getIDFrom(aDb, 'Paths',
                                        'Path', '\'{}\''.format(aQuery[key]))
                    if path_id is None:
                        return []

                    query += ''' path_id LIKE {}'''.format(path_id)
                    andNead = True

        rawUpdates = db.sqliteDB.readFromDataBase(aDb, query)
        return SQLite.rawUpdatesToUpdates(aDb, rawUpdates)

    @staticmethod
    def rawUpdatesToUpdates(aDb, aRawUpdates):

        updates = []

        for rawUpdate in aRawUpdates:

            update = {}

            update['Path'] = SQLite.getPathByID(aDb, rawUpdate[2])

            kb = rawUpdate[0]
            if -1 != kb:
                update['KB'] = kb
            else:
                update['KB'] = UnknownSubstance.unknown('UNKNOWN KB',
                                                        update['Path'])

            version = SQLite.getVersionByID(aDb, rawUpdate[3])
            if 'UNKNOWN VERSION' != version:
                update['Version'] = version
            else:
                update['Version'] = UnknownSubstance.unknown('UNKNOWN VERSION',
                                                             update['Path'])

            osType = SQLite.getTypeByID(aDb, rawUpdate[4])
            if 'UNKNOWN TYPE' != osType:
                update['Type'] = osType
            else:
                update['Type'] = UnknownSubstance.unknown('UNKNOWN TYPE',
                                                          update['Path'])

            osLanguage = SQLite.getLanguageByID(aDb, rawUpdate[5])
            if 'UNKNOWN LANGUAGE' != osLanguage:
                update['Language'] = osLanguage
            else:
                update['Language'] = UnknownSubstance.unknown('UNKNOWN LANGUAGE',
                                                              update['Path'])

            update['Date'] = SQLite.getDateByID(aDb, rawUpdate[1])

            updates.append(update)

        return updates

    @staticmethod
    def getDateByID(aDb, aId):

        return SQLite.getSomethingByIDFrom(aDb, 'Dates', 'Date', aId)

    @staticmethod
    def getPathByID(aDb, aId):

        return SQLite.getSomethingByIDFrom(aDb, 'Paths', 'Path', aId)

    @staticmethod
    def getVersionByID(aDb, aId):

        return SQLite.getSomethingByIDFrom(aDb, 'Versions', 'Version', aId)

    @staticmethod
    def getTypeByID(aDb, aId):

        return SQLite.getSomethingByIDFrom(aDb, 'Types', 'Type', aId)

    @staticmethod
    def getLanguageByID(aDb, aId):

        return SQLite.getSomethingByIDFrom(aDb, 'Languages', 'Language', aId)

    @staticmethod
    def getSetSubstanceID(aDb, aTable, aRowName, aItem):

        substanceID = SQLite.getIDFrom(aDb, aTable, aRowName, aItem)

        if substanceID is not None:
            return substanceID

        db.sqliteDB.insertInto(aDb, aTable, [aItem], aRowName)
        return SQLite.getIDFrom(aDb, aTable, aRowName, aItem)

    @staticmethod
    def listCollections(aDb, aTable):

        query = '''SELECT * FROM {}'''.format(aTable)
        rawData = db.sqliteDB.readFromDataBase(aDb, query, lambda l: l.fetchall())
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

    @staticmethod
    def addUpdates(aDb, aUpdates):

        i = 1
        count = len(aUpdates)
        cursor = aDb.cursor()

        for update in aUpdates:
            kb = update['KB'] if not isinstance(update['KB'], dict) else -1
            kb_id = SQLite.getSetSubstanceID(aDb, 'KBs', 'id', kb)

            osVersion = (update['Version']
                if not isinstance(update['Version'], dict) else 'UNKNOWN VERSION')
            version_id = SQLite.getSetSubstanceID(aDb, 'Versions', 'Version',
                                           '\'{}\''.format(osVersion))

            osType = (
                update['Type'] if not isinstance(update['Type'], dict) else
                    'UNKNOWN TYPE')
            type_id = SQLite.getSetSubstanceID(aDb, 'Types', 'Type',
                '\'{}\''.format(osType))

            language = (
                update['Language'] if not isinstance(update['Language'], dict) else
                    'UNKNOWN LANGUAGE')
            language_id = SQLite.getSetSubstanceID(aDb, 'Languages', 'Language',
                                            '\'{}\''.format(language))

            date_id = SQLite.getSetSubstanceID(aDb, 'Dates', 'Date',
                                        '\'{}\''.format(update['Date']))
            path_id = SQLite.getSetSubstanceID(aDb, 'Paths', 'Path',
                                        '\'{}\''.format(update['Path']))

            cursor.execute('''INSERT INTO Updates
                           (kb_id, date_id, path_id, version_id,
                           type_id, language_id)
                           VALUES ({}, {}, {}, {}, {}, {})'''.format
                   (kb_id, date_id, path_id, version_id, type_id, language_id))

            print('{} / {}'.format(i, count))
            i += 1

        aDb.commit()

    @staticmethod
    def createTableKBs(aDb):

        db.sqliteDB.writeToDataBase(aDb, '''CREATE TABLE KBs (
            id INTEGER PRIMARY KEY NOT NULL)''')

    @staticmethod
    def createTableDates(aDb):

        db.sqliteDB.writeToDataBase(aDb, '''CREATE TABLE Dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            Date TEXT UNIQUE NOT NULL)''')

    @staticmethod
    def createTablePaths(aDb):

        db.sqliteDB.writeToDataBase(aDb, '''CREATE TABLE Paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            Path TEXT UNIQUE NOT NULL)''')

    @staticmethod
    def createTableVersions(aDb):

        db.sqliteDB.writeToDataBase(aDb, '''CREATE TABLE Versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            Version TEXT UNIQUE NOT NULL)''')

    @staticmethod
    def createTableTypes(aDb):

        db.sqliteDB.writeToDataBase(aDb, '''CREATE TABLE Types (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            Type TEXT UNIQUE NOT NULL)''')

    @staticmethod
    def createTableLanguages(aDb):

        db.sqliteDB.writeToDataBase(aDb, '''CREATE TABLE Languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            Language TEXT UNIQUE NOT NULL)''')

    @staticmethod
    def createTableUpdates(aDb):

        db.sqliteDB.writeToDataBase(aDb, '''CREATE TABLE Updates (
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

    def getAvalibleVersions(self):

        mutex = thread.allocate_lock()
        items = []
        thread.start_new_thread(SQLite._getAvalibleVersions, (mutex, self.mInit, items))
        while not mutex.locked():
            pass
        return SQLite.makeAvalibleList(items)

    def getAvalibleTypes(self):

        mutex = thread.allocate_lock()
        items = []
        thread.start_new_thread(SQLite._getAvalibleTypes, (mutex, self.mInit, items))
        while not mutex.locked():
            pass
        return SQLite.makeAvalibleList(items)

    def getAvalibleLanguages(self):

        mutex = thread.allocate_lock()
        items = []
        thread.start_new_thread(SQLite._getAvalibleLanguages, (mutex, self.mInit, items))
        while not mutex.locked():
            pass
        return SQLite.makeAvalibleList(items)

    def get(self, aQuery):

        mutex = thread.allocate_lock()
        updates = []
        thread.start_new_thread(SQLite._get, (mutex, self.mInit, aQuery, updates))
        while not mutex.locked():
            pass
        return updates

    @staticmethod
    def makeAvalibleList(aList):

        items = []
        for i in aList:
            if not isinstance(i, dict):
                items.append(i)
        return items


class MongoDB(Storage):

    def __init__(self, aInit):

        if 2 == sys.version_info[0]:
            Storage.__init__(self, 'MongoDB')
        else:
            super(MongoDB, self).__init__('MongoDB')
        self.mDbClient = db.mongoDB.MongoDBClient(aInit)

    def getAvalibleVersions(self):

        expression = []
        expression.append({'$group': {'_id': {'Version': '$Version'}, 'count': {'$sum': 1}}})
        expression.append({'$sort': {'count': -1}})
        expression.append({'$project': {'_id':'$_id.Version', 'count': '$_id.count'}})
        return MongoDB.makeAvalibleList(self.mDbClient.aggregate('win32', 'updates', expression))

    def getAvalibleTypes(self):

        expression = []
        expression.append({'$group': {'_id': {'Type': '$Type'}, 'count': {'$sum': 1}}})
        expression.append({'$sort': {'count': -1}})
        expression.append({'$project': {'_id': '$_id.Type', 'count': '$_id.count'}})
        return MongoDB.makeAvalibleList(self.mDbClient.aggregate('win32', 'updates', expression))

    def getAvalibleLanguages(self):

        expression = []
        expression.append({'$group': {'_id': {'Language': '$Language'}, 'count': {'$sum': 1}}})
        expression.append({'$sort': {'count': -1}})
        expression.append({'$project': {'_id':'$_id.Language', 'count': '$_id.count'}})
        return MongoDB.makeAvalibleList(self.mDbClient.aggregate('win32', 'updates', expression))

    def getWithSkipLimitAndSort(self, aQuery, aSkip, aLimit, aSort):

        return self.mDbClient.getItemsFromDB('win32', 'updates', aQuery, {'_id': 0}, aSkip, aLimit, aSort)

    def get(self, aQuery):

        return self.mDbClient.getItemsFromDB('win32', 'updates', aQuery)

    @staticmethod
    def makeAvalibleList(aList):

        items = []
        for i in aList:
            key = list(i.keys())[0]
            if not isinstance(i[key], dict):
                items.append(i[key])
        return items


def getStorage(aInit):

    if os.path.isdir(aInit) or os.path.isfile(aInit):
        if os.path.exists(aInit):
            if os.path.isdir(aInit):
                return Uif(aInit)
            else:
                name, extension = os.path.splitext(aInit)
                extension = os.path.normcase(os.path.normpath(extension))
                if '.uif' == extension:
                    return Uif(aInit)
                else:
                    return SQLite(aInit)
        else:
            raise IOError('Path {} does not exist'.format(aInit))
    elif ':memory:' == aInit:
        return SQLite(aInit)
    else:
        return MongoDB(aInit)
