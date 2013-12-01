import sys
import cherrypy
import core.updates
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
        '<p><input type=submit value=\'Make request.\'></p>'
        '</form>' +
        self.footer())

    @cherrypy.expose
    def process_report(self, aVersion=None, aPlatform=None, aLanguage=None,
                       aReport=None):

        KBs = core.updates.getKBsFromReport(aReport)
        if len(KBs) == 0:

            return (
            self.header() +
            '<H1>Nothing to show. KBs\' list is empty.</H2>' +
            self.footer())

        query = {}
        query['$or'] = self.kbsToQueryList(KBs)
        query['Version'] = aVersion
        query['Type'] = aPlatform
        query['Language'] = aLanguage

        items = self.db.getItemsFromDB('win32', 'updates', aQuery=query)
        if items.count() == 0:

            return (
            self.header() +
            '<H1>Not founded updates</H1>' + self.kbsToTable(KBs) +
            self.footer())

        updates = core.updates.Updates()
        updates.addUpdates(items)

        updatesList = ('<H1>Update List</H1><p><ul>' +
                       self.itemsData2TableRow(updates) +
                       '</ul><p><H1>End List</H1>')

        KBs = self.notFoundedKbList(KBs, updates)
        if len(KBs) == 0:

            return (
            self.header() +
            updatesList +
            self.footer())

        query = {}
        query['$or'] = self.kbsToQueryList(KBs)

        items = self.db.getItemsFromDB('win32', 'updates', aQuery=query)
        if items.count() == 0:

            return (
            self.header() +
            updatesList +
            '<H1>Not founded updates</H1>' + self.kbsToTable(KBs) +
            self.footer())

        updates = core.updates.Updates()
        updates.addUpdates(items)

        kbsNumberList = ('<br><br>' +
                         '<H1>Values only by number</H1><p><ul>' +
                         self.itemsData2TableRow(updates) +
                         '</ul><p><H1>End List</H1>')

        KBs = self.notFoundedKbList(KBs, updates)
        if len(KBs) == 0:

            return (
            self.header() +
            updatesList +
            kbsNumberList +
            self.footer())

        return (
        self.header() +
        updatesList +
        kbsNumberList +
        '<H1>Not founded updates</H1>' + self.kbsToTable(KBs) +
        self.footer())

    def kbsToQueryList(self, aKBs):

        kbList = []
        for kb in aKBs:

            kbList.append({'KB': kb})

        return kbList

    def kbsToTable(self, aKBs):

        kbItems = '<p><ul>'
        for kb in aKBs:
            kbItems = (kbItems +
            '<li><a href=\'http://support.microsoft.com/KB/%s\'>%s</a></li>' %
            (kb, kb))
        kbItems = kbItems + '</ul><p>'
        return kbItems

    def itemsData2TableRow(self, aItems):

        row = ''
        for item in aItems:
            row = (row +
            '<li>KB: %s Type: %s Date: %s Version: %s Language: %s Path: %s' %
            (item['KB'], item['Type'], item['Date'].date(), item['Version'],
            item['Language'], item['Path']))
        return row

    def notFoundedKbList(self, aKBs, aItems):

        kbList = []
        for kb in aKBs:

            founded = False
            for it in aItems:

                if kb == it['KB']:

                    founded = True
                    break

            if not founded:
                kbList.append(kb)

        return kbList

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
