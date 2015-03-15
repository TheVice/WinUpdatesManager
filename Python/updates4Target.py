import os
import sys
import inspectReport
import db.storage
import core.kb
from core.versions import Versions
from core.types import Types
from core.languages import Languages

if __name__ == '__main__':

    argc = len(sys.argv)
    if 4 < argc:
        updates = db.storage.getStorage(sys.argv[1])

        KBs = None
        if 5 < argc:
            KBs = core.kb.getKBsFromReportFile(sys.argv[5])

        version = Versions().getVersion(
                    '{0}{1}{0}'.format(os.sep, sys.argv[2].replace(' ', '')))
        platform = Types().getType(
                                    '{0}{1}{0}'.format(os.sep, sys.argv[3]))
        language = Languages().getLanguage(
                                    '{0}{1}{0}'.format(os.sep, sys.argv[4]))

        print('Target:\n'
              '\tVersion - {}\n'
              '\tPlatform - {}\n'
              '\tLanguage - {}\n'
              '\tKBs - {}\n'.format(version, platform, language, KBs))

        updates = inspectReport.getDataByVersionTypeLanguage(updates,
                                                             KBs,
                                                             version,
                                                             platform,
                                                             language)

        updates = updates['Updates']
        core.updates.Updates.sortByFieldUpToDown(updates, 'Path')

        for up in updates:
            print(up['Path'])

    else:
        print('Use next (for example): \n'
              '\t<Folder or file with update info (*.uif)|\n'
              '\tPath to SQLite base|\n'
              '\tPath to MongoDB server, for example http://127.0.0.1:8080>\n'
              '<Os name> '
              '<Type>x86|x64 '
              '<Language>English|Russian|Neutral '
              '<Report.txt> [Optional]')
