import sys
import cherrypy
import core.updates
import inspectReport
import batchGenerator
import db.mongoDB


class Page:

    mTitle = 'Untitled Page'

    def header(self):

        return (
        '<!DOCTYPE html>'
        '<html>'
        '<head>'
        '<meta charset=\'utf-8\'><title>%s</title>'
        '</head>'
        '<body>'
        ) % self.mTitle

    def footer(self):

        return (
        '</body>'
        '</html>'
        )


class Main(Page):

    mTitle = 'Windows Updates Getter'

    def __init__(self, aDB):

        self.db = aDB

    @cherrypy.expose
    def index(self):

        return (
        self.header() +
        '<a href=\'/update_viewer\'>Go to update viewer</a>' +
        '<br>' +
        '<a href=\'/batch_generator\'>Go to batch generator</a>' +
        self.footer())

    @cherrypy.expose
    def update_viewer(self):

        return (
        self.header() +
        '<form action=\'process_report\' method=\'post\'>'
        '<p><label>Windows Version <input list=\'WinVersions\''
        ' name=aVersion required type=\'text\'></label>'
        '<datalist id=\'WinVersions\'>'
        '<option value=\'Vista\'></option>'
        '<option value=\'Windows 7\'></option>'
        '<option value=\'Eight\'></option>'
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
        '</form>' +
        self.footer())

    @cherrypy.expose
    def process_report(self, aVersion=None, aPlatform=None, aLanguage=None,
                       aReport=None):

        KBs = core.updates.getKBsFromReport(aReport)
        if len(KBs) == 0:

            return (
            self.header() +
            '<H1>Nothing to show. KBs\' list is empty.</H1>' +
            self.footer())

        str_list = []

        str_list.append('At the input report located')
        for kb in KBs:
            str_list.append('<br><I>')
            str_list.append(str(kb))
            str_list.append('</I>')

        str_list.append('<br><H1>Count - ')
        str_list.append(str(len(KBs)))
        str_list.append('</H1>')

        query = {}
        query['$or'] = inspectReport.kbsToQueryPathList(KBs)
        # inspectReport.kbsToQueryList(KBs)
        query['Version'] = aVersion
        query['Type'] = aPlatform
        query['Language'] = aLanguage

        sort = [('Date', 1), ('KB', 1)]

        data = inspectReport.getData(KBs, query, sort)

        updates = data.get('Updates')

        if updates is not None:
            str_list.append('<br>Count of updates queried from db - ')
            str_list.append(str(len(updates)))

            for up in updates:
                str_list.append('<br><I>')
                str_list.append(up['Path'])
                str_list.append('</I>')
        else:
            str_list.append('<br>Unable to find any updates')

        KBs = data.get('KBs')

        if 0 != len(KBs):
            str_list.append('<br>Not founded by strict query')

            for kb in KBs:
                str_list.append('<br><I>')
                str_list.append(str(kb))
                str_list.append('</I>')

            query = {}
            query['$or'] = inspectReport.kbsToQueryList(KBs)

            data = inspectReport.getData(KBs, query)

            updates = data.get('Updates')

            if updates is not None:
                str_list.append('<br>Founded by number only')

                for up in updates:
                    str_list.append('<br><I>')
                    str_list.append(up['Path'])
                    str_list.append('</I>')

            KBs = data.get('KBs')

            if 0 != len(KBs):
                str_list.append('<br>Not founded')

                KBs = self.kbsToTable(KBs)

                for kb in KBs:
                    str_list.append(str(kb))

        return (
                self.header() +
                ''.join(str_list) +
                self.footer())

    def kbsToTable(self, aKBs):

        kbItems = '<p><ul>'
        for kb in aKBs:
            kbItems = (kbItems +
            '<li><a href=\'http://support.microsoft.com/KB/%s\'>%s</a></li>' %
            (kb, kb))
        kbItems = kbItems + '</ul><p>'
        return kbItems

    @cherrypy.expose
    def batch_generator(self):

        return (
        self.header() +
        '<form action=\'process_generation\' method=\'post\'>'
        '<p><label>Root path (if req): <input list=\'Roots\''
        ' name=aRoot type=\'text\'></label>'
        '<datalist id=\'Roots\'>'
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
        '</form>' +
        self.footer())

    @cherrypy.expose
    def process_generation(self, aReport, aSwitch, aRoot=None):

        return (
        self.header() +
        '<textarea cols=100 rows=25>' +
        batchGenerator.generate(aReport.split('\n'), aRoot, aSwitch) +
        '</textarea>' +
        '<br>' +
        '<a href=\'/update_viewer\'>Go to update viewer</a>' +
        '<br>' +
        '<a href=\'/batch_generator\'>Go to batch generator</a>' +
        self.footer())

conf = {'/global': {'server.socket_host': '127.0.0.1',
                    'server.socket_port': 8080,
                    'server.thread_pool': 10}}

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 1:

        cherrypy.quickstart(Main(db.mongoDB.MongoDBClient()), config=conf)

    elif argc == 2:
        cherrypy.quickstart(Main(db.mongoDB.MongoDBClient()),
                            config=sys.argv[1])
#else:
#    cherrypy.tree.mount(Main(), config=conf)