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

import re
import threading
import wx

import Queue

import eos.db
import eos.types

try:
    from collections import OrderedDict
except ImportError:
    from gui.utils.compat import OrderedDict

# Event which tells threads dependent on Market that it's initialized
mktRdy = threading.Event()

class ShipBrowserWorkerThread(threading.Thread):
    def run(self):
        self.queue = Queue.Queue()
        self.cache = {}
        # Wait for full market initialization (otherwise there's high risky
        # this thread will attempt to init Market which is already being inited)
        mktRdy.wait(5)
        self.processRequests()

    def processRequests(self):
        queue = self.queue
        cache = self.cache
        sMarket = Market.getInstance()
        while True:
            try:
                callback, id = queue.get()
                set = cache.get(id)
                if set is None:
                    set = sMarket.getShipList(id)
                    cache[id] = set

                wx.CallAfter(callback, (id, set))
            except:
                pass
            finally:
                try:
                    queue.task_done()
                except:
                    pass

class PriceWorkerThread(threading.Thread):
    def run(self):
        self.queue = Queue.Queue()
        self.processUpdates()

    def processUpdates(self):
        queue = self.queue
        while True:
            # Grab our data
            callback, requests = queue.get()

            # Grab prices, this is the time-consuming part
            if len(requests) > 0:
                eos.types.Price.fetchPrices(*requests)

            wx.CallAfter(callback)
            queue.task_done()

    def trigger(self, prices, callbacks):
        self.queue.put((callbacks, prices))

class SearchWorkerThread(threading.Thread):
    def run(self):
        self.cv = threading.Condition()
        self.searchRequest = None
        self.processSearches()

    def processSearches(self):
        cv = self.cv

        while True:
            cv.acquire()
            while self.searchRequest is None:
                cv.wait()

            request, callback = self.searchRequest
            self.searchRequest = None
            cv.release()
            sMarket = Market.getInstance()
            # Rely on category data provided by eos as we don't hardcode them much in service
            filter = eos.types.Category.name.in_(sMarket.SEARCH_CATEGORIES)
            results = eos.db.searchItems(request, where=filter,
                                         join=(eos.types.Item.group, eos.types.Group.category),
                                         eager=("icon", "group.category", "metaGroup", "metaGroup.parent"))

            items = set()
            # Return only published items, consult with Market service this time
            for item in results:
                if sMarket.getPublicityByItem(item):
                    items.add(item)
            wx.CallAfter(callback, items)

    def scheduleSearch(self, text, callback):
        self.cv.acquire()
        self.searchRequest = (text, callback)
        self.cv.notify()
        self.cv.release()

class Market():
    instance = None
    def __init__(self):
        self.priceCache = {}

        # Start price fetcher
        self.priceWorkerThread = PriceWorkerThread()
        self.priceWorkerThread.daemon = True
        self.priceWorkerThread.start()

        # Thread which handles search
        self.searchWorkerThread = SearchWorkerThread()
        self.searchWorkerThread.daemon = True
        self.searchWorkerThread.start()

        # Ship browser helper thread
        self.shipBrowserWorkerThread = ShipBrowserWorkerThread()
        self.shipBrowserWorkerThread.daemon = True
        self.shipBrowserWorkerThread.start()

        # Items' group overrides
        self.customGroups = set()
        # Limited edition ships
        self.les_grp = eos.types.Group()
        self.les_grp.ID = -1
        self.les_grp.name = "Limited Issue Ships"
        self.les_grp.published = True
        ships = self.getCategory("Ship")
        self.les_grp.category = ships
        self.les_grp.categoryID = ships.ID
        self.les_grp.description = ""
        self.les_grp.icon = None
        self.ITEMS_FORCEGROUP = {
            "Opux Luxury Yacht": self.les_grp, # One of those is wedding present at CCP fanfest, another was hijacked from ISD guy during an event
            "Silver Magnate": self.les_grp,  # Amarr Championship prize
            "Gold Magnate": self.les_grp,  # Amarr Championship prize
            "Armageddon Imperial Issue": self.les_grp,  # Amarr Championship prize
            "Apocalypse Imperial Issue": self.les_grp, # Amarr Championship prize
            "Guardian-Vexor": self.les_grp, # Illegal rewards for the Gallente Frontier Tour Lines event arc
            "Megathron Federate Issue": self.les_grp, # Reward during Crielere event
            "Raven State Issue": self.les_grp,  # AT4 prize
            "Tempest Tribal Issue": self.les_grp, # AT4 prize
            "Apotheosis": self.les_grp, # 5th EVE anniversary present
            "Zephyr": self.les_grp, # 2010 new year gift
            "Primae": self.les_grp, # Promotion of planetary interaction
            "Freki": self.les_grp, # AT7 prize
            "Mimir": self.les_grp, # AT7 prize
            "Utu": self.les_grp, # AT8 prize
            "Adrestia": self.les_grp, # AT8 prize
            "Echelon": self.les_grp, # 2011 new year gift
            "Malice": self.les_grp, # AT9 prize
            "Vangel": self.les_grp } # AT9 prize
        self.ITEMS_FORCEGROUP_R = self.__makeRevDict(self.ITEMS_FORCEGROUP)
        self.les_grp.items += list(self.getItem(itmn) for itmn in self.ITEMS_FORCEGROUP_R[self.les_grp])
        self.customGroups.add(self.les_grp)

        # List of items which are forcibly published or hidden
        self.ITEMS_FORCEPUBLISHED = {
            "Ibis": True, # Noobship
            "Impairor": True, # Noobship
            "Velator": True, # Noobship
            "Reaper": True, # Noobship
            "TEST Damage Mod": False, # Marked as published by CCP for whatever reason
            "Ghost Heavy Missile": False, # Missile used by Sansha
            "Nano Paint": False, # It will be used for ship paint job, no use as of today
            "Deimos Old": False,
            "Large Shield Transporter II - 5 players": False,
            "TEST Damage Mod - 10 Players": False,
            "TEST Damage Mod - 20 Players": False,
            "TEST Damage Mod - 40 Players": False,
            "TEST Damage Mod - 5 Players": False,
            "Large Remote Armor Repair System II - 5 players": False }

        # List of groups which are forcibly published
        self.GROUPS_FORCEPUBLISHED = {
            "Prototype Exploration Ship": False, # We moved the only ship from this group to other group anyway
            "Rookie ship": True } # Group-container for published noobships

        # Dictionary of items with forced meta groups, uses following format:
        # Item name: (metagroup name, parent type name)
        self.ITEMS_FORCEDMETAGROUP = {
            "'Habitat' Miner I": ("Storyline", "Miner I"),
            "'Wild' Miner I": ("Storyline", "Miner I"),
            "Medium Nano Armor Repair Unit I": ("Tech I", "Medium Armor Repairer I"),
            "Large 'Reprieve' Vestment Reconstructer I": ("Storyline", "Large Armor Repairer I"),
            "Khanid Navy Siege Missile Launcher": ("Faction", "Siege Missile Launcher I"),
            "Dark Blood Tracking Disruptor": ("Faction", "Tracking Disruptor I"),
            "True Sansha Tracking Disruptor": ("Faction", "Tracking Disruptor I"),
            "Shadow Serpentis Remote Sensor Dampener": ("Faction", "Remote Sensor Dampener I") }
        # Parent type name: set(item names)
        self.ITEMS_FORCEDMETAGROUP_R = {}
        for item, value in self.ITEMS_FORCEDMETAGROUP.items():
            parent = value[1]
            if not parent in self.ITEMS_FORCEDMETAGROUP_R:
                self.ITEMS_FORCEDMETAGROUP_R[parent] = set()
            self.ITEMS_FORCEDMETAGROUP_R[parent].add(item)
        # Dictionary of items with forced market group (service assumes they have no
        # market group assigned in db, otherwise they'll appear in both original and forced groups)
        self.ITEMS_FORCEDMARKETGROUP = {
            "'Alpha' Codebreaker I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "'Codex' Codebreaker I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "'Daemon' Codebreaker I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "'Libram' Codebreaker I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "Akemon's Modified 'Noble' ZET5000": 1185, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 10 > Armor Implants
            "Cerebral Accelerator": 977, # Implants & Boosters > Booster
            "Civilian Ballistic Deflection Field": 760, # Ship Equipment > Civilian Modules
            "Civilian Bloodclaw Light Missile": 920, # Ammunition & Charges > Missiles > Light Missiles > Standard Light Missiles
            "Civilian Damage Control": 760, # Ship Equipment > Civilian Modules
            "Civilian Explosion Dampening Field": 760, # Ship Equipment > Civilian Modules
            "Civilian Heat Dissipation Field": 760, # Ship Equipment > Civilian Modules
            "Civilian Hobgoblin": 837, # Drones > Combat Drones > Light Scout Drones
            "Civilian Photon Scattering Field": 760, # Ship Equipment > Civilian Modules
            "Civilian Remote Armor Repair System": 760, # Ship Equipment > Civilian Modules
            "Civilian Remote Shield Transporter": 760, # Ship Equipment > Civilian Modules
            "Civilian Standard Missile Launcher": 760, # Ship Equipment > Civilian Modules
            "Civilian Stasis Webifier": 760, # Ship Equipment > Civilian Modules
            "Civilian Warp Disruptor": 760, # Ship Equipment > Civilian Modules
            "Hardwiring - Inherent Implants 'Gentry' ZEX10": 1152, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Armor Implants
            "Hardwiring - Inherent Implants 'Gentry' ZEX100": 1152, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Armor Implants
            "Hardwiring - Inherent Implants 'Gentry' ZEX1000": 1152, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Armor Implants
            "Hardwiring - Inherent Implants 'Gentry' ZEX20": 1160, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 7 > Armor Implants
            "Hardwiring - Inherent Implants 'Gentry' ZEX200": 1160, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 7 > Armor Implants
            "Hardwiring - Inherent Implants 'Gentry' ZEX2000": 1160, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 7 > Armor Implants
            "Hardwiring - Zainou 'Sharpshooter' ZMX10": 1156, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Missile Implants
            "Hardwiring - Zainou 'Sharpshooter' ZMX100": 1156, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Missile Implants
            "Hardwiring - Zainou 'Sharpshooter' ZMX1000": 1156, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Missile Implants
            "Hardwiring - Zainou 'Sharpshooter' ZMX11": 1156, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Missile Implants
            "Hardwiring - Zainou 'Sharpshooter' ZMX110": 1156, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Missile Implants
            "Hardwiring - Zainou 'Sharpshooter' ZMX1100": 1156, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Missile Implants
            "Hardwiring - Zainou 'Sprite' KXX1000": 1154, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Engineering Implants
            "Hardwiring - Zainou 'Sprite' KXX2000": 1154, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Engineering Implants
            "Hardwiring - Zainou 'Sprite' KXX500": 1154, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Engineering Implants
            "Imperial Navy Modified 'Noble' Implant": 1185, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 10 > Armor Implants
            "Imperial Special Ops Field Enhancer - Standard": 618, # Implants & Boosters > Implants > Attribute Enhancers > Implant Slot 1
            "Michi's Excavation Augmentor": 1187, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 10 > Industry Implants
            "Nugoehuvi Synth Blue Pill Booster": 977, # Implants & Boosters > Booster
            "Numon Family Heirloom": 1152, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Armor Implants
            "Ogdin's Eye Coordination Enhancer": 1163, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 7 > Gunnery Implants
            "Pashan's Turret Customization Mindlink": 1180, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 9 > Gunnery Implants
            "Pashan's Turret Handling Mindlink": 1186, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 10 > Gunnery Implants
            "Prototype Iris Probe Launcher": 712, # Ship Equipment > Turrets & Bays > Scan Probe Launchers
            "Quafe Zero": 977, # Implants & Boosters > Booster
            "Republic Special Ops Field Enhancer - Gamma": 620, # Implants & Boosters > Implants > Attribute Enhancers > Implant Slot 3
            "Sansha Modified 'Gnome' Implant": 1167, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 7 > Shield Implants
            "Shadow": 1310, # Drones > Combat Drones > Fighter Bombers
            "Shaqil's Speed Enhancer": 1157, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 6 > Navigation Implants
            "Sleeper Data Analyzer I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "Talocan Data Analyzer I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "Terran Data Analyzer I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "Tetrimon Data Analyzer I": 714, # Ship Equipment > Electronics and Sensor Upgrades > Scanners > Data and Composition Scanners
            "Whelan Machorin's Ballistic Smartlink": 1189, # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 10 > Missile Implants
            "Zor's Custom Navigation Hyper-Link": 1176 } # Implants & Boosters > Implants > Skill Hardwiring > Implant Slot 8 > Navigation Implants
        self.ITEMS_FORCEDMARKETGROUP_R = self.__makeRevDict(self.ITEMS_FORCEDMARKETGROUP)

        # Misc definitions
        # 0 is for items w/o meta group
        self.META_MAP = OrderedDict([("normal",  frozenset((0, 1, 2, 14))),
                                     ("faction", frozenset((4, 3))),
                                     ("complex", frozenset((6,))),
                                     ("officer", frozenset((5,)))])
        self.SEARCH_CATEGORIES = ("Drone", "Module", "Subsystem", "Charge", "Implant")
        self.ROOT_MARKET_GROUPS = (9,     # Modules
                                   1111,  # Rigs
                                   157,   # Drones
                                   11,    # Ammo
                                   1112,  # Subsystems
                                   24)    # Implants & Boosters
        # Tell other threads that Market is at their service
        mktRdy.set()

    @classmethod
    def getInstance(cls):
        if cls.instance == None:
            cls.instance = Market()
        return cls.instance

    def __makeRevDict(self, orig):
        """Creates reverse dictionary"""
        rev = {}
        for item, value in orig.items():
            if not value in rev:
                rev[value] = set()
            rev[value].add(item)
        return rev

    def getItem(self, identity, *args, **kwargs):
        """Get item by its ID or name"""
        if isinstance(identity, eos.types.Item):
            item = identity
        elif isinstance(identity, (int, basestring)):
            item = eos.db.getItem(identity, *args, **kwargs)
        elif isinstance(identity, float):
            id = int(identity)
            item = eos.db.getItem(id, *args, **kwargs)
        else:
            raise TypeError("Need Item object, integer, float or string as argument")
        return item

    def getGroup(self, identity, *args, **kwargs):
        """Get group by its ID or name"""
        if isinstance(identity, eos.types.Group):
            return identity
        elif isinstance(identity, (int, float, basestring)):
            if isinstance(identity, float):
                identity = int(identity)
            # Check custom groups
            for cgrp in self.customGroups:
                # During first comparison we need exact int, not float for matching
                if cgrp.ID == identity or cgrp.name == identity:
                    # Return first match
                    return cgrp
            # Return eos group if everything else returned nothing
            return eos.db.getGroup(identity, *args, **kwargs)
        else:
            raise TypeError("Need Group object, integer, float or string as argument")

    def getCategory(self, identity, *args, **kwargs):
        """Get category by its ID or name"""
        if isinstance(identity, eos.types.Category):
            category = identity
        elif isinstance(identity, (int, basestring)):
            category = eos.db.getCategory(identity, *args, **kwargs)
        elif isinstance(identity, float):
            id = int(identity)
            category = eos.db.getCategory(id, *args, **kwargs)
        else:
            raise TypeError("Need Category object, integer, float or string as argument")
        return category

    def getMetaGroup(self, identity, *args, **kwargs):
        """Get meta group by its ID or name"""
        if isinstance(identity, eos.types.MetaGroup):
            metaGroup = identity
        elif isinstance(identity, (int, basestring)):
            metaGroup = eos.db.getMetaGroup(identity, *args, **kwargs)
        elif isinstance(identity, float):
            id = int(identity)
            metaGroup = eos.db.getMetaGroup(id, *args, **kwargs)
        else:
            raise TypeError("Need MetaGroup object, integer, float or string as argument")
        return metaGroup

    def getMarketGroup(self, identity, *args, **kwargs):
        """Get market group by its ID"""
        if isinstance(identity, eos.types.MarketGroup):
            marketGroup = identity
        elif isinstance(identity, (int, float)):
            id = int(identity)
            marketGroup = eos.db.getMarketGroup(id, *args, **kwargs)
        else:
            raise TypeError("Need MarketGroup object, integer or float as argument")
        return marketGroup

    def getGroupByItem(self, item):
        """Get group by item"""
        if item.name in self.ITEMS_FORCEGROUP:
            group = self.ITEMS_FORCEGROUP[item.name]
        else:
            group = item.group
        return group

    def getCategoryByItem(self, item):
        """Get category by item"""
        grp = self.getGroupByItem(item)
        cat = grp.category
        return cat

    def getMetaGroupByItem(self, item):
        """Get meta group by item"""
        # Check if item is in forced metagroup map
        if item.name in self.ITEMS_FORCEDMETAGROUP:
            # Create meta group from scratch
            metaGroup = eos.types.MetaType()
            # Get meta group info object based on meta group name
            metaGroupInfo = self.getMetaGroup(self.ITEMS_FORCEDMETAGROUP[item.name][0])
            # Get parent item based on its name
            parent = self.getItem(self.ITEMS_FORCEDMETAGROUP[item.name][1])
            # Assign all required for metaGroup variables
            metaGroup.info = metaGroupInfo
            metaGroup.items = item
            metaGroup.parent = parent
            metaGroup.metaGroupID = metaGroupInfo.ID
            metaGroup.parentTypeID = parent.ID
            metaGroup.typeID = item.ID
        # If no forced meta group is provided, try to use item's
        # meta group if any
        else:
            metaGroup = item.metaGroup
        return metaGroup

    def getMetaGroupIdByItem(self, item, fallback=0):
        """Get meta group ID by item"""
        id = getattr(self.getMetaGroupByItem(item), "ID", fallback)
        return id

    def getMarketGroupByItem(self, item, parentcheck=True):
        """Get market group by item, its ID or name"""
        # Check if we force market group for given item
        if item.name in self.ITEMS_FORCEDMARKETGROUP:
            mgid = self.ITEMS_FORCEDMARKETGROUP[item.name]
            return self.getMarketGroup(mgid)
        # Check if item itself has market group
        elif item.marketGroupID:
            return item.marketGroup
        elif parentcheck:
            # If item doesn't have marketgroup, check if it has parent
            # item and use its market group
            parent = self.getParentItemByItem(item, selfparent=False)
            if parent:
                return parent.marketGroup
            else:
                return None
        else:
            return None

    def getParentItemByItem(self, item, selfparent=True):
        """Get parent item by item"""
        mg = self.getMetaGroupByItem(item)
        if mg:
            parent = mg.parent
        # Consider self as parent if item has no parent in database
        elif selfparent is True:
            parent = item
        else:
            parent = None
        return parent

    def getVariationsByItems(self, items, alreadyparent=False):
        """Get item variations by item, its ID or name"""
        # Set for IDs of parent items
        parents = set()
        # Set-container for variables
        variations = set()
        for item in items:
            # Get parent item
            if alreadyparent is False:
                parent = self.getParentItemByItem(item)
            else:
                parent = item
            # Combine both in the same set
            parents.add(parent)
            # Check for overrides and add them if any
            if parent.name in self.ITEMS_FORCEDMETAGROUP_R:
                for itmn in self.ITEMS_FORCEDMETAGROUP_R[parent.name]:
                    variations.add(self.getItem(itmn))
        # Add all parents to variations set
        variations.update(parents)
        # Add all variations of parents to the set
        parentids = tuple(item.ID for item in parents)
        variations.update(eos.db.getVariations(parentids))
        return variations

    def getGroupsByCategory(self, cat):
        """Get groups from given category"""
        groups = set(filter(lambda grp: self.getPublicityByGroup(grp), cat.groups))
        return groups

    def getMarketGroupChildren(self, mg):
        """Get the children marketGroups of marketGroup."""
        children = set()
        for child in mg.children:
            children.add(child)
        return children

    def getItemsByGroup(self, group):
        """Get items assigned to group"""
        # Return only public items; also, filter out items
        # which were forcibly set to other groups
        items = set(filter(lambda item: self.getPublicityByItem(item) and self.getGroupByItem(item) == group, group.items))
        return items

    def getItemsByMarketGroup(self, mg, vars=True):
        """Get items in the given market group"""
        result = set()
        # Get items from eos market group
        baseitms = set(mg.items)
        # Add hardcoded items to set
        if mg.ID in self.ITEMS_FORCEDMARKETGROUP_R:
            forceditms = set(self.getItem(itmn) for itmn in self.ITEMS_FORCEDMARKETGROUP_R[mg.ID])
            baseitms.update(forceditms)
        if vars:
            parents = set()
            for item in baseitms:
                # Add one of the base market group items to result
                result.add(item)
                parent = self.getParentItemByItem(item, selfparent=False)
                # If item has no parent, it's base item (or at least should be)
                if parent is None:
                    parents.add(item)
            # Fetch variations only for parent items
            variations = self.getVariationsByItems(parents, alreadyparent=True)
            for variation in variations:
                # Exclude items with their own explicitly defined market groups
                if self.getMarketGroupByItem(variation, parentcheck=False) is None:
                    result.add(variation)
        else:
            result = baseitms
        # Get rid of unpublished items
        result = set(filter(lambda item: self.getPublicityByItem(item), result))
        return result

    def marketGroupHasTypesCheck(self, mg):
        """If market group has any items, return true"""
        if mg.ID in self.ITEMS_FORCEDMARKETGROUP_R:
            return True
        elif not mg.hasTypes:
            return False
        elif len(mg.items) > 0:
            return True
        else:
            return False

    def marketGroupValidityCheck(self, mg):
        """Check market group validity"""
        # The only known case when group can be invalid is
        # when it's declared to have types, but it doesn't contain anything
        if mg.hasTypes and not self.marketGroupHasTypesCheck(mg):
            return False
        else:
            return True

    def getIconByMarketGroup(self, mg):
        """Return icon associated to marketgroup"""
        if mg.icon:
            return mg.icon.iconFile
        else:
            if self.marketGroupHasTypesCheck(mg):
                # Do not request variations to make process faster
                # Pick random item and use its icon
                item = self.getItemsByMarketGroup(mg, vars=False).pop()
                return item.icon.iconFile if item.icon else ""
            elif self.getMarketGroupChildren(mg) > 0:
                return self.getIconByMarketGroup(self.getMarketGroupChildren(mg).pop())
            else:
                return ""

    def getPublicityByItem(self, item):
        """Return if an item is published"""
        if item.name in self.ITEMS_FORCEPUBLISHED:
            pub = self.ITEMS_FORCEPUBLISHED[item.name]
        else:
            pub = item.published
        return pub

    def getPublicityByGroup(self, group):
        """Return if an group is published"""
        if group.name in self.GROUPS_FORCEPUBLISHED:
            pub = self.GROUPS_FORCEPUBLISHED[group.name]
        else:
            pub = group.published
        return pub

    def getMarketRoot(self):
        """
        Get the root of the market tree.
        Returns a list, where each element is a tuple containing:
        the ID, the name and the icon of the group
        """
        root = set()
        for id in self.ROOT_MARKET_GROUPS:
            mg = self.getMarketGroup(id, eager="icon")
            root.add(mg)

        return root

    def getShipRoot(self):
        cat = self.getCategory("Ship")
        root = set(self.getGroupsByCategory(cat))
        return root

    def getShipList(self, grpid):
        """Get ships for given group id"""
        grp = self.getGroup(grpid, eager=("items", "items.group", "items.marketGroup"))
        ships = self.getItemsByGroup(grp)
        for ship in ships:
            ship.race
        return ships

    def getShipListDelayed(self, id, callback):
        """Background version of getShipList"""
        self.shipBrowserWorkerThread.queue.put((id, callback))

    def searchShips(self, name):
        """Find ships according to given text pattern"""
        results = eos.db.searchItems(name)
        ships = set()
        for item in results:
            if self.getCategoryByItem(item).name == "Ship" and self.getPublicityByItem(item):
                ships.add(item)
        return ships

    def searchItems(self, name, callback):
        """Find items according to given text pattern"""
        self.searchWorkerThread.scheduleSearch(name, callback)

    def directAttrRequest(self, items, attribs):
        try:
            itemIDs = tuple(map(lambda i: i.ID, items))
        except TypeError:
            itemIDs = (items.ID,)
        try:
            attrIDs = tuple(map(lambda i: i.ID, attribs))
        except TypeError:
            attrIDs = (attribs.ID,)
        info = {}
        for itemID, typeID, val in eos.db.directAttributeRequest(itemIDs, attrIDs):
            info[itemID] = val

        return info

    def getImplantTree(self):
        """Return implant market group children"""
        img = self.getMarketGroup(27)
        return self.getMarketGroupChildren(img)

    def filterItemsByMeta(self, items, metas):
        """Filter items by meta lvl"""
        filtered = set(filter(lambda item: self.getMetaGroupIdByItem(item) in metas, items))
        return filtered

    def getPriceNow(self, typeID):
        """Get price for provided typeID"""
        price = self.priceCache.get(typeID)
        if price is None:
            price = eos.db.getPrice(typeID)
            if price is None:
                price = eos.types.Price(typeID)
                eos.db.add(price)

            self.priceCache[typeID] = price

        return price

    def getPricesNow(self, typeIDs):
        """Return map of calls to get price against list of typeIDs"""
        return map(self.getPrice, typeIDs)

    def getPrices(self, typeIDs, callback):
        """Get prices for multiple typeIDs"""
        requests = []
        for typeID in typeIDs:
            price = self.getPriceNow(typeID)
            requests.append(price)

        def cb():
            try:
                callback(requests)
            except:
                pass
            eos.db.commit()

        self.priceWorkerThread.trigger(requests, cb)

    def getSystemWideEffects(self):
        """
        Get dictionary with system-wide effects
        """
        # Container for system-wide effects
        effects = {}
        # Expressions for matching when detecting effects we're looking for
        validgroups = ("Black Hole Effect Beacon",
                       "Cataclysmic Variable Effect Beacon",
                       "Magnetar Effect Beacon",
                       "Pulsar Effect Beacon",
                       "Red Giant Beacon",
                       "Wolf Rayet Effect Beacon",
                       "Incursion Effect")
        # Stuff we don't want to see in names
        garbages = ("Effect", "Beacon")
        # Get group with all the system-wide beacons
        grp = self.getGroup("Effect Beacon")
        beacons = self.getItemsByGroup(grp)
        # Cycle through them
        for beacon in beacons:
            # Check if it belongs to any valid group
            for group in validgroups:
                # Check beginning of the name only
                if re.match(group, beacon.name):
                    # Get full beacon name
                    beaconname = beacon.name
                    for garbage in garbages:
                        beaconname = re.sub(garbage, "", beaconname)
                    beaconname = re.sub(" {2,}", " ", beaconname).strip()
                    # Get short name
                    shortname = re.sub(group, "", beacon.name)
                    for garbage in garbages:
                        shortname = re.sub(garbage, "", shortname)
                    shortname = re.sub(" {2,}", " ", shortname).strip()
                    # Get group name
                    groupname = group
                    for garbage in garbages:
                        groupname = re.sub(garbage, "", groupname)
                    groupname = re.sub(" {2,}", " ", groupname).strip()
                    # Add stuff to dictionary
                    if not groupname in effects:
                        effects[groupname] = set()
                    effects[groupname].add((beacon, beaconname, shortname))
                    # Break loop on 1st result
                    break
        return effects
