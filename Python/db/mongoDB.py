from hashlib import new
from sys import exc_info
try:
    from bson import ObjectId
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
except:
    pass

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
            raise Exception(exc_info()[1])

    def getItemsFromDB(self, aDB, aTable, aQuery={}, aProjection=None,
                       aSkip=None, aLimit=None, aSort=None):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

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

            return list(items)

        except:
            raise Exception(exc_info()[1])

    def getItemsCount(self, aDB, aTable, aQuery={}):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            items = table.find(aQuery)

            return items.count(True)

        except:
            raise Exception(exc_info()[1])

    def insertToDB(self, aDB, aTable, aItems):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            if isinstance(aItems, list):
                table.insert_many(aItems)
            else:
                table.insert_one(aItems)

        except:
            raise Exception(exc_info()[1])

    def updateInDB(self, aDB, aTable, aItems):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            if isinstance(aItems, list):
                for item in aItems:
                    try:
                        table.insert_one(item)
                    except DuplicateKeyError:
                        table.replace_one({'_id': item['_id']}, item)
            else:
                try:
                    table.insert_one(aItems)
                except DuplicateKeyError:
                    table.replace_one({'_id': aItems['_id']}, aItems)

        except:
            raise Exception(exc_info()[1])

    def deleteFromDB(self, aDB, aTable, aItems):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            if isinstance(aItems, list):
                for item in aItems:
                    table.delete_one(item)
            else:
                table.delete_one(aItems)

        except:
            raise Exception(exc_info()[1])

    def dropDB(self, aDB):

        try:
            self.mClient.drop_database(aDB)

        except:
            raise Exception(exc_info()[1])

    def dropCollectionsInDB(self, aDB, aTable):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            table.drop()

        except:
            raise Exception(exc_info()[1])

    def getDBs(self):

        return self.mClient.database_names()

    def getCollectionsFromDB(self, aDB):

        try:
            db = self.mClient[aDB]
            return db.collection_names()

        except:
            raise Exception(exc_info()[1])

    def aggregate(self, aDB, aTable, aAggregateExpression):

        try:
            db = self.mClient[aDB]
            table = db[aTable]

            return list(table.aggregate(aAggregateExpression))

        except:
            raise Exception(exc_info()[1])

    def getUniqueItemsFromCollection(self, aDB, aTable, aCollection):

        collection = []

        inputIds = []
        for item in aCollection:
            inputIds.append(item['_id'])

        if 0 < len(inputIds):

            query = {'_id': {'$in': inputIds}}
            items = self.getItemsFromDB(aDB, aTable, query)

            dbIds = []
            for item in items:
                dbIds.append(item['_id'])

            uniqueIds = list(set(inputIds) - set(dbIds))

            for uniqueId in uniqueIds:
                for inputItem in aCollection:
                    if uniqueId == inputItem['_id']:
                        collection.append(inputItem)
                        break

        return collection

    @staticmethod
    def generateObjectId(aString):

        h = new('sha256', aString.encode('utf-8'))
        s = h.hexdigest()[:12]
        return ObjectId(s.encode('utf-8'))

    @staticmethod
    def addObjectIdFieldAtCollection(aCollection):

        for item in aCollection:
            if (item.get('Path') and item.get('KB') and
                item.get('Version') and item.get('Type') and
                item.get('Language') and item.get('Date')):
                s = '{}{}{}{}{}{}'.format(item['Path'],
                                          item['KB'],
                                          item['Version'],
                                          item['Type'],
                                          item['Language'],
                                          item['Date']
                                          )
                item['_id'] = MongoDBClient.generateObjectId(s)
            else:
                s = []
                keys = sorted(item.keys())
                for key in keys:
                    if '_id' != key:
                        s.append('{}'.format(item[key]))
                item['_id'] = MongoDBClient.generateObjectId(''.join(s))

        return aCollection
