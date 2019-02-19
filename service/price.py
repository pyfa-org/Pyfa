# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


import queue
import threading

import wx
from logbook import Logger

from eos import db
from eos.saveddata.price import PriceStatus
from service.fit import Fit
from service.market import Market
from service.network import TimeoutError


pyfalog = Logger(__name__)


class Price:
    instance = None

    systemsList = {
        "Jita": 30000142,
        "Amarr": 30002187,
        "Dodixie": 30002659,
        "Rens": 30002510,
        "Hek": 30002053
    }

    sources = {}

    def __init__(self):
        # Start price fetcher
        self.priceWorkerThread = PriceWorkerThread()
        self.priceWorkerThread.daemon = True
        self.priceWorkerThread.start()

    @classmethod
    def register(cls, source):
        cls.sources[source.name] = source

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Price()
        return cls.instance

    @classmethod
    def fetchPrices(cls, prices, timeout=5):
        """Fetch all prices passed to this method"""

        # Dictionary for our price objects
        priceMap = {}
        # Check all provided price objects, and add those we want to update to
        # dictionary
        for price in prices:
            if not price.isValid:
                priceMap[price.typeID] = price

        if not priceMap:
            return

        # Compose list of items we're going to request
        for typeID in tuple(priceMap):
            # Get item object
            item = db.getItem(typeID)
            # We're not going to request items only with market group, as our current market
            # sources do not provide any data for items not on the market
            if item is None:
                continue
            if not item.marketGroupID:
                priceMap[typeID].update(PriceStatus.notSupported)
                del priceMap[typeID]
                continue

        if not priceMap:
            return

        sFit = Fit.getInstance()

        if len(cls.sources.keys()) == 0:
            pyfalog.warn('No price source can be found')
            return

        # attempt to find user's selected price source, otherwise get first one
        sourcesToTry = list(cls.sources.keys())
        curr = sFit.serviceFittingOptions["priceSource"] if sFit.serviceFittingOptions["priceSource"] in sourcesToTry else sourcesToTry[0]

        # Record timeouts as it will affect our final decision
        timeouts = {}

        while priceMap and sourcesToTry:
            timeouts[curr] = False
            sourcesToTry.remove(curr)
            try:
                sourceCls = cls.sources.get(curr)
                sourceCls(priceMap, cls.systemsList[sFit.serviceFittingOptions["priceSystem"]], timeout)
            except TimeoutError:
                pyfalog.warning("Price fetch timeout for source {}".format(curr))
                timeouts[curr] = True
            except Exception as e:
                pyfalog.warn('Failed to fetch prices from price source {}: {}'.format(curr, e))
            if sourcesToTry:
                curr = sourcesToTry[0]
                pyfalog.warn('Trying {}'.format(curr))

        # If we get to this point, then we've failed to get price with all our sources
        # If all sources failed due to timeouts, set one status
        if all(to is True for to in timeouts.values()):
            for typeID in priceMap.keys():
                priceMap[typeID].update(PriceStatus.fetchTimeout)
        # If some sources failed due to any other reason, then it's definitely not network
        # timeout and we just set another status
        else:
            for typeID in priceMap.keys():
                priceMap[typeID].update(PriceStatus.fetchFail)

    @classmethod
    def fitItemsList(cls, fit):
        # Compose a list of all the data we need & request it
        fit_items = [fit.ship.item]

        for mod in fit.modules:
            if not mod.isEmpty:
                fit_items.append(mod.item)

        for drone in fit.drones:
            fit_items.append(drone.item)

        for fighter in fit.fighters:
            fit_items.append(fighter.item)

        for cargo in fit.cargo:
            fit_items.append(cargo.item)

        for boosters in fit.boosters:
            fit_items.append(boosters.item)

        for implants in fit.implants:
            fit_items.append(implants.item)

        return list(set(fit_items))

    def getPriceNow(self, objitem):
        """Get price for provided typeID"""
        sMkt = Market.getInstance()
        item = sMkt.getItem(objitem)

        return item.price.price

    def getPrices(self, objitems, callback, waitforthread=False):
        """Get prices for multiple typeIDs"""
        requests = []
        sMkt = Market.getInstance()
        for objitem in objitems:
            item = sMkt.getItem(objitem)
            requests.append(item.price)

        def cb():
            try:
                callback(requests)
            except Exception as e:
                pyfalog.critical("Callback failed.")
                pyfalog.critical(e)

            db.commit()

        if waitforthread:
            self.priceWorkerThread.setToWait(requests, cb)
        else:
            self.priceWorkerThread.trigger(requests, cb)

    def clearPriceCache(self):
        pyfalog.debug("Clearing Prices")
        db.clearPrices()


class PriceWorkerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "PriceWorker"
        self.queue = queue.Queue()
        self.wait = {}
        pyfalog.debug("Initialize PriceWorkerThread.")

    def run(self):
        queue = self.queue
        while True:
            # Grab our data
            callback, requests = queue.get()

            # Grab prices, this is the time-consuming part
            if len(requests) > 0:
                Price.fetchPrices(requests)

            wx.CallAfter(callback)
            queue.task_done()

            # After we fetch prices, go through the list of waiting items and call their callbacks
            for price in requests:
                callbacks = self.wait.pop(price.typeID, None)
                if callbacks:
                    for callback in callbacks:
                        wx.CallAfter(callback)

    def trigger(self, prices, callbacks):
        self.queue.put((callbacks, prices))

    def setToWait(self, prices, callback):
        for x in prices:
            if x.typeID not in self.wait:
                self.wait[x.typeID] = []
            self.wait[x.typeID].append(callback)


# Import market sources only to initialize price source modules, they register on their own
from service.marketSources import evemarketer, evemarketdata  # noqa: E402
