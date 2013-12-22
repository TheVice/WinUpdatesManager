import sys
import os


def batchTemplate(aPath, aStrNumber, aSwitch=' /quiet /norestart'):

# for notes see http://www.skymind.com/~ocrow/python_string/

# Template like this
#
# :UP
# IF NOT EXIST updateToPackage.cm GOTO N
# echo "Installing..."
# :...
# GOTO Y
# :N
# echo "File not present.
# echo Please change media and press any key..."
# PAUSE > nul:
# GOTO UP
# :Y

    str_list = []
    str_list.append(':')
    str_list.append('UP')
    str_list.append(aStrNumber)

    str_list.append(os.linesep)
    str_list.append('IF NOT EXIST \"')
    str_list.append(aPath)
    str_list.append('\" GOTO ')
    str_list.append('N')
    str_list.append(aStrNumber)

    str_list.append(os.linesep)
    str_list.append(os.linesep)
    str_list.append('echo Installing ')
    str_list.append(aPath)
    str_list.append(' UP')
    str_list.append(aStrNumber)

    str_list.append(os.linesep)
    str_list.append('\"')
    str_list.append(aPath)
    str_list.append('\"')
    str_list.append(aSwitch)
    str_list.append(os.linesep)

    str_list.append('GOTO ')
    str_list.append('Y')
    str_list.append(aStrNumber)
    str_list.append(os.linesep)

    str_list.append(os.linesep)
    str_list.append(':')
    str_list.append('N')
    str_list.append(aStrNumber)

    str_list.append(os.linesep)
    str_list.append('echo File ')
    str_list.append(aPath)
    str_list.append(' not present.')

    str_list.append(os.linesep)
    str_list.append('echo Please change media and press any key...')

    str_list.append(os.linesep)
    str_list.append('PAUSE > nul:')
    str_list.append(os.linesep)

    str_list.append('GOTO ')
    str_list.append('UP')
    str_list.append(aStrNumber)

    str_list.append(os.linesep)
    str_list.append(':')
    str_list.append('Y')
    str_list.append(aStrNumber)

    str_list.append(os.linesep)

    return ''.join(str_list)

if __name__ == '__main__':

    argc = len(sys.argv)
    if 1 < argc:

        try:
            inputFile = open(sys.argv[1], 'r')

            print('@echo off')
            print('GOTO %1')

            i = 1
            if 2 < argc:
                for kbPath in inputFile:
                    kbPath = os.path.join(sys.argv[2], kbPath)
                    print(batchTemplate(kbPath[:len(kbPath) - 1], str(i)))
                    i += 1
            else:
                for kbPath in inputFile:
                    print(batchTemplate(kbPath[:len(kbPath) - 1], str(i)))
                    i += 1

            inputFile.close()
        except:
            print('Error while read file', sys.argv[1])

    else:
        print('Using', sys.argv[0], '<path to report file>' +
                                    '[root path (if req)]')
