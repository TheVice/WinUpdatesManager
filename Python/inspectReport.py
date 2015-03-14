import sys
import core.kb
import core.updates
import db.uif


def items2KBs(aItems):

    kbs = []
    for it in aItems:

        kbs.append(it['KB'])

    return kbs


def getListDiff(aParentList, aChildList):

    return list(set(aParentList) - set(aChildList))


def makeDefineUnknownUpdates(aKBs):

    for i in range(0, len(aKBs)):
        if isinstance(aKBs[i], dict):
            aKBs[i] = -1


def getData(aUpdates, aKBs, aQuery):

    if (isinstance(aUpdates, list)):
        aUpdates = core.updates.Updates.convertUifListIntoUpdates(aUpdates)

    ret = {}
    updates = core.updates.Updates()

    if aQuery == {}:

        condition = lambda a, b: ((a in b) or (b in a))
        for kb in aKBs:
            aQuery['Path'] = str(kb)
            updates.addUpdates(
                aUpdates.getUpdatesByCondition(condition, aQuery))
    else:

        if (aKBs is None):
            updates.addUpdates(aUpdates.getUpdates(aQuery))
        else:
            for kb in aKBs:
                aQuery['KB'] = kb
                updates.addUpdates(aUpdates.getUpdates(aQuery))

    if (aKBs is None):
        ret['Updates'] = updates
        return ret

    if 0 != len(updates):

        items = items2KBs(updates)
        makeDefineUnknownUpdates(items)
        KBs = getListDiff(aKBs, items)

        ret['Updates'] = updates
        ret['KBs'] = KBs
    else:

        ret['KBs'] = aKBs

    return ret


def getDataByVersionTypeLanguage(aUpdates, aKBs,
                                 aVersion, aPlatform, aLanguage):

    query = {}
    query['Version'] = aVersion
    query['Type'] = aPlatform
    query['Language'] = aLanguage
    return getData(aUpdates, aKBs, query)


def getDataByKbPath(aUpdates, aKBs):

    query = {}
    return getData(aUpdates, aKBs, query)

if __name__ == '__main__':

    argc = len(sys.argv)
    if 4 < argc:
        uifData = db.uif.getUpdatesFromStorage(sys.argv[1])
        reportFile = sys.argv[2]
        version = sys.argv[3]
        platform = sys.argv[4]
        language = sys.argv[5]

        print('Converting from uif list into updates.\n'
              'Please standing by...')
        if (isinstance(uifData, list)):
            uifData = core.updates.Updates.convertUifListIntoUpdates(uifData)
        print('Uif converted')

        KBs = core.kb.getKBsFromReportFile(reportFile)

        print('At the input report', reportFile, 'located', KBs)
        print('Count', len(KBs))

        data = getDataByVersionTypeLanguage(uifData, KBs, version, platform,
                                            language)
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

            data = getDataByKbPath(uifData, KBs)
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
