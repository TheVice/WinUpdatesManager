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


class Storage:

    def __init__(self, aType):

        self.mType = aType

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

    def get(self, aQuery):

        updates = []

        for update in self.mUpdates:
            match = True

            for key in aQuery.keys():
                if not update[key] == aQuery.get(key):
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
            files = []
            allFiles = core.dirs.getSubDirectoryFiles(aPath)
            for f in allFiles:
                if -1 != f.rfind('.uif'):
                    files.append(os.path.normpath('{}{}'.format(aPath, f)))

            count = len(files)
            i = 1
            for f in files:
                updates.extend(Uif.getUpdatesFromFile(f))
                print(str(i) + ' / ' + str(count) + ' ' + str(f))
                i += 1
        return updates

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
        aItems.extend(db.sqliteDB.listCollections(sqlite, 'Versions'))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _getAvalibleTypes(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(db.sqliteDB.listCollections(sqlite, 'Types'))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _getAvalibleLanguages(aMutex, aPath, aItems):

        sqlite = db.sqliteDB.connect(aPath)
        aItems.extend(db.sqliteDB.listCollections(sqlite, 'Languages'))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

    @staticmethod
    def _get(aMutex, aPath, aQuery, aUpdates):

        sqlite = db.sqliteDB.connect(aPath)
        aUpdates.extend(db.sqliteDB.getUpdates(sqlite, aQuery))
        db.sqliteDB.disconnect(sqlite)
        aMutex.acquire()

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

            print('Path {0} does not exist'.format(aInit))

    elif ':memory:' == aInit:

        return SQLite(aInit)
    else:

        return MongoDB(aInit)
