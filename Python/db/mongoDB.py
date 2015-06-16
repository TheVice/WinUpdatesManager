import sys
import hashlib
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
from bson import ObjectId


class MongoDBClient:

    def __init__(self, aHostAndPort, aServerSelectionTimeoutMS=1000):

        self.mClient = None
        self.changeServer(aHostAndPort, aServerSelectionTimeoutMS)

    def changeServer(self, aHostAndPort, aServerSelectionTimeoutMS):

        if self.mClient is not None:
            self.mClient.close()

        self.mClient = MongoClient(host=aHostAndPort,
                            serverSelectionTimeoutMS=aServerSelectionTimeoutMS)
        try:
            self.mClient.server_info()
        except ServerSelectionTimeoutError:
            raise Exception(sys.exc_info())

    def getItemsFromDB(self, aDB, aTable, aQuery={}, aProjection=None,
                       aSkip=None, aLimit=None, aSort=None):

        try:
            db = self.mClient[aDB]
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

    def insertToDB(self, aDB, aTable, aItems):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            table.insert(aItems)

        except DuplicateKeyError:
            raise Exception('DuplicateKey:', sys.exc_info())

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def updateInDB(self, aDB, aTable, aItems):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            for item in aItems:
                table.save(item)

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def deleteFromDB(self, aDB, aTable, aItems):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            for item in aItems:
                table.remove(item)

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def dropDB(self, aDB):

        try:
            self.mClient.drop_database(aDB)

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def dropCollectionsInDB(self, aDB, aTable):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            table.drop()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def getDBs(self):

        try:
            return self.mClient.database_names()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def getCollectionsFromDB(self, aDB):

        try:
            db = self.mClient[aDB]
            return db.collection_names()

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def aggregate(self, aDB, aTable, aAggregateExpression):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            return table.aggregate(aAggregateExpression)

        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

    def removeDubsFromCollectionByObjectId(self, aDB, aTable, aCollection):

        collection = []

        inputObjectIds = []
        for item in aCollection:
            inputObjectIds.append(item['_id'])

        if 0 < len(inputObjectIds):

            query = {'_id': {'$in': inputObjectIds}}
            items = list(self.getItemsFromDB(aDB, aTable, query))

            dataBaseObjectIds = []
            for item in items:
                dataBaseObjectIds.append(item['_id'])

            uniqueObjectIds = list(set(inputObjectIds) -
                                   set(dataBaseObjectIds))
            if 0 < len(uniqueObjectIds):
                for id in uniqueObjectIds:
                    for inputItem in aCollection:
                        if id == inputItem['_id']:
                            collection.append(inputItem)
                            break

        return collection

    def deleteUpdateDubsFromTable(self, aDB, aTableName):

        items = self.getItemsFromDB(aDB, aTableName)

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

            items = self.getItemsFromDB(aDB, aTableName, query)

            if items.count() > 1:

                dubUpdates = []
                for it in items:
                    dubUpdates.append(it)

                dubUpdates.remove(dubUpdates[0])
                self.deleteFromDB(aDB, aTableName, dubUpdates)

    def getUpdateDubsFromTable(self, aDB, aTableName, aSkip=0, aLimit=5):

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

        result = self.aggregate(aDB=aDB,
                                  aTable=aTableName,
                                  aAggregateExpression=expression)

        try:
            if result['result'][0]['count'] < 2:
                return None
        except:
            raise Exception('Unexpected error:', sys.exc_info()[0])

        return result

    @staticmethod
    def generateObjectId(aString):

        h = hashlib.new('sha256', aString.encode('utf-8'))
        aString = h.hexdigest()[:12]
        if ObjectId.is_valid(aString.encode('utf-8')):
            return ObjectId(aString.encode('utf-8'))
        else:
            raise Exception('Unable to generate ObjectId for:', aString)

    @staticmethod
    def addObjectIdFieldAtCollection(aCollection):

        for item in aCollection:
            s = '{}{}{}{}{}{}'.format(item['Path'],
                                      item['KB'],
                                      item['Version'],
                                      item['Type'],
                                      item['Language'],
                                      item['Date']
                                      )
            item['_id'] = MongoDBClient.generateObjectId(s)

        return aCollection
