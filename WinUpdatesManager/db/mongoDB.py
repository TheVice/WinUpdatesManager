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
        print('Unexpected error:', sys.exc_info())


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
        print('Unexpected error:', sys.exc_info())


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
        print('Unexpected error:', sys.exc_info())


def constructQueryFromUpdateInfo(aFileName='',
                                 aKb='',
                                 aVersion='',
                                 aOsType='',
                                 aLanguage='',
                                 aDate=''):

    query = {'Name': aFileName,
             'KB': aKb,
             'Version': aVersion,
             'Type': aOsType,
             'Language': aLanguage,
             'Date': aDate
            }

    return query


if __name__ == '__main__':

    items = [constructQueryFromUpdateInfo('file')]
    print('insert')
    insertToDB('test', 'items', items)
    print('get')
    items2 = getFromDB('test', 'items')
    print('print what we get')
    for item in items2:
            print(item)
    print('delete')
    deleteFromDB('test', 'items', items)
    print('print what present')
    items2 = getFromDB('test', 'items')
    for item in items2:
            print(item)
