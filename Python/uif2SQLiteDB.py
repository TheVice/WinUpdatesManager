import sys
from db.storage import Uif, SQLite
import db.sqliteDB


def uif2SQLiteDB(aPath2DataBase):

    dataBase = db.sqliteDB.connect(aPath2DataBase)

    if not db.sqliteDB.isTableExist(dataBase, 'KBs'):
        SQLite.createTableKBs(dataBase)

    if not db.sqliteDB.isTableExist(dataBase, 'Dates'):
        SQLite.createTableDates(dataBase)

    if not db.sqliteDB.isTableExist(dataBase, 'Paths'):
        SQLite.createTablePaths(dataBase)

    if not db.sqliteDB.isTableExist(dataBase, 'Versions'):
        SQLite.createTableVersions(dataBase)

    if not db.sqliteDB.isTableExist(dataBase, 'Types'):
        SQLite.createTableTypes(dataBase)

    if not db.sqliteDB.isTableExist(dataBase, 'Languages'):
        SQLite.createTableLanguages(dataBase)

    if not db.sqliteDB.isTableExist(dataBase, 'Updates'):
        SQLite.createTableUpdates(dataBase)

    SQLite.addUpdates(dataBase, updates)
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
