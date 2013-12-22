import sys
import datetime
import pymongo


class MongoDBClient:

    def getItemsFromDB(self,
                       aDB,
                       aTable,
                       aHostAndPort=None,
                       aWriteConcern='majority',
                       aJournal=True,
                       aQuery={},
                       aProjection=None,
                       aSkip=None,
                       aLimit=None,
                       aSort=None):

        try:
            client = pymongo.MongoClient(host=aHostAndPort,
                                         w=aWriteConcern,
                                         j=aJournal)
            db = client[aDB]
            table = db[aTable]

            items = {}

            if aProjection is not None:
                items = table.find(aQuery, aProjection)
            else:
                items = table.find(aQuery)

            if aSkip is not None:
                items = items.skip(aSkip)

            if aLimit is not None:
                items = items.limit(aLimit)

            if aSort is not None:
                items = items.sort(aSort)

            return items

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def insertToDB(self,
                   aDB,
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

    def updateInDB(self,
                   aDB,
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

    def deleteFromDB(self,
                     aDB,
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

    def dropTableInDB(self,
                      aDB,
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

    def getDBs(self,
               aHostAndPort=None,
               aWriteConcern='majority',
               aJournal=True):

        try:
            client = pymongo.MongoClient(host=aHostAndPort,
                                         w=aWriteConcern,
                                         j=aJournal)

            return client.database_names()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def getCollections(self,
                       aDB,
                       aHostAndPort=None,
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


def pymongoDate2DateTime(aCollection=[], aFieldName=None):

    for i in range(0, len(aCollection)):
        date = aCollection[i][aFieldName]
        aCollection[i][aFieldName] = datetime.datetime(date.year,
                                                       date.month,
                                                       date.day)

    return aCollection
