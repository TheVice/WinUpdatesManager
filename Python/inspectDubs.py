import os
import sys
import core.dirs
import db.uif
import db.mongoDB

dbClient = db.mongoDB.MongoDBClient()


def deleteUpdateDubsFromTable(aDbName='win32', aTableName='updates'):

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


def getUpdateDubsFromTable(aDbName='win32', aTableName='updates',
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

    result = dbClient.aggregate(aDB=aDbName,
                                aTable=aTableName,
                                aAggregateExpression=expression)

    try:
        if result['result'][0]['count'] < 2:
            return None
    except:
        raise Exception('Unexpected error:', sys.exc_info()[0])

    return result


def showUpdateDubsFromJsonFiles(aFiles):

    updates = {}

    for jFile in aFiles:
        fileName = jFile[jFile.rfind(os.sep) + 1:]
        ups = []
        db.uif.getUpdatesFromFile(jFile, ups)
        updates[fileName] = ups

    for key, value in updates.items():
        for key1, value1 in updates.items():
            if key == key1:
                continue

            for up in value:
                for up1 in value1:
                    if up == up1:
                        print(key + ' <-> ' + key1)
                        print(up)

if __name__ == '__main__':

    argc = len(sys.argv)

    if argc == 1:
        print(getUpdateDubsFromTable())
    elif argc == 2:
        jsonStorage = core.dirs.getFilesInDirectory(sys.argv[1], '.json')
        if jsonStorage == []:
            print('There are no JSON files at ' + sys.argv[1])
        else:
            showUpdateDubsFromJsonFiles(jsonStorage)
    elif argc == 3:
        deleteUpdateDubsFromTable()
    else:
        print('Using')
        print(sys.argv[0] + ' for display sample of dubs at db')
        print(sys.argv[0] + ' <path to folder with JSON files>' +
                            ' for inspect JSON files on dubs')
