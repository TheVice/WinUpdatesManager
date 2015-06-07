import sys
import json
import datetime

class JsonHelper:

    def __init__(self, aFileName):

        inputFile = open(aFileName, 'r')
        fileContent = inputFile.read()
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
            raise TypeError('\'{1}\' at \'{0}\' is not an Dictionary'.format(aTestName, aVariableName))
        return data


    def GetArray(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, list):
            raise TypeError('\'{1}\' at \'{0}\' is not an Array'.format(aTestName, aVariableName))
        return data

    def GetSting(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if 2 == sys.version_info[0]:
            data = data.encode('utf-8')
        if not isinstance(data, str):
            raise TypeError('\'{1}\' at \'{0}\' is not a String'.format(aTestName, aVariableName))
        return data

    def GetStingArray(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, list):
            raise TypeError('\'{1}\' at \'{0}\' is not an Array'.format(aTestName, aVariableName))
        if len(data) < 1 or not isinstance(data[0], str):
            raise TypeError('\'{1}\' at \'{0}\' is not a String Array'.format(aTestName, aVariableName))
        return data

    def GetInteger(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, int):
            raise TypeError('\'{1}\' at \'{0}\' is not an Integer'.format(aTestName, aVariableName))
        return data

    def GetIntegerArray(self, aTestName, aVariableName):

        data = self.GetTestVariable(aTestName, aVariableName)
        if not isinstance(data, list):
            raise TypeError('\'{1}\' at \'{0}\' is not an Array'.format(aTestName, aVariableName))
        if len(data) < 1 or not isinstance(data[0], int):
            raise TypeError('\'{1}\' at \'{0}\' is not an Integer Array'.format(aTestName, aVariableName))
        return data
