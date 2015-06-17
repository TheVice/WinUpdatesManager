import os
import sys
import json


class JsonHelper:

    def __init__(self, aFileName):

        inputFile = open(aFileName, 'r')
        fileContent = inputFile.read()
        if os.name != 'nt':
            fileContent = fileContent.replace('\\r', '')
        self.mData = json.loads(fileContent)
        inputFile.close()

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

    def GetDictionary(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, dict):
            raise TypeError('\'{}\' at \'{}\' is not an Dictionary'.format(aVariableName, aTestName))
        return data

    def GetArray(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, list):
            raise TypeError('\'{}\' at \'{}\' is not an Array'.format(aVariableName, aTestName))
        return data

    def GetSting(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if 2 == sys.version_info[0]:
            data = data.encode('utf-8')
        if not isinstance(data, str):
            raise TypeError('\'{}\' at \'{}\' is not a String'.format(aVariableName, aTestName))
        return data

    def GetInteger(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, int):
            raise TypeError('\'{}\' at \'{}\' is not an Integer'.format(aVariableName, aTestName))
        return data
