# ===============================================================================
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
# ===============================================================================

import re
import threading
from logbook import Logger
import queue

# noinspection PyPackageRequirements
import wx
from sqlalchemy.sql import or_

import config
import eos.db
from service import conversions
from service.settings import SettingsProvider
from service.jargon import JargonLoader

from eos.gamedata import Category as types_Category, Group as types_Group, Item as types_Item, MarketGroup as types_MarketGroup, \
    MetaGroup as types_MetaGroup, MetaType as types_MetaType
from collections import OrderedDict

pyfalog = Logger(__name__)

# Event which tells threads dependent on Market that it's initialized
mktRdy = threading.Event()

class ShipBrowserWorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pyfalog.debug("Initialize ShipBrowserWorkerThread.")
        self.name = "ShipBrowser"

    def run(self):
        self.queue = queue.Queue()
        self.cache = {}
        # Wait for full market initialization (otherwise there's high risky
        # this thread will attempt to init Market which is already being inited)
        mktRdy.wait(5)
        self.processRequests()

    def processRequests(self):
        queue = self.queue
        cache = self.cache
        sMkt = Market.getInstance()
        while True:
            try:
                id_, callback = queue.get()
                set_ = cache.get(id_)
                if set_ is None:
                    set_ = sMkt.getShipList(id_)
                    cache[id_] = set_

                wx.CallAfter(callback, (id_, set_))
            except Exception as e:
                pyfalog.critical("Callback failed.")
                pyfalog.critical(e)
            finally:
                try:
                    queue.task_done()
                except Exception as e:
                    pyfalog.critical("Queue task done failed.")
                    pyfalog.critical(e)


class SearchWorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "SearchWorker"
        self.jargonLoader = JargonLoader.instance()
        # load the jargon while in an out-of-thread context, to spot any problems while in the main thread
        self.jargonLoader.get_jargon()
        self.jargonLoader.get_jargon().apply('test string')

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

            request, callback, filterOn = self.searchRequest
            self.searchRequest = None
            cv.release()
            sMkt = Market.getInstance()
            if filterOn is True:
                # Rely on category data provided by eos as we don't hardcode them much in service
                filter_ = or_(types_Category.name.in_(sMkt.SEARCH_CATEGORIES), types_Group.name.in_(sMkt.SEARCH_GROUPS))
            elif filterOn:  # filter by selected categories
                filter_ = types_Category.name.in_(filterOn)
            else:
                filter_ = None


            jargon_request = self.jargonLoader.get_jargon().apply(request)


            results = []
            if len(request) >= config.minItemSearchLength:
                results = eos.db.searchItems(request, where=filter_,
                                             join=(types_Item.group, types_Group.category),
                                             eager=("icon", "group.category", "metaGroup", "metaGroup.parent"))

            jargon_results = []
            if len(jargon_request) >= config.minItemSearchLength:
                jargon_results = eos.db.searchItems(jargon_request, where=filter_,
                                             join=(types_Item.group, types_Group.category),
                                             eager=("icon", "group.category", "metaGroup", "metaGroup.parent"))

            items = set()
            # Return only published items, consult with Market service this time
            for item in [*results, *jargon_results]:
                if sMkt.getPublicityByItem(item):
                    items.add(item)
            wx.CallAfter(callback, items)

    def scheduleSearch(self, text, callback, filterOn=True):
        self.cv.acquire()
        self.searchRequest = (text, callback, filterOn)
        self.cv.notify()
        self.cv.release()


class Market(object):
    instance = None

    def __init__(self):

        # Init recently used module storage
        serviceMarketRecentlyUsedModules = {"pyfaMarketRecentlyUsedModules": []}

        self.serviceMarketRecentlyUsedModules = SettingsProvider.getInstance().getSettings(
                "pyfaMarketRecentlyUsedModules", serviceMarketRecentlyUsedModules)

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
        self.les_grp = types_Group()
        self.les_grp.ID = -1
        self.les_grp.name = "Limited Issue Ships"
        self.les_grp.published = True
        ships = self.getCategory("Ship")
        self.les_grp.category = ships
        self.les_grp.categoryID = ships.ID
        self.les_grp.description = ""
        self.les_grp.icon = None
        self.ITEMS_FORCEGROUP = {
            "Opux Luxury Yacht"           : self.les_grp,
            # One of those is wedding present at CCP fanfest, another was hijacked from ISD guy during an event
            "Silver Magnate"              : self.les_grp,  # Amarr Championship prize
            "Gold Magnate"                : self.les_grp,  # Amarr Championship prize
            "Armageddon Imperial Issue"   : self.les_grp,  # Amarr Championship prize
            "Apocalypse Imperial Issue"   : self.les_grp,  # Amarr Championship prize
            "Guardian-Vexor"              : self.les_grp,  # Illegal rewards for the Gallente Frontier Tour Lines event arc
            "Megathron Federate Issue"    : self.les_grp,  # Reward during Crielere event
            "Raven State Issue"           : self.les_grp,  # AT4 prize
            "Tempest Tribal Issue"        : self.les_grp,  # AT4 prize
            "Apotheosis"                  : self.les_grp,  # 5th EVE anniversary present
            "Zephyr"                      : self.les_grp,  # 2010 new year gift
            "Primae"                      : self.les_grp,  # Promotion of planetary interaction
            "Council Diplomatic Shuttle"  : self.les_grp,  # CSM X celebration
            "Freki"                       : self.les_grp,  # AT7 prize
            "Mimir"                       : self.les_grp,  # AT7 prize
            "Utu"                         : self.les_grp,  # AT8 prize
            "Adrestia"                    : self.les_grp,  # AT8 prize
            "Echelon"                     : self.les_grp,  # 2011 new year gift
            "Malice"                      : self.les_grp,  # AT9 prize
            "Vangel"                      : self.les_grp,  # AT9 prize
            "Cambion"                     : self.les_grp,  # AT10 prize
            "Etana"                       : self.les_grp,  # AT10 prize
            "Chremoas"                    : self.les_grp,  # AT11 prize :(
            "Moracha"                     : self.les_grp,  # AT11 prize
            "Stratios Emergency Responder": self.les_grp,  # Issued for Somer Blink lottery
            "Miasmos Quafe Ultra Edition" : self.les_grp,  # Gift to people who purchased FF HD stream
            "InterBus Shuttle"            : self.les_grp,
            "Leopard"                     : self.les_grp,  # 2013 new year gift
            "Whiptail"                    : self.les_grp,  # AT12 prize
            "Chameleon"                   : self.les_grp,  # AT12 prize
            "Victorieux Luxury Yacht"     : self.les_grp,  # Worlds Collide prize \o/ chinese getting owned
            "Imp"                         : self.les_grp,  # AT13 prize
            "Fiend"                       : self.les_grp,  # AT13 prize
            "Caedes"                      : self.les_grp,  # AT14 prize
            "Rabisu"                      : self.les_grp,  # AT14 prize
            "Victor"                      : self.les_grp,  # AT prize
            "Virtuoso"                    : self.les_grp,  # AT prize
        }

        self.ITEMS_FORCEGROUP_R = self.__makeRevDict(self.ITEMS_FORCEGROUP)
        self.les_grp.addItems = list(self.getItem(itmn) for itmn in self.ITEMS_FORCEGROUP_R[self.les_grp])
        self.customGroups.add(self.les_grp)

        # List of items which are forcibly published or hidden
        self.ITEMS_FORCEPUBLISHED = {
            "Data Subverter I"                         : False,  # Not used in EVE, probably will appear with Dust link
            "QA Cross Protocol Analyzer"               : False,  # QA modules used by CCP internally
            "QA Damage Module"                         : False,
            "QA ECCM"                                  : False,
            "QA Immunity Module"                       : False,
            "QA Multiship Module - 10 Players"         : False,
            "QA Multiship Module - 20 Players"         : False,
            "QA Multiship Module - 40 Players"         : False,
            "QA Multiship Module - 5 Players"          : False,
            "QA Remote Armor Repair System - 5 Players": False,
            "QA Shield Transporter - 5 Players"        : False,
            "Goru's Shuttle"                           : False,
            "Guristas Shuttle"                         : False,
            "Mobile Decoy Unit"                        : False,  # Seems to be left over test mod for deployables
            "Tournament Micro Jump Unit"               : False,  # Normally seen only on tournament arenas
        }

        # do not publish ships that we convert
        for name in conversions.packs['skinnedShips']:
            self.ITEMS_FORCEPUBLISHED[name] = False

        if config.debug:
            # Publish Tactical Dessy Modes if in debug
            # Cannot use GROUPS_FORCEPUBLISHED as this does not force items
            # within group to be published, but rather for the group itself
            # to show up on ship list
            group = self.getGroup("Ship Modifiers", eager="items")
            for item in group.items:
                self.ITEMS_FORCEPUBLISHED[item.name] = True

        # List of groups which are forcibly published
        self.GROUPS_FORCEPUBLISHED = {
            "Prototype Exploration Ship": False
        }  # We moved the only ship from this group to other group anyway

        # Dictionary of items with forced meta groups, uses following format:
        # Item name: (metagroup name, parent type name)
        self.ITEMS_FORCEDMETAGROUP = {
            "'Habitat' Miner I"                        : ("Storyline", "Miner I"),
            "'Wild' Miner I"                           : ("Storyline", "Miner I"),
            "Medium Nano Armor Repair Unit I"          : ("Tech I", "Medium Armor Repairer I"),
            "Large 'Reprieve' Vestment Reconstructer I": ("Storyline", "Large Armor Repairer I"),
            "Khanid Navy Torpedo Launcher"             : ("Faction", "Torpedo Launcher I"),
        }
        # Parent type name: set(item names)
        self.ITEMS_FORCEDMETAGROUP_R = {}
        for item, value in list(self.ITEMS_FORCEDMETAGROUP.items()):
            parent = value[1]
            if parent not in self.ITEMS_FORCEDMETAGROUP_R:
                self.ITEMS_FORCEDMETAGROUP_R[parent] = set()
            self.ITEMS_FORCEDMETAGROUP_R[parent].add(item)
        # Dictionary of items with forced market group (service assumes they have no
        # market group assigned in db, otherwise they'll appear in both original and forced groups)
        self.ITEMS_FORCEDMARKETGROUP = {
            "Advanced Cerebral Accelerator"             : 977,  # Implants & Boosters > Booster
            "Civilian Damage Control"                   : 615,  # Ship Equipment > Hull & Armor > Damage Controls
            "Civilian EM Ward Field"                    : 1695,
            # Ship Equipment > Shield > Shield Hardeners > EM Shield Hardeners
            "Civilian Explosive Deflection Field"       : 1694,
            # Ship Equipment > Shield > Shield Hardeners > Explosive Shield Hardeners
            "Civilian Hobgoblin"                        : 837,  # Drones > Combat Drones > Light Scout Drones
            "Civilian Kinetic Deflection Field"         : 1693,
            # Ship Equipment > Shield > Shield Hardeners > Kinetic Shield Hardeners
            "Civilian Light Missile Launcher"           : 640,
            # Ship Equipment > Turrets & Bays > Missile Launchers > Light Missile Launchers
            "Civilian Scourge Light Missile"            : 920,
            # Ammunition & Charges > Missiles > Light Missiles > Standard Light Missiles
            "Civilian Small Remote Armor Repairer"      : 1059,
            # Ship Equipment > Hull & Armor > Remote Armor Repairers > Small
            "Civilian Small Remote Shield Booster"      : 603,  # Ship Equipment > Shield > Remote Shield Boosters > Small
            "Civilian Stasis Webifier"                  : 683,  # Ship Equipment > Electronic Warfare > Stasis Webifiers
            "Civilian Warp Disruptor"                   : 1935,  # Ship Equipment > Electronic Warfare > Warp Disruptors
            "Hardwiring - Zainou 'Sharpshooter' ZMX10"  : 1493,
            # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX100" : 1493,
            # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX1000": 1493,
            # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX11"  : 1493,
            # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX110" : 1493,
            # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX1100": 1493,
            # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Nugoehuvi Synth Blue Pill Booster"         : 977,  # Implants & Boosters > Booster
            "Prototype Cerebral Accelerator"            : 977,  # Implants & Boosters > Booster
            "Prototype Iris Probe Launcher"             : 712,  # Ship Equipment > Turrets & Bays > Scan Probe Launchers
            "Shadow"                                    : 1310,  # Drones > Combat Drones > Fighter Bombers
            "Standard Cerebral Accelerator"             : 977,  # Implants & Boosters > Booster
        }

        self.ITEMS_FORCEDMARKETGROUP_R = self.__makeRevDict(self.ITEMS_FORCEDMARKETGROUP)

        self.FORCEDMARKETGROUP = {
            685: False,  # Ship Equipment > Electronic Warfare > ECCM
            681: False,  # Ship Equipment > Electronic Warfare > Sensor Backup Arrays
        }

        # Misc definitions
        # 0 is for items w/o meta group
        self.META_MAP = OrderedDict([("normal", frozenset((0, 1, 2, 14))),
                                     ("faction", frozenset((4, 3))),
                                     ("complex", frozenset((6,))),
                                     ("officer", frozenset((5,)))])
        self.SEARCH_CATEGORIES = (
            "Drone",
            "Module",
            "Subsystem",
            "Charge",
            "Implant",
            "Deployable",
            "Fighter",
            "Structure",
            "Structure Module",
        )
        self.SEARCH_GROUPS = ("Ice Product",)
        self.ROOT_MARKET_GROUPS = (9,  # Modules
                                   1111,  # Rigs
                                   157,  # Drones
                                   11,  # Ammo
                                   1112,  # Subsystems
                                   24,  # Implants & Boosters
                                   404,  # Deployables
                                   2202,  # Structure Equipment
                                   2203  # Structure Modifications
                                   )
        # Tell other threads that Market is at their service
        mktRdy.set()

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Market()
        return cls.instance

    @staticmethod
    def __makeRevDict(orig):
        """Creates reverse dictionary"""
        rev = {}
        for item, value in list(orig.items()):
            if value not in rev:
                rev[value] = set()
            rev[value].add(item)
        return rev

    @staticmethod
    def getItem(identity, *args, **kwargs):
        """Get item by its ID or name"""
        try:
            if isinstance(identity, types_Item):
                item = identity
            elif isinstance(identity, int):
                item = eos.db.getItem(identity, *args, **kwargs)
            elif isinstance(identity, str):
                # We normally lookup with string when we are using import/export
                # features. Check against overrides
                identity = conversions.all.get(identity, identity)
                item = eos.db.getItem(identity, *args, **kwargs)

            elif isinstance(identity, float):
                id_ = int(identity)
                item = eos.db.getItem(id_, *args, **kwargs)
            else:
                raise TypeError("Need Item object, integer, float or string as argument")
        except:
            pyfalog.error("Could not get item: {0}", identity)
            raise

        return item

    def getGroup(self, identity, *args, **kwargs):
        """Get group by its ID or name"""
        if isinstance(identity, types_Group):
            return identity
        elif isinstance(identity, (int, float, str)):
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

    @staticmethod
    def getCategory(identity, *args, **kwargs):
        """Get category by its ID or name"""
        if isinstance(identity, types_Category):
            category = identity
        elif isinstance(identity, (int, str)):
            category = eos.db.getCategory(identity, *args, **kwargs)
        elif isinstance(identity, float):
            id_ = int(identity)
            category = eos.db.getCategory(id_, *args, **kwargs)
        else:
            raise TypeError("Need Category object, integer, float or string as argument")
        return category

    @staticmethod
    def getMetaGroup(identity, *args, **kwargs):
        """Get meta group by its ID or name"""
        if isinstance(identity, types_MetaGroup):
            metaGroup = identity
        elif isinstance(identity, (int, str)):
            metaGroup = eos.db.getMetaGroup(identity, *args, **kwargs)
        elif isinstance(identity, float):
            id_ = int(identity)
            metaGroup = eos.db.getMetaGroup(id_, *args, **kwargs)
        else:
            raise TypeError("Need MetaGroup object, integer, float or string as argument")
        return metaGroup

    @staticmethod
    def getMarketGroup(identity, *args, **kwargs):
        """Get market group by its ID"""
        if isinstance(identity, types_MarketGroup):
            marketGroup = identity
        elif isinstance(identity, (int, float)):
            id_ = int(identity)
            marketGroup = eos.db.getMarketGroup(id_, *args, **kwargs)
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
            metaGroup = types_MetaType()
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
        id_ = getattr(self.getMetaGroupByItem(item), "ID", fallback)
        return id_

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
        variations_limiter = set()

        # if item belongs to these categories, use their group to find "variations"
        categories = ['Drone', 'Fighter', 'Implant']

        for item in items:
            if item.category.ID == 20:  # Implants and Boosters
                implant_remove_list = set()
                implant_remove_list.add("Low-Grade ")
                implant_remove_list.add("Low-grade ")
                implant_remove_list.add("Mid-Grade ")
                implant_remove_list.add("Mid-grade ")
                implant_remove_list.add("High-Grade ")
                implant_remove_list.add("High-grade ")
                implant_remove_list.add("Limited ")
                implant_remove_list.add(" - Advanced")
                implant_remove_list.add(" - Basic")
                implant_remove_list.add(" - Elite")
                implant_remove_list.add(" - Improved")
                implant_remove_list.add(" - Standard")
                implant_remove_list.add("Copper ")
                implant_remove_list.add("Gold ")
                implant_remove_list.add("Silver ")
                implant_remove_list.add("Advanced ")
                implant_remove_list.add("Improved ")
                implant_remove_list.add("Prototype ")
                implant_remove_list.add("Standard ")
                implant_remove_list.add("Strong ")
                implant_remove_list.add("Synth ")

                for implant_prefix in ("-6", "-7", "-8", "-9", "-10"):
                    for i in range(50):
                        implant_remove_list.add(implant_prefix + str("%02d" % i))

                for text_to_remove in implant_remove_list:
                    if text_to_remove in item.name:
                        variations_limiter.add(item.name.replace(text_to_remove, ""))

            # Get parent item
            if alreadyparent is False:
                parent = self.getParentItemByItem(item)
            else:
                parent = item
            # Combine both in the same set
            parents.add(parent)
            # Check for overrides and add them if any
            if parent.name in self.ITEMS_FORCEDMETAGROUP_R:
                for _item in self.ITEMS_FORCEDMETAGROUP_R[parent.name]:
                    i = self.getItem(_item)
                    if i:
                        variations.add(i)
        # Add all parents to variations set
        variations.update(parents)
        # Add all variations of parents to the set
        parentids = tuple(item.ID for item in parents)
        groupids = tuple(item.group.ID for item in parents if item.category.name in categories)
        variations_list = eos.db.getVariations(parentids, groupids)

        if variations_limiter:
            for limit in variations_limiter:
                trimmed_variations_list = [variation_item for variation_item in variations_list if limit in variation_item.name]
            if trimmed_variations_list:
                variations_list = trimmed_variations_list

        variations.update(variations_list)
        return variations

    def getGroupsByCategory(self, cat):
        """Get groups from given category"""
        groups = set([grp for grp in cat.groups if self.getPublicityByGroup(grp)])

        return groups

    @staticmethod
    def getMarketGroupChildren(mg):
        """Get the children marketGroups of marketGroup."""
        children = set()
        for child in mg.children:
            children.add(child)
        return children

    def getItemsByGroup(self, group):
        """Get items assigned to group"""
        # Return only public items; also, filter out items
        # which were forcibly set to other groups
        groupItems = set(group.items)
        if hasattr(group, 'addItems'):
            groupItems.update(group.addItems)
        items = set(
                [item for item in groupItems if self.getPublicityByItem(item) and self.getGroupByItem(item) == group])
        return items

    def getItemsByMarketGroup(self, mg, vars_=True):
        """Get items in the given market group"""
        result = set()
        # Get items from eos market group
        baseitms = set(mg.items)
        # Add hardcoded items to set
        if mg.ID in self.ITEMS_FORCEDMARKETGROUP_R:
            forceditms = set(self.getItem(itmn) for itmn in self.ITEMS_FORCEDMARKETGROUP_R[mg.ID])
            baseitms.update(forceditms)
        if vars_:
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
        result = set([item_ for item_ in result if self.getPublicityByItem(item_)])
        return result

    def marketGroupHasTypesCheck(self, mg):
        """If market group has any items, return true"""
        if mg and mg.ID in self.ITEMS_FORCEDMARKETGROUP_R:
            return True
        elif len(mg.items) > 0:
            return True
        else:
            return False

    def marketGroupValidityCheck(self, mg):
        """Check market group validity"""
        # The only known case when group can be invalid is
        # when it's declared to have types, but it doesn't contain anything
        if mg.ID in self.FORCEDMARKETGROUP:
            return self.FORCEDMARKETGROUP[mg.ID]
        if mg.hasTypes and not self.marketGroupHasTypesCheck(mg):
            return False
        else:
            return True

    def getIconByMarketGroup(self, mg):
        """Return icon associated to marketgroup"""
        if mg.icon:
            return mg.icon.iconFile
        else:
            while mg and not mg.hasTypes:
                mg = mg.parent
            if not mg:
                return ""
            elif self.marketGroupHasTypesCheck(mg):
                # Do not request variations to make process faster
                # Pick random item and use its icon
                items = self.getItemsByMarketGroup(mg, vars_=False)
                try:
                    item = items.pop()
                except KeyError:
                    return ""

                return item.icon.iconFile if item.icon else ""
            elif self.getMarketGroupChildren(mg) > 0:
                kids = self.getMarketGroupChildren(mg)
                mktGroups = self.getIconByMarketGroup(kids)
                size = len(mktGroups)
                return mktGroups.pop() if size > 0 else ""
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
        for id_ in self.ROOT_MARKET_GROUPS:
            mg = self.getMarketGroup(id_, eager="icon")
            root.add(mg)

        return root

    def getShipRoot(self):
        cat1 = self.getCategory("Ship")
        cat2 = self.getCategory("Structure")
        root = set(self.getGroupsByCategory(cat1) | self.getGroupsByCategory(cat2))

        return root

    def getShipList(self, grpid):
        """Get ships for given group id"""
        grp = self.getGroup(grpid, eager=("items", "items.group", "items.marketGroup"))
        ships = self.getItemsByGroup(grp)
        return ships

    def getShipListDelayed(self, id_, callback):
        """Background version of getShipList"""
        self.shipBrowserWorkerThread.queue.put((id_, callback))

    def searchShips(self, name):
        """Find ships according to given text pattern"""
        filter_ = types_Category.name.in_(["Ship", "Structure"])
        results = eos.db.searchItems(name, where=filter_,
                                     join=(types_Item.group, types_Group.category),
                                     eager=("icon", "group.category", "metaGroup", "metaGroup.parent"))
        ships = set()
        for item in results:
            if self.getPublicityByItem(item):
                ships.add(item)
        return ships

    def searchItems(self, name, callback, filterOn=True):
        """Find items according to given text pattern"""
        self.searchWorkerThread.scheduleSearch(name, callback, filterOn)

    @staticmethod
    def getItemsWithOverrides():
        overrides = eos.db.getAllOverrides()
        items = set()
        for x in overrides:
            if x.item is None:
                eos.db.saveddata_session.delete(x)
                eos.db.commit()
            else:
                items.add(x.item)
        return list(items)

    @staticmethod
    def directAttrRequest(items, attribs):
        try:
            itemIDs = tuple([i.ID for i in items])
        except TypeError:
            itemIDs = (items.ID,)
        try:
            attrIDs = tuple([i.ID for i in attribs])
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
        filtered = set([item for item in items if self.getMetaGroupIdByItem(item) in metas])
        return filtered

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
                       "Incursion ship attributes effects")
        # Stuff we don't want to see in names
        garbages = ("Effect", "Beacon", "ship attributes effects")
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
                    if groupname not in effects:
                        effects[groupname] = set()
                    effects[groupname].add((beacon, beaconname, shortname))
                    # Break loop on 1st result
                    break
        return effects
