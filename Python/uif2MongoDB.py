import sys
from core.storage import Uif, MongoDB


if __name__ == '__main__':

    argc = len(sys.argv)
    if 4 == argc or 5 == argc:
        storagePath = sys.argv[1]
        dataBaseName = sys.argv[2]
        tableName = sys.argv[3]
        hostAndPort = sys.argv[4] if 5 == argc else None
        updates = Uif.getUpdatesFromStorage(storagePath)
        itemsCount = len(updates)

        if 0 < itemsCount:
            print('At \'{}\' found {} update objects'.format(storagePath,
                                                             itemsCount))

            itemsCount = MongoDB.uif2MongoDB(updates, dataBaseName, tableName,
                                             hostAndPort)

            print('At table \'{}\' of database \'{}\' now {} items'.format(
                                        tableName, dataBaseName, itemsCount))
        else:
            print('Not found update objects at {}'.format(storagePath))

    else:
        print('Using', sys.argv[0],
              '<Folder or file with update info (*.uif)>',
              '<db name> <table name> <host address and port>[optional]',
              'if not set used mongodb://127.0.0.1:27017/')
