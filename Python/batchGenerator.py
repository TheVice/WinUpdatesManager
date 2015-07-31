import os
import sys


headTemplate = (
    '@echo off{3}'
    'if [%1] == [] GOTO UP1{3}'
    'GOTO %1{3}'
)


templateWithOutCopy = (
    '{3}'
    ':UP{0}{3}'
    'IF NOT EXIST \"{1}\" GOTO N{0}'
    '{3}'
    'echo Installing {1} UP{0}{3}'
    '\"{1}\" {2}{3}'
    'GOTO Y{0}{3}'
    '{3}'
    ':N{0}{3}'
    'echo File {1} not present.{3}'
    'echo Please change media and press any key...{3}'
    'PAUSE > nul:{3}'
    'GOTO UP{0}{3}'
    ':Y{0}{3}'
    '{3}'
)


templateWithCopy = templateWithOutCopy.replace(
    '\"{1}\" {2}{3}',
    'copy \"{1}\" "%TEMP%{5}{4}" /Y{3}'
    '\"%TEMP%{5}{4}\" {2}{3}'
)


def batchTemplate(aPath, aStrNumber, aSwitch, aCopyRequired):

    if aCopyRequired:
        strList = templateWithCopy
    else:
        strList = templateWithOutCopy
    strList = strList.replace('{0}', '{}'.format(aStrNumber))
    strList = strList.replace('{1}', aPath)
    strList = strList.replace('{2}', aSwitch)
    strList = strList.replace('{3}', os.linesep)
    if aCopyRequired:
        strList = strList.replace('{4}', os.path.split(aPath)[1])
        strList = strList.replace('{5}', os.sep)
    return strList


def generate(aLines,
             aRoot=None,
             aSwitch='/quiet /norestart',
             aCopyRequired=True):

    strList = headTemplate
    strList = strList.replace('{3}', os.linesep)

    for line, i in zip(aLines, range(1, len(aLines) + 1)):

        line = line.replace('\r', '')
        if aRoot:
            line = os.path.join(aRoot, line)

        line = batchTemplate(line, i, aSwitch, aCopyRequired)
        strList = '{}{}'.format(strList, line)

    return strList


if __name__ == '__main__':

    argc = len(sys.argv)
    if 1 < argc:
        try:
            inputFile = open(sys.argv[1], 'r')
            lines = inputFile.read()
            inputFile.close()
            if 2 < argc:
                print(generate(lines.split('\n'), sys.argv[2]))
            else:
                print(generate(lines.split('\n')))
        except:
            print('Unexpected error while work with file {} {}'.format(
                                            sys.argv[1], sys.exc_info()[1]))
    else:
        print('Using', sys.argv[0],
              '<path to report file> <root path>[optional]')
