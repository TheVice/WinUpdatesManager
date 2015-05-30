import sys
import hashlib
import datetime
import pymongo
import bson


class MongoDBClient:

    def getItemsFromDB(self,
                       aDB,
                       aTable,
                       aHostAndPort,
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
                   aHostAndPort,
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
                   aHostAndPort,
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
                     aHostAndPort,
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
                      aHostAndPort):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)
            db = client[aDB]
            table = db[aTable]

            table.drop()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def getDBs(self,
               aHostAndPort):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)

            return client.database_names()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def getCollections(self,
                       aDB,
                       aHostAndPort):

        try:
            client = pymongo.MongoClient(host=aHostAndPort)

            db = client[aDB]
            return db.collection_names()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def aggregate(self,
                  aDB,
                  aTable,
                  aHostAndPort,
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


def getColumnFromCollection(aCollection, aColumnName):

    columnList = []
    for i in range(0, len(aCollection)):
        columnList.append(aCollection[i][aColumnName])
    return columnList


def removeDubsByObjectId(aDB, aTable, aHostAndPort, aCollection):

    collection = []
    objectIds = getColumnFromCollection(aCollection, '_id')

    if 0 < len(objectIds):

        dbClient = MongoDBClient()
        query = {'_id': {'$in': objectIds}}
        items = dbClient.getItemsFromDB(aDB, aTable, aHostAndPort, query)

        internalItems = []
        for item in items:
            internalItems.append(item)

        for inputItem in aCollection:
            found = False

            for item in internalItems:
                if inputItem['_id'] == item['_id']:
                    found = True
                    break

            if found is False:
                collection.append(inputItem)

    return collection


def deleteUpdateDubsFromTable(aDbName, aTableName, aHostAndPort):

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

        items = dbClient.getItemsFromDB(aDbName, aTableName,
                                        aHostAndPort, aQuery=query)

        if items.count() > 1:

            dubUpdates = []
            for it in items:
                dubUpdates.append(it)

            dubUpdates.remove(dubUpdates[0])
            dbClient.deleteFromDB(aDbName, aTableName, aItems=dubUpdates)

    items = dbClient.getItemsFromDB(aDbName, aTableName, aHostAndPort)
    print(items.count())


def getUpdateDubsFromTable(aDbName, aTableName, aHostAndPort,
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
