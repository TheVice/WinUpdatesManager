import sys
import pymongo


def getItemsFromDB(aDB,
                   aTable,
                   aHostAndPort=None,
                   aWriteConcern='majority',
                   aJournal=True,
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
        raise Exception('Unexpected error:', sys.exc_info()[0])


def insertToDB(aDB,
               aTable,
               aHostAndPort=None,
               aWriteConcern=1,
               aJournal=True,
               aItems=[]):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        table.insert(aItems)

    except:
        raise Exception('Unexpected error:', sys.exc_info()[0])


def updateInDB(aDB,
               aTable,
               aHostAndPort=None,
               aWriteConcern=1,
               aJournal=True,
               aItems=[]):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        for item in aItems:
            table.save(item)

    except:
        raise('Unexpected error:', sys.exc_info()[0])


def deleteFromDB(aDB,
                 aTable,
                 aHostAndPort=None,
                 aWriteConcern=1,
                 aJournal=True,
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
        raise Exception('Unexpected error:', sys.exc_info()[0])


def dropTableInDB(aDB,
                  aTable,
                  aHostAndPort=None,
                  aWriteConcern=1,
                  aJournal=True):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)
        db = client[aDB]
        table = db[aTable]

        table.drop()

    except:
        raise Exception('Unexpected error:', sys.exc_info()[0])


def getDBs(aHostAndPort=None,
           aWriteConcern='majority',
           aJournal=True):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)

        return client.database_names()

    except:
        raise Exception('Unexpected error:', sys.exc_info()[0])


def getCollections(aDB, aHostAndPort=None,
                   aWriteConcern='majority',
                   aJournal=True):

    try:
        client = pymongo.MongoClient(host=aHostAndPort,
                                     w=aWriteConcern,
                                     j=aJournal)

        db = client[aDB]
        return db.collection_names()

    except:
        raise Exception('Unexpected error:', sys.exc_info()[0])

