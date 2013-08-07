import sys
import pymongo


def getFromDB(aHostAndPort='mongodb://localhost:27017',
              aWriteConcern='majority',
              aJournal=True,
              aDB='win32',
              aTable='updates',
              aQuery={'': ''},
              aProjection={'': ''}):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
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


def insertToDB(aHostAndPort='mongodb://localhost:27017',
               aWriteConcern=1,
               aJournal=True,
               aDB='win32',
               aTable='updates',
               aItems=[],
               aRawItems=False):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        if aRawItems:
            for item in aItems:
                table.insert(item)
        else:
            for item in aItems:
                table.insert(item.toJSON())

    except:
        print('Unexpected error:', sys.exc_info()[0])


def deleteFromDB(aHostAndPort='mongodb://localhost:27017',
                 aWriteConcern=1,
                 aJournal=True,
                 aDB='win32',
                 aTable='updates',
                 aItems=[],
                 aRawItems=False):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        if aRawItems:
            for item in aItems:
                table.remove(item)
        else:
            for item in aItems:
                table.remove(item.toJSON())

    except:
        print('Unexpected error:', sys.exc_info()[0])


