import sys
import pymongo


def getFromDB(aHostAndPort=None,
              aWriteConcern='majority',
              aJournal=True,
              aDB='win32',
              aTable='updates',
              aQuery={},
              aProjection={},
              aSkip=None,
              aLimit=None):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        items = {}

        if aProjection != {}:
            items = table.find(aQuery, aProjection)
        else:
            items = table.find(aQuery)

        if aSkip is not None:
            items = items.skip(aSkip)

        if aLimit is not None:
            items = items.limit(aLimit)

        return items

    except:
        print('Unexpected error:', sys.exc_info()[0])


def insertToDB(aHostAndPort=None,
               aWriteConcern=1,
               aJournal=True,
               aDB='win32',
               aTable='updates',
               aItems=[]):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        table.insert(aItems)

    except:
        print('Unexpected error:', sys.exc_info()[0])


def updateInDB(aHostAndPort=None,
               aWriteConcern=1,
               aJournal=True,
               aDB='win32',
               aTable='updates',
               aItems=[]):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        table.save(aItems)

    except:
        print('Unexpected error:', sys.exc_info()[0])


def deleteFromDB(aHostAndPort=None,
                 aWriteConcern=1,
                 aJournal=True,
                 aDB='win32',
                 aTable='updates',
                 aItems=[]):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        for item in aItems:
            table.remove(item)

    except:
        print('Unexpected error:', sys.exc_info()[0])


def dropTableInDB(aHostAndPort=None,
                 aWriteConcern=1,
                 aJournal=True,
                 aDB='win32',
                 aTable='updates'):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        table.drop()

    except:
        print('Unexpected error:', sys.exc_info()[0])
