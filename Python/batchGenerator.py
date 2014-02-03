import sys
import os


def batchTemplate(aPath, aStrNumber, aSwitch):

    strList = []
    strList.append(':')
    strList.append('UP')
    strList.append(aStrNumber)

    strList.append(os.linesep)
    strList.append('IF NOT EXIST \"')
    strList.append(aPath)
    strList.append('\" GOTO ')
    strList.append('N')
    strList.append(aStrNumber)

    strList.append(os.linesep)
    strList.append(os.linesep)
    strList.append('echo Installing ')
    strList.append(aPath)
    strList.append(' UP')
    strList.append(aStrNumber)

    strList.append(os.linesep)
    strList.append('\"')
    strList.append(aPath)
    strList.append('\"')
    strList.append(aSwitch)
    strList.append(os.linesep)

    strList.append('GOTO ')
    strList.append('Y')
    strList.append(aStrNumber)
    strList.append(os.linesep)

    strList.append(os.linesep)
    strList.append(':')
    strList.append('N')
    strList.append(aStrNumber)

    strList.append(os.linesep)
    strList.append('echo File ')
    strList.append(aPath)
    strList.append(' not present.')

    strList.append(os.linesep)
    strList.append('echo Please change media and press any key...')

    strList.append(os.linesep)
    strList.append('PAUSE > nul:')
    strList.append(os.linesep)

    strList.append('GOTO ')
    strList.append('UP')
    strList.append(aStrNumber)

    strList.append(os.linesep)
    strList.append(':')
    strList.append('Y')
    strList.append(aStrNumber)

    strList.append(os.linesep)

    return ''.join(strList)


def generate(aLines, aRoot=None, aSwitch=' /quiet /norestart'):

    strList = []
    strList.append('@echo off')
    strList.append(os.linesep)
    strList.append('GOTO %1')
    strList.append(os.linesep)

    i = 1
    if aRoot is not None:
        for kbPath in aLines:
            kbPath = kbPath.replace('\n', '')
            kbPath = kbPath.replace('\r', '')
            kbPath = os.path.join(aRoot, kbPath)
            strList.append(batchTemplate(kbPath, str(i), aSwitch))
            i += 1
    else:
        for kbPath in aLines:
            kbPath = kbPath.replace('\n', '')
            kbPath = kbPath.replace('\r', '')
            strList.append(batchTemplate(kbPath, str(i), aSwitch))
            i += 1

    return ''.join(strList)

if __name__ == '__main__':

    argc = len(sys.argv)
    if 1 < argc:

        try:
            inputFile = open(sys.argv[1], 'r')
            lines = inputFile.read()
            inputFile.close()

            #see note on os.linesep in help
            if 2 < argc:
                print(generate(lines.split('\n'), sys.argv[2]))
            else:
                print(generate(lines.split('\n')))
        except:
            print('Error while read file', sys.argv[1])

    else:
        print('Using', sys.argv[0], '<path to report file>' +
                                    '[root path (if req)]')
