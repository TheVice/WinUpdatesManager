import sys
import core.dates
import core.dirs
import core.updates
import db.mongoDB

dbClient = db.mongoDB.MongoDBClient()

if __name__ == '__main__':

    argc = len(sys.argv)

    if argc == 1:
        print('Bad using.')
        print('Sample using ' + sys.argv[0] +
              ' <path to directory with updates>' +
              ' <date for non year edition>')
        print('Sample using ' + sys.argv[0] +
              ' <path to JSON data file, from that insert to MongoDB info>' +
              ' <data base name> <table name>')

    elif argc == 2:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        paths = core.dirs.Paths(files)
        dates = core.dates.getDatesOfUpdates(paths.getRootObjects())
        updates = {'known': [], 'unKnown': []}

        for path, date in zip(paths.getRootPaths(), dates):
            files = paths.getSubObjects(path, True)
            monthUpdates = core.updates.getUpdatesFromPackage(files, date)
            monthUpdates = core.updates.separateToKnownAndUnknown(monthUpdates)
            updates['known'].append(monthUpdates['known'])
            updates['unKnown'].append(monthUpdates['unKnown'])

        for monthUpdates in updates['known']:
            for update in monthUpdates:
                print(update)

        for monthUpdates in updates['unKnown']:
            for update in monthUpdates:
                print(update)

    elif argc == 3:
        files = core.dirs.getSubDirectoryFiles(sys.argv[1])
        updates = core.updates.getUpdatesFromPackage(files,
                  core.dates.getDatesOfUpdates([sys.argv[2]])[0])
        updates = core.updates.separateToKnownAndUnknown(updates)

        for update in updates['known']:
            print(update)

        for update in updates['unKnown']:
            print(update)

    elif argc == 4:
        updates = core.updates.getUpdatesFromJSONfile(sys.argv[1])
        updates = db.mongoDB.pymongoDate2DateTime(updates, 'Date')
        dbClient.insertToDB(aDB=sys.argv[2], aTable=sys.argv[3],
                            aItems=updates)
