import os
import sys
import core.kb
import core.storage
from core.types import Types
from core.updates import Updates
from core.versions import Versions
from core.languages import Languages


def updates4Target(aStorage, aVersion, aPlatform, aLanguage, aPathToReport):

    KBs = core.kb.getKBsFromReportFile(aPathToReport) if None != aPathToReport else None
    version = Versions().getVersion('{0}{1}{0}'.format(os.sep, aVersion.replace(' ', '')))
    platform = Types().getType('{0}{1}{0}'.format(os.sep, aPlatform))
    language = Languages().getLanguage('{0}{1}{0}'.format(os.sep, aLanguage))

    query = {}
    if None != KBs and KBs != []:
        query['KB'] = KBs
    if not isinstance(version, dict):
        query['Version'] = version
    if not isinstance(platform, dict):
        query['Type'] = platform
    if not isinstance(language, dict):
        query['Language'] = language

    updates = aStorage.get(query)
    Updates.sortByFieldUpToDown(updates, 'Path')

    return (updates, version, platform, language, KBs)


if __name__ == '__main__':

    argc = len(sys.argv)
    if 5 == argc or 6 == argc:
        storagePath = sys.argv[1]
        storage = core.storage.getStorage(storagePath)
        itemsCount = len(storage.get({}))

        if 0 < itemsCount:
            print('At \'{}\' found {} update objects'.format(storagePath, itemsCount))

            version = sys.argv[2]
            platform = sys.argv[3]
            language = sys.argv[4]
            pathToReport = sys.argv[5] if 6 == argc else None

            updates, version, platform, language, KBs = updates4Target(storage, version, platform, language, pathToReport)

            if 0 < len(updates):
                for up in updates:
                    print(up['Path'])
            else:
                print('There is no updates for given target{0}'
                      'Version - {1}{0}'
                      'Platform - {2}{0}'
                      'Language - {3}{0}'
                      'Path to report - {4}{0}'
                      'KBs - {5}'.format(os.linesep, version, platform, language, pathToReport, KBs))

        else:
            print('Not found update objects at {}'.format(storagePath))

    else:
        print('Using', sys.argv[0],
              '<Folder or file with update info (*.uif)|'
              'Path to SQLite base|'
              'Path to MongoDB server, for example http://127.0.0.1:8080>',
              '<Os name>',
              '<Type>',
              '<Language>',
              '<Path to report file>[Optional]')
