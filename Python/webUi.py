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
    def view_updates(self, aQuery='', aLimit=15, aSkip=0, aSort=''):

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
            aQuery = Main.decodeQuery(aQuery)
            aSort = Main.decodeSort(aSort)

            try:
                aLimit = int(aLimit)
            except:
                aLimit = 15

            try:
                aSkip = int(aSkip)
            except:
                aSkip = 0

            count = self.mStorage.getCount(aQuery)
            updates = self.mStorage.get(aQuery, aLimit, aSkip, aSort)

            if 'Date' in aQuery.keys():
                aQuery['Date'] = core.dates.toString(aQuery['Date'])

            aQuery = Main.encodeQuery(aQuery)

            template_list = [
                '<a href=\'/view_updates?',
                'aQuery={}',
                '&amp;',
                'aSkip={}',
                '&amp;',
                'aLimit={}',
                '&amp;',
                'aSort={}',
                '\'>{}</a>',
                '<br>'
            ]

            str_list = []

            str_list.append('<table border="1"><tr>')
            for head in Updates.validKeys:
                if head in aSort.keys():
                    sort = {head: -1 * aSort[head]}
                else:
                    sort = {head: -1}
                sort = Main.encodeSort(sort)

                subTemplate = []
                subTemplate.extend(template_list)

                subTemplate = Main.normalize(subTemplate, 'aQuery={}', aQuery)
                subTemplate = Main.normalize(subTemplate, 'aSkip={}', 0)
                subTemplate = Main.normalize(subTemplate, 'aLimit={}', aLimit)
                subTemplate = Main.normalize(subTemplate, 'aSort={}', sort)
                subTemplate = Main.normalize(subTemplate, '\'>{}</a>', head)
                subTemplate = ''.join(subTemplate)

                str_list.append('<th>{}</th>'.format(subTemplate))
            str_list.append('</tr>')

            aSort = Main.encodeSort(aSort)

            for up in updates:
                str_list.append('<tr>')
                up['Date'] = core.dates.toDate(up['Date'])
                for key in Updates.validKeys:
                    if isinstance(up[key], dict):
                        keys = list(up[key].keys())
                        if keys:
                            str_list.append('<td>{}</td>'.format(keys[0]))
                        continue

                    if key == 'Date':
                        query = {key: core.dates.toString(up[key])}
                    else:
                        query = {key: up[key]}
                    query = Main.encodeQuery(query)

                    subTemplate = []
                    subTemplate.extend(template_list)

                    subTemplate = Main.normalize(subTemplate, 'aQuery={}', query)
                    subTemplate = Main.normalize(subTemplate, 'aSkip={}', 0)
                    subTemplate = Main.normalize(subTemplate, 'aLimit={}', aLimit)
                    subTemplate = Main.normalize(subTemplate, 'aSort={}', aSort)
                    subTemplate = Main.normalize(subTemplate, '\'>{}</a>', up[key])
                    subTemplate = ''.join(subTemplate)

                    str_list.append('<td>{}</td>'.format(subTemplate))
                str_list.append('</tr>')
            str_list.append('</table>')

            if 0 < aSkip:
                subTemplate = []
                subTemplate.extend(template_list)

                subTemplate = Main.normalize(subTemplate, 'aQuery={}', aQuery)
                subTemplate = Main.normalize(subTemplate, 'aSkip={}', aSkip - aLimit)
                subTemplate = Main.normalize(subTemplate, 'aLimit={}', aLimit)
                subTemplate = Main.normalize(subTemplate, 'aSort={}', aSort)
                subTemplate = Main.normalize(subTemplate, '\'>{}</a>', 'Back')
                subTemplate = ''.join(subTemplate)

                str_list.append(subTemplate)

            if aSkip + aLimit < count:
                subTemplate = []
                subTemplate.extend(template_list)

                subTemplate = Main.normalize(subTemplate, 'aQuery={}', aQuery)
                subTemplate = Main.normalize(subTemplate, 'aSkip={}', aSkip + aLimit)
                subTemplate = Main.normalize(subTemplate, 'aLimit={}', aLimit)
                subTemplate = Main.normalize(subTemplate, 'aSort={}', aSort)
                subTemplate = Main.normalize(subTemplate, '\'>{}</a>', 'Forward')
                subTemplate = ''.join(subTemplate)

                str_list.append(subTemplate)

            template = '{0}{1}{0}'.format('{}', ''.join(str_list))

        return template.format(self.header(), self.footer())

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

    @staticmethod
    def decodeQuery(aQuery):

        query = {}

        for key in Updates.validKeys:
            if key in aQuery:
                startValue = 1 + aQuery.find(key) + len(key)
                value = aQuery[startValue:]

                if ',' in value:
                    value = value[:value.find(',')]

                if 'Date' == key:
                    if '%20' in value:
                        value = value.replace('%20', ', ')
                    elif ' ' in value:
                        value = value.replace(' ', ', ')
                else:
                    value = value.replace('%20', ' ')
                if 'KB' == key:
                    try:
                        value = int(value)
                    except:
                        continue

                query[key] = value

        return query

    @staticmethod
    def encodeQuery(aQuery):

        str_list = []
        for key in Updates.validKeys:
            if key in aQuery.keys():
                value = '{}'.format(aQuery[key])
                if 'Date' == key:
                    value = core.dates.toString(value)
                    value = value.replace(', ', '%20')
                else:
                    value = value.replace(' ', '%20')
                str_list.append('{},{}'.format(key, value))
                str_list.append(',')

        if str_list:
            del str_list[len(str_list)-1]
            return ''.join(str_list)
        else:
            return ''

    @staticmethod
    def decodeSort(aSort):

        sort = {}
        for key in Updates.validKeys:
            if key in aSort:
                startValue = 1 + aSort.find(key) + len(key)
                value = aSort[startValue:]

                try:
                    value = int(value)
                except:
                    value = 1

                sort[key] = value
                break

        return sort

    @staticmethod
    def encodeSort(aSort):

        str_list = []
        for key in Updates.validKeys:
            if key in aSort.keys():
                value = '{}'.format(aSort[key])
                str_list.append('{},{}'.format(key, value))
                break

        if str_list:
            return ''.join(str_list)
        else:
            return ''

    @staticmethod
    def normalize(aTemplate, aParameterName, aParameter):

        if aParameterName in aTemplate:

            i = aTemplate.index(aParameterName)
            if aParameter == '':
                if i + 1 < len(aTemplate):
                    if '&amp;' == aTemplate[i + 1]:
                        del aTemplate[i + 1]
                del aTemplate[i]
            else:
                aTemplate[i] = aParameterName.format(aParameter)

        return aTemplate


if __name__ == '__main__':

    argc = len(sys.argv)
    if argc == 2:
        conf = {'/global': {'server.socket_host': '127.0.0.1',
                    'server.socket_port': 8080,
                    'server.thread_pool': 10}}
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
