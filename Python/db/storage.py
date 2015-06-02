import os.path
import db.uif
import db.sqliteDB
import db.mongoDB


class Storage:

    def __init__(self, aType):

        self.mType = aType

    def get(self, aQuery, aCondition=(lambda a, b: (a == b))):

        pass

    def __str__(self):

        return str(self.mType)


class Uif(Storage):

    def __init__(self, aInit):

        super(Uif, self).__init__('Uif')
        self.mUpdates = db.uif.getUpdatesFromStorage(aInit)

    def get(self, aQuery, aCondition=(lambda a, b: (a == b))):

        return db.uif.get(self.mUpdates, aQuery, aCondition)


class SQLite(Storage):

    def __init__(self, aInit):

        super(SQLite, self).__init__('SQLite')
        self.mDb = db.sqliteDB.connect(aInit)

    def get(self, aQuery, aCondition=(lambda a, b: (a == b))):

        # TODO: aCondition not used
        return db.sqliteDB.getUpdates(self.mDb, aQuery)


class MongoDB(Storage):

    def __init__(self, aInit):

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
