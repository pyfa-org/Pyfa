import threading
import time
import service
import wx

class exportHtml():
    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = exportHtml()

        return cls._instance

    def __init__(self):
        self.thread = exportHtmlThread()

    def refreshFittingHtml(self, force = False, callback = False):
        settings = service.settings.HTMLExportSettings.getInstance()

        if (force or settings.getEnabled()):
            self.thread.stop()
            self.thread = exportHtmlThread(callback)
            self.thread.start()

class exportHtmlThread(threading.Thread):

    def __init__(self, callback = False):
        threading.Thread.__init__(self)
        self.callback = callback
        self.stopRunning = False

    def stop(self):
        self.stopRunning = True

    def run(self):
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
  <title>Pyfa Fittings</title>
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
    .ui-content { max-width: 800px !important; margin: 0 auto !important;  }
    .ui-listview > .ui-li-static.ui-li-has-count { padding-right: 0px }
  </style>

  <script>
    $(document).ready(function() {
      $('a[data-dna]').each(function( index ) {
        var dna = $(this).data('dna');
        if (typeof CCPEVE !== 'undefined') { // inside IGB
          $(this).attr('href', 'javascript:CCPEVE.showFitting("'+dna+'");'); }
        else {                               // outside IGB
          $(this).attr('href', 'https://null-sec.com/hangar/?dna='+dna); }
      });
    });
  </script>
</head>
<body>
<div  id="canvas" data-role="page">
  <div data-role="header">
    <h1>Pyfa fits</h1>
  </div>
  <div data-role="content">

"""
        HTML += '  <ul data-role="listview" class="ui-listview-outer" data-inset="true" data-filter="true">\n'
        categoryList = list(sMarket.getShipRoot())
        categoryList.sort(key=lambda ship: ship.name)
        for group in categoryList:
            # init market group string to give ships something to attach to
            HTMLgroup = ''

            ships = list(sMarket.getShipList(group.ID))
            ships.sort(key=lambda ship: ship.name)

            # Keep track of how many ships per group
            groupFits = 0
            for ship in ships:
                fits = sFit.getFitsWithShip(ship.ID)
                if len(fits) > 0:
                    groupFits += len(fits)

                    # Ship group header
                    HTMLship = (
                    '        <li data-role="collapsible" data-iconpos="right" data-shadow="false" data-corners="false">\n'
                    '        <h2>' + ship.name + ' <span class="ui-li-count">'+str(len(fits))+'</span></h2>\n'
                    '          <ul data-role="listview" data-shadow="false" data-inset="true" data-corners="false">\n')

                    for fit in fits:
                        if self.stopRunning:
                            return;
                        dnaFit = sFit.exportDna(fit[0])
                        HTMLship += '          <li><a data-dna="' + dnaFit + '" target="_blank">' + fit[1] + '</a></li>\n'

                    HTMLgroup += HTMLship + ('          </ul>\n'
                                             '        </li>\n')
            if groupFits > 0:
                # Market group header
                HTML += (
                '    <li data-role="collapsible" data-iconpos="right" data-shadow="false" data-corners="false">\n'
                '      <h2>' + group.groupName + ' <span class="ui-li-count">'+str(groupFits)+'</span></h2>\n'
                '      <ul data-role="listview" data-shadow="false" data-inset="true" data-corners="false">\n'
                + HTMLgroup +
                '      </ul>\n'
                '    </li>')

        HTML += """
  </ul>
 </div>
</div>
</body>
</html>"""

        try:
            FILE = open(settings.getPath(), "w")
            FILE.write(HTML.encode('utf-8'));
            FILE.close();
        except IOError:
            print "Failed to write to " + settings.getPath()
            pass

        if self.callback:
            wx.CallAfter(self.callback)

