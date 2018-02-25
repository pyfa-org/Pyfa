# =============================================================================
# Copyright (C) 2014 Ryan Holmes
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

import re
import os
import xml.dom
from logbook import Logger
import collections
import json
import threading
import locale

from codecs import open

import xml.parsers.expat

from eos import db
from service.fit import Fit as svcFit

# noinspection PyPackageRequirements
import wx

from eos.saveddata.cargo import Cargo
from eos.saveddata.implant import Implant
from eos.saveddata.booster import Booster
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module, State, Slot
from eos.saveddata.ship import Ship
from eos.saveddata.citadel import Citadel
from eos.saveddata.fit import Fit
from service.market import Market
from utils.strfunctions import sequential_rep, replace_ltgt
from abc import ABCMeta, abstractmethod

if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
    from service.crest import Crest

pyfalog = Logger(__name__)

try:
    from collections import OrderedDict
except ImportError:
    from utils.compat import OrderedDict

EFT_SLOT_ORDER = [Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM, Slot.SERVICE]
INV_FLAGS = {
    Slot.LOW: 11,
    Slot.MED: 19,
    Slot.HIGH: 27,
    Slot.RIG: 92,
    Slot.SUBSYSTEM: 125,
    Slot.SERVICE: 164
}

INV_FLAG_CARGOBAY = 5
INV_FLAG_DRONEBAY = 87
INV_FLAG_FIGHTER = 158

# 2017/04/05 NOTE: simple validation, for xml file
RE_XML_START = r'<\?xml\s+version="1.0"\s*\?>'

# -- 170327 Ignored description --
RE_LTGT = "&(lt|gt);"
L_MARK = "&lt;localized hint=&quot;"
# &lt;localized hint=&quot;([^"]+)&quot;&gt;([^\*]+)\*&lt;\/localized&gt;
LOCALIZED_PATTERN = re.compile(r'<localized hint="([^"]+)">([^\*]+)\*</localized>')


def _extract_match(t):
    m = LOCALIZED_PATTERN.match(t)
    # hint attribute, text content
    return m.group(1), m.group(2)


def _resolve_ship(fitting, sMkt, b_localized):
    # type: (xml.dom.minidom.Element, service.market.Market, bool) -> eos.saveddata.fit.Fit
    """ NOTE: Since it is meaningless unless a correct ship object can be constructed,
        process flow changed
    """
    # ------ Confirm ship
    # <localized hint="Maelstrom">Maelstrom</localized>
    shipType = fitting.getElementsByTagName("shipType").item(0).getAttribute("value")
    anything = None
    if b_localized:
        # expect an official name, emergency cache
        shipType, anything = _extract_match(shipType)

    limit = 2
    ship = None
    while True:
        must_retry = False
        try:
            try:
                ship = Ship(sMkt.getItem(shipType))
            except ValueError:
                ship = Citadel(sMkt.getItem(shipType))
        except Exception as e:
            pyfalog.warning("Caught exception on _resolve_ship")
            pyfalog.error(e)
            limit -= 1
            if limit is 0:
                break
            shipType = anything
            must_retry = True
        if not must_retry:
            break

    if ship is None:
        raise Exception("cannot resolve ship type.")

    fitobj = Fit(ship=ship)
    # ------ Confirm fit name
    anything = fitting.getAttribute("name")
    # 2017/03/29 NOTE:
    #    if fit name contained "<" or ">" then reprace to named html entity by EVE client
    # if re.search(RE_LTGT, anything):
    if "&lt;" in anything or "&gt;" in anything:
        anything = replace_ltgt(anything)
    fitobj.name = anything

    return fitobj


def _resolve_module(hardware, sMkt, b_localized):
    # type: (xml.dom.minidom.Element, service.market.Market, bool) -> eos.saveddata.module.Module
    moduleName = hardware.getAttribute("type")
    emergency = None
    if b_localized:
        # expect an official name, emergency cache
        moduleName, emergency = _extract_match(moduleName)

    item = None
    limit = 2
    while True:
        must_retry = False
        try:
            item = sMkt.getItem(moduleName, eager="group.category")
        except Exception as e:
            pyfalog.warning("Caught exception on _resolve_module")
            pyfalog.error(e)
            limit -= 1
            if limit is 0:
                break
            moduleName = emergency
            must_retry = True
        if not must_retry:
            break
    return item


class UserCancelException(Exception):
    """when user cancel on port processing."""
    pass


class IPortUser:

    __metaclass__ = ABCMeta

    ID_PULSE = 1
    # Pulse the progress bar
    ID_UPDATE = ID_PULSE << 1
    # Replace message with data: update messate
    ID_DONE = ID_PULSE << 2
    # open fits: import process done
    ID_ERROR = ID_PULSE << 3
    # display error: raise some error

    PROCESS_IMPORT = ID_PULSE << 4
    # means import process.
    PROCESS_EXPORT = ID_PULSE << 5
    # means import process.

    @abstractmethod
    def on_port_processing(self, action, data=None):
        """
        While importing fits from file, the logic calls back to this function to
        update progress bar to show activity. XML files can contain multiple
        ships with multiple fits, whereas EFT cfg files contain many fits of
        a single ship. When iterating through the files, we update the message
        when we start a new file, and then Pulse the progress bar with every fit
        that is processed.

        action : a flag that lets us know how to deal with :data
                None: Pulse the progress bar
                1: Replace message with data
                other: Close dialog and handle based on :action (-1 open fits, -2 display error)
        """

        """return: True is continue process, False is cancel."""
        pass

    def on_port_process_start(self):
        pass


class Port(object):
    """
    2017/03/31 NOTE: About change
        1. want to keep the description recorded in fit
        2. i think should not write wx.CallAfter in here
    """
    instance = None
    __tag_replace_flag = True

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Port()

        return cls.instance

    @classmethod
    def set_tag_replace(cls, b):
        cls.__tag_replace_flag = b

    @classmethod
    def is_tag_replace(cls):
        # might there is a person who wants to hold tags.
        # (item link in EVE client etc. When importing again to EVE)
        return cls.__tag_replace_flag

    @staticmethod
    def backupFits(path, iportuser):
        pyfalog.debug("Starting backup fits thread.")
#         thread = FitBackupThread(path, callback)
#         thread.start()
        threading.Thread(
            target=PortProcessing.backupFits,
            args=(path, iportuser)
        ).start()

    @staticmethod
    def importFitsThreaded(paths, iportuser):
        # type: (tuple, IPortUser) -> None
        """
        :param paths: fits data file path list.
        :param iportuser:  IPortUser implemented class.
        :rtype: None
        """
        pyfalog.debug("Starting import fits thread.")
#         thread = FitImportThread(paths, iportuser)
#         thread.start()
        threading.Thread(
            target=PortProcessing.importFitsFromFile,
            args=(paths, iportuser)
        ).start()

    @staticmethod
    def importFitFromFiles(paths, iportuser=None):
        """
        Imports fits from file(s). First processes all provided paths and stores
        assembled fits into a list. This allows us to call back to the GUI as
        fits are processed as well as when fits are being saved.
        returns
        """
        defcodepage = locale.getpreferredencoding()
        sFit = svcFit.getInstance()

        fit_list = []
        try:
            for path in paths:
                if iportuser:  # Pulse
                    msg = "Processing file:\n%s" % path
                    pyfalog.debug(msg)
                    PortProcessing.notify(iportuser, IPortUser.PROCESS_IMPORT | IPortUser.ID_UPDATE, msg)
                    # wx.CallAfter(callback, 1, msg)

                with open(path, "r") as file_:
                    srcString = file_.read()

                if len(srcString) == 0:  # ignore blank files
                    pyfalog.debug("File is blank.")
                    continue

                codec_found = None
                # If file had ANSI encoding, decode it to unicode using detection
                # of BOM header or if there is no header try default
                # codepage then fallback to utf-16, cp1252

                if isinstance(srcString, str):
                    savebom = None

                    encoding_map = (
                        ('\xef\xbb\xbf', 'utf-8'),
                        ('\xff\xfe\0\0', 'utf-32'),
                        ('\0\0\xfe\xff', 'UTF-32BE'),
                        ('\xff\xfe', 'utf-16'),
                        ('\xfe\xff', 'UTF-16BE'))

                    for bom, encoding in encoding_map:
                        if srcString.startswith(bom):
                            codec_found = encoding
                            savebom = bom

                    if codec_found is None:
                        pyfalog.info("Unicode BOM not found in file {0}.", path)
                        attempt_codecs = (defcodepage, "utf-8", "utf-16", "cp1252")

                        for page in attempt_codecs:
                            try:
                                pyfalog.info("Attempting to decode file {0} using {1} page.", path, page)
                                srcString = unicode(srcString, page)
                                codec_found = page
                                pyfalog.info("File {0} decoded using {1} page.", path, page)
                            except UnicodeDecodeError:
                                pyfalog.info("Error unicode decoding {0} from page {1}, trying next codec", path, page)
                            else:
                                break
                    else:
                        pyfalog.info("Unicode BOM detected in {0}, using {1} page.", path, codec_found)
                        srcString = unicode(srcString[len(savebom):], codec_found)

                else:
                    # nasty hack to detect other transparent utf-16 loading
                    if srcString[0] == '<' and 'utf-16' in srcString[:128].lower():
                        codec_found = "utf-16"
                    else:
                        codec_found = "utf-8"

                if codec_found is None:
                    return False, "Proper codec could not be established for %s" % path

                try:
                    _, fitsImport = Port.importAuto(srcString, path, iportuser=iportuser, encoding=codec_found)
                    fit_list += fitsImport
                except xml.parsers.expat.ExpatError:
                    pyfalog.warning("Malformed XML in:\n{0}", path)
                    return False, "Malformed XML in %s" % path

            # IDs = []  # NOTE: what use for IDs?
            numFits = len(fit_list)
            for idx, fit in enumerate(fit_list):
                # Set some more fit attributes and save
                fit.character = sFit.character
                fit.damagePattern = sFit.pattern
                fit.targetResists = sFit.targetResists
                db.save(fit)
                # IDs.append(fit.ID)
                if iportuser:  # Pulse
                    pyfalog.debug("Processing complete, saving fits to database: {0}/{1}", idx + 1, numFits)
                    PortProcessing.notify(
                        iportuser, IPortUser.PROCESS_IMPORT | IPortUser.ID_UPDATE,
                        "Processing complete, saving fits to database\n(%d/%d) %s" % (idx + 1, numFits, fit.ship.name)
                    )

        except UserCancelException:
            return False, "Processing has been canceled.\n"
        except Exception as e:
            pyfalog.critical("Unknown exception processing: {0}", path)
            pyfalog.critical(e)
            # TypeError: not all arguments converted during string formatting
#                 return False, "Unknown Error while processing {0}" % path
            return False, "Unknown error while processing %s\n\n Error: %s" % (path, e.message)

        return True, fit_list

    @staticmethod
    def importFitFromBuffer(bufferStr, activeFit=None):
        # type: (basestring, object) -> object
        # TODO: catch the exception?
        # activeFit is reserved?, bufferStr is unicode? (assume only clipboard string?
        sFit = svcFit.getInstance()
        _, fits = Port.importAuto(bufferStr, activeFit=activeFit)
        for fit in fits:
            fit.character = sFit.character
            fit.damagePattern = sFit.pattern
            fit.targetResists = sFit.targetResists
            db.save(fit)
        return fits

    """Service which houses all import/export format functions"""

    @classmethod
    def exportCrest(cls, ofit, callback=None):
        # A few notes:
        # max fit name length is 50 characters
        # Most keys are created simply because they are required, but bogus data is okay

        nested_dict = lambda: collections.defaultdict(nested_dict)
        fit = nested_dict()
        sCrest = Crest.getInstance()
        sFit = svcFit.getInstance()

        eve = sCrest.eve

        # max length is 50 characters
        name = ofit.name[:47] + '...' if len(ofit.name) > 50 else ofit.name
        fit['name'] = name
        fit['ship']['href'] = "%sinventory/types/%d/" % (eve._authed_endpoint, ofit.ship.item.ID)
        fit['ship']['id'] = ofit.ship.item.ID
        fit['ship']['name'] = ''

        # 2017/03/29 NOTE: "<" or "&lt;" is Ignored
        # fit['description'] = "<pyfa:%d />" % ofit.ID
        fit['description'] = ofit.notes[:397] + '...' if len(ofit.notes) > 400 else ofit.notes if ofit.notes is not None else ""
        fit['items'] = []

        slotNum = {}
        charges = {}
        for module in ofit.modules:
            if module.isEmpty:
                continue

            item = nested_dict()
            slot = module.slot

            if slot == Slot.SUBSYSTEM:
                # Order of subsystem matters based on this attr. See GH issue #130
                slot = int(module.getModifiedItemAttr("subSystemSlot"))
                item['flag'] = slot
            else:
                if slot not in slotNum:
                    slotNum[slot] = INV_FLAGS[slot]

                item['flag'] = slotNum[slot]
                slotNum[slot] += 1

            item['quantity'] = 1
            item['type']['href'] = "%sinventory/types/%d/" % (eve._authed_endpoint, module.item.ID)
            item['type']['id'] = module.item.ID
            item['type']['name'] = ''
            fit['items'].append(item)

            if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                if module.chargeID not in charges:
                    charges[module.chargeID] = 0
                # `or 1` because some charges (ie scripts) are without qty
                charges[module.chargeID] += module.numCharges or 1

        for cargo in ofit.cargo:
            item = nested_dict()
            item['flag'] = INV_FLAG_CARGOBAY
            item['quantity'] = cargo.amount
            item['type']['href'] = "%sinventory/types/%d/" % (eve._authed_endpoint, cargo.item.ID)
            item['type']['id'] = cargo.item.ID
            item['type']['name'] = ''
            fit['items'].append(item)

        for chargeID, amount in charges.items():
            item = nested_dict()
            item['flag'] = INV_FLAG_CARGOBAY
            item['quantity'] = amount
            item['type']['href'] = "%sinventory/types/%d/" % (eve._authed_endpoint, chargeID)
            item['type']['id'] = chargeID
            item['type']['name'] = ''
            fit['items'].append(item)

        for drone in ofit.drones:
            item = nested_dict()
            item['flag'] = INV_FLAG_DRONEBAY
            item['quantity'] = drone.amount
            item['type']['href'] = "%sinventory/types/%d/" % (eve._authed_endpoint, drone.item.ID)
            item['type']['id'] = drone.item.ID
            item['type']['name'] = ''
            fit['items'].append(item)

        for fighter in ofit.fighters:
            item = nested_dict()
            item['flag'] = INV_FLAG_FIGHTER
            item['quantity'] = fighter.amountActive
            item['type']['href'] = "%sinventory/types/%d/" % (eve._authed_endpoint, fighter.item.ID)
            item['type']['id'] = fighter.item.ID
            item['type']['name'] = fighter.item.name
            fit['items'].append(item)

        return json.dumps(fit)

    @classmethod
    def importAuto(cls, string, path=None, activeFit=None, iportuser=None, encoding=None):
        # type: (basestring, basestring, object, IPortUser, basestring) -> object
        # Get first line and strip space symbols of it to avoid possible detection errors
        firstLine = re.split("[\n\r]+", string.strip(), maxsplit=1)[0]
        firstLine = firstLine.strip()

        # If XML-style start of tag encountered, detect as XML
        if re.search(RE_XML_START, firstLine):
            if encoding:
                return "XML", cls.importXml(string, iportuser, encoding)
            else:
                return "XML", cls.importXml(string, iportuser)

        # If JSON-style start, parse as CREST/JSON
        if firstLine[0] == '{':
            return "JSON", (cls.importCrest(string),)

        # If we've got source file name which is used to describe ship name
        # and first line contains something like [setup name], detect as eft config file
        if re.match("\[.*\]", firstLine) and path is not None:
            filename = os.path.split(path)[1]
            shipName = filename.rsplit('.')[0]
            return "EFT Config", cls.importEftCfg(shipName, string, iportuser)

        # If no file is specified and there's comma between brackets,
        # consider that we have [ship, setup name] and detect like eft export format
        if re.match("\[.*,.*\]", firstLine):
            return "EFT", (cls.importEft(string),)

        # Use DNA format for all other cases
        return "DNA", (cls.importDna(string),)

    @staticmethod
    def importCrest(str_):

        sMkt = Market.getInstance()
        fitobj = Fit()
        refobj = json.loads(str_)
        items = refobj['items']
        # "<" and ">" is replace to "&lt;", "&gt;" by EVE client
        fitobj.name = refobj['name']
        # 2017/03/29: read description
        fitobj.notes = refobj['description']

        try:
            refobj = refobj['ship']['id']
            try:
                fitobj.ship = Ship(sMkt.getItem(refobj))
            except ValueError:
                fitobj.ship = Citadel(sMkt.getItem(refobj))
        except:
            pyfalog.warning("Caught exception in importCrest")
            return None

        items.sort(key=lambda k: k['flag'])

        moduleList = []
        for module in items:
            try:
                item = sMkt.getItem(module['type']['id'], eager="group.category")
                if module['flag'] == INV_FLAG_DRONEBAY:
                    d = Drone(item)
                    d.amount = module['quantity']
                    fitobj.drones.append(d)
                elif module['flag'] == INV_FLAG_CARGOBAY:
                    c = Cargo(item)
                    c.amount = module['quantity']
                    fitobj.cargo.append(c)
                elif module['flag'] == INV_FLAG_FIGHTER:
                    fighter = Fighter(item)
                    fitobj.fighters.append(fighter)
                else:
                    try:
                        m = Module(item)
                    # When item can't be added to any slot (unknown item or just charge), ignore it
                    except ValueError:
                        pyfalog.debug("Item can't be added to any slot (unknown item or just charge)")
                        continue
                    # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                    if item.category.name == "Subsystem":
                        if m.fits(fitobj):
                            fitobj.modules.append(m)
                    else:
                        if m.isValidState(State.ACTIVE):
                            m.state = State.ACTIVE

                        moduleList.append(m)

            except:
                pyfalog.warning("Could not process module.")
                continue

        # Recalc to get slot numbers correct for T3 cruisers
        svcFit.getInstance().recalc(fitobj)

        for module in moduleList:
            if module.fits(fitobj):
                fitobj.modules.append(module)

        return fitobj

    @staticmethod
    def importDna(string):
        sMkt = Market.getInstance()

        ids = map(int, re.findall(r'\d+', string))
        for id_ in ids:
            try:
                try:
                    try:
                        Ship(sMkt.getItem(sMkt.getItem(id_)))
                    except ValueError:
                        Citadel(sMkt.getItem(sMkt.getItem(id_)))
                except ValueError:
                    Citadel(sMkt.getItem(id_))
                string = string[string.index(str(id_)):]
                break
            except:
                pyfalog.warning("Exception caught in importDna")
                pass
        string = string[:string.index("::") + 2]
        info = string.split(":")

        f = Fit()
        try:
            try:
                f.ship = Ship(sMkt.getItem(int(info[0])))
            except ValueError:
                f.ship = Citadel(sMkt.getItem(int(info[0])))
            f.name = "{0} - DNA Imported".format(f.ship.item.name)
        except UnicodeEncodeError:
            def logtransform(s_):
                if len(s_) > 10:
                    return s_[:10] + "..."
                return s_

            pyfalog.exception("Couldn't import ship data {0}", [logtransform(s) for s in info])
            return None

        moduleList = []
        for itemInfo in info[1:]:
            if itemInfo:
                itemID, amount = itemInfo.split(";")
                item = sMkt.getItem(int(itemID), eager="group.category")

                if item.category.name == "Drone":
                    d = Drone(item)
                    d.amount = int(amount)
                    f.drones.append(d)
                elif item.category.name == "Fighter":
                    ft = Fighter(item)
                    ft.amount = int(amount) if ft.amount <= ft.fighterSquadronMaxSize else ft.fighterSquadronMaxSize
                    if ft.fits(f):
                        f.fighters.append(ft)
                elif item.category.name == "Charge":
                    c = Cargo(item)
                    c.amount = int(amount)
                    f.cargo.append(c)
                else:
                    for i in xrange(int(amount)):
                        try:
                            m = Module(item)
                        except:
                            pyfalog.warning("Exception caught in importDna")
                            continue
                        # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                        if item.category.name == "Subsystem":
                            if m.fits(f):
                                f.modules.append(m)
                        else:
                            m.owner = f
                            if m.isValidState(State.ACTIVE):
                                m.state = State.ACTIVE
                            moduleList.append(m)

        # Recalc to get slot numbers correct for T3 cruisers
        svcFit.getInstance().recalc(f)

        for module in moduleList:
            if module.fits(f):
                module.owner = f
                if module.isValidState(State.ACTIVE):
                    module.state = State.ACTIVE
                f.modules.append(module)

        return f

    @staticmethod
    def importEft(eftString):
        sMkt = Market.getInstance()
        offineSuffix = " /OFFLINE"

        fit = Fit()
        eftString = eftString.strip()
        lines = re.split('[\n\r]+', eftString)
        info = lines[0][1:-1].split(",", 1)

        if len(info) == 2:
            shipType = info[0].strip()
            fitName = info[1].strip()
        else:
            shipType = info[0].strip()
            fitName = "Imported %s" % shipType

        try:
            ship = sMkt.getItem(shipType)
            try:
                fit.ship = Ship(ship)
            except ValueError:
                fit.ship = Citadel(ship)
            fit.name = fitName
        except:
            pyfalog.warning("Exception caught in importEft")
            return

        # maintain map of drones and their quantities
        droneMap = {}
        cargoMap = {}
        moduleList = []
        for i in range(1, len(lines)):
            ammoName = None
            extraAmount = None

            line = lines[i].strip()
            if not line:
                continue

            setOffline = line.endswith(offineSuffix)
            if setOffline is True:
                # remove offline suffix from line
                line = line[:len(line) - len(offineSuffix)]

            modAmmo = line.split(",")
            # matches drone and cargo with x{qty}
            modExtra = modAmmo[0].split(" x")

            if len(modAmmo) == 2:
                # line with a module and ammo
                ammoName = modAmmo[1].strip()
                modName = modAmmo[0].strip()
            elif len(modExtra) == 2:
                # line with drone/cargo and qty
                extraAmount = modExtra[1].strip()
                modName = modExtra[0].strip()
            else:
                # line with just module
                modName = modExtra[0].strip()

            try:
                # get item information. If we are on a Drone/Cargo line, throw out cargo
                item = sMkt.getItem(modName, eager="group.category")
            except:
                # if no data can be found (old names)
                pyfalog.warning("no data can be found (old names)")
                continue

            if item.category.name == "Drone":
                extraAmount = int(extraAmount) if extraAmount is not None else 1
                if modName not in droneMap:
                    droneMap[modName] = 0
                droneMap[modName] += extraAmount
            elif item.category.name == "Fighter":
                extraAmount = int(extraAmount) if extraAmount is not None else 1
                fighterItem = Fighter(item)
                if extraAmount > fighterItem.fighterSquadronMaxSize:  # Amount bigger then max fightergroup size
                    extraAmount = fighterItem.fighterSquadronMaxSize
                if fighterItem.fits(fit):
                    fit.fighters.append(fighterItem)

            if len(modExtra) == 2 and item.category.name != "Drone" and item.category.name != "Fighter":
                extraAmount = int(extraAmount) if extraAmount is not None else 1
                if modName not in cargoMap:
                    cargoMap[modName] = 0
                cargoMap[modName] += extraAmount
            elif item.category.name == "Implant":
                if "implantness" in item.attributes:
                    fit.implants.append(Implant(item))
                elif "boosterness" in item.attributes:
                    fit.boosters.append(Booster(item))
                else:
                    pyfalog.error("Failed to import implant: {0}", line)
            # elif item.category.name == "Subsystem":
            #     try:
            #         subsystem = Module(item)
            #     except ValueError:
            #         continue
            #
            #     if subsystem.fits(fit):
            #         fit.modules.append(subsystem)
            else:
                try:
                    m = Module(item)
                except ValueError:
                    continue
                # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                if item.category.name == "Subsystem":
                    if m.fits(fit):
                        fit.modules.append(m)
                else:
                    if ammoName:
                        try:
                            ammo = sMkt.getItem(ammoName)
                            if m.isValidCharge(ammo) and m.charge is None:
                                m.charge = ammo
                        except:
                            pass

                    if setOffline is True and m.isValidState(State.OFFLINE):
                        m.state = State.OFFLINE
                    elif m.isValidState(State.ACTIVE):
                        m.state = State.ACTIVE

                    moduleList.append(m)

        # Recalc to get slot numbers correct for T3 cruisers
        svcFit.getInstance().recalc(fit)

        for m in moduleList:
            if m.fits(fit):
                m.owner = fit
                if not m.isValidState(m.state):
                    pyfalog.warning("Error: Module {0} cannot have state {1}", m, m.state)

                fit.modules.append(m)

        for droneName in droneMap:
            d = Drone(sMkt.getItem(droneName))
            d.amount = droneMap[droneName]
            fit.drones.append(d)

        for cargoName in cargoMap:
            c = Cargo(sMkt.getItem(cargoName))
            c.amount = cargoMap[cargoName]
            fit.cargo.append(c)

        return fit

    @staticmethod
    def importEftCfg(shipname, contents, iportuser=None):
        """Handle import from EFT config store file"""

        # Check if we have such ship in database, bail if we don't
        sMkt = Market.getInstance()
        try:
            sMkt.getItem(shipname)
        except:
            return []  # empty list is expected

        # If client didn't take care of encoding file contents into Unicode,
        # do it using fallback encoding ourselves
        if isinstance(contents, str):
            contents = unicode(contents, locale.getpreferredencoding())

        fits = []  # List for fits
        fitIndices = []  # List for starting line numbers for each fit
        lines = re.split('[\n\r]+', contents)  # Separate string into lines

        for line in lines:
            # Detect fit header
            if line[:1] == "[" and line[-1:] == "]":
                # Line index where current fit starts
                startPos = lines.index(line)
                fitIndices.append(startPos)

        for i, startPos in enumerate(fitIndices):
            # End position is last file line if we're trying to get it for last fit,
            # or start position of next fit minus 1
            endPos = len(lines) if i == len(fitIndices) - 1 else fitIndices[i + 1]

            # Finally, get lines for current fitting
            fitLines = lines[startPos:endPos]

            try:
                # Create fit object
                fitobj = Fit()
                # Strip square brackets and pull out a fit name
                fitobj.name = fitLines[0][1:-1]
                # Assign ship to fitting
                try:
                    fitobj.ship = Ship(sMkt.getItem(shipname))
                except ValueError:
                    fitobj.ship = Citadel(sMkt.getItem(shipname))

                moduleList = []
                for x in range(1, len(fitLines)):
                    line = fitLines[x]
                    if not line:
                        continue

                    # Parse line into some data we will need
                    misc = re.match("(Drones|Implant|Booster)_(Active|Inactive)=(.+)", line)
                    cargo = re.match("Cargohold=(.+)", line)
                    # 2017/03/27 NOTE: store description from EFT
                    description = re.match("Description=(.+)", line)

                    if misc:
                        entityType = misc.group(1)
                        entityState = misc.group(2)
                        entityData = misc.group(3)
                        if entityType == "Drones":
                            droneData = re.match("(.+),([0-9]+)", entityData)
                            # Get drone name and attempt to detect drone number
                            droneName = droneData.group(1) if droneData else entityData
                            droneAmount = int(droneData.group(2)) if droneData else 1
                            # Bail if we can't get item or it's not from drone category
                            try:
                                droneItem = sMkt.getItem(droneName, eager="group.category")
                            except:
                                pyfalog.warning("Cannot get item.")
                                continue
                            if droneItem.category.name == "Drone":
                                # Add drone to the fitting
                                d = Drone(droneItem)
                                d.amount = droneAmount
                                if entityState == "Active":
                                    d.amountActive = droneAmount
                                elif entityState == "Inactive":
                                    d.amountActive = 0
                                fitobj.drones.append(d)
                            elif droneItem.category.name == "Fighter":  # EFT saves fighter as drones
                                ft = Fighter(droneItem)
                                ft.amount = int(droneAmount) if ft.amount <= ft.fighterSquadronMaxSize else ft.fighterSquadronMaxSize
                                fitobj.fighters.append(ft)
                            else:
                                continue
                        elif entityType == "Implant":
                            # Bail if we can't get item or it's not from implant category
                            try:
                                implantItem = sMkt.getItem(entityData, eager="group.category")
                            except:
                                pyfalog.warning("Cannot get item.")
                                continue
                            if implantItem.category.name != "Implant":
                                continue
                            # Add implant to the fitting
                            imp = Implant(implantItem)
                            if entityState == "Active":
                                imp.active = True
                            elif entityState == "Inactive":
                                imp.active = False
                            fitobj.implants.append(imp)
                        elif entityType == "Booster":
                            # Bail if we can't get item or it's not from implant category
                            try:
                                boosterItem = sMkt.getItem(entityData, eager="group.category")
                            except:
                                pyfalog.warning("Cannot get item.")
                                continue
                            # All boosters have implant category
                            if boosterItem.category.name != "Implant":
                                continue
                            # Add booster to the fitting
                            b = Booster(boosterItem)
                            if entityState == "Active":
                                b.active = True
                            elif entityState == "Inactive":
                                b.active = False
                            fitobj.boosters.append(b)
                    # If we don't have any prefixes, then it's a module
                    elif cargo:
                        cargoData = re.match("(.+),([0-9]+)", cargo.group(1))
                        cargoName = cargoData.group(1) if cargoData else cargo.group(1)
                        cargoAmount = int(cargoData.group(2)) if cargoData else 1
                        # Bail if we can't get item
                        try:
                            item = sMkt.getItem(cargoName)
                        except:
                            pyfalog.warning("Cannot get item.")
                            continue
                        # Add Cargo to the fitting
                        c = Cargo(item)
                        c.amount = cargoAmount
                        fitobj.cargo.append(c)
                    # 2017/03/27 NOTE: store description from EFT
                    elif description:
                        fitobj.notes = description.group(1).replace("|", "\n")
                    else:
                        withCharge = re.match("(.+),(.+)", line)
                        modName = withCharge.group(1) if withCharge else line
                        chargeName = withCharge.group(2) if withCharge else None
                        # If we can't get module item, skip it
                        try:
                            modItem = sMkt.getItem(modName)
                        except:
                            pyfalog.warning("Cannot get item.")
                            continue

                        # Create module
                        m = Module(modItem)

                        # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                        if modItem.category.name == "Subsystem":
                            if m.fits(fitobj):
                                fitobj.modules.append(m)
                        else:
                            m.owner = fitobj
                            # Activate mod if it is activable
                            if m.isValidState(State.ACTIVE):
                                m.state = State.ACTIVE
                            # Add charge to mod if applicable, on any errors just don't add anything
                            if chargeName:
                                try:
                                    chargeItem = sMkt.getItem(chargeName, eager="group.category")
                                    if chargeItem.category.name == "Charge":
                                        m.charge = chargeItem
                                except:
                                    pyfalog.warning("Cannot get item.")
                                    pass
                            # Append module to fit
                            moduleList.append(m)

                # Recalc to get slot numbers correct for T3 cruisers
                svcFit.getInstance().recalc(fitobj)

                for module in moduleList:
                    if module.fits(fitobj):
                        fitobj.modules.append(module)

                # Append fit to list of fits
                fits.append(fitobj)

                if iportuser:  # NOTE: Send current processing status
                    PortProcessing.notify(
                        iportuser, IPortUser.PROCESS_IMPORT | IPortUser.ID_UPDATE,
                        "%s:\n%s" % (fitobj.ship.name, fitobj.name)
                    )

            # Skip fit silently if we get an exception
            except Exception as e:
                pyfalog.error("Caught exception on fit.")
                pyfalog.error(e)
                pass

        return fits

    @staticmethod
    def importXml(text, iportuser=None, encoding="utf-8"):
        # type: (basestring, IPortUser, basestring) -> list[eos.saveddata.fit.Fit]
        sMkt = Market.getInstance()
        doc = xml.dom.minidom.parseString(text.encode(encoding))
        # NOTE:
        #   When L_MARK is included at this point,
        #   Decided to be localized data
        b_localized = L_MARK in text
        fittings = doc.getElementsByTagName("fittings").item(0)
        fittings = fittings.getElementsByTagName("fitting")
        fit_list = []
        failed = 0

        for fitting in fittings:
            try:
                fitobj = _resolve_ship(fitting, sMkt, b_localized)
            except:
                failed += 1
                continue

            # -- 170327 Ignored description --
            # read description from exported xml. (EVE client, EFT)
            description = fitting.getElementsByTagName("description").item(0).getAttribute("value")
            if description is None:
                description = ""
            elif len(description):
                # convert <br> to "\n" and remove html tags.
                if Port.is_tag_replace():
                    description = replace_ltgt(
                        sequential_rep(description, r"<(br|BR)>", "\n", r"<[^<>]+>", "")
                    )
            fitobj.notes = description

            hardwares = fitting.getElementsByTagName("hardware")
            moduleList = []
            for hardware in hardwares:
                try:
                    item = _resolve_module(hardware, sMkt, b_localized)
                    if not item:
                        continue

                    if item.category.name == "Drone":
                        d = Drone(item)
                        d.amount = int(hardware.getAttribute("qty"))
                        fitobj.drones.append(d)
                    elif item.category.name == "Fighter":
                        ft = Fighter(item)
                        ft.amount = int(hardware.getAttribute("qty")) if ft.amount <= ft.fighterSquadronMaxSize else ft.fighterSquadronMaxSize
                        fitobj.fighters.append(ft)
                    elif hardware.getAttribute("slot").lower() == "cargo":
                        # although the eve client only support charges in cargo, third-party programs
                        # may support items or "refits" in cargo. Support these by blindly adding all
                        # cargo, not just charges
                        c = Cargo(item)
                        c.amount = int(hardware.getAttribute("qty"))
                        fitobj.cargo.append(c)
                    else:
                        try:
                            m = Module(item)
                        # When item can't be added to any slot (unknown item or just charge), ignore it
                        except ValueError:
                            pyfalog.warning("item can't be added to any slot (unknown item or just charge), ignore it")
                            continue
                        # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                        if item.category.name == "Subsystem":
                            if m.fits(fitobj):
                                m.owner = fitobj
                                fitobj.modules.append(m)
                        else:
                            if m.isValidState(State.ACTIVE):
                                m.state = State.ACTIVE

                            moduleList.append(m)

                except KeyboardInterrupt:
                    pyfalog.warning("Keyboard Interrupt")
                    continue

            # Recalc to get slot numbers correct for T3 cruisers
            svcFit.getInstance().recalc(fitobj)

            for module in moduleList:
                if module.fits(fitobj):
                    module.owner = fitobj
                    fitobj.modules.append(module)

            fit_list.append(fitobj)
            if iportuser:  # NOTE: Send current processing status
                PortProcessing.notify(
                    iportuser, IPortUser.PROCESS_IMPORT | IPortUser.ID_UPDATE,
                    "Processing %s\n%s" % (fitobj.ship.name, fitobj.name)
                )

        return fit_list

    @staticmethod
    def _exportEftBase(fit):
        """Basically EFT format does not require blank lines
            also, it's OK to arrange modules randomly?
        """
        offineSuffix = " /OFFLINE"
        export = u"[%s, %s]\n" % (fit.ship.item.name, fit.name)
        stuff = {}
        sFit = svcFit.getInstance()
        for module in fit.modules:
            slot = module.slot
            if slot not in stuff:
                stuff[slot] = []
            curr = module.item.name if module.item \
                else ("[Empty %s slot]" % Slot.getName(slot).capitalize() if slot is not None else "")
            if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                curr += ", %s" % module.charge.name
            if module.state == State.OFFLINE:
                curr += offineSuffix
            curr += "\n"
            stuff[slot].append(curr)

        for slotType in EFT_SLOT_ORDER:
            data = stuff.get(slotType)
            if data is not None:
                export += "\n"
                for curr in data:
                    export += curr

        if len(fit.drones) > 0:
            export += "\n\n"
            for drone in fit.drones:
                export += "%s x%s\n" % (drone.item.name, drone.amount)

        if len(fit.fighters) > 0:
            export += "\n\n"
            for fighter in fit.fighters:
                export += "%s x%s\n" % (fighter.item.name, fighter.amountActive)

        if export[-1] == "\n":
            export = export[:-1]

        return export

    @classmethod
    def exportEft(cls, fit):
        export = cls._exportEftBase(fit)

        if len(fit.cargo) > 0:
            export += "\n\n\n"
            for cargo in fit.cargo:
                export += "%s x%s\n" % (cargo.item.name, cargo.amount)
        if export[-1] == "\n":
            export = export[:-1]

        return export

    @classmethod
    def exportEftImps(cls, fit):
        export = cls._exportEftBase(fit)

        if len(fit.implants) > 0 or len(fit.boosters) > 0:
            export += "\n\n\n"
            for implant in fit.implants:
                export += "%s\n" % implant.item.name
            for booster in fit.boosters:
                export += "%s\n" % booster.item.name

        if export[-1] == "\n":
            export = export[:-1]

        if len(fit.cargo) > 0:
            export += "\n\n\n"
            for cargo in fit.cargo:
                export += "%s x%s\n" % (cargo.item.name, cargo.amount)
        if export[-1] == "\n":
            export = export[:-1]

        return export

    @staticmethod
    def exportDna(fit):
        dna = str(fit.shipID)
        subsystems = []  # EVE cares which order you put these in
        mods = OrderedDict()
        charges = OrderedDict()
        sFit = svcFit.getInstance()
        for mod in fit.modules:
            if not mod.isEmpty:
                if mod.slot == Slot.SUBSYSTEM:
                    subsystems.append(mod)
                    continue
                if mod.itemID not in mods:
                    mods[mod.itemID] = 0
                mods[mod.itemID] += 1

                if mod.charge and sFit.serviceFittingOptions["exportCharges"]:
                    if mod.chargeID not in charges:
                        charges[mod.chargeID] = 0
                    # `or 1` because some charges (ie scripts) are without qty
                    charges[mod.chargeID] += mod.numCharges or 1

        for subsystem in sorted(subsystems, key=lambda mod_: mod_.getModifiedItemAttr("subSystemSlot")):
            dna += ":{0};1".format(subsystem.itemID)

        for mod in mods:
            dna += ":{0};{1}".format(mod, mods[mod])

        for drone in fit.drones:
            dna += ":{0};{1}".format(drone.itemID, drone.amount)

        for fighter in fit.fighters:
            dna += ":{0};{1}".format(fighter.itemID, fighter.amountActive)

        for fighter in fit.fighters:
            dna += ":{0};{1}".format(fighter.itemID, fighter.amountActive)

        for cargo in fit.cargo:
            # DNA format is a simple/dumb format. As CCP uses the slot information of the item itself
            # without designating slots in the DNA standard, we need to make sure we only include
            # charges in the DNA export. If modules were included, the EVE Client will interpret these
            # as being "Fitted" to whatever slot they are for, and it causes an corruption error in the
            # client when trying to save the fit
            if cargo.item.category.name == "Charge":
                if cargo.item.ID not in charges:
                    charges[cargo.item.ID] = 0
                charges[cargo.item.ID] += cargo.amount

        for charge in charges:
            dna += ":{0};{1}".format(charge, charges[charge])

        return dna + "::"

    @staticmethod
    def exportXml(iportuser=None, *fits):
        doc = xml.dom.minidom.Document()
        fittings = doc.createElement("fittings")
        # fit count
        fit_count = len(fits)
        fittings.setAttribute("count", "%s" % fit_count)
        doc.appendChild(fittings)
        sFit = svcFit.getInstance()

        for i, fit in enumerate(fits):
            try:
                fitting = doc.createElement("fitting")
                fitting.setAttribute("name", fit.name)
                fittings.appendChild(fitting)
                description = doc.createElement("description")
                # -- 170327 Ignored description --
                try:
                    notes = fit.notes  # unicode

                    if notes:
                        notes = notes[:397] + '...' if len(notes) > 400 else notes

                    description.setAttribute(
                        "value", re.sub("(\r|\n|\r\n)+", "<br>", notes) if notes is not None else ""
                    )
                except Exception as e:
                    pyfalog.warning("read description is failed, msg=%s\n" % e.args)

                fitting.appendChild(description)
                shipType = doc.createElement("shipType")
                shipType.setAttribute("value", fit.ship.name)
                fitting.appendChild(shipType)

                charges = {}
                slotNum = {}
                for module in fit.modules:
                    if module.isEmpty:
                        continue

                    slot = module.slot

                    if slot == Slot.SUBSYSTEM:
                        # Order of subsystem matters based on this attr. See GH issue #130
                        slotId = module.getModifiedItemAttr("subSystemSlot") - 125
                    else:
                        if slot not in slotNum:
                            slotNum[slot] = 0

                        slotId = slotNum[slot]
                        slotNum[slot] += 1

                    hardware = doc.createElement("hardware")
                    hardware.setAttribute("type", module.item.name)
                    slotName = Slot.getName(slot).lower()
                    slotName = slotName if slotName != "high" else "hi"
                    hardware.setAttribute("slot", "%s slot %d" % (slotName, slotId))
                    fitting.appendChild(hardware)

                    if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                        if module.charge.name not in charges:
                            charges[module.charge.name] = 0
                        # `or 1` because some charges (ie scripts) are without qty
                        charges[module.charge.name] += module.numCharges or 1

                for drone in fit.drones:
                    hardware = doc.createElement("hardware")
                    hardware.setAttribute("qty", "%d" % drone.amount)
                    hardware.setAttribute("slot", "drone bay")
                    hardware.setAttribute("type", drone.item.name)
                    fitting.appendChild(hardware)

                for fighter in fit.fighters:
                    hardware = doc.createElement("hardware")
                    hardware.setAttribute("qty", "%d" % fighter.amountActive)
                    hardware.setAttribute("slot", "fighter bay")
                    hardware.setAttribute("type", fighter.item.name)
                    fitting.appendChild(hardware)

                for cargo in fit.cargo:
                    if cargo.item.name not in charges:
                        charges[cargo.item.name] = 0
                    charges[cargo.item.name] += cargo.amount

                for name, qty in charges.items():
                    hardware = doc.createElement("hardware")
                    hardware.setAttribute("qty", "%d" % qty)
                    hardware.setAttribute("slot", "cargo")
                    hardware.setAttribute("type", name)
                    fitting.appendChild(hardware)
            except Exception as e:
                # print("Failed on fitID: %d" % fit.ID)
                pyfalog.error("Failed on fitID: %d, message: %s" % e.message)
                continue
            finally:
                if iportuser:
                    PortProcessing.notify(
                        iportuser, IPortUser.PROCESS_EXPORT | IPortUser.ID_UPDATE,
                        (i, "convert to xml (%s/%s) %s" % (i + 1, fit_count, fit.ship.name))
                    )
#                     wx.CallAfter(callback, i, "(%s/%s) %s" % (i, fit_count, fit.ship.name))

        return doc.toprettyxml()

    @staticmethod
    def exportMultiBuy(fit):
        export = "%s\n" % fit.ship.item.name
        stuff = {}
        sFit = svcFit.getInstance()
        for module in fit.modules:
            slot = module.slot
            if slot not in stuff:
                stuff[slot] = []
            curr = "%s\n" % module.item.name if module.item else ""
            if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                curr += "%s x%s\n" % (module.charge.name, module.numCharges)
            stuff[slot].append(curr)

        for slotType in EFT_SLOT_ORDER:
            data = stuff.get(slotType)
            if data is not None:
                # export += "\n"
                for curr in data:
                    export += curr

        if len(fit.drones) > 0:
            for drone in fit.drones:
                export += "%s x%s\n" % (drone.item.name, drone.amount)

        if len(fit.cargo) > 0:
            for cargo in fit.cargo:
                export += "%s x%s\n" % (cargo.item.name, cargo.amount)

        if len(fit.implants) > 0:
            for implant in fit.implants:
                export += "%s\n" % implant.item.name

        if len(fit.boosters) > 0:
            for booster in fit.boosters:
                export += "%s\n" % booster.item.name

        if len(fit.fighters) > 0:
            for fighter in fit.fighters:
                export += "%s x%s\n" % (fighter.item.name, fighter.amountActive)

        if export[-1] == "\n":
            export = export[:-1]

        return export


class PortProcessing(object):
    """Port Processing class """
    @staticmethod
    def backupFits(path, iportuser):
        success = True
        try:
            iportuser.on_port_process_start()
            backedUpFits = Port.exportXml(iportuser, *svcFit.getInstance().getAllFits())
            backupFile = open(path, "w", encoding="utf-8")
            backupFile.write(backedUpFits)
            backupFile.close()
        except UserCancelException:
            success = False
        # Send done signal to GUI
#         wx.CallAfter(callback, -1, "Done.")
        flag = IPortUser.ID_ERROR if not success else IPortUser.ID_DONE
        iportuser.on_port_processing(IPortUser.PROCESS_EXPORT | flag,
                                   "User canceled or some error occurrence." if not success else "Done.")

    @staticmethod
    def importFitsFromFile(paths, iportuser):
        iportuser.on_port_process_start()
        success, result = Port.importFitFromFiles(paths, iportuser)
        flag = IPortUser.ID_ERROR if not success else IPortUser.ID_DONE
        iportuser.on_port_processing(IPortUser.PROCESS_IMPORT | flag, result)

    @staticmethod
    def notify(iportuser, flag, data):
        if not iportuser.on_port_processing(flag, data):
            raise UserCancelException
