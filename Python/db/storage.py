import sys
import json
import os.path
import core.dirs
import db.mongoDB
import db.sqliteDB


class Storage:

    def __init__(self, aType):

        self.mType = aType

    def get(self, aQuery, aCondition=(lambda a, b: (a == b))):

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

    def get(self, aQuery, aCondition=(lambda a, b: (a == b))):

        updates = []

        for update in self.mUpdates:
            match = True

            for key in aQuery.keys():
                if not aCondition(update[key], aQuery.get(key)):
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
        self.mDb = db.sqliteDB.connect(aInit)

    def get(self, aQuery, aCondition=(lambda a, b: (a == b))):

        # TODO: aCondition not used
        return db.sqliteDB.getUpdates(self.mDb, aQuery)


class MongoDB(Storage):

    def __init__(self, aInit):

        if 2 == sys.version_info[0]:
            Storage.__init__(self, 'MongoDB')
        else:
            super(MongoDB, self).__init__('MongoDB')
        self.mDbClient = db.mongoDB.MongoDBClient(aInit)

    def get(self, aQuery, aCondition=(lambda a, b: (a == b))):

        # TODO: aCondition not used
        return self.mDbClient.getItemsFromDB('win32', 'updates', aQuery)


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
