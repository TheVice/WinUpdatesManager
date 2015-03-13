import os
import core.kb
from core.versions import Versions
from core.types import Types
from core.languages import Languages


class Updates:

    def __init__(self):

        self.mData = []
        self.mIndex = 0

    def addUpdates(self, aUpdates):

        for up in aUpdates:
            self.addUpdate(up['Path'], up['KB'], up['Version'],
                       up['Type'], up['Language'], up['Date'])

    def addUpdate(self, aPath=None, aKB=None, aOsVersion=None,
                  aOsType=None, aLanguage=None, aDate=None):

        update = {}

        update['Path'] = aPath
        update['KB'] = aKB
        update['Version'] = aOsVersion
        update['Type'] = aOsType
        update['Language'] = aLanguage
        update['Date'] = aDate

        self.addUpdateDict(update)

    def addUpdateDict(self, aUpdate):

        if 0 == self.mData.count(aUpdate):
            self.mData.append(aUpdate)
            self.mIndex += 1

    def getUpdatesByCondition(self, aCondition, aQuery):

        updates = []

        for update in self:
            match = True
            for key in aQuery.keys():
                if (False == aCondition(update[key], aQuery.get(key))):
                    match = False
                    break
            if match:
                updates.append(update)

        return updates

    def getUpdates(self, aQuery):

        condition = lambda a, b: (a == b)
        return self.getUpdatesByCondition(condition, aQuery)

    def __iter__(self):

        return self

    def __next__(self):

        if self.mIndex == 0:
            self.mIndex = len(self.mData)
            raise StopIteration

        self.mIndex -= 1
        return self.mData[self.mIndex]

    def next(self):

        return self.__next__()

    def __len__(self):

        return len(self.mData)

    def __getitem__(self, aKey):

        if aKey < 0 or self.mIndex <= aKey:
            raise IndexError

        return self.mData[aKey]

    def __str__(self):

        updates = []
        for up in self:
            updates.append(str(up))
            updates.append(os.linesep)

        return ''.join(updates)


def getUpdatesFromPackage(aFiles, aDate):

    updates = Updates()
    versions = Versions()
    types = Types()
    languages = Languages()

    for updateFile in aFiles:

        updateFile = updateFile[updateFile.find(os.sep):]

        kb = core.kb.getKB(updateFile)
        osVersion = versions.getVersion(updateFile)
        osType = types.getType(updateFile)
        language = languages.getLanguage(updateFile)

        updates.addUpdate(updateFile, kb, osVersion, osType, language, aDate)

    return updates


def assignmentUp2Up(aUp1, aUp2):

    if len(aUp1.keys()) == len(aUp2.keys()):
        for key in aUp1.keys():
            aUp1[key] = aUp2[key]


def exchangeUps(aUp1, aUp2):

    if len(aUp1.keys()) == len(aUp2.keys()):
        tmp = {}
        for key in aUp1.keys():
            tmp[key] = aUp1[key]
        assignmentUp2Up(aUp1, aUp2)
        assignmentUp2Up(aUp2, tmp)


def sortByCondition(aCondition, aUpdates, aField):

    for a in range(0, len(aUpdates)):
        for b in range(0, len(aUpdates)):
            if aCondition(aUpdates[a][aField], aUpdates[b][aField]):
                exchangeUps(aUpdates[b], aUpdates[a])


def sortByFieldUpToDown(aUpdates, aField):

    condition = lambda a, b: (a < b)
    return sortByCondition(condition, aUpdates, aField)


def sortByFieldDownToUp(aUpdates, aField):

    condition = lambda a, b: (a > b)
    return sortByCondition(condition, aUpdates, aField)


def separateToKnownAndUnknown(aUpdates):

    updates = {'known': [], 'unKnown': []}

    for up in aUpdates:
        if (isinstance(up['KB'], dict) or isinstance(up['Version'], dict) or
            isinstance(up['Type'], dict) or isinstance(up['Language'], dict)):

            updates['unKnown'].append(up)
        else:
            updates['known'].append(up)

    return updates
