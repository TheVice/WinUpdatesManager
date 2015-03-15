import sys
import hashlib
import datetime
import pymongo
import bson


class MongoDBClient:

    def getItemsFromDB(self,
                       aDB,
                       aTable,
                       aHostAndPort=None,
                       aQuery={},
                       aProjection=None,
                       aSkip=None,
                       aLimit=None,
                       aSort=None):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)
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
                   aItems=[]):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)
            db = client[aDB]
            table = db[aTable]

            table.insert(aItems)

        except pymongo.errors.DuplicateKeyError:
            print('DuplicateKey:', sys.exc_info())

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def updateInDB(self,
                   aDB,
                   aTable,
                   aHostAndPort=None,
                   aItems=[]):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)
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
                     aItems=[]):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)
            db = client[aDB]
            table = db[aTable]

            for item in aItems:
                table.remove(item)

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def dropTableInDB(self,
                      aDB,
                      aTable,
                      aHostAndPort=None):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)
            db = client[aDB]
            table = db[aTable]

            table.drop()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def getDBs(self,
               aHostAndPort=None):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)

            return client.database_names()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def getCollections(self,
                       aDB,
                       aHostAndPort=None):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)

            db = client[aDB]
            return db.collection_names()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def aggregate(self,
                  aDB,
                  aTable,
                  aHostAndPort=None,
                  aAggregateExpression=[]):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)
            db = client[aDB]
            table = db[aTable]

            return table.aggregate(aAggregateExpression)

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])


def pymongoDate2DateTime(aCollection=[], aFieldName=None):

    for i in range(0, len(aCollection)):
        date = aCollection[i][aFieldName]
        aCollection[i][aFieldName] = datetime.datetime(date.year,
                                                       date.month,
                                                       date.day)

    return aCollection


def addObjectIdField(aCollection=[]):

    for i in range(0, len(aCollection)):
        s = '{}{}{}{}{}{}'.format(aCollection[i]['Path'],
                                  aCollection[i]['KB'],
                                  aCollection[i]['Version'],
                                  aCollection[i]['Type'],
                                  aCollection[i]['Language'],
                                  aCollection[i]['Date']
                                  )
        h = hashlib.new('sha256', s.encode('utf-8'))
        s = h.hexdigest()[:12]
        if bson.ObjectId.is_valid(s.encode('utf-8')):
            aCollection[i]['_id'] = bson.objectid.ObjectId(s.encode('utf-8'))
        else:
            print('Unable set ObjectId for:', str(aCollection[i]))

    return aCollection


def removeDubsByObjectId(aDB, aTable, aCollection, aHostAndPort=None):

    collection = []
    dbClient = MongoDBClient()

    for i in range(0, len(aCollection)):

        objectId = aCollection[i]['_id']
        items = dbClient.getItemsFromDB(aDB, aTable,
                        aHostAndPort=aHostAndPort, aQuery={'_id': objectId})
        itemsCount = items.count()
        if 0 == itemsCount:
            collection.append(aCollection[i])

    return collection


def deleteUpdateDubsFromTable(aDbName, aTableName, aHostAndPort=None):

    dbClient = MongoDBClient()
    items = dbClient.getItemsFromDB(aDbName, aTableName)
    print(items.count())

    updates = []
    for it in items:
        updates.append(it)

    for update in updates:
        query = {}
        query['Path'] = update['Path']
        query['KB'] = update['KB']
        query['Version'] = update['Version']
        query['Type'] = update['Type']
        query['Language'] = update['Language']
        #query['Date'] = update['Date']

        items = dbClient.getItemsFromDB(aDbName, aTableName, aQuery=query)

        if items.count() > 1:

            dubUpdates = []
            for it in items:
                dubUpdates.append(it)

            dubUpdates.remove(dubUpdates[0])
            dbClient.deleteFromDB(aDbName, aTableName, aItems=dubUpdates)

    items = dbClient.getItemsFromDB(aDbName, aTableName)
    print(items.count())


def getUpdateDubsFromTable(aDbName, aTableName, aHostAndPort=None,
                           aSkip=0, aLimit=5):

    expression = [
                  {'$group':
                      {'_id': {
                              'Path': '$Path',
                              'KB': '$KB',
                              'Version': '$Version',
                              'Type': '$Type',
                              'Language': '$Language',
                              'Date': '$Date'
                              },
                         'count': {'$sum': 1}
                      }
                  },
                  {'$sort': {'count': -1}},
                  {'$skip': aSkip},
                  {'$limit': aLimit}]

    client = pymongo.MongoClient(host=aHostAndPort)
    result = client.aggregate(aDB=aDbName,
                              aTable=aTableName,
                              aAggregateExpression=expression)

    try:
        if result['result'][0]['count'] < 2:
            return None
    except:
        raise Exception('Unexpected error:', sys.exc_info()[0])

    return result
