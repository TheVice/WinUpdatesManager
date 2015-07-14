import os
import sys
import json


class JsonHelper:

    def __init__(self, aFileName):

        pathAndExtention = os.path.splitext(aFileName)
        if '.json' != pathAndExtention[1]:
            aFileName = '{}.json'.format(pathAndExtention[0])
        inputFile = open(aFileName, 'r')
        fileContent = inputFile.read()
        self.mData = json.loads(fileContent)
        inputFile.close()
        self.mData = JsonHelper.MakeDataPlatformIndependence(self.mData)

    def __str__(self):

        return str(self.mData)

    def GetTestRoot(self, aTestName):

        return self.mData[aTestName]

    def GetTestVariable(self, aTestName, aVariableName):

        return self.mData[aTestName][aVariableName]

    def GetTestInputOutputData(self, aTestName):

        testRoot = self.GetTestRoot(aTestName)
        tInput = []
        tOutput = []
        for tData in testRoot:
            tInput.append(list(tData.keys())[0])
            tOutput.append(tData[tInput[len(tInput) - 1]])
        return zip(tInput, tOutput)

    def GetArray(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, list):
            raise TypeError('\'{}\' at \'{}\' is not an Array'.format(aVariableName, aTestName))
        return data

    def GetSting(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, str):
            raise TypeError('\'{}\' at \'{}\' is not a String'.format(aVariableName, aTestName))
        return data

    def GetInteger(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, int):
            raise TypeError('\'{}\' at \'{}\' is not an Integer'.format(aVariableName, aTestName))
        return data

    @staticmethod
    def MakeDataPlatformIndependence(aData):

        if isinstance(aData, dict):
            for key in aData.keys():
                aData[key] = JsonHelper.MakeDataPlatformIndependence(aData[key])
            newDict = {}
            for key in aData.keys():
                newKey = JsonHelper.MakeDataPlatformIndependence(key)
                newDict[newKey] = aData[key]
            aData = newDict
        elif isinstance(aData, list):
            for i in range(0, len(aData)):
                aData[i] = JsonHelper.MakeDataPlatformIndependence(aData[i])
        elif isinstance(aData, str):
            aData = aData.replace('os.linesep', os.linesep)
            if os.name != 'nt':
                from string import ascii_letters
                for i in list(ascii_letters):
                    aData = aData.replace('{}:\\'.format(i), '{0}media_{1}{0}'.format(os.sep, i))
                aData = aData.replace('\\', os.sep)
        elif 2 == sys.version_info[0] and isinstance(aData, unicode):
            aData = aData.encode('utf-8')
            aData = JsonHelper.MakeDataPlatformIndependence(aData)

        return aData
