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
import xml.dom
import xml.parsers.expat

from logbook import Logger

from eos.saveddata.cargo import Cargo
from eos.saveddata.citadel import Citadel
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit
from eos.saveddata.module import Module, State, Slot
from eos.saveddata.ship import Ship
from service.fit import Fit as svcFit
from service.market import Market
from utils.strfunctions import sequential_rep, replace_ltgt

from service.port.shared import IPortUser, processing_notify


pyfalog = Logger(__name__)

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


def importXml(text, iportuser):
    from .port import Port
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


def exportXml(iportuser, *fits):
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
            pyfalog.error("Failed on fitID: %d, message: %s" % e.message)
            continue
        finally:
            if iportuser:
                processing_notify(
                    iportuser, IPortUser.PROCESS_EXPORT | IPortUser.ID_UPDATE,
                    (i, "convert to xml (%s/%s) %s" % (i + 1, fit_count, fit.ship.name))
                )
    return doc.toprettyxml()
