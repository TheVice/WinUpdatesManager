import sys
import db.uif
import db.mongoDB

if __name__ == '__main__':

    argc = len(sys.argv)
    if 3 < argc:

        updates = db.uif.getUpdatesFromStorage(sys.argv[1])

        if len(updates) > 0:
            print('At {0} found {1} update objects'.format(sys.argv[1],
                                                           len(updates)))

            updates = db.mongoDB.pymongoDate2DateTime(updates, 'Date')
            updates = db.mongoDB.addObjectIdField(updates)
            dataBase = db.mongoDB.MongoDBClient()

            if 4 < argc:
                dataBase.insertToDB(aDB=sys.argv[2], aTable=sys.argv[3],
                                    aItems=updates, aHostAndPort=sys.argv[4])
            else:
                dataBase.insertToDB(aDB=sys.argv[2], aTable=sys.argv[3],
                                    aItems=updates)

            items = dataBase.getItemsFromDB(aDB=sys.argv[2],
                                            aTable=sys.argv[3])
            print('At table {0} of database {1} now {2} items'.format(
                                    sys.argv[3], sys.argv[2], items.count()))

        else:
            print('Not found update objects at {0}'.format(sys.argv[1]))

    else:
        print('Using', sys.argv[0],
              '<Folder or file with update info (*.uif)>',
              '<db name> <table name> <host address and port>[optional, '
              'if not set used mongodb://127.0.0.1:27017/]')
