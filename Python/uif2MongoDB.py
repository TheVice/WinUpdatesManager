import sys
from test.jsonHelper import JsonHelper
from db.storage import Uif
from db.mongoDB import MongoDBClient

if __name__ == '__main__':

    argc = len(sys.argv)
    if 3 < argc:

        updates = Uif.getUpdatesFromStorage(sys.argv[1])

        if 0 < len(updates):
            print('At \'{0}\' found {1} update objects'.format(sys.argv[1],
                                                           len(updates)))

            dataBaseName = sys.argv[2]
            tableName = sys.argv[3]
            hostAndPort = None
            if 4 < argc:
                hostAndPort = sys.argv[4]

            for update in updates:
                update['Date'] = JsonHelper.intList2DateTime(JsonHelper.string2intList(update['Date']))

            updates = MongoDBClient.addObjectIdFieldAtCollection(updates)
            dataBase = MongoDBClient(hostAndPort)
            updates = dataBase.removeDubsFromCollectionByObjectId(dataBaseName, tableName, updates)

            if 0 < len(updates):
                dataBase.insertToDB(dataBaseName, tableName, updates)

            itemsCount = dataBase.getItemsFromDB(dataBaseName, tableName).count()
            print('At table \'{0}\' of database \'{1}\' now {2} items'.format(
                                        tableName, dataBaseName, itemsCount))
        else:
            print('Not found update objects at {0}'.format(sys.argv[1]))

    else:
        print('Using', sys.argv[0],
              '<Folder or file with update info (*.uif)>',
              '<db name> <table name> <host address and port>[optional, '
              'if not set used mongodb://127.0.0.1:27017/]')
