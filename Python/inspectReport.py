import sys
import core.updates
import db.mongoDB

dbClient = db.mongoDB.MongoDBClient()


def kbsToQueryPathList(aKBs):

    kbList = []
    for kb in aKBs:

        kbList.append({'Path': {'$regex': str(kb)}})

    return kbList


def kbsToQueryList(aKBs):

    kbList = []
    for kb in aKBs:

        kbList.append({'KB': kb})

    return kbList


def items2KBs(aItems):

    kbs = []
    for it in aItems:

        kbs.append(it['KB'])

    return kbs


def getListDiff(aParentList, aChildList):

    return list(set(aParentList) - set(aChildList))


def getData(aKBs, aQueryReq, aSortReq=None):

    ret = {}
    items = dbClient.getItemsFromDB('win32', 'updates', aQuery=aQueryReq,
                                    aSort=aSortReq)

    if 0 != items.count():
        updates = core.updates.Updates()
        updates.addUpdates(items)

        KBs = getListDiff(aKBs, items2KBs(updates))

        ret['Updates'] = updates
        ret['KBs'] = KBs
    else:
        ret['KBs'] = KBs

    return ret

if __name__ == '__main__':

    argc = len(sys.argv)
    if 4 < argc:
        KBs = core.updates.getKBsFromReportFile(sys.argv[1])

        print('At the input report', sys.argv[1], 'located', KBs)
        print('Count', len(KBs))

        version = sys.argv[2]
        platform = sys.argv[3]
        language = sys.argv[4]

        query = {}
        query['$or'] = kbsToQueryPathList(KBs)  # kbsToQueryList(KBs)
        query['Version'] = version
        query['Type'] = platform
        query['Language'] = language

        sort = [('Date', 1), ('KB', 1)]

        data = getData(KBs, query, sort)

        updates = data.get('Updates')

        if updates is not None:
            print('Count of updates queried from db -', len(updates))

            for up in updates:
                print(up['Path'])
        else:
            print('Unable to find any updates')

        KBs = data.get('KBs')

        if 0 != len(KBs):
            print('Not founded by strict query')

            for kb in KBs:
                print(kb)

            query = {}
            query['$or'] = kbsToQueryList(KBs)

            data = getData(KBs, query)

            updates = data.get('Updates')

            if updates is not None:
                print('Founded by number only')

                for up in updates:
                    print(up['Path'])

            KBs = data.get('KBs')

            if 0 != len(KBs):
                print('Not founded')

                for kb in KBs:
                    print(kb)

    else:
        print('Using', sys.argv[0],
              '<Report file> <Version> <Type> <Language>')
