import os
import json


class Updates:

    validKeys = ['KB', 'Path', 'Version', 'Type', 'Language', 'Date']

    def __init__(self):

        self.mData = []
        self.mIndex = 0

    def addUpdates(self, aUpdates):

        for up in aUpdates:

            path = None
            KB = None
            osVersion = None
            osType = None
            language = None
            date = None

            for key in up.keys():

                if key == 'Path':
                    path = up['Path']
                elif key == 'KB':
                    KB = up['KB']
                elif key == 'Version':
                    osVersion = up['Version']
                elif key == 'Type':
                    osType = up['Type']
                elif key == 'Language':
                    language = up['Language']
                elif key == 'Date':
                    date = up['Date']

            self.addUpdate(path, KB, osVersion, osType, language, date)

    def addUpdate(self, aPath, aKB, aOsVersion, aOsType, aLanguage, aDate):

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
            updates.append(json.dumps(up))
            updates.append(os.linesep)

        return ''.join(updates)

    @staticmethod
    def assignmentUp2Up(aUp1, aUp2):

        if len(aUp1.keys()) == len(aUp2.keys()):
            for key in aUp1.keys():
                aUp1[key] = aUp2[key]

    @staticmethod
    def exchangeUps(aUp1, aUp2):

        if len(aUp1.keys()) == len(aUp2.keys()):
            tmp = {}
            for key in aUp1.keys():
                tmp[key] = aUp1[key]
            Updates.assignmentUp2Up(aUp1, aUp2)
            Updates.assignmentUp2Up(aUp2, tmp)

    @staticmethod
    def sortByCondition(aCondition, aUpdates, aField):

        for a in range(0, len(aUpdates)):
            for b in range(0, len(aUpdates)):
                if aCondition(aUpdates[a][aField], aUpdates[b][aField]):
                    Updates.exchangeUps(aUpdates[b], aUpdates[a])

    @staticmethod
    def sortByFieldUpToDown(aUpdates, aField):

        condition = lambda a, b: (a < b)
        return Updates.sortByCondition(condition, aUpdates, aField)

    @staticmethod
    def sortByFieldDownToUp(aUpdates, aField):

        condition = lambda a, b: (a > b)
        return Updates.sortByCondition(condition, aUpdates, aField)

    @staticmethod
    def separateToKnownAndUnknown(aUpdates):

        updates = {'known': [], 'unKnown': []}

        for up in aUpdates:
            if 'UNKNOWN' in '{}'.format(up):
                updates['unKnown'].append(up)
            else:
                updates['known'].append(up)

        return updates
