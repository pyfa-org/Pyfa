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

import queue
import re
import threading
from collections import OrderedDict
from itertools import chain

# noinspection PyPackageRequirements
import wx
from logbook import Logger
from sqlalchemy.sql import or_

import config
import eos.db
from eos.gamedata import Category as types_Category, Group as types_Group, Item as types_Item, MarketGroup as types_MarketGroup, \
    MetaGroup as types_MetaGroup
from service import conversions
from service.jargon import JargonLoader
from service.settings import SettingsProvider
from utils.cjk import isStringCjk

pyfalog = Logger(__name__)
_t = wx.GetTranslation

# Event which tells threads dependent on Market that it's initialized
mktRdy = threading.Event()


class RegexTokenizationError(Exception):
    pass


class ShipBrowserWorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pyfalog.debug("Initialize ShipBrowserWorkerThread.")
        self.name = "ShipBrowser"
        self.running = True

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
            if not self.running:
                break
            try:
                id_, callback = queue.get()
                set_ = cache.get(id_)
                if set_ is None:
                    set_ = sMkt.getShipList(id_)
                    cache[id_] = set_

                wx.CallAfter(callback, (id_, set_))
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                pyfalog.critical("Callback failed.")
                pyfalog.critical(e)
            finally:
                try:
                    queue.task_done()
                except (KeyboardInterrupt, SystemExit):
                    raise
                except Exception as e:
                    pyfalog.critical("Queue task done failed.")
                    pyfalog.critical(e)

    def stop(self):
        self.running = False


class SearchWorkerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "SearchWorker"
        self.jargonLoader = JargonLoader.instance()
        # load the jargon while in an out-of-thread context, to spot any problems while in the main thread
        self.jargonLoader.get_jargon()
        self.jargonLoader.get_jargon().apply('test string'.split())
        self.running = True

    def run(self):
        self.cv = threading.Condition()
        self.searchRequest = None
        self.processSearches()

    def processSearches(self):
        cv = self.cv

        while True:
            if not self.running:
                break
            cv.acquire()
            while self.searchRequest is None:
                cv.wait()

            request, callback, filterName = self.searchRequest
            self.searchRequest = None
            cv.release()
            sMkt = Market.getInstance()
            if filterName == 'market':
                # Rely on category data provided by eos as we don't hardcode them much in service
                filters = [or_(
                    types_Category.name.in_(sMkt.SEARCH_CATEGORIES),
                    types_Group.name.in_(sMkt.SEARCH_GROUPS))]
            # Used in implant editor
            elif filterName == 'implants':
                filters = [types_Category.name == 'Implant']
            # Actually not everything, just market search + ships
            elif filterName == 'everything':
                filters = [
                    or_(
                        types_Category.name.in_(sMkt.FIT_CATEGORIES),
                        types_Group.name.in_(sMkt.FIT_GROUPS)),
                    or_(
                        types_Category.name.in_(sMkt.SEARCH_CATEGORIES),
                        types_Group.name.in_(sMkt.SEARCH_GROUPS))]
            else:
                filters = [None]

            if request.strip().lower().startswith('re:'):
                requestTokens = self._prepareRequestRegex(request[3:])
            else:
                requestTokens = self._prepareRequestNormal(request)
            requestTokens = self.jargonLoader.get_jargon().apply(requestTokens)

            all_results = set()
            joinedTokens = ' '.join(requestTokens)
            if (
                (isStringCjk(joinedTokens) and len(joinedTokens) >= config.minItemSearchLengthCjk)
                or len(joinedTokens) >= config.minItemSearchLength
            ):
                for filter_ in filters:
                    filtered_results = eos.db.searchItemsRegex(
                        requestTokens, where=filter_,
                        join=(types_Item.group, types_Group.category),
                        eager=("group.category", "metaGroup"))
                    all_results.update(filtered_results)

            item_IDs = set()
            # Return only published items, consult with Market service this time
            for item in all_results:
                if sMkt.getPublicityByItem(item):
                    item_IDs.add(item.ID)
            wx.CallAfter(callback, sorted(item_IDs))

    def scheduleSearch(self, text, callback, filterName=None):
        self.cv.acquire()
        self.searchRequest = (text, callback, filterName)
        self.cv.notify()
        self.cv.release()

    def stop(self):
        self.running = False

    def _prepareRequestNormal(self, request):
        # Escape regexp-specific symbols, and un-escape whitespaces
        request = re.escape(request)
        request = re.sub(r'\\(?P<ws>\s+)', '\g<ws>', request)
        # Imitate wildcard search
        request = re.sub(r'\\\*', r'\\w*', request)
        request = re.sub(r'\\\?', r'\\w?', request)
        tokens = request.split()
        return tokens

    def _prepareRequestRegex(self, request):
        roundLvl = 0
        squareLvl = 0
        nextEscaped = False
        tokens = []
        currentToken = ''

        def verifyErrors():
            if squareLvl not in (0, 1):
                raise RegexTokenizationError('Square braces level is {}'.format(squareLvl))
            if roundLvl < 0:
                raise RegexTokenizationError('Round braces level is {}'.format(roundLvl))

        try:
            for char in request:
                thisEscaped = nextEscaped
                nextEscaped = False
                if thisEscaped:
                    currentToken += char
                elif char == '\\':
                    currentToken += char
                    nextEscaped = True
                elif char == '[':
                    currentToken += char
                    squareLvl += 1
                elif char == ']':
                    currentToken += char
                    squareLvl -= 1
                elif char == '(' and squareLvl == 0:
                    currentToken += char
                    roundLvl += 1
                elif char == ')' and squareLvl == 0:
                    currentToken += char
                    roundLvl -= 1
                elif char.isspace() and roundLvl == squareLvl == 0:
                    if currentToken:
                        tokens.append(currentToken)
                        currentToken = ''
                else:
                    currentToken += char
                verifyErrors()
            else:
                if currentToken:
                    tokens.append(currentToken)
        # Treat request as normal string if regex tokenization fails
        except RegexTokenizationError:
            tokens = self._prepareRequestNormal(request)
        return tokens


class Market:
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
        self.les_grp.displayName = _t("Limited Issue Ships")
        self.les_grp.published = True
        ships = self.getCategory("Ship")
        self.les_grp.category = ships
        self.les_grp.categoryID = ships.ID
        self.les_grp.description = ""
        self.les_grp.icon = None
        self.ITEMS_FORCEGROUP = {
            "Capsule"                     : self.getGroup("Shuttle"),
            "Opux Luxury Yacht"           : self.les_grp,  # One of those is wedding present at CCP fanfest, another was hijacked from ISD guy during an event
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
            "Victor"                      : self.les_grp,  # AT15 prize
            "Virtuoso"                    : self.les_grp,  # AT15 prize
            "Hydra"                       : self.les_grp,  # AT16 prize
            "Tiamat"                      : self.les_grp,  # AT16 prize
            "Raiju"                       : self.les_grp,  # AT17 prize
            "Laelaps"                     : self.les_grp,  # AT17 prize
            "Boobook"                     : self.les_grp,  # 19th EVE anniversary gift
            "Geri"                        : self.les_grp,  # AT18 prize
            "Bestla"                      : self.les_grp,  # AT18 prize
        }

        self.ITEMS_FORCEGROUP_R = self.__makeRevDict(self.ITEMS_FORCEGROUP)
        for grp, itemNames in self.ITEMS_FORCEGROUP_R.items():
            grp.addItems = list(self.getItem(i) for i in itemNames)
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
            "'Habitat' Miner I": ("Storyline", "Miner I"),
            "'Wild' Miner I": ("Storyline", "Miner I"),
            "Khanid Navy Torpedo Launcher": ("Faction", "Torpedo Launcher I"),
            "Dread Guristas Standup Variable Spectrum ECM": ("Structure Faction", "Standup Variable Spectrum ECM I"),
            "Dark Blood Standup Heavy Energy Neutralizer": ("Structure Faction", "Standup Heavy Energy Neutralizer I")}
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
            "Advanced Cerebral Accelerator"             : 2487,  # Implants & Boosters > Booster > Cerebral Accelerators
            "Civilian Hobgoblin"                        : 837,  # Drones > Combat Drones > Light Scout Drones
            "Civilian Light Missile Launcher"           : 640,  # Ship Equipment > Turrets & Launchers > Missile Launchers > Light Missile Launchers
            "Civilian Scourge Light Missile"            : 920,  # Ammunition & Charges > Missiles > Light Missiles > Standard Light Missiles
            "Civilian Small Remote Armor Repairer"      : 1059,  # Ship Equipment > Hull & Armor > Remote Armor Repairers > Small
            "Civilian Small Remote Shield Booster"      : 603,  # Ship Equipment > Shield > Remote Shield Boosters > Small
            "Hardwiring - Zainou 'Sharpshooter' ZMX10"  : 1493,  # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX100" : 1493,  # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX1000": 1493,  # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX11"  : 1493,  # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX110" : 1493,  # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Hardwiring - Zainou 'Sharpshooter' ZMX1100": 1493,  # Implants & Boosters > Implants > Skill Hardwiring > Missile Implants > Implant Slot 06
            "Prototype Cerebral Accelerator"            : 2487,  # Implants & Boosters > Booster > Cerebral Accelerators
            "Prototype Iris Probe Launcher"             : 712,  # Ship Equipment > Scanning Equipment > Scan Probe Launchers
            "Standard Cerebral Accelerator"             : 2487,  # Implants & Boosters > Booster > Cerebral Accelerators
        }

        self.ITEMS_FORCEDMARKETGROUP_R = self.__makeRevDict(self.ITEMS_FORCEDMARKETGROUP)

        self.FORCEDMARKETGROUP = {
            685: False,   # Ship Equipment > Electronic Warfare > ECCM
            681: False,   # Ship Equipment > Electronic Warfare > Sensor Backup Arrays
            1639: False,  # Ship Equipment > Fleet Assistance > Command Processors
            2527: True,   # Ship Equipment > Hull & Armor > Mutadaptive Remote Armor Repairers - has hasTypes set to 1 while actually having no types
        }

        # Misc definitions
        # 0 is for items w/o meta group
        self.META_MAP = OrderedDict([("faction", frozenset((4, 3, 52))),
                                     ("complex", frozenset((6,))),
                                     ("officer", frozenset((5,)))])
        nonNormalMetas = set(chain(*self.META_MAP.values()))
        self.META_MAP["normal"] = frozenset((0, *(mg.ID for mg in eos.db.getMetaGroups() if mg.ID not in nonNormalMetas)))
        self.META_MAP.move_to_end("normal", last=False)
        self.META_MAP_REVERSE = {sv: k for k, v in self.META_MAP.items() for sv in v}
        self.META_MAP_REVERSE_GROUPED = {}
        i = 0
        for mgids in self.META_MAP.values():
            for mgid in mgids:
                self.META_MAP_REVERSE_GROUPED[mgid] = i
            i += 1
        self.META_MAP_REVERSE_INDICES = self.__makeReverseMetaMapIndices()
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
        self.SEARCH_GROUPS = (
            "Ice Product",
            "Cargo Container",
            "Secure Cargo Container",
            "Audit Log Secure Container",
            "Freight Container",
            "Jump Filaments",
            "Triglavian Space Filaments"
        )
        self.ROOT_MARKET_GROUPS = (9,  # Ship Equipment
                                   1111,  # Rigs
                                   157,  # Drones
                                   11,  # Ammunition & Charges
                                   1112,  # Subsystems
                                   24,  # Implants & Boosters
                                   404,  # Deployable Structures
                                   2202,  # Structure Equipment
                                   2203,  # Structure Modifications
                                   2456  # Filaments
                                   )
        self.SHOWN_MARKET_GROUPS = eos.db.getMarketTreeNodeIds(self.ROOT_MARKET_GROUPS)
        self.FIT_CATEGORIES = ['Ship']
        self.FIT_GROUPS = ['Citadel', 'Engineering Complex', 'Refinery']
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

    def __makeReverseMetaMapIndices(self):
        revmap = {}
        i = 0
        for mgids in self.META_MAP.values():
            for mgid in mgids:
                revmap[mgid] = i
            i += 1
        return revmap

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
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pyfalog.error("Could not get item: {0}", identity)
            raise

        return item

    @staticmethod
    def getItems(itemIDs, eager=None):
        items = eos.db.getItems(itemIDs, eager=eager)
        return items

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
        if item.typeName in self.ITEMS_FORCEGROUP:
            group = self.ITEMS_FORCEGROUP[item.typeName]
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
            metaGroupName = self.ITEMS_FORCEDMETAGROUP[item.name][0]
            metaGroup = eos.db.getMetaGroup(metaGroupName)
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
            if mgid in self.SHOWN_MARKET_GROUPS:
                return self.getMarketGroup(mgid)
            else:
                return None
        # Check if item itself has market group
        elif item.marketGroupID:
            if item.marketGroupID in self.SHOWN_MARKET_GROUPS:
                return item.marketGroup
            else:
                return None
        elif parentcheck:
            # If item doesn't have marketgroup, check if it has parent
            # item and use its market group
            parent = self.getParentItemByItem(item, selfparent=False)
            if parent and parent.marketGroupID in self.SHOWN_MARKET_GROUPS:
                return parent.marketGroup
            else:
                return None
        else:
            return None

    def getParentItemByItem(self, item, selfparent=True):
        """Get parent item by item"""
        parent = None
        if item.name in self.ITEMS_FORCEDMETAGROUP:
            parentName = self.ITEMS_FORCEDMETAGROUP[item.name][1]
            parent = self.getItem(parentName)
        if parent is None:
            parent = item.varParent
        # Consider self as parent if item has no parent in database
        if parent is None and selfparent is True:
            parent = item
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
            if item.category.ID == 20 and item.group.ID != 303:  # Implants not Boosters
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

        # If the items are boosters then filter variations to only include boosters for the same slot.
        BOOSTER_GROUP_ID = 303
        if all(map(lambda i: i.group.ID == BOOSTER_GROUP_ID, items)) and len(items) > 0:
            # 'boosterness' is the database's attribute name for Booster Slot
            reqSlot = next(items.__iter__()).getAttribute('boosterness')
            # If the item and it's variation both have a marketGroupID it should match for the variation to be considered valid.
            marketGroupID = [next(filter(None, map(lambda i: i.marketGroupID, items)), None), None]
            matchSlotAndMktGrpID = lambda v: v.getAttribute('boosterness') == reqSlot and v.marketGroupID in marketGroupID
            variations_list = list(filter(matchSlotAndMktGrpID, variations_list))

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
        items = set([
            item for item in groupItems
            if self.getPublicityByItem(item) and self.getGroupByItem(item) == group])
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
            # This shouldn't occur normally but makes errors more mild when ITEMS_FORCEDMARKETGROUP is outdated.
            if len(mg.children) > 0 and len(mg.items) == 0:
                pyfalog.error(("Market group \"{0}\" contains no items and has children. "
                    "ITEMS_FORCEDMARKETGROUP is likely outdated and will need to be "
                    "updated for {1} to display correctly.").format(mg, self.ITEMS_FORCEDMARKETGROUP_R[mg.ID]))
                return False
            return True
        elif len(mg.items) > 0 and len(mg.children) == 0:
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
        if mg.iconID:
            return mg.iconID
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

                return item.iconID if getattr(item, "icon", None) else ""
            elif self.getMarketGroupChildren(mg) > 0:
                kids = self.getMarketGroupChildren(mg)
                mktGroups = self.getIconByMarketGroup(kids)
                size = len(mktGroups)
                return mktGroups.pop() if size > 0 else ""
            else:
                return ""

    def getPublicityByItem(self, item):
        """Return if an item is published"""
        if item.typeName in self.ITEMS_FORCEPUBLISHED:
            pub = self.ITEMS_FORCEPUBLISHED[item.typeName]
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
            mg = self.getMarketGroup(id_)
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
                                     eager=("group.category", "metaGroup"))
        ships = set()
        for item in results:
            if self.getPublicityByItem(item):
                ships.add(item)
        return ships

    def searchItems(self, name, callback, filterName=None):
        """Find items according to given text pattern"""
        self.searchWorkerThread.scheduleSearch(name, callback, filterName)

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
        filtered = [item for item in items if self.getMetaGroupIdByItem(item) in metas]
        return filtered

    def getReplacements(self, identity):
        item = self.getItem(identity)
        # We already store needed type IDs in database
        replTypeIDs = {int(i) for i in item.replacements.split(",") if i} if item.replacements is not None else {}
        if not replTypeIDs:
            return ()
        # As replacements were generated without keeping track which items were published,
        # filter them out here
        items = []
        for typeID in replTypeIDs:
            item = self.getItem(typeID)
            if not item:
                continue
            if self.getPublicityByItem(item):
                items.append(item)
        return items

    def getRecentlyUsed(self):
        recentlyUsedItems = []
        for itemID in self.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"]:
            item = self.getItem(itemID)
            if item is None:
                self.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"].remove(itemID)
            recentlyUsedItems.append(item)
        return recentlyUsedItems

    def storeRecentlyUsed(self, itemID):
        recentlyUsedModules = self.serviceMarketRecentlyUsedModules["pyfaMarketRecentlyUsedModules"]
        while itemID in recentlyUsedModules:
            recentlyUsedModules.remove(itemID)
        item = self.getItem(itemID)
        if item.isAbyssal:
            return
        while len(recentlyUsedModules) >= 20:
            recentlyUsedModules.pop(-1)
        recentlyUsedModules.insert(0, itemID)

    def itemSort(self, item, reverseMktGrp=False):
        catname = self.getCategoryByItem(item).name
        try:
            mktgrpid = self.getMarketGroupByItem(item).ID
        except AttributeError:
            mktgrpid = -1
            pyfalog.warning("unable to find market group for {}".format(item.typeName))
        if reverseMktGrp:
            mktgrpid = -mktgrpid
        parentname = self.getParentItemByItem(item).name
        # Get position of market group
        metagrpid = self.getMetaGroupIdByItem(item)
        metatab = self.META_MAP_REVERSE_GROUPED.get(metagrpid)
        metalvl = item.metaLevel or 0
        return catname, mktgrpid, parentname, metatab, metalvl, item.name
