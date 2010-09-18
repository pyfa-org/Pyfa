#===============================================================================
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
#===============================================================================

import eos.db
import eos.types
import wx
import collections
import threading
from sqlalchemy.orm.exc import NoResultFound

class PriceWorkerThread(threading.Thread):
    def run(self):
        self.cv = threading.Condition()
        self.updateRequests = collections.deque()
        self.scheduled = set()
        self.processUpdates()

    def processUpdates(self):
        updateRequests = self.updateRequests
        cv = self.cv

        while True:
            cv.acquire()

            while len(updateRequests) == 0:
                cv.wait()

            # Grab our data and rerelease the lock
            callback, requests = self.updateRequests.popleft()
            self.scheduled.clear()
            cv.release()

            # Grab prices, this is the time-consuming part
            if len(requests) > 0:
                eos.types.Price.fetchPrices(*requests)

            callback()


    def trigger(self, prices, callbacks):
        self.cv.acquire()
        self.updateRequests.append((callbacks, prices))
        self.scheduled.update(prices)
        self.cv.notify()
        self.cv.release()

    def isScheduled(self, price):
        self.cv.acquire()
        scheduled = price in self.scheduled
        self.cv.release()
        return scheduled

class Market():
    instance = None
    FORCED_SHIPS = ("Freki", "Mimir", "Utu", "Adrestia", "Ibis", "Impairor", "Velator", "Reaper")
    FORCED_GROUPS = ("Rookie ship",)
    META_MAP = {"normal": (1, 2, 14),
                "faction": (4, 3),
                "complex": (6,),
                "officer": (5,)}
    SEARCH_CATEGORIES = ("Drone", "Module", "Subsystem", "Charge", "Implant")

    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = Market()

        return cls.instance

    def __init__(self):
        self.activeMetas = set()
        self.priceCache = {}
        self.workerThread = PriceWorkerThread()
        self.workerThread.daemon = True
        self.workerThread.start()

    def getChildren(self, id):
        """
        Get the children of the group or marketGroup with the passed id.
        Returns a list, where each element is a tuple containing:
        the id, the name, the icon, wether the group has more children.
        """

        group = eos.db.getMarketGroup(id, eager="icon")
        children = []
        for child in group.children:
            icon = child.icon.iconFile if child.icon else ""
            children.append((child.ID, child.name, icon, not child.hasTypes))


        return children

    def getShipRoot(self):
        cat = eos.db.getCategory(6)
        root = []
        for grp in cat.groups:
            if grp.published  or grp.name in self.FORCED_GROUPS:
                root.append((grp.ID, grp.name))

        return root

    def getShipList(self, id):
        ships = []
        grp = eos.db.getGroup(id, eager=("items"))
        for item in grp.items:
            if item.published  or item.name in self.FORCED_SHIPS:
                ships.append((item.ID, item.name, item.race))

        return ships

    def searchShips(self, name):
        results = eos.db.searchItems(name)
        ships = []
        for item in results:
            if item.category.name == "Ship" and (item.published or item.name in self.FORCED_SHIPS):
                ships.append((item.ID, item.name, item.race))

        return ships

    def searchItems(self, name):
        filter = (eos.types.Category.name.in_(self.SEARCH_CATEGORIES), eos.types.Item.published == True)
        results = eos.db.searchItems(name, where=filter,
                                     join=(eos.types.Item.group, eos.types.Group.category),
                                     eager=("icon", "group.category"))

        items = []
        for item in results:
            if item.category.name in self.SEARCH_CATEGORIES:
                items.append((item.ID, item.name, item.group.name, item.metaGroup.ID if item.metaGroup else 1, item.icon.iconFile if item.icon else ""))

        return items

    def searchFits(self, name):
        results = eos.db.searchFits(name)
        fits = []
        for fit in results:
            fits.append((fit.ID, fit.name, fit.ship.item.name))

        return fits

    def getMarketRoot(self):
        """
        Get the root of the market tree.
        Returns a list, where each element is a tuple containing:
        the ID, the name and the icon of the group
        """

        marketGroups = (9, #Modules
                        1111, #Rigs
                        157, #Drones
                        11, #Ammo
                        1112, #Subsystems
                        24) #Implants & Boosters
        root = []
        for id in marketGroups:
            mg = eos.db.getMarketGroup(id, eager="icon")
            root.append((id, mg.name, mg.icon.iconFile if mg.icon else ""))

        return root

    def activateMetaGroup(self, name):
        for meta in self.META_MAP[name]:
            self.activeMetas.add(meta)

    def disableMetaGroup(self, name):
        for meta in self.META_MAP[name]:
            if meta in self.activeMetas:
                self.activeMetas.remove(meta)

    def isMetaIdActive(self, meta):
        return meta in self.activeMetas

    def getMetaName(self, metaId):
        for name, ids in self.META_MAP.items():
            for id in ids:
                if metaId == id:
                    return name

    def getVariations(self, marketGroupId):
        if len(self.activeMetas) == 0:
            return tuple()

        mg = eos.db.getMarketGroup(marketGroupId)
        l = []
        done = set()
        for item in mg.items:
            if 1 in self.activeMetas:
                if item not in done:
                    done.add(item)
                    l.append((item.ID, item.name, item.icon.iconFile if item.icon else ""))

            vars = eos.db.getVariations(item, metaGroups = tuple(self.activeMetas), eager="icon")
            for var in vars:
                if var not in done:
                    done.add(var)
                    l.append((var.ID, var.name, var.icon.iconFile if var.icon else ""))

        return l

    def getPrices(self, typeIDs, callback):
        fetch = set()
        all = []
        new = []
        for typeID in typeIDs:
            price = self.priceCache.get(typeID)
            if price is None:
                try:
                    price = eos.db.getPrice(typeID)
                except NoResultFound:
                    price = eos.types.Price(typeID)
                    new.append(price)

                self.priceCache[typeID] = price

            all.append(price)
            if not price.isValid and not self.workerThread.isScheduled(price):
                fetch.add(price)

        def dbAdd():
            for price in new:
                eos.db.saveddata_session.add(price)
                eos.db.saveddata_session.commit()
                eos.db.saveddata_session.flush()

        def cb():
            wx.CallAfter(callback, all)
            wx.CallAfter(dbAdd)

        self.workerThread.trigger(fetch, cb)
