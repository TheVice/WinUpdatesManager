import sys
from db.storage import Uif
import db.sqliteDB


def uif2SQLiteDB(aPath2DataBase):

    dataBase = db.sqliteDB.connect(aPath2DataBase)
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


if __name__ == '__main__':

    argc = len(sys.argv)
    if 3 == argc:
        storagePath = sys.argv[1]
        updates = Uif.getUpdatesFromStorage(storagePath)
        itemsCount = len(updates)

        if 0 < itemsCount:
            print('At \'{}\' found {} update objects'.format(storagePath,
                                                             itemsCount))

            dataBasePath = sys.argv[2]

            uif2SQLiteDB(dataBasePath)
        else:
            print('Not found update objects at {}'.format(storagePath))

    else:
        print('Using', sys.argv[0],
              '<Folder or file with update info (*.uif)>',
              '<Path to SQLite file>')
