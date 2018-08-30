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
from bs4 import UnicodeDammit


from codecs import open

import xml.parsers.expat

from eos import db
from service.fit import Fit as svcFit

# noinspection PyPackageRequirements
import wx

from eos.saveddata.cargo import Cargo
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module, State, Slot
from eos.saveddata.ship import Ship
from eos.saveddata.citadel import Citadel
from eos.saveddata.fit import Fit, ImplantLocation
from service.market import Market
from utils.strfunctions import sequential_rep, replace_ltgt

from service.esi import Esi
from service.port.dna import exportDna, importDna
from service.port.eft import EftPort, SLOT_ORDER as EFT_SLOT_ORDER
from service.port.shared import IPortUser, UserCancelException, processing_notify


class ESIExportException(Exception):
    pass


pyfalog = Logger(__name__)

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


class Port(object):
    """Service which houses all import/export format functions"""
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

        def backupFitsWorkerFunc(path, iportuser):
            success = True
            try:
                iportuser.on_port_process_start()
                backedUpFits = Port.exportXml(iportuser,
                                              *svcFit.getInstance().getAllFits())
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

        threading.Thread(
            target=backupFitsWorkerFunc,
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

        def importFitsFromFileWorkerFunc(paths, iportuser):
            iportuser.on_port_process_start()
            success, result = Port.importFitFromFiles(paths, iportuser)
            flag = IPortUser.ID_ERROR if not success else IPortUser.ID_DONE
            iportuser.on_port_processing(IPortUser.PROCESS_IMPORT | flag, result)

        threading.Thread(
            target=importFitsFromFileWorkerFunc,
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

        sFit = svcFit.getInstance()

        fit_list = []
        try:
            for path in paths:
                if iportuser:  # Pulse
                    msg = "Processing file:\n%s" % path
                    pyfalog.debug(msg)
                    processing_notify(iportuser, IPortUser.PROCESS_IMPORT | IPortUser.ID_UPDATE, msg)
                    # wx.CallAfter(callback, 1, msg)

                with open(path, "rb") as file_:
                    srcString = file_.read()
                    dammit = UnicodeDammit(srcString)
                    srcString = dammit.unicode_markup

                if len(srcString) == 0:  # ignore blank files
                    pyfalog.debug("File is blank.")
                    continue

                try:
                    _, fitsImport = Port.importAuto(srcString, path, iportuser=iportuser)
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
                if len(fit.implants) > 0:
                    fit.implantLocation = ImplantLocation.FIT
                else:
                    useCharImplants = sFit.serviceFittingOptions["useCharacterImplantsByDefault"]
                    fit.implantLocation = ImplantLocation.CHARACTER if useCharImplants else ImplantLocation.FIT
                db.save(fit)
                # IDs.append(fit.ID)
                if iportuser:  # Pulse
                    pyfalog.debug("Processing complete, saving fits to database: {0}/{1}", idx + 1, numFits)
                    processing_notify(
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
            if len(fit.implants) > 0:
                fit.implantLocation = ImplantLocation.FIT
            else:
                useCharImplants = sFit.serviceFittingOptions["useCharacterImplantsByDefault"]
                fit.implantLocation = ImplantLocation.CHARACTER if useCharImplants else ImplantLocation.FIT
            db.save(fit)
        return fits

    @classmethod
    def exportESI(cls, ofit, callback=None):
        # A few notes:
        # max fit name length is 50 characters
        # Most keys are created simply because they are required, but bogus data is okay

        nested_dict = lambda: collections.defaultdict(nested_dict)
        fit = nested_dict()
        sFit = svcFit.getInstance()

        # max length is 50 characters
        name = ofit.name[:47] + '...' if len(ofit.name) > 50 else ofit.name
        fit['name'] = name
        fit['ship_type_id'] = ofit.ship.item.ID

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
            item['type_id'] = module.item.ID
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
            item['type_id'] = cargo.item.ID
            fit['items'].append(item)

        for chargeID, amount in list(charges.items()):
            item = nested_dict()
            item['flag'] = INV_FLAG_CARGOBAY
            item['quantity'] = amount
            item['type_id'] = chargeID
            fit['items'].append(item)

        for drone in ofit.drones:
            item = nested_dict()
            item['flag'] = INV_FLAG_DRONEBAY
            item['quantity'] = drone.amount
            item['type_id'] = drone.item.ID
            fit['items'].append(item)

        for fighter in ofit.fighters:
            item = nested_dict()
            item['flag'] = INV_FLAG_FIGHTER
            item['quantity'] = fighter.amountActive
            item['type_id'] = fighter.item.ID
            fit['items'].append(item)

        if len(fit['items']) == 0:
            raise ESIExportException("Cannot export fitting: module list cannot be empty.")

        return json.dumps(fit)

    @classmethod
    def importAuto(cls, string, path=None, activeFit=None, iportuser=None):
        # type: (basestring, basestring, object, IPortUser, basestring) -> object
        # Get first line and strip space symbols of it to avoid possible detection errors
        firstLine = re.split("[\n\r]+", string.strip(), maxsplit=1)[0]
        firstLine = firstLine.strip()

        # If XML-style start of tag encountered, detect as XML
        if re.search(RE_XML_START, firstLine):
            return "XML", cls.importXml(string, iportuser)

        # If JSON-style start, parse as CREST/JSON
        if firstLine[0] == '{':
            return "JSON", (cls.importESI(string),)

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
    def importESI(str_):

        sMkt = Market.getInstance()
        fitobj = Fit()
        refobj = json.loads(str_)
        items = refobj['items']
        # "<" and ">" is replace to "&lt;", "&gt;" by EVE client
        fitobj.name = refobj['name']
        # 2017/03/29: read description
        fitobj.notes = refobj['description']

        try:
            ship = refobj['ship_type_id']
            try:
                fitobj.ship = Ship(sMkt.getItem(ship))
            except ValueError:
                fitobj.ship = Citadel(sMkt.getItem(ship))
        except:
            pyfalog.warning("Caught exception in importESI")
            return None

        items.sort(key=lambda k: k['flag'])

        moduleList = []
        for module in items:
            try:
                item = sMkt.getItem(module['type_id'], eager="group.category")
                if not item.published:
                    continue
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
    def importXml(text, iportuser=None):
        # type: (str, IPortUser) -> list[eos.saveddata.fit.Fit]
        sMkt = Market.getInstance()
        doc = xml.dom.minidom.parseString(text)
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
                    if not item or not item.published:
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
                processing_notify(
                    iportuser, IPortUser.PROCESS_IMPORT | IPortUser.ID_UPDATE,
                    "Processing %s\n%s" % (fitobj.ship.name, fitobj.name)
                )

        return fit_list

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

                for name, qty in list(charges.items()):
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
                    processing_notify(
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

    # EFT-related methods
    @staticmethod
    def importEft(eftString):
        return EftPort.importEft(eftString)

    @staticmethod
    def importEftCfg(shipname, contents, iportuser=None):
        return EftPort.importEftCfg(shipname, contents, iportuser)

    @classmethod
    def exportEft(cls, fit, options):
        return EftPort.exportEft(fit, options)

    # DNA-related methods
    @staticmethod
    def importDna(string):
        return importDna(string)

    @staticmethod
    def exportDna(fit):
        return exportDna(fit)
