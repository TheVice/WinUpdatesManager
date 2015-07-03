import sys
import db.sqliteDB
from db.storage import Uif, SQLite


if __name__ == '__main__':

    argc = len(sys.argv)
    if 3 == argc:
        storagePath = sys.argv[1]
        dataBasePath = sys.argv[2]
        updates = Uif.getUpdatesFromStorage(storagePath)
        itemsCount = len(updates)

        if 0 < itemsCount:
            print('At \'{}\' found {} update objects'.format(storagePath,
                                                             itemsCount))
            dataBase = db.sqliteDB.connect(dataBasePath, False)
            SQLite.uif2SQLiteDB(dataBase.cursor(), updates)
            dataBase.commit()

            itemsCount = db.sqliteDB.getItemsCount(dataBase, 'Updates')
            db.sqliteDB.disconnect(dataBase)

            print('At database \'{}\' now {} items'.format(dataBasePath, itemsCount))
        else:
            print('Not found update objects at {}'.format(storagePath))

    else:
        print('Using', sys.argv[0],
              '<Folder or file with update info (*.uif)>',
              '<Path to SQLite file>')
