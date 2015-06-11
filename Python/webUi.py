import re
import sys
import core.kb
import datetime
import cherrypy
import db.storage
import batchGenerator


class Page:

    mTitle = 'Untitled Page'

    def header(self):

        str_list = []
        str_list.append('<!DOCTYPE html>')
        str_list.append('<html><head>')
        str_list.append('<meta charset=\'utf-8\'>')
        str_list.append('<title>{}</title>'.format(self.mTitle))
        str_list.append('</head><body>')
        return ''.join(str_list)

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

        str_list = []
        if isinstance(self.mStorage, db.storage.MongoDB):
            str_list.append('<a href=\'/view_updates\'>Go to view updates</a><br>')
        str_list.append('<a href=\'/report_submit\'>Go to report submit</a><br>')
        str_list.append('<a href=\'/batch_generator\'>Go to batch generator</a><br>')
        return '{}{}{}'.format(self.header(), ''.join(str_list), self.footer())

    @cherrypy.expose
    def view_updates(self, aSkip=None, aLimit=None, aSort=None, aQuery=None):

        str_list = []
        if isinstance(self.mStorage, db.storage.MongoDB):

            aQuery = Main.normalizeQuery(aQuery, {})
            aLimit = Main.normalizeLimit(aLimit, 15)
            count = self.mStorage.get(aQuery).count()

            if count > aLimit:
                count = count - aLimit

            if 0 < count:
                aSkip = Main.normalizeSkip(aSkip, count)
                aSort = Main.normalizeSort(aSort, 'Date,-1')
                updates = self.mStorage.getWithSkipLimitAndSort(aQuery, aSkip, aLimit, aSort)
                str_list.extend(Main.updates2HtmlTable(updates))
                aSort = ''.join(Main.encodeSort(aSort))
                aQuery = Main.encodeQuery(aQuery)

                if [] == aQuery:
                    aQuery = None
                else:
                    aQuery = ''.join(aQuery)

                if 0 < aSkip:
                    str_list.append('<a href=\'/view_updates?')
                    str_list.append('aSkip={}'.format(aSkip - aLimit))
                    str_list.append('&amp;aLimit={}'.format(aLimit))
                    str_list.append('&amp;aSort={}'.format(aSort))
                    if None != aQuery:
                        str_list.append('&amp;aQuery={}'.format(aQuery))
                    str_list.append('\'>{}</a><br>'.format('Back'))

                if aSkip + aLimit < count:
                    str_list.append('<a href=\'/view_updates?')
                    str_list.append('aSkip={}'.format(aSkip + aLimit))
                    str_list.append('&amp;aLimit={}'.format(aLimit))
                    str_list.append('&amp;aSort={}'.format(aSort))
                    if None != aQuery:
                        str_list.append('&amp;aQuery={}'.format(aQuery))
                    str_list.append('\'>{}</a><br>'.format('Forward'))

        return '{}{}{}'.format(self.header(), ''.join(str_list), self.footer())

    @cherrypy.expose
    def report_submit(self):

        str_list = []
        if 0 < len(self.mVersions) and 0 < len(self.mTypes) and 0 < len(self.mLanguages):
            str_list.append('<form action=\'process_report\' method=\'post\'>')

            str_list.append('<p><label>Windows Version ')
            str_list.append('<select name=aVersion>')
            for version in self.mVersions:
                str_list.append('<option value=\'{0}\'>{0}'.format(version))
            str_list.append('</select></p>')

            str_list.append('<p><label>Platform ')
            str_list.append('<select name=aPlatform>')
            for platform in self.mTypes:
                str_list.append('<option value=\'{0}\'>{0}'.format(platform))
            str_list.append('</select></p>')

            str_list.append('<p><label>Language ')
            str_list.append('<select name=aLanguage>')
            for language in self.mLanguages:
                str_list.append('<option value=\'{0}\'>{0}'.format(language))
            str_list.append('</select></p>')

            str_list.append('<p><label>Windows Update Report<br><br>')
            str_list.append('<textarea name=aReport cols=100 rows=25 required></textarea>')
            str_list.append('</label></p>')
            str_list.append('<p><input type=submit value=\'Make request\'></p>')

            str_list.append('</form>')

        return '{}{}{}'.format(self.header(), ''.join(str_list), self.footer())

    @cherrypy.expose
    def process_report(self, aReport, aVersion, aPlatform, aLanguage):

        KBs = core.kb.getKBsFromReport(aReport)
        if len(KBs) == 0:
            return '{}{}{}'.format(self.header(), '<H1>Nothing to show. KBs\' list is empty.</H1>', self.footer())

        str_list = []

        str_list.append('At the input report located')
        for kb in KBs:
            str_list.append('<br><I>{}</I>'.format(kb))

        str_list.append('<br><H1>Count - {}</H1>'.format(len(KBs)))

        updates = []
        if isinstance(self.mStorage, db.storage.MongoDB):
            query = {'KB': {'$in': KBs}, 'Version': aVersion, 'Type': aPlatform, 'Language': aLanguage}
            updates.extend(self.mStorage.get(query))
        elif isinstance(self.mStorage, db.storage.Uif):
            query = {'KB': KBs, 'Version': aVersion, 'Type': aPlatform, 'Language': aLanguage}
            updates.extend(self.mStorage.get(query))
        elif isinstance(self.mStorage, db.storage.SQLite):
            for kb in KBs:
                query = {'KB': kb, 'Version': aVersion, 'Type': aPlatform, 'Language': aLanguage}
                updates.extend(self.mStorage.get(query))

        if 0 < len(updates):
            str_list.append('<br>Count of updates queried from db - {}'.format(len(updates)))

            for up in updates:
                str_list.append('<br><I>{}</I>'.format(up['Path']))
        else:
            str_list.append('<br>Unable to find any updates')

        foundedKBs = []
        for item in updates:
            foundedKBs.append(item['KB'])

        notFoundedKBs = list(set(KBs) - set(foundedKBs))
        if 0 < len(notFoundedKBs):
            str_list.append('<br>Not founded by strict query')
            str_list.extend(Main.kbsToTable(notFoundedKBs))

        return '{}{}{}'.format(self.header(), ''.join(str_list), self.footer())

    @staticmethod
    def kbsToTable(aKBs):

        str_list = []
        str_list.append('<p><ul>')
        for kb in aKBs:
            str_list.append('<li><a href=\'http://support.microsoft.com/KB/{0}\'>{0}</a></li>'.format(kb))
        str_list.append('</ul><p>')
        return str_list

    @staticmethod
    def normalizeSkip(aSkip, aMaxCount):

        try:
            aSkip = int(aSkip)
        except:
            aSkip = 0
        if aSkip > aMaxCount:
            aSkip = aMaxCount
        if aSkip < 0:
            aSkip = 0
        return aSkip

    @staticmethod
    def normalizeLimit(aLimit, aDefaultLimit):

        try:
            aLimit = int(aLimit)
        except:
            aLimit = aDefaultLimit
        return aLimit

    @staticmethod
    def normalizeSort(aSort, aDefaultSort):

        try:
            aSort = Main.decodeSort(aSort)
        except:
            aSort = Main.decodeSort(aDefaultSort)
        if aSort == []:
            aSort = Main.decodeSort(aDefaultSort)
        return aSort

    @staticmethod
    def updates2HtmlTable(aUpdates):

        str_list = []
        str_list.append('<table border="1"><tr>')
        tableHead = ['KB', 'Path', 'Version', 'Type', 'Language', 'Date']
        for t in tableHead:
            str_list.append('<th>{}</th>'.format(t))
        str_list.append('</tr>')

        for up in aUpdates:
            str_list.append('<tr>')
            up['Date'] = up['Date'].date()
            for t in tableHead:
                query = Main.encodeQuery({t: up[t]})
                if [] == query:
                    str_list.append('<td>{}</td>'.format(up[t]))
                else:
                    str_list.append('<td><a href=\'/view_updates?aQuery={}\'>{}</a></td>'.format(''.join(query), up[t]))

            str_list.append('</tr>')
        str_list.append('</table>')

        return str_list

    @staticmethod
    def decodeSort(aSort):

        sort = []

        digitPattern = '-?\d+'
        kbPattern = 'KB,{}'.format(digitPattern)
        pathPattern = 'Path,{}'.format(digitPattern)
        versionPattern = 'Version,{}'.format(digitPattern)
        typePattern = 'Type,{}'.format(digitPattern)
        languagePattern = 'Language,{}'.format(digitPattern)
        datePattern = 'Date,{}'.format(digitPattern)

        patterns = [kbPattern, pathPattern, versionPattern, typePattern, languagePattern, datePattern]

        for p in patterns:
            m = re.search(p, aSort)
            if m:
                i = m.group(0)
                separator = p.find(',')
                sort.append((i[:separator], int(i[1 + separator:])))

        return sort

    @staticmethod
    def encodeSort(aSort):

        str_list = []
        for a in aSort:
            for b in a:
                str_list.append('{},'.format(b))

        if 0 < len(str_list):
            last = str_list[len(str_list) - 1]
            last = last[:last.find(',')]
            str_list[len(str_list) - 1] = last

        return str_list

    @staticmethod
    def normalizeQuery(aQuery, aDefaultQuery):

        try:
            aQuery = Main.decodeQuery(aQuery)
        except:
            aQuery = aDefaultQuery
        if aQuery == []:
            aQuery = aDefaultQuery
        return aQuery

    @staticmethod
    def decodeQuery(aQuery):

        query = {}

        kbPattern = 'KB,'
        pathPattern = 'Path,'
        versionPattern = 'Version,'
        typePattern = 'Type,'
        languagePattern = 'Language,'
        datePattern = 'Date,'

        patterns = [kbPattern, pathPattern, versionPattern, typePattern, languagePattern, datePattern]

        for p in patterns:
            m = aQuery.find(p)
            if -1 != m:
                pattern = (m, m + len(p))
                endValue = aQuery[pattern[1]:].find(',')
                if -1 != endValue:
                    endValue = pattern[1] + endValue
                else:
                    endValue = len(aQuery)
                value = (pattern[1], endValue)
                pattern = (pattern[0], pattern[1] - 1)

                pattern = aQuery[pattern[0]:pattern[1]]
                value = aQuery[value[0]:value[1]]
                if 'KB' == pattern:
                    try:
                        query[pattern] = int(value)
                    except:
                        pass
                elif 'Date' == pattern:
                    try:
                        query[pattern] = datetime.datetime.strptime(value, '%Y-%m-%d')
                    except:
                        pass
                else:
                    query[pattern] = value

        return query

    @staticmethod
    def encodeQuery(aQuery):

        str_list = []
        for key in aQuery.keys():
            if 'Date' == key and isinstance(aQuery[key], datetime.datetime):
                try:
                    value = '{}'.format(aQuery[key].date())
                    str_list.append('{},{},'.format(key, value))
                except:
                    pass
            else:
                value = '{}'.format(aQuery[key])
                if -1 == value.find('{'):
                    str_list.append('{},{},'.format(key, value))

        if 0 < len(str_list):
            last = str_list[len(str_list) - 1]
            last = last[:last.rfind(',')]
            str_list[len(str_list) - 1] = last

        return str_list

    @cherrypy.expose
    def batch_generator(self):

        return '{}{}{}'.format(self.header(),
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
        '<option value=\' /quiet /norestart\'></option>'
        '<option value=\' -u -q -norestart\'></option>'
        '</datalist>'
        '</p>'
        '<p><label><u>List of paths</u><br><br>'
        '<textarea name=aReport cols=100 rows=25 required></textarea>'
        '</label></p>'
        '<p><input type=submit value=\'Generate\'></p>'
        '</form>',
        self.footer())

    @cherrypy.expose
    def process_generation(self, aReport, aSwitch, aRoot=None):

        return '{}{}{}{}{}'.format(self.header(),
               '<textarea cols=100 rows=25>',
               batchGenerator.generate(aReport.split('\n'), aRoot, aSwitch),
               '</textarea>'
               '<br>'
               '<a href=\'/report_submit\'>Go to report submit</a>'
               '<br>'
               '<a href=\'/batch_generator\'>Go to batch generator</a>',
               self.footer())

conf = {'/global': {'server.socket_host': '127.0.0.1',
                    'server.socket_port': 8080,
                    'server.thread_pool': 10}}

if __name__ == '__main__':

    argc = len(sys.argv)
    if argc == 2:
        cherrypy.quickstart(Main(db.storage.getStorage(sys.argv[1])), config=conf)

    elif argc == 3:
        cherrypy.quickstart(Main(db.storage.getStorage(sys.argv[1])), config=sys.argv[2])

    else:
        print('Using', sys.argv[0], '\n',
              '\t<Folder or file with update info (*.uif)|\n'
              '\tPath to SQLite base|\n'
              '\tPath to MongoDB server, '
              'for example mongodb://127.0.0.1:27017/>\n')
