import sys
import cherrypy
import core.kb
import db.storage
import batchGenerator


class Page:

    mTitle = 'Untitled Page'

    def header(self):

        return (
        '<!DOCTYPE html>'
        '<html>'
        '<head>'
        '<meta charset=\'utf-8\'><title>{}</title>'
        '</head>'
        '<body>'
        ).format(self.mTitle)

    def footer(self):

        return (
        '</body>'
        '</html>'
        )


class Main(Page):

    mTitle = 'Windows Updates Getter'

    def __init__(self, aStorage):

        self.mStorage = aStorage

    @cherrypy.expose
    def index(self):

        return ('{}{}{}'.format(self.header(),
                '<a href=\'/report_submit\'>Go to report submit</a>'
                '<br>'
                '<a href=\'/batch_generator\'>Go to batch generator</a>',
                self.footer()))

    @cherrypy.expose
    def report_submit(self):

        return ('{}{}{}'.format(self.header(),
        '<form action=\'process_report\' method=\'post\'>'
        '<p><label>Windows Version <input list=\'WinVersions\''
        ' name=aVersion required type=\'text\'></label>'
        '<datalist id=\'WinVersions\'>'
        '<option value=\'Windows Vista\'></option>'
        '<option value=\'Windows 7\'></option>'
        '<option value=\'Windows 8\'></option>'
        '<option value=\'Windows 8.1\'></option>'
        '<option value=\'Windows 10\'></option>'
        '</datalist>'
        '</p>'
        '<p><label>Platform <input list=\'platformList\''
        ' name=aPlatform required type=\'text\'></label>'
        '<datalist id=\'platformList\'>'
        '<option value=\'x86\'></option>'
        '<option value=\'x64\'></option>'
        '<option value=\'ARM\'></option>'
        '</datalist>'
        '</p>'
        '<p><label>Language'
        ' <input name=aLanguage value=\'Neutral\' type=\'text\'></label></p>'
        '<p><label>Windows Update Report<br><br>'
        '<textarea name=aReport cols=100 rows=25 required></textarea>'
        '</label></p>'
        '<p><input type=submit value=\'Make request\'></p>'
        '</form>',
        self.footer()))

    @cherrypy.expose
    def process_report(self, aReport, aVersion, aPlatform, aLanguage=None):

        KBs = core.kb.getKBsFromReport(aReport)
        if len(KBs) == 0:
            return '{}{}{}'.format(self.header(), '<H1>Nothing to show. KBs\' list is empty.</H1>', self.footer())

        if aLanguage is None:
            aLanguage = 'Neutral'

        str_list = []

        str_list.append('At the input report located')
        for kb in KBs:
            str_list.append('<br><I>{}</I>'.format(kb))

        str_list.append('<br><H1>Count - {}</H1>'.format(len(KBs)))

        updates = []

        if isinstance(self.mStorage, db.storage.MongoDB):
            query = {'KB': {'$in': KBs}, 'Version': aVersion, 'Type': aPlatform, 'Language': aLanguage}
            updates.extend(self.mStorage.get(query))
        elif isinstance(self.mStorage, db.storage.Uif) or isinstance(self.mStorage, db.storage.SQLite):
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
            str_list.append(Main.kbsToTable(notFoundedKBs))

        return '{}{}{}'.format(self.header(), ''.join(str_list), self.footer())

    @staticmethod
    def kbsToTable(aKBs):

        kbItems = []
        kbItems.append('<p><ul>')
        for kb in aKBs:
            kbItems.append('<li><a href=\'http://support.microsoft.com/KB/{0}\'>{0}</a></li>'.format(kb, kb))
        kbItems.append('</ul><p>')
        return ''.join(kbItems)

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
        cherrypy.quickstart( Main(db.storage.getStorage(sys.argv[1])), config=sys.argv[2])

    else:
        print('Using', sys.argv[0], '\n',
              '\t<Folder or file with update info (*.uif)|\n'
              '\tPath to SQLite base|\n'
              '\tPath to MongoDB server, '
              'for example mongodb://127.0.0.1:27017/>\n')
