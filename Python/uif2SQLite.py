import sys
from db.storage import Uif
import db.sqliteDB

if __name__ == '__main__':

    argc = len(sys.argv)
    if 2 < argc:

        updates = Uif.getUpdatesFromStorage(sys.argv[1])

        if len(updates) > 0:
            print('At {0} found {1} update objects'.format(sys.argv[1],
                                                           len(updates)))

            dataBase = db.sqliteDB.connect(sys.argv[2])
            tables = db.sqliteDB.listTables(dataBase)
            if 0 == tables.count('KBs'):

                db.sqliteDB.createTableKBs(dataBase)

            if 0 == tables.count('Dates'):

                db.sqliteDB.createTableDates(dataBase)

            if 0 == tables.count('Paths'):

                db.sqliteDB.createTablePaths(dataBase)

            if 0 == tables.count('Versions'):

                db.sqliteDB.createTableVersions(dataBase)

            if 0 == tables.count('Types'):

                db.sqliteDB.createTableTypes(dataBase)

            if 0 == tables.count('Languages'):

                db.sqliteDB.createTableLanguages(dataBase)

            if 0 == tables.count('Updates'):

                db.sqliteDB.createTableUpdates(dataBase)

            db.sqliteDB.addUpdates(dataBase, updates)
            db.sqliteDB.disconnect(dataBase)

        else:
            print('Not found update objects at {0}'.format(sys.argv[1]))

    else:
        print('Using', sys.argv[0],
              '<Folder or file with update info (*.uif)>',
              '<Path to SQLite file>')
