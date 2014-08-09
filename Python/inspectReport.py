import sys
import core.updates


def items2KBs(aItems):

    kbs = []
    for it in aItems:

        kbs.append(it['KB'])

    return kbs


def getListDiff(aParentList, aChildList):

    return list(set(aParentList) - set(aChildList))


def getData(aUpdates, aKBs, aQuery):

    ret = {}
    updates = core.updates.Updates()

    for kb in aKBs:
        aQuery['KB'] = kb
        updates.addUpdates(aUpdates.getUpdates(aQuery))

    if 0 != len(updates):
        KBs = getListDiff(aKBs, items2KBs(updates))

        ret['Updates'] = updates
        ret['KBs'] = KBs
    else:
        ret['KBs'] = aKBs

    return ret

if __name__ == '__main__':

    argc = len(sys.argv)
    if 4 < argc:
        uifData = core.updates.getUpdatesFromUIF_Storage(sys.argv[1])
        reportFile = sys.argv[2]
        version = sys.argv[3]
        platform = sys.argv[4]
        language = sys.argv[5]

        KBs = core.updates.getKBsFromReportFile(reportFile)

        print('At the input report', reportFile, 'located', KBs)
        print('Count', len(KBs))

        query = {}
        query['Version'] = version
        query['Type'] = platform
        query['Language'] = language

        data = getData(uifData, KBs, query)

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
            data = getData(uifData, KBs, query)

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
              '<Folder or file with update info (*.uif)> ' +
              '<Report file> <Version> <Type> <Language>')
