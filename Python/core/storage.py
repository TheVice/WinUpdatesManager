import sys
import json
import os.path
import core.dirs
import core.dates
import db.sqliteDB
from core.updates import Updates
from db.mongoDB import MongoDBClient
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

    def get(self, aQuery, aLimit=-1, aSkip=0, aSort=None):

        pass

    def getCount(self, aQuery):

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

    def get(self, aQuery, aLimit=-1, aSkip=0, aSort=None):

        for key in aQuery.keys():
            if key not in Updates.validKeys:
                raise Exception('Unknown field {}'.format(key))

        updates = []

        for update in self.mUpdates:
            match = True

            for key in aQuery.keys():
                if 'Date' == key:
                    aQuery[key] = core.dates.toDate(aQuery[key])
                if isinstance(aQuery.get(key), list):
                    if update[key] not in aQuery[key]:
                        match = False
                        break
                elif not update[key] == aQuery[key]:
                    match = False
                    break

            if match:
                updates.append(update)

        return updates

    def getCount(self, aQuery):

        if aQuery:
            return len(self.get(aQuery))
        return len(self.mUpdates)

    @staticmethod
    def getUpdatesFromFile(aFile):

        updates = []

        try:
            inputFile = open(aFile, 'r')

            for line in inputFile:
                update = json.loads(line)
                update['Date'] = core.dates.toDate(update['Date'])
                updates.append(update)

            inputFile.close()
        except:
            raise Exception('Unexpected error while work with file {} {}'.format(aFile, sys.exc_info()[1]))

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
        return sorted(list(items))


class SQLite(Storage):

    def __init__(self, aInit):

        if 2 == sys.version_info[0]:
            Storage.__init__(self, 'SQLite')
        else:
            super(SQLite, self).__init__('SQLite')
        self.mInit = aInit

    def getAvalibleVersions(self):

        return SQLite.makeAvalibleList(db.sqliteDB.getFrom(self.mInit, 'Versions', 'Version', [], {'Version': 1}))

    def getAvalibleTypes(self):

        return SQLite.makeAvalibleList(db.sqliteDB.getFrom(self.mInit, 'Types', 'Type', [], {'Type': 1}))

    def getAvalibleLanguages(self):

        return SQLite.makeAvalibleList(db.sqliteDB.getFrom(self.mInit, 'Languages', 'Language', [], {'Language': 1}))

    def get(self, aQuery, aLimit=-1, aSkip=0, aSort=None):

        statement = {}
        for key in aQuery.keys():
            row = key
            if 'KB' == key:
                table = 'KBs'
                row = 'id'
                id_name = 'kb_id'
            elif 'Date' == key:
                table = 'Dates'
                id_name = 'date_id'
                aQuery[key] = core.dates.toString(aQuery[key])
            elif 'Version' == key:
                table = 'Versions'
                id_name = 'version_id'
            elif 'Type' == key:
                table = 'Types'
                id_name = 'type_id'
            elif 'Language' == key:
                table = 'Languages'
                id_name = 'language_id'
            elif 'Path' == key:
                table = 'Paths'
                id_name = 'path_id'
            else:
                raise Exception('Unknown field {}'.format(key))

            ids = db.sqliteDB.getFrom(self.mInit, table, 'id', {row: aQuery[key]})

            if ids:
                statement[id_name] = ids
            else:
                return []

        table = 'Updates'
        rows = 'kb_id, date_id, path_id, version_id, type_id, language_id'
        rawUpdates = db.sqliteDB.getFrom(self.mInit, table, rows, statement, aSort, aLimit, aSkip)
        return SQLite.rawUpdatesToUpdates(self.mInit, rawUpdates)

    def getCount(self, aQuery):

        statement = {}
        for key in aQuery.keys():
            row = key
            if 'KB' == key:
                table = 'KBs'
                row = 'id'
                id_name = 'kb_id'
            elif 'Date' == key:
                table = 'Dates'
                id_name = 'date_id'
                aQuery[key] = core.dates.toString(aQuery[key])
            elif 'Version' == key:
                table = 'Versions'
                id_name = 'version_id'
            elif 'Type' == key:
                table = 'Types'
                id_name = 'type_id'
            elif 'Language' == key:
                table = 'Languages'
                id_name = 'language_id'
            elif 'Path' == key:
                table = 'Paths'
                id_name = 'path_id'
            else:
                raise Exception('Unknown field {}'.format(key))

            ids = db.sqliteDB.getFrom(self.mInit, table, 'id', {row: aQuery[key]})

            if ids:
                statement[id_name] = ids
            else:
                return 0

        table = 'Updates'
        return db.sqliteDB.getItemsCount(self.mInit, table, statement)

    @staticmethod
    def makeAvalibleList(aList):

        items = []
        for i in aList:
            if 'UNKNOWN' not in '{}'.format(i):
                items.append(i)
        return items

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

        d = db.sqliteDB.getFrom(aDb, 'Dates', 'Date', {'id': aId})[0]
        return core.dates.toDate(d)

    @staticmethod
    def getPathByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Paths', 'Path', {'id': aId})[0]

    @staticmethod
    def getVersionByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Versions', 'Version', {'id': aId})[0]

    @staticmethod
    def getTypeByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Types', 'Type', {'id': aId})[0]

    @staticmethod
    def getLanguageByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Languages', 'Language', {'id': aId})[0]

    @staticmethod
    def getSetSubstanceID(aDb, aTable, aRowName, aItem):

        substanceID = db.sqliteDB.getFrom(aDb, aTable, 'id', {aRowName: aItem})

        if len(substanceID):
            return substanceID[0]

        db.sqliteDB.insertInto(aDb, aTable, aRowName, aItem)

        return db.sqliteDB.getFrom(aDb, aTable, 'id', {aRowName: aItem})[0]

    @staticmethod
    def uif2SQLiteDB(aDataBase, aUpdates):

        statement = []

        if not db.sqliteDB.isTableExist(aDataBase, 'KBs'):
            statement.append('CREATE TABLE KBs ('
                             'id INTEGER PRIMARY KEY UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(aDataBase, 'Dates'):
            statement.append('CREATE TABLE Dates ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Date DATE UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(aDataBase, 'Paths'):
            statement.append('CREATE TABLE Paths ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Path TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(aDataBase, 'Versions'):
            statement.append('CREATE TABLE Versions ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Version TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(aDataBase, 'Types'):
            statement.append('CREATE TABLE Types ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Type TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(aDataBase, 'Languages'):
            statement.append('CREATE TABLE Languages('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Language TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(aDataBase, 'Updates'):
            statement.append('CREATE TABLE Updates ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'kb_id INTEGER NOT NULL,'
                             'date_id INTEGER NOT NULL,'
                             'path_id INTEGER NOT NULL,'
                             'version_id INTEGER NOT NULL,'
                             'type_id INTEGER NOT NULL,'
                             'language_id INTEGER NOT NULL,'
                             'FOREIGN KEY(kb_id) REFERENCES KBs(id),'
                             'FOREIGN KEY(date_id) REFERENCES Dates(id),'
                             'FOREIGN KEY(path_id) REFERENCES Paths(id),'
                             'FOREIGN KEY(version_id) REFERENCES Versions(id),'
                             'FOREIGN KEY(type_id) REFERENCES Types(id),'
                             'FOREIGN KEY(language_id) REFERENCES Languages(id));')

        db.sqliteDB.writeAsync(aDataBase, ''.join(statement))

        count = len(aUpdates)

        for update, i in zip(aUpdates, range(1, count + 1)):
            kb = update['KB'] if not isinstance(update['KB'], dict) else -1
            date = '{}'.format(update['Date'])
            path = '{}'.format(update['Path'])
            osVersion = '{}'.format(update['Version'] if not isinstance(update['Version'], dict) else 'UNKNOWN VERSION')
            osType = '{}'.format(update['Type'] if not isinstance(update['Type'], dict) else 'UNKNOWN TYPE')
            language = '{}'.format(update['Language'] if not isinstance(update['Language'], dict) else 'UNKNOWN LANGUAGE')

            kb_id = SQLite.getSetSubstanceID(aDataBase, 'KBs', 'id', kb)
            date_id = SQLite.getSetSubstanceID(aDataBase, 'Dates', 'Date', date)
            path_id = SQLite.getSetSubstanceID(aDataBase, 'Paths', 'Path', path)
            version_id = SQLite.getSetSubstanceID(aDataBase, 'Versions', 'Version', osVersion)
            type_id = SQLite.getSetSubstanceID(aDataBase, 'Types', 'Type', osType)
            language_id = SQLite.getSetSubstanceID(aDataBase, 'Languages', 'Language', language)

            table = 'Updates'
            rows = 'kb_id, date_id, path_id, version_id, type_id, language_id'
            items = [[kb_id, date_id, path_id, version_id, type_id, language_id]]
            db.sqliteDB.insertInto(aDataBase, table, rows, items)

            print('{} / {}'.format(i, count))


class MongoDB(Storage):

    def __init__(self, aInit, aDataBase, aTable):

        if 2 == sys.version_info[0]:
            Storage.__init__(self, 'MongoDB')
        else:
            super(MongoDB, self).__init__('MongoDB')
        self.mDbClient = db.mongoDB.MongoDBClient(aInit)
        self.mDataBase = aDataBase
        self.mTable = aTable

    def getAvalibleVersions(self):

        expression = []
        expression.append({'$group': {'_id': {'Version': '$Version'}, 'count': {'$sum': 1}}})
        expression.append({'$sort': {'_id': 1}})
        expression.append({'$project': {'_id':'$_id.Version', 'count': '$_id.count'}})
        return MongoDB.makeAvalibleList(self.mDbClient.aggregate(self.mDataBase, self.mTable, expression))

    def getAvalibleTypes(self):

        expression = []
        expression.append({'$group': {'_id': {'Type': '$Type'}, 'count': {'$sum': 1}}})
        expression.append({'$sort': {'_id': 1}})
        expression.append({'$project': {'_id': '$_id.Type', 'count': '$_id.count'}})
        return MongoDB.makeAvalibleList(self.mDbClient.aggregate(self.mDataBase, self.mTable, expression))

    def getAvalibleLanguages(self):

        expression = []
        expression.append({'$group': {'_id': {'Language': '$Language'}, 'count': {'$sum': 1}}})
        expression.append({'$sort': {'_id': 1}})
        expression.append({'$project': {'_id':'$_id.Language', 'count': '$_id.count'}})
        return MongoDB.makeAvalibleList(self.mDbClient.aggregate(self.mDataBase, self.mTable, expression))

    def get(self, aQuery, aLimit=-1, aSkip=0, aSort=None):

        for key in aQuery.keys():
            if key not in Updates.validKeys:
                raise Exception('Unknown field {}'.format(key))

        for key in aQuery.keys():
            if 'Date' == key:
                aQuery[key] = core.dates.toDateTime(aQuery[key])
            if isinstance(aQuery[key], list):
                aQuery[key] = {'$in': aQuery[key]}
        if aLimit < 0:
            aLimit = None
        return self.mDbClient.getItemsFromDB(self.mDataBase, self.mTable, aQuery, {'_id': 0}, aSkip, aLimit, aSort)

    def getCount(self, aQuery):

        for key in aQuery.keys():
            if key not in Updates.validKeys:
                raise Exception('Unknown field {}'.format(key))

        for key in aQuery.keys():
            if 'Date' == key:
                aQuery[key] = core.dates.toDateTime(aQuery[key])
            if isinstance(aQuery[key], list):
                aQuery[key] = {'$in': aQuery[key]}
        return self.mDbClient.getItemsCount(self.mDataBase, self.mTable, aQuery)

    @staticmethod
    def makeAvalibleList(aList):

        items = []
        for i in aList:
            key = list(i.keys())[0]
            if not isinstance(i[key], dict):
                items.append(i[key])
        return items

    @staticmethod
    def uif2MongoDB(aUpdates, aDataBaseName, aTableName, aHostAndPort):

        for update in aUpdates:
            update['Date'] = core.dates.toDateTime(update['Date'])

        updates = MongoDBClient.addObjectIdFieldAtCollection(aUpdates)
        dataBase = MongoDBClient(aHostAndPort)
        updates = dataBase.getUniqueItemsFromCollection(aDataBaseName, aTableName, updates)

        if 0 < len(updates):
            dataBase.insertToDB(aDataBaseName, aTableName, updates)

        return len(dataBase.getItemsFromDB(aDataBaseName, aTableName))


def getStorage(aInit):

    if os.path.isdir(aInit) or os.path.isfile(aInit):
        if os.path.exists(aInit):
            if os.path.isdir(aInit):
                return Uif(aInit)
            else:
                extension = os.path.splitext(aInit)[1]
                if '.uif' == str.lower(extension):
                    return Uif(aInit)
                else:
                    return SQLite(aInit)
        else:
            raise OSError('Path {} does not exist'.format(aInit))
    elif ':memory:' == aInit:
        return SQLite(aInit)
    else:
        return MongoDB(aInit, 'win32', 'updates')
