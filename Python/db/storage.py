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
    def uif2SQLiteDB(aDataBase, aUpdates):

        connection = db.sqliteDB.connect(aDataBase)
        statement = []

        if not db.sqliteDB.isTableExist(connection, 'KBs'):
            statement.append('CREATE TABLE KBs ('
                             'id INTEGER PRIMARY KEY UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(connection, 'Dates'):
            statement.append('CREATE TABLE Dates ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Date DATE UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(connection, 'Paths'):
            statement.append('CREATE TABLE Paths ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Path TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(connection, 'Versions'):
            statement.append('CREATE TABLE Versions ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Version TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(connection, 'Types'):
            statement.append('CREATE TABLE Types ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Type TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(connection, 'Languages'):
            statement.append('CREATE TABLE Languages('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,'
                             'Language TEXT UNIQUE NOT NULL);')

        if not db.sqliteDB.isTableExist(connection, 'Updates'):
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

        db.sqliteDB.write(connection, ''.join(statement))

        SQLite.addUpdates(connection, aUpdates)
        db.sqliteDB.disconnect(connection)


    @staticmethod
    def _getAvalibleVersions(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(SQLite.makeAvalibleList(db.sqliteDB.getFrom(sqlite, 'Versions', 'Version')))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _getAvalibleTypes(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(SQLite.makeAvalibleList(db.sqliteDB.getFrom(sqlite, 'Types', 'Type')))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _getAvalibleLanguages(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(SQLite.makeAvalibleList(db.sqliteDB.getFrom(sqlite, 'Languages', 'Language')))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _get(aMutex, aPath, aQuery, aUpdates):

        sqlite = db.sqliteDB.connect(aPath)
        aUpdates.extend(SQLite.getUpdates(sqlite, aQuery))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def getUpdates(aDb, aQuery):

        statement = ('SELECT kb_id, date_id, path_id, version_id,'
                     ' type_id, language_id FROM Updates')

        template = []
        for key in aQuery.keys():
            if 'KB' == key:
                kb_id = db.sqliteDB.getFrom(aDb, 'KBs', ['id'], {'id': aQuery[key]})
                if kb_id == []:
                    return []
                template.append('kb_id LIKE {}'.format(kb_id[0]))
            elif 'Date' == key:
                date_id = db.sqliteDB.getFrom(aDb, 'Dates', ['id'], {'Date': '{}'.format(aQuery[key])})
                if date_id == []:
                    return []
                template.append('date_id LIKE {}'.format(date_id[0]))
            elif 'Version' == key:
                version_id = db.sqliteDB.getFrom(aDb, 'Versions', ['id'], {'Version': '{}'.format(aQuery[key])})
                if version_id == []:
                    return []
                template.append('version_id LIKE {}'''.format(version_id[0]))
            elif 'Type' == key:
                    type_id = db.sqliteDB.getFrom(aDb, 'Types', ['id'], {'Type': '{}'.format(aQuery[key])})
                    if type_id == []:
                        return []
                    template.append('type_id LIKE {}'.format(type_id[0]))
            elif 'Language' == key:
                    language_id = db.sqliteDB.getFrom(aDb, 'Languages', ['id'], {'Language': '{}'.format(aQuery[key])})
                    if language_id == []:
                        return []
                    template.append('language_id LIKE {}'.format(language_id[0]))
            elif 'Path' == key:
                    path_id = db.sqliteDB.getFrom(aDb, 'Paths', ['id'], {'Path': '{}'.format(aQuery[key])})
                    if path_id is None:
                        return []
                    template.append('path_id LIKE {}'''.format(path_id[0]))

        if len(template):
            template = '{}'.format(template)
            template = template.replace('[', '').replace(']', '')
            template = template.replace('\'', '')
            template = template.replace(',', ' AND')
            statement = '{} WHERE {}'.format(statement, template)

        rawUpdates = db.sqliteDB.read(aDb, statement, lambda l: l.fetchall())
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

        return db.sqliteDB.getFrom(aDb, 'Dates', ['Date'], {'id': aId})[0]

    @staticmethod
    def getPathByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Paths', ['Path'], {'id': aId})[0]

    @staticmethod
    def getVersionByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Versions', ['Version'], {'id': aId})[0]

    @staticmethod
    def getTypeByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Types', ['Type'], {'id': aId})[0]

    @staticmethod
    def getLanguageByID(aDb, aId):

        return db.sqliteDB.getFrom(aDb, 'Languages', ['Language'], {'id': aId})[0]

    @staticmethod
    def getSetSubstanceID(aDb, aTable, aRowName, aItem):

        substanceID = db.sqliteDB.getFrom(aDb, aTable, ['id'], {aRowName: aItem})

        if len(substanceID):
            return substanceID[0]

        db.sqliteDB.insertInto(aDb, aTable, [aItem], aRowName)

        return db.sqliteDB.getFrom(aDb, aTable, ['id'], {aRowName: aItem})[0]

    @staticmethod
    def addUpdates(aDb, aUpdates):

        count = len(aUpdates)
        cursor = aDb.cursor()

        for update, i in zip(aUpdates, range(count)):
            kb = update['KB'] if not isinstance(update['KB'], dict) else -1
            date = '\'{}\''.format(update['Date'])
            path = '\'{}\''.format(update['Path'])
            osVersion = '\'{}\''.format(update['Version'] if not isinstance(update['Version'], dict) else 'UNKNOWN VERSION')
            osType = '\'{}\''.format(update['Type'] if not isinstance(update['Type'], dict) else 'UNKNOWN TYPE')
            language = '\'{}\''.format(update['Language'] if not isinstance(update['Language'], dict) else 'UNKNOWN LANGUAGE')

            kb_id = SQLite.getSetSubstanceID(cursor, 'KBs', 'id', kb)
            date_id = SQLite.getSetSubstanceID(cursor, 'Dates', 'Date', date)
            path_id = SQLite.getSetSubstanceID(cursor, 'Paths', 'Path', path)
            version_id = SQLite.getSetSubstanceID(cursor, 'Versions', 'Version', osVersion)
            type_id = SQLite.getSetSubstanceID(cursor, 'Types', 'Type', osType)
            language_id = SQLite.getSetSubstanceID(cursor, 'Languages', 'Language', language)

            statement = 'INSERT INTO Updates (kb_id, date_id, path_id, version_id, type_id, language_id) VALUES ({}, {}, {}, {}, {}, {})'
            statement = statement.format(kb_id, date_id, path_id, version_id, type_id, language_id)

            cursor.execute(statement)

            print('{} / {}'.format(i, count))

        aDb.commit()

    def getAvalibleVersions(self):

        mutex = thread.allocate_lock()
        items = []
        thread.start_new_thread(SQLite._getAvalibleVersions, (mutex, self.mInit, items))
        while not mutex.locked():
            pass
        return items

    def getAvalibleTypes(self):

        mutex = thread.allocate_lock()
        items = []
        thread.start_new_thread(SQLite._getAvalibleTypes, (mutex, self.mInit, items))
        while not mutex.locked():
            pass
        return items

    def getAvalibleLanguages(self):

        mutex = thread.allocate_lock()
        items = []
        thread.start_new_thread(SQLite._getAvalibleLanguages, (mutex, self.mInit, items))
        while not mutex.locked():
            pass
        return items

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
            if -1 == '{}'.format(i).find('UNKNOWN'):
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
