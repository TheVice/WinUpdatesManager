import os
import sys
import core.kb
import cherrypy
import core.dates
import core.storage
import batchGenerator
from core.updates import Updates


class Page:

    mTitle = 'Untitled Page'

    def header(self):

        template = (
            '<!DOCTYPE html>'
            '<html><head>'
            '<meta charset=\'utf-8\'>'
            '<title>{}</title>'
            '</head><body>'
        )
        return template.format(self.mTitle)

    def footer(self):

        return '</body></html>'


class Main(Page):

    mTitle = 'Windows Updates Getter'

    def __init__(self, aStorage):

        self.mStorage = aStorage
        self.mVersions = self.mStorage.getAvalibleVersions()
        self.mTypes = self.mStorage.getAvalibleTypes()
        self.mLanguages = self.mStorage.getAvalibleLanguages()

    @cherrypy.expose
    def index(self):

        template = (
            '{}'
            '<a href=\'/view_updates\'>Go to view updates</a><br>'
            '<a href=\'/report_submit\'>Go to report submit</a><br>'
            '<a href=\'/batch_generator\'>Go to batch generator</a><br>'
            '{}'
        )
        return template.format(self.header(), self.footer())

    @cherrypy.expose
    def view_updates(self, aQuery={}, aLimit=-1, aSkip=0, aSort=None):

        updates = self.mStorage.get(aQuery, aLimit=15)

        str_list = []

        str_list.append('<table border="1"><tr>')
        for head in Updates.validKeys:
            str_list.append('<th>{}</th>'.format(head))
        str_list.append('</tr>')

        for up in updates:
            str_list.append('<tr>')
            up['Date'] = core.dates.toDate(up['Date'])
            for t in Updates.validKeys:
                str_list.append('<td>{}</td>'.format(up[t]))

            str_list.append('</tr>')
        str_list.append('</table>')

        template = (
            '{}'
            '{}'
            '{}'
        )

        return template.format(self.header(), ''.join(str_list), self.footer())

    @cherrypy.expose
    def report_submit(self):

        if (not self.mVersions or
            None == self.mVersions[0] or
            not self.mTypes or
            None == self.mTypes[0] or
            not self.mLanguages or
            None == self.mLanguages[0]):

            template = (
                '{}'
                'There are no valid data in the storage.'
                '{}'
            )

        else:
            versions = []
            types = []
            languages = []

            for version in self.mVersions:
                versions.append('<option value=\'{0}\'>{0}'.format(version))

            for platform in self.mTypes:
                types.append('<option value=\'{0}\'>{0}'.format(platform))

            for language in self.mLanguages:
                languages.append('<option value=\'{0}\'>{0}'.format(language))

            template = (
                '<form action=\'process_report\' method=\'post\'>'
                '<p><label>Windows Version '
                '<select name=aVersion>'
                '{}'
                '</select></p>'
                '<p><label>Platform '
                '<select name=aPlatform>'
                '{}'
                '</select></p>'
                '<p><label>Language '
                '<select name=aLanguage>'
                '{}'
                '</select></p>'
                '<p><label>Windows Update Report<br><br>'
                '<textarea name=aReport cols=100 rows=25 required></textarea>'
                '</label></p>'
                '<p><input type=submit value=\'Make request\'></p>'
                '</form>'
            )
            template = template.format(''.join(versions), ''.join(types), ''.join(languages))
            template = template.format('{0}{1}{0}'.format('{}', template))

        return template.format(self.header(), self.footer())

    @cherrypy.expose
    def process_report(self, aReport, aVersion, aPlatform, aLanguage):

        kbs = core.kb.getKBsFromReport(aReport)

        if not kbs:
            template = (
                '{}'
                '<H1>Nothing to show. KBs\' list is empty.</H1>'
                '{}'
            )
        else:
            template = (
                'At the input report located'
                '{}'
                '<br><H1>Count - {}</H1>'
            )

            kbsText = []
            for kb in kbs:
                kbsText.append('<br><I>{}</I>'.format(kb))

            template = template.format(''.join(kbsText), len(kbs))

            updates = []
            query = {'KB': kbs, 'Version': aVersion, 'Type': aPlatform, 'Language': aLanguage}
            updates.extend(self.mStorage.get(query))

            str_list = []

            if updates:
                str_list.append('<br>Count of updates queried from db - {}'.format(len(updates)))

                foundedKBs = []
                for up in updates:
                    str_list.append('<br><I>{}</I>'.format(up['Path']))
                    foundedKBs.append(up['KB'])

                notFoundedKBs = list(set(kbs) - set(foundedKBs))
                if notFoundedKBs:
                    str_list.append('<br>Not founded by strict query')

                    kbTemplate = (
                        '<li>{0} - <a href=\'http://support.microsoft.com/KB/{0}\'>support</a>,'
                        ' '
                        '<a href=\'http://www.microsoft.com/en-us/Search/result.aspx?q=KB{0}\'>search</a></li>'
                    )
                    kbs = []
                    for kb in notFoundedKBs:
                        kbs.append(kbTemplate.format(kb))
                        kbs.append(os.linesep)

                    subTemplate = (
                        '<p><ul>'
                        '{}'
                        '</ul><p>'
                    )

                    str_list.append(subTemplate.format(''.join(kbs)))
            else:
                str_list.append('<br>Unable to find any updates')

            template = '{0}{1}{2}{0}'.format('{}', template, ''.join(str_list))

        return template.format(self.header(), self.footer())

    @cherrypy.expose
    def batch_generator(self):

        template = (
            '{}'
            '<form action=\'process_generation\' method=\'post\'>'
            '<p><label>Root path (if req): <input list=\'Roots\''
            ' name=aRoot type=\'text\'></label>'
            '<datalist id=\'Roots\'>'
            '<option value=\'\\\\192.168.56.1\\0\'></option>'
            '<option value=\'Z:\\\'></option>'
            '</datalist>'
            '</p>'
            '<p><label>Switch: <input list=\'Switchs\''
            ' name=aSwitch type=\'text\'></label>'
            '<datalist id=\'Switchs\'>'
            '<option value=\'/quiet /norestart\'></option>'
            '<option value=\'-u -q -norestart\'></option>'
            '</datalist>'
            '</p>'
            '<p>'
            '<input type="checkbox" name="aCopyRequired">Copy updates into %TEMP% before installing<br>'
            '</p>'
            '<p><label><u>List of paths</u><br><br>'
            '<textarea name=aReport cols=100 rows=25 required></textarea>'
            '</label></p>'
            '<p><input type=submit value=\'Generate\'></p>'
            '</form>'
            '{}')

        return template.format(self.header(), self.footer())

    @cherrypy.expose
    def process_generation(self, aReport, aRoot, aSwitch, aCopyRequired=False):

        batchList = batchGenerator.generate(aReport.split('\n'), aRoot, aSwitch, aCopyRequired)

        template = (
            '{}'
            '<textarea cols=100 rows=25>'
            '{}'
            '</textarea><br>'
            '<a href=\'/view_updates\'>Go to view updates</a><br>'
            '<a href=\'/report_submit\'>Go to report submit</a><br>'
            '<a href=\'/batch_generator\'>Go to batch generator</a><br>'
            '{}')

        return template.format(self.header(), batchList, self.footer())


conf = {'/global': {'server.socket_host': '127.0.0.1',
                    'server.socket_port': 8080,
                    'server.thread_pool': 10}}


if __name__ == '__main__':

    argc = len(sys.argv)
    if argc == 2:
        cherrypy.quickstart(Main(core.storage.getStorage(sys.argv[1])),
                                                       config=conf)
    elif argc == 3:
        cherrypy.quickstart(Main(core.storage.getStorage(sys.argv[1])),
                                                       config=sys.argv[2])
    else:
        print('Using {0}'
              ' <Folder or file with update info (*.uif)>{1}'
              'Using {0}'
              ' <Path to SQLite base>{1}'
              'Using {0}'
              ' <Path to MongoDB server'
              ' for example mongodb://127.0.0.1:27017/>'.format(sys.argv[0],
                                                                os.linesep))
