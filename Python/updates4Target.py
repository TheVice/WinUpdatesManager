import os
import sys
import inspectReport
import core.updates

if __name__ == '__main__':

    argc = len(sys.argv)
    if 4 < argc:
        updates = core.updates.getUpdatesFromUIF_Storage(sys.argv[1])

        KBs = None
        if 5 < argc:
            KBs = core.updates.getKBsFromReportFile(sys.argv[5])

        version = core.updates.Versions().getVersion(
                    '{0}{1}{0}'.format(os.sep, sys.argv[2].replace(' ', '')))
        platform = core.updates.Types().getType(
                                    '{0}{1}{0}'.format(os.sep, sys.argv[3]))
        language = core.updates.Languages().getLanguage(
                                    '{0}{1}{0}'.format(os.sep, sys.argv[4]))

        updates = inspectReport.getDataByVersionTypeLanguage(updates,
                                                             KBs,
                                                             version,
                                                             platform,
                                                             language)

        updates = updates['Updates']
        core.updates.sortByFieldUpToDown(updates, 'Path')

        for up in updates:
            print(up['Path'])

    else:
        print('Use next (for example): \n'
              '<File with updates info>.uif '
              '<Os name> '
              '<Type>x86|x64 '
              '<Language>English|Russian|Neutral '
              '<Report.txt> [Optional]')
