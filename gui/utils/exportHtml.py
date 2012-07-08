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
        self.thread = exportHtmlThread()
    
    def refreshFittingHTMl(self):
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
            <link rel="stylesheet" href="http://code.jquery.com/mobile/1.1.0/jquery.mobile-1.1.0.min.css" />
            <script src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
            <script src="http://code.jquery.com/mobile/1.1.0/jquery.mobile-1.1.0.min.js"></script>
        </head> 
        <body>
        <div  id="canvas" data-role="page"> 
            <div data-role="header">
                <h1>PyFa fits</h1>
            </div>
            <div data-role="content">     
        """     
        
        HTML += '<ul data-role="listview" data-inset="true" data-filter="true">';
        categoryList = [];
        self.categoryList = list(sMarket.getShipRoot())
        self.categoryList.sort(key=lambda ship: ship.name)
        for shipType in self.categoryList:
           ships = sMarket.getShipList(shipType.ID)
           for ship in ships:
               HTMLship = '<li><h2>' + ship.name + '</h2><ul>'
               fits = sFit.getFitsWithShip(ship.ID)
               for fit in fits:
                   if self.stopRunning: 
                       return;
                   dnaFit = sFit.exportDna(fit[0])
                   HTMLship += "<li><a href=\"javascript:CCPEVE.showFitting('" + dnaFit + "');\" >" + fit[1] + "</a></li>"

               HTMLship += "</ul></li>"
               if len(fits) > 0:
                   HTML += HTMLship

        HTML += """
                </ul>           
            </div>
        </div>
        </body>
        """
    
        try:
            FILE = open(settings.getPath(), "w")
            FILE.write(HTML);
            FILE.close();
        except IOError:
            print "Failed to write to " + settings.getPath()
            pass
        
