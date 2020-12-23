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
import timeit
from itertools import chain

import math
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
    def fetchPrices(cls, prices, fetchTimeout, validityOverride):
        """Fetch all prices passed to this method"""

        # Dictionary for our price objects
        priceMap = {}
        # Check all provided price objects, and add those we want to update to
        # dictionary
        for price in prices:
            if not price.isValid(validityOverride):
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
        sourceAll = list(cls.sources.keys())
        sourcePrimary = sFit.serviceFittingOptions["priceSource"] if sFit.serviceFittingOptions["priceSource"] in sourceAll else sourceAll[0]
        # When we have picked primary source, make sure to include only sources from the same group to avoid fetching
        # tranquility data for serenity or vice versa
        sourceAll = list(n for n, s in cls.sources.items() if s.group == cls.sources[sourcePrimary].group)

        # Format: {source name: timeout weight}
        sources = {sourcePrimary: len(sourceAll)}
        for source in sourceAll:
            if source == sourcePrimary:
                continue
            sources[source] = min(sources.values()) - 1

        # Record timeouts as it will affect our final decision
        timedOutSources = {}

        remainingTime = fetchTimeout

        for source in sorted(sources, key=sources.get, reverse=True):
            timeBefore = timeit.default_timer()
            pyfalog.info('Trying {}'.format(source))
            timedOutSources[source] = False
            # Time we allocate for a source depends on source weight and remaining time
            sourceFetchTimeout = remainingTime * sources[source] / sum(sources.values())
            try:
                sourceCls = cls.sources.get(source)
                sourceCls(priceMap, cls.systemsList[sFit.serviceFittingOptions["priceSystem"]], sourceFetchTimeout)
            except TimeoutError:
                pyfalog.warning("Price fetch timeout for source {}".format(source))
                timedOutSources[source] = True
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                pyfalog.warn('Failed to fetch prices from price source {}: {}'.format(source, e))
            # Sources remove price map items as they fetch info, if none remain then we're done
            if not priceMap:
                break
            timeAfter = timeit.default_timer()
            # Remove source so it doesn't affect time weights of sources we're going to use next
            del sources[source]
            remainingTime -= timeAfter - timeBefore
            # No time remaining (should not happen) - mark remaining sources as timeout
            if remainingTime <= 0:
                for source in sources:
                    timedOutSources[source] = True
                break


        # If we get to this point, then we've failed to get price with all our sources
        # If all sources failed due to timeouts, set one status
        if all(to is True for to in timedOutSources.values()):
            for typeID in priceMap.keys():
                priceMap[typeID].update(PriceStatus.fetchTimeout)
        # If some sources failed due to any other reason, then it's definitely not network
        # timeout and we just set another status
        else:
            for typeID in priceMap.keys():
                priceMap[typeID].update(PriceStatus.fetchFail)

    def getPriceNow(self, objitem):
        """Get price for provided typeID"""
        sMkt = Market.getInstance()
        item = sMkt.getItem(objitem)

        return item.price.price

    def getPrices(self, objitems, callback, fetchTimeout=30, waitforthread=False, validityOverride=None):
        """Get prices for multiple typeIDs"""
        requests = []
        sMkt = Market.getInstance()
        for objitem in objitems:
            item = sMkt.getItem(objitem)
            requests.append(item.price)

        def cb():
            try:
                callback(requests)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                pyfalog.critical("Execution of callback from getPrices failed.")
                pyfalog.critical(e)
            db.commit()

        if waitforthread:
            self.priceWorkerThread.setToWait(requests, cb)
        else:
            self.priceWorkerThread.trigger(requests, cb, fetchTimeout, validityOverride)

    def clearPriceCache(self):
        pyfalog.debug("Clearing Prices")
        db.clearPrices()

    def findCheaperReplacements(self, items, callback, fetchTimeout=10):
        sMkt = Market.getInstance()

        replacementsAll = {}  # All possible item replacements
        for item in items:
            if item in replacementsAll:
                continue
            itemRepls = sMkt.getReplacements(item)
            if itemRepls:
                replacementsAll[item] = itemRepls
        itemsToFetch = {i for i in chain(replacementsAll.keys(), *replacementsAll.values())}

        def makeCheapMapCb(requests):
            # Decide what we are going to replace
            replacementsCheaper = {}  # Items which should be replaced
            for replacee, replacers in replacementsAll.items():
                replacer = min(replacers, key=lambda i: i.price.price or math.inf)
                if (replacer.price.price or math.inf) < (replacee.price.price or math.inf):
                    replacementsCheaper[replacee] = replacer
            try:
                callback(replacementsCheaper)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                pyfalog.critical("Execution of callback from findCheaperReplacements failed.")
                pyfalog.critical(e)

        # Prices older than 2 hours have to be refetched
        validityOverride = 2 * 60 * 60
        self.getPrices(itemsToFetch, makeCheapMapCb, fetchTimeout=fetchTimeout, validityOverride=validityOverride)




class PriceWorkerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "PriceWorker"
        self.queue = queue.Queue()
        self.wait = {}
        self.running = True
        pyfalog.debug("Initialize PriceWorkerThread.")

    def run(self):
        queue = self.queue
        while True:
            if not self.running:
                break
            # Grab our data
            callback, requests, fetchTimeout, validityOverride = queue.get()

            # Grab prices, this is the time-consuming part
            if len(requests) > 0:
                Price.fetchPrices(requests, fetchTimeout, validityOverride)

            wx.CallAfter(callback)
            queue.task_done()

            # After we fetch prices, go through the list of waiting items and call their callbacks
            for price in requests:
                callbacks = self.wait.pop(price.typeID, None)
                if callbacks:
                    for callback in callbacks:
                        wx.CallAfter(callback)

    def trigger(self, prices, callbacks, fetchTimeout, validityOverride):
        self.queue.put((callbacks, prices, fetchTimeout, validityOverride))

    def setToWait(self, prices, callback):
        for price in prices:
            callbacks = self.wait.setdefault(price.typeID, [])
            callbacks.append(callback)

    def stop(self):
        self.running = False


# Import market sources only to initialize price source modules, they register on their own
from service.marketSources import evemarketer, evemarketdata, evepraisal, fuzzwork, cevemarket  # noqa: E402
