import db.mongoDB

#before apply check at mongo that you real have dubs
#db.updates.aggregate([
#{"$group" : {"_id" : {"Path" : "$Path", "KB" : "$KB",
#    "Version" : "$Version", "Language" : "$Language",
#    "Date" : "$Date"}, "count" : {"$sum" : 1}}},
#{"$sort" : {"count" : -1}},
#{"$limit" : 5}
#]);

dbClient = db.mongoDB.MongoDBClient()

if __name__ == '__main__':
    items = dbClient.getItemsFromDB('win32', 'updates')
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

        items = dbClient.getItemsFromDB('win32', 'updates', aQuery=query)

        if items.count() > 1:

            dubUpdates = []
            for it in items:
                dubUpdates.append(it)

            dubUpdates.remove(dubUpdates[0])
            dbClient.deleteFromDB('win32', 'updates', aItems=dubUpdates)

    items = dbClient.getItemsFromDB('win32', 'updates')
    print(items.count())
