import threading
import time
# noinspection PyPackageRequirements
import wx
from service.settings import HTMLExportSettings
from service.fit import Fit
from service.port import Port
from service.market import Market
from logbook import Logger
from eos.db import getFit

pyfalog = Logger(__name__)


class exportHtml(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = exportHtml()

        return cls._instance

    def __init__(self):
        self.thread = exportHtmlThread()

    def refreshFittingHtml(self, force=False, callback=False):
        settings = HTMLExportSettings.getInstance()

        if force or settings.getEnabled():
            self.thread.stop()
            self.thread = exportHtmlThread(callback)
            self.thread.start()


class exportHtmlThread(threading.Thread):
    def __init__(self, callback=False):
        threading.Thread.__init__(self)
        self.name = "HTMLExport"
        self.callback = callback
        self.stopRunning = False

    def stop(self):
        self.stopRunning = True

    def run(self):
        # wait 1 second just in case a lot of modifications get made
        time.sleep(1)
        if self.stopRunning:
            return

        sMkt = Market.getInstance()
        sFit = Fit.getInstance()
        settings = HTMLExportSettings.getInstance()

        minimal = settings.getMinimalEnabled()
        dnaUrl = "https://o.smium.org/loadout/dna/"

        if minimal:
            HTML = self.generateMinimalHTML(sMkt, sFit, dnaUrl)
        else:
            HTML = self.generateFullHTML(sMkt, sFit, dnaUrl)

        try:
            FILE = open(settings.getPath(), "w")
            FILE.write(HTML.encode('utf-8'))
            FILE.close()
        except IOError:
            print("Failed to write to " + settings.getPath())
            pass

        if self.callback:
            wx.CallAfter(self.callback, -1)

    def generateFullHTML(self, sMkt, sFit, dnaUrl):
        """ Generate the complete HTML with styling and javascript """
        timestamp = time.localtime(time.time())
        localDate = "%d/%02d/%02d %02d:%02d" % (timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4])

        HTML = """
<!DOCTYPE html>
<html>
  <head>
  <title>Pyfa Fittings</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.css" />
  <script src="https://code.jquery.com/jquery-1.11.0.min.js"></script>
  <script>
    // http://stackoverflow.com/questions/32453806/uncaught-securityerror-failed-to-execute-replacestate-on-history-cannot-be
    $(document).bind('mobileinit',function(){
        $.mobile.changePage.defaults.changeHash = false;
        $.mobile.hashListeningEnabled = false;
        $.mobile.pushStateEnabled = false;
    });
  </script>
  <script src="https://code.jquery.com/mobile/1.4.2/jquery.mobile-1.4.2.min.js"></script>
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
      var start = new Date(%d * 1000);

      setInterval(function() {
        var diff = (new Date - start) / 1000;

        var days = Math.floor((diff %% 31536000) / 86400);
        var hours = Math.floor(((diff %% 31536000) %% 86400) / 3600);
        var minutes = Math.floor((((diff %% 31536000) %% 86400) %% 3600) / 60);
        var seconds = Math.floor(((diff %% 31536000) %% 86400) %% 3600) %% 60;

        $('.timer').text(days+":"+hours+":"+minutes+":"+seconds+" ago");
      }, 1000);

      $('a[data-dna]').each(function( index ) {
        var dna = $(this).data('dna');
        if (typeof CCPEVE !== 'undefined') { // inside IGB
          $(this).attr('href', 'javascript:CCPEVE.showFitting("'+dna+'");');}
        else {                               // outside IGB
          $(this).attr('href', '%s'+dna); }
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
  <div style="text-align: center;"><strong>Last updated:</strong> %s <small>(<span class="timer"></span>)</small></div>

""" % (time.time(), dnaUrl, localDate)
        HTML += '  <ul data-role="listview" class="ui-listview-outer" data-inset="true" data-filter="true">\n'
        categoryList = list(sMkt.getShipRoot())
        categoryList.sort(key=lambda _ship: _ship.name)

        count = 0

        for group in categoryList:
            # init market group string to give ships something to attach to
            HTMLgroup = ''

            ships = list(sMkt.getShipList(group.ID))
            ships.sort(key=lambda _ship: _ship.name)

            # Keep track of how many ships per group
            groupFits = 0
            for ship in ships:
                fits = sFit.getFitsWithShip(ship.ID)

                if len(fits) > 0:
                    groupFits += len(fits)

                    if len(fits) == 1:
                        if self.stopRunning:
                            return
                        fit = fits[0]
                        try:
                            dnaFit = Port.exportDna(getFit(fit[0]))
                            HTMLgroup += '        <li><a data-dna="' + dnaFit + '" target="_blank">' + ship.name + ": " + \
                                         fit[1] + '</a></li>\n'
                        except:
                            pyfalog.warning("Failed to export line")
                            pass
                        finally:
                            if self.callback:
                                wx.CallAfter(self.callback, count)
                            count += 1
                    else:
                        # Ship group header
                        HTMLship = (
                            '        <li data-role="collapsible" data-iconpos="right" data-shadow="false" data-corners="false">\n'
                            '        <h2>' + ship.name + ' <span class="ui-li-count">' + str(
                                len(fits)) + '</span></h2>\n'
                                             '          <ul data-role="listview" data-shadow="false" data-inset="true" data-corners="false">\n'
                        )

                        for fit in fits:
                            if self.stopRunning:
                                return
                            try:
                                dnaFit = Port.exportDna(getFit(fit[0]))
                                print dnaFit
                                HTMLship += '          <li><a data-dna="' + dnaFit + '" target="_blank">' + fit[
                                    1] + '</a></li>\n'
                            except:
                                pyfalog.warning("Failed to export line")
                                continue
                            finally:
                                if self.callback:
                                    wx.CallAfter(self.callback, count)
                                count += 1
                        HTMLgroup += HTMLship + ('          </ul>\n'
                                                 '        </li>\n')

            if groupFits > 0:
                # Market group header
                HTML += (
                    '    <li data-role="collapsible" data-iconpos="right" data-shadow="false" data-corners="false">\n'
                    '      <h2>' + group.groupName + ' <span class="ui-li-count">' + str(groupFits) + '</span></h2>\n'
                    '      <ul data-role="listview" data-shadow="false" data-inset="true" data-corners="false">\n' + HTMLgroup +
                    '      </ul>\n'
                    '    </li>'
                )

        HTML += """
  </ul>
 </div>
</div>
</body>
</html>"""

        return HTML

    def generateMinimalHTML(self, sMkt, sFit, dnaUrl):
        """ Generate a minimal HTML version of the fittings, without any javascript or styling"""
        categoryList = list(sMkt.getShipRoot())
        categoryList.sort(key=lambda _ship: _ship.name)

        count = 0
        HTML = ''
        for group in categoryList:
            # init market group string to give ships something to attach to

            ships = list(sMkt.getShipList(group.ID))
            ships.sort(key=lambda _ship: _ship.name)

            ships.sort(key=lambda _ship: _ship.name)

            for ship in ships:
                fits = sFit.getFitsWithShip(ship.ID)
                for fit in fits:
                    if self.stopRunning:
                        return
                    try:
                        dnaFit = Port.exportDna(getFit(fit[0]))
                        HTML += '<a class="outOfGameBrowserLink" target="_blank" href="' + dnaUrl + dnaFit + '">' + ship.name + ': ' + \
                                fit[1] + '</a><br> \n'
                    except:
                        pyfalog.error("Failed to export line")
                        continue
                    finally:
                        if self.callback:
                            wx.CallAfter(self.callback, count)
                        count += 1
        return HTML
