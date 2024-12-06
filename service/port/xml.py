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
from xml.dom import minidom
# import xml.parsers.expat

from logbook import Logger

from eos.const import FittingModuleState, FittingSlot
from eos.db import getDynamicItem
from eos.saveddata.cargo import Cargo
from eos.saveddata.citadel import Citadel
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship
from gui.fitCommands.helpers import activeStateLimit
from service.fit import Fit as svcFit
from service.market import Market
from service.port.muta import renderMutantAttrs, parseMutantAttrs
from service.port.shared import fetchItem
from html import unescape
from utils.strfunctions import sequential_rep
from config import EVE_FIT_NOTE_MAX

from eos.gamedata import Item # for type annotation
# NOTE: I want to define an interface in the utils package and reference it (IProgress)
# gui.utils.progressHelper.ProgressHelper inherits utils.IProgress
from gui.utils.progressHelper import ProgressHelper # for type annotation


pyfalog = Logger(__name__)

# -- 170327 Ignored description --
L_MARK = "&lt;localized hint=&quot;"
# &lt;localized hint=&quot;([^"]+)&quot;&gt;([^\*]+)\*&lt;\/localized&gt;
LOCALIZED_PATTERN = re.compile(r'<localized hint="([^"*]+)\*?">([^*]+)\*?</localized>')
class ExtractingError(Exception):
    pass

def _extract_match(t):
    # type: (str) -> tuple[str, str]
    m = LOCALIZED_PATTERN.match(t)
    if m is None:
        raise ExtractingError
    # hint attribute, text content
    return m.group(1), m.group(2)

def doIt(text, b_localized):
    # type: (str, bool) -> tuple[str, str|None]
    altText = None
    if b_localized:
        try:
            # expect an official name, emergency cache
            text, altText = _extract_match(text)
        except ExtractingError:
            pass

    return text, altText

def _solve(name, altName, handler):
    # type: (str, str|None, function) -> any # enable inferer
    limit = 2
    subject = None
    while True:
        must_retry = False
        try:
            subject = handler(name)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            # pyfalog.warning("Caught exception on _solve")
            pyfalog.error("Caught exception on _solve:: {}", e)
            limit -= 1
            if limit == 0:
                break
            name = altName
            must_retry = True
        if not must_retry:
            break

    return subject

def _solve_ship(fitting, sMkt, b_localized):
    # type: (minidom.Element, Market, bool) -> Fit
    """ NOTE: Since it is meaningless unless a correct ship object can be constructed,
        process flow changed
    """
    def handler(name):
        # type: (str) -> Ship
        item = sMkt.getItem(name)
        try:
            return Ship(item)
        except ValueError:
            return Citadel(item)

    # ------ Confirm ship
    # <localized hint="Maelstrom">Maelstrom</localized>
    shipType, anything = doIt(
        fitting.getElementsByTagName("shipType")[0].getAttribute("value"), b_localized
    )
    ship = _solve(shipType, anything, handler) # type: Ship

    if ship is None:
        raise Exception(
            f"cannot solve ship type, name: '{shipType}', altName: '{anything}'"
        )

    fitobj = Fit(ship=ship)
    # ------ Confirm fit name
    anything = fitting.getAttribute("name")
    # 2017/03/29 NOTE:
    #    if fit name contained "<" or ">" then replace to named html entity by EVE client
    if re.search(f"&(lt|gt);", anything):
        anything = unescape(anything)
    fitobj.name = anything

    return fitobj


def _solve_module(hardware, sMkt, b_localized):
    # type: (minidom.Element, Market, bool) -> tuple[Item, Item|None, dict[int, float]|None]
    def handler(name):
        # type: (str) -> Item
        mod = sMkt.getItem(name, eager="group.category")
        if not mod:
            raise ValueError(f'"{name}" is not valid')
        pyfalog.info('_solve_module - sMkt.getItem: {}', mod)
        return mod

    moduleName, emergency = doIt(
        hardware.getAttribute("base_type") or hardware.getAttribute("type"), b_localized
    )
    item = _solve(moduleName, emergency, handler)
    if item is None:
        raise Exception(
            f"cannot solve module, name: '{moduleName}', altName: '{emergency}'"
        )

    mutaplasmidName = hardware.getAttribute("mutaplasmid")
    mutaplasmidItem = fetchItem(mutaplasmidName) if mutaplasmidName else None

    mutatedAttrsText = hardware.getAttribute("mutated_attrs")
    mutatedAttrs = parseMutantAttrs(mutatedAttrsText) if mutatedAttrsText else None

    return item, mutaplasmidItem, mutatedAttrs


def importXml(text, progress, path="---"):
    # type: (str, ProgressHelper, str) -> list[Fit]
    from .port import Port
    import os.path
    sMkt = Market.getInstance()

    # NOTE:
    #   When L_MARK is included at this point,
    #   Decided to be localized data
    b_localized = L_MARK in text
    fittings = minidom.parseString(text).getElementsByTagName("fitting")
    fit_list = [] # type: list[Fit]
    failed = 0

    pyfalog.info(
        f"importXml - fitting is {'localized' if b_localized else 'normally'}"
    )

    if progress:
        progress.setRange(fittings.length)
        progress.current = 0
        path = os.path.basename(path)
    for idx, fitting in enumerate(fittings):
        if progress and progress.userCancelled:
            return []

        try:
            fitobj = _solve_ship(fitting, sMkt, b_localized)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            failed += 1
            continue

        if progress:
            currentIdx = idx + 1
            if (currentIdx < fittings.length):
                progress.current = currentIdx
            # progress.message = "Processing %s\n%s" % (fitobj.ship.name, fitobj.name)
            progress.message = f"""Processing file: {path}
  current  - {fitobj.ship.name}
  fit name - {fitobj.name}
"""
        # -- 170327 Ignored description --
        # read description from exported xml. (EVE client, EFT)
        description = fitting.getElementsByTagName("description")[0].getAttribute("value")
        if description is None:
            description = ""
        elif len(description):
            # convert <br> to "\n" and remove html tags.
            if Port.is_tag_replace():
                description = unescape(
                    sequential_rep(description, r"<(br|BR)>", "\n", r"<[^<>]+>", "")
                )
        fitobj.notes = description

        hardwares = fitting.getElementsByTagName("hardware")
        # Sorting by "slot" attr is cool
        hardwares.sort(key=lambda e: e.getAttribute("slot"))
        moduleList = [] # type: list[Module]
        for hardware in hardwares:
            try:
                item, mutaItem, mutaAttrs = _solve_module(hardware, sMkt, b_localized)
                if not item or not item.published:
                    continue

                if item.category.name == "Drone":
                    d = None
                    if mutaItem:
                        mutaplasmid = getDynamicItem(mutaItem.ID)
                        if mutaplasmid:
                            try:
                                d = Drone(mutaplasmid.resultingItem, item, mutaplasmid)
                            except ValueError:
                                pass
                            else:
                                for attrID, mutator in d.mutators.items():
                                    if attrID in mutaAttrs:
                                        mutator.value = mutaAttrs[attrID]
                    if d is None:
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
                    m = None # type: Module
                    try:
                        if mutaItem:
                            mutaplasmid = getDynamicItem(mutaItem.ID)
                            if mutaplasmid:
                                try:
                                    m = Module(mutaplasmid.resultingItem, item, mutaplasmid)
                                except ValueError:
                                    pass
                                else:
                                    for attrID, mutator in m.mutators.items():
                                        if attrID in mutaAttrs:
                                            mutator.value = mutaAttrs[attrID]
                        if m is None:
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
                        if m.isValidState(FittingModuleState.ACTIVE):
                            m.state = activeStateLimit(m.item)

                        moduleList.append(m)

            except KeyboardInterrupt:
                pyfalog.warning("Keyboard Interrupt")
                continue

        # Recalc to get slot numbers correct for T3 cruisers
        sFit = svcFit.getInstance()
        sFit.recalc(fitobj)
        sFit.fill(fitobj)

        for module in moduleList:
            if module.fits(fitobj):
                module.owner = fitobj
                fitobj.modules.append(module)

        fit_list.append(fitobj)

    pyfalog.info(f"importXml - stats of parse, succeeded: {fittings.length - failed}, failed: {failed}")

    return fit_list

def exportXml(fits, progress, callback):
    # type: (list[Fit], ProgressHelper, function) -> str|None
    doc = minidom.Document()
    fittings = doc.createElement("fittings")
    # fit count
    fit_count = len(fits)
    fittings.setAttribute("count", str(fit_count))
    doc.appendChild(fittings)

    def addMutantAttributes(node, mutant):
        node.setAttribute("base_type", mutant.baseItem.name)
        node.setAttribute("mutaplasmid", mutant.mutaplasmid.item.name)
        node.setAttribute("mutated_attrs", renderMutantAttrs(mutant))

    for i, fit in enumerate(fits):
        if progress:
            if progress.userCancelled:
                return None
            processedFits = i + 1
            progress.current = processedFits
            progress.message = f"converting to xml ({processedFits}/{fit_count}) {fit.ship.name}"
        
        try:
            fitting = doc.createElement("fitting")
            fitting.setAttribute("name", fit.name)
            fittings.appendChild(fitting)
            description = doc.createElement("description")
            # -- 170327 Ignored description --
            try:
                notes = re.sub(r"(\r|\n|\r\n)", "<br>", fit.notes or "")
                if len(notes) > EVE_FIT_NOTE_MAX:
                    notes = notes[:EVE_FIT_NOTE_MAX - 3] + '...'
                description.setAttribute("value", notes)
            except (KeyboardInterrupt, SystemExit):
                raise
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

                if slot == FittingSlot.SUBSYSTEM:
                    # Order of subsystem matters based on this attr. See GH issue #130
                    slotId = module.getModifiedItemAttr("subSystemSlot") - 125
                else:
                    if slot not in slotNum:
                        slotNum[slot] = 0

                    slotId = slotNum[slot]
                    slotNum[slot] += 1

                hardware = doc.createElement("hardware")
                hardware.setAttribute("type", module.item.name)
                slotName = FittingSlot(slot).name.lower()
                slotName = slotName if slotName != "high" else "hi"
                hardware.setAttribute("slot", f"{slotName} slot {slotId}")
                if module.isMutated:
                    addMutantAttributes(hardware, module)

                fitting.appendChild(hardware)

                if module.charge:
                    if module.charge.name not in charges:
                        charges[module.charge.name] = 0
                    # `or 1` because some charges (ie scripts) are without qty
                    charges[module.charge.name] += module.numCharges or 1

            for drone in fit.drones:
                hardware = doc.createElement("hardware")
                hardware.setAttribute("qty", "%d" % drone.amount)
                hardware.setAttribute("slot", "drone bay")
                hardware.setAttribute("type", drone.item.name)
                if drone.isMutated:
                    addMutantAttributes(hardware, drone)

                fitting.appendChild(hardware)

            for fighter in fit.fighters:
                hardware = doc.createElement("hardware")
                hardware.setAttribute("qty", "%d" % fighter.amount)
                hardware.setAttribute("slot", "fighter bay")
                hardware.setAttribute("type", fighter.item.name)
                fitting.appendChild(hardware)

            for cargo in fit.cargo:
                if cargo.item.name not in charges:
                    charges[cargo.item.name] = 0
                charges[cargo.item.name] += cargo.amount

            for name, qty in charges.items():
                hardware = doc.createElement("hardware")
                hardware.setAttribute("qty", str(qty))
                hardware.setAttribute("slot", "cargo")
                hardware.setAttribute("type", name)
                fitting.appendChild(hardware)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            pyfalog.error(f"Failed on fitID: {fit.ship.ID}, message: {e}")
            continue
    text = doc.toprettyxml()

    if callback:
        callback(text)
    else:
        return text
