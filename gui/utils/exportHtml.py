import threading
import time
import service

class exportHtml():
    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = exportHtml()

        return cls._instance

    def __init__(self):
        print "init exportHtml()"
        self.thread = exportHtmlThread()

    def refreshFittingHTMl(self):
        print "refresh HTML"
        settings = service.settings.HTMLExportSettings.getInstance()

        if (settings.getEnabled()):
            self.thread.stop()
            self.thread = exportHtmlThread()
            self.thread.start()

class exportHtmlThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopRunning = False

    def stop(self):
        self.stopRunning = True

    def run(self):
        print "run"
        # wait 1 second just in case a lot of modifications get made
        time.sleep(1);
        if self.stopRunning:
            return;

        sMarket = service.Market.getInstance()
        sFit    = service.Fit.getInstance()
        settings = service.settings.HTMLExportSettings.getInstance()

        HTML = """
        <!DOCTYPE html>
        <html>
            <head>
            <title>My Page</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.css" />
            <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
            <script src="http://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.js"></script>
            <style>
                /* Basic settings */
                .ui-li-static.ui-collapsible {
                    padding: 0;
                }
                .ui-li-static.ui-collapsible > .ui-collapsible-content > .ui-listview,
                .ui-li-static.ui-collapsible > .ui-collapsible-heading {
                    margin: 0;
                }
                .ui-li-static.ui-collapsible > .ui-collapsible-content {
                    padding-top: 0;
                    padding-bottom: 0;
                    padding-right: 0;
                    border-bottom-width: 0;
                }
                /* collapse vertical borders */
                .ui-li-static.ui-collapsible > .ui-collapsible-content > .ui-listview > li.ui-last-child,
                .ui-li-static.ui-collapsible.ui-collapsible-collapsed > .ui-collapsible-heading > a.ui-btn {
                    border-bottom-width: 0;
                }
                .ui-li-static.ui-collapsible > .ui-collapsible-content > .ui-listview > li.ui-first-child,
                .ui-li-static.ui-collapsible > .ui-collapsible-content > .ui-listview > li.ui-first-child > a.ui-btn,
                .ui-li-static.ui-collapsible > .ui-collapsible-heading > a.ui-btn {
                    border-top-width: 0;
                }
                /* Remove right borders */
                .ui-li-static.ui-collapsible > .ui-collapsible-heading > a.ui-btn,
                .ui-li-static.ui-collapsible > .ui-collapsible-content > .ui-listview > .ui-li-static,
                .ui-li-static.ui-collapsible > .ui-collapsible-content > .ui-listview > li > a.ui-btn,
                .ui-li-static.ui-collapsible > .ui-collapsible-content {
                    border-right-width: 0;
                }
                /* Remove left borders */
                /* Here, we need class ui-listview-outer to identify the outermost listview */
                .ui-listview-outer > .ui-li-static.ui-collapsible .ui-li-static.ui-collapsible.ui-collapsible,
                .ui-listview-outer > .ui-li-static.ui-collapsible > .ui-collapsible-heading > a.ui-btn,
                .ui-li-static.ui-collapsible > .ui-collapsible-content {
                    border-left-width: 0;
                }
                .ui-content { width: 800px !important; margin: 0 auto !important;  }
            </style>
        </head>
        <body>
        <div  id="canvas" data-role="page">
            <div data-role="header">
                <h1>PyFa fits</h1>
            </div>
            <div data-role="content">
        """
        HTML += '<ul data-role="listview" class="ui-listview-outer" data-inset="true" data-filter="true">';
        categoryList = [];
        self.categoryList = list(sMarket.getShipRoot())
        self.categoryList.sort(key=lambda ship: ship.name)
        for shipType in self.categoryList:
            HTMLgroup = (
                '<li data-role="collapsible" data-iconpos="right" data-shadow="false" data-corners="false">\n'
                '\t<h2>' + shipType.groupName + '</h2>\n'
                '\t<ul data-role="listview" data-shadow="false" data-inset="true" data-corners="false">\n')
            ships = sMarket.getShipList(shipType.ID)
            for ship in ships:
                HTMLship = (
                '\t\t<li data-role="collapsible" data-iconpos="right" data-shadow="false" data-corners="false">\n'
                '\t\t<h2>' + ship.name + '</h2>\n'
                '\t\t\t<ul data-role="listview" data-shadow="false" data-inset="true" data-corners="false">\n')
                fits = sFit.getFitsWithShip(ship.ID)
                for fit in fits:
                    if self.stopRunning:
                        return;
                    dnaFit = sFit.exportDna(fit[0])
                    HTMLship += "\t\t\t\t<li><a href=\"javascript:CCPEVE.showFitting('" + dnaFit + "');\" >" + fit[1] + "</a></li>\n"

                HTMLship += "\t\t\t</ul>\n\t\t</li>\n"
                if len(fits) > 0:
                    HTMLgroup += HTMLship
            HTMLgroup += "\t</ul>\n</li>\n"
            if len(ships) > 0:
                HTML += HTMLgroup

        HTML += """
                </ul>
            </div>
        </div>
        </body>
        """

        try:
            print "write"
            FILE = open(settings.getPath(), "w")
            FILE.write(HTML.encode('utf-8'));
            FILE.close();
        except IOError:
            print "Failed to write to " + settings.getPath()
            pass

