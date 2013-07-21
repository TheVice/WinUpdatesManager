import sys
import pymongo


def getFromDB(aDB='win32',
              aTable='updates',
              aQuery={'': ''},
              aProjection={'': ''},
              aHostAndPort='mongodb://localhost:27017'):

    try:
        client = pymongo.MongoClient(host=aHostAndPort, w='majority', j=True)
        db = client[aDB]
        table = db[aTable]

        items = {}
        if aQuery != {'': ''}:
            if aProjection != {'': ''}:
                items = table.find(aQuery, aProjection)
            else:
                items = table.find(aQuery)
        else:
            items = table.find()

        return items

    except:
        print('Unexpected error:', sys.exc_info()[0])


def insertToDB(aDB='win32',
               aTable='updates',
               aItems=[],
               aHostAndPort='mongodb://localhost:27017'):

    try:
        client = pymongo.MongoClient(host=aHostAndPort, w=1, j=True)
        db = client[aDB]
        table = db[aTable]

        for item in aItems:
            table.insert(item)

    except:
        print('Unexpected error:', sys.exc_info()[0])


def deleteFromDB(aDB='win32',
                 aTable='updates',
                 aItems=[],
                 aHostAndPort='mongodb://localhost:27017'):

    try:
        client = pymongo.MongoClient(host=aHostAndPort, w=1, j=True)
        db = client[aDB]
        table = db[aTable]

        for item in aItems:
            table.remove(item)

    except:
        print('Unexpected error:', sys.exc_info()[0])


if __name__ == '__main__':

    srcItems = [{'file': 1}]
    print('insert')
    insertToDB('test', 'items', srcItems)

    print('get')
    items = getFromDB('test', 'items')

    print('print what we get')
    for item in items:
            print(item)

    print('delete')
    deleteFromDB('test', 'items', items)

    print('print what present')
    items = getFromDB('test', 'items')
    for item in items:
            print(item)
