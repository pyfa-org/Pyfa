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

from logbook import Logger

from eos.db.gamedata.queries import getAttributeInfo, getDynamicItem
from eos.saveddata.cargo import Cargo
from eos.saveddata.citadel import Citadel
from eos.saveddata.booster import Booster
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.implant import Implant
from eos.saveddata.module import Module, State, Slot
from eos.saveddata.ship import Ship
from eos.saveddata.fit import Fit
from gui.utils.numberFormatter import roundToPrec
from service.fit import Fit as svcFit
from service.market import Market
from service.port.shared import IPortUser, processing_notify
from enum import Enum


pyfalog = Logger(__name__)


class Options(Enum):
    IMPLANTS = 1
    MUTATIONS = 2


MODULE_CATS = ('Module', 'Subsystem', 'Structure Module')
SLOT_ORDER = (Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM, Slot.SERVICE)
OFFLINE_SUFFIX = '/OFFLINE'

EFT_OPTIONS = {
    Options.IMPLANTS.value: {
        "name": "Implants",
        "description": "Exports implants"
    },
    Options.MUTATIONS.value: {
        "name": "Mutated Attributes",
        "description": "Exports Abyssal stats"
    }
}


def exportEft(fit, options):
    # EFT formatted export is split in several sections, each section is
    # separated from another using 2 blank lines. Sections might have several
    # sub-sections, which are separated by 1 blank line
    sections = []

    header = '[{}, {}]'.format(fit.ship.item.name, fit.name)

    # Section 1: modules, rigs, subsystems, services
    modsBySlotType = {}
    sFit = svcFit.getInstance()
    for module in fit.modules:
        modsBySlotType.setdefault(module.slot, []).append(module)
    modSection = []

    mutants = {}  # Format: {reference number: module}
    mutantReference = 1
    for slotType in SLOT_ORDER:
        rackLines = []
        modules = modsBySlotType.get(slotType, ())
        for module in modules:
            if module.item:
                mutated = bool(module.mutators)
                # if module was mutated, use base item name for export
                if mutated:
                    modName = module.baseItem.name
                else:
                    modName = module.item.name
                if mutated and options & Options.MUTATIONS.value:
                    mutants[mutantReference] = module
                    mutationSuffix = ' [{}]'.format(mutantReference)
                    mutantReference += 1
                else:
                    mutationSuffix = ''
                modOfflineSuffix = ' {}'.format(OFFLINE_SUFFIX) if module.state == State.OFFLINE else ''
                if module.charge and sFit.serviceFittingOptions['exportCharges']:
                    rackLines.append('{}, {}{}{}'.format(
                        modName, module.charge.name, modOfflineSuffix, mutationSuffix))
                else:
                    rackLines.append('{}{}{}'.format(modName, modOfflineSuffix, mutationSuffix))
            else:
                rackLines.append('[Empty {} slot]'.format(
                    Slot.getName(slotType).capitalize() if slotType is not None else ''))
        if rackLines:
            modSection.append('\n'.join(rackLines))
    if modSection:
        sections.append('\n\n'.join(modSection))

    # Section 2: drones, fighters
    minionSection = []
    droneLines = []
    for drone in sorted(fit.drones, key=lambda d: d.item.name):
        droneLines.append('{} x{}'.format(drone.item.name, drone.amount))
    if droneLines:
        minionSection.append('\n'.join(droneLines))
    fighterLines = []
    for fighter in sorted(fit.fighters, key=lambda f: f.item.name):
        fighterLines.append('{} x{}'.format(fighter.item.name, fighter.amountActive))
    if fighterLines:
        minionSection.append('\n'.join(fighterLines))
    if minionSection:
        sections.append('\n\n'.join(minionSection))

    # Section 3: implants, boosters
    if options & Options.IMPLANTS.value:
        charSection = []
        implantLines = []
        for implant in fit.implants:
            implantLines.append(implant.item.name)
        if implantLines:
            charSection.append('\n'.join(implantLines))
        boosterLines = []
        for booster in fit.boosters:
            boosterLines.append(booster.item.name)
        if boosterLines:
            charSection.append('\n'.join(boosterLines))
        if charSection:
            sections.append('\n\n'.join(charSection))

    # Section 4: cargo
    cargoLines = []
    for cargo in sorted(
        fit.cargo,
        key=lambda c: (c.item.group.category.name, c.item.group.name, c.item.name)
    ):
        cargoLines.append('{} x{}'.format(cargo.item.name, cargo.amount))
    if cargoLines:
        sections.append('\n'.join(cargoLines))

    # Section 5: mutated modules' details
    mutationLines = []
    if mutants and options & Options.MUTATIONS.value:
        for mutantReference in sorted(mutants):
            mutant = mutants[mutantReference]
            mutatedAttrs = {}
            for attrID, mutator in mutant.mutators.items():
                attrName = getAttributeInfo(attrID).name
                mutatedAttrs[attrName] = mutator.value
            mutationLines.append('[{}] {}'.format(mutantReference, mutant.baseItem.name))
            mutationLines.append('  {}'.format(mutant.mutaplasmid.item.name))
            # Round to 7th significant number to avoid exporting float errors
            customAttrsLine = ', '.join(
                '{} {}'.format(a, roundToPrec(mutatedAttrs[a], 7))
                for a in sorted(mutatedAttrs))
            mutationLines.append('  {}'.format(customAttrsLine))
    if mutationLines:
        sections.append('\n'.join(mutationLines))

    return '{}\n\n{}'.format(header, '\n\n\n'.join(sections))


def importEft(eftString):
    lines = _importPrepareString(eftString)
    try:
        fit = _importCreateFit(lines)
    except EftImportError:
        return

    aFit = AbstractFit()
    aFit.mutations = _importGetMutationData(lines)

    nameChars = '[^,/\[\]]'  # Characters which are allowed to be used in name
    stubPattern = '^\[.+?\]$'
    modulePattern = '^(?P<typeName>{0}+?)(,\s*(?P<chargeName>{0}+?))?(?P<offline>\s*{1})?(\s*\[(?P<mutation>\d+?)\])?$'.format(nameChars, OFFLINE_SUFFIX)
    droneCargoPattern = '^(?P<typeName>{}+?) x(?P<amount>\d+?)$'.format(nameChars)

    sections = []
    for section in _importSectionIter(lines):
        for line in section.lines:
            # Stub line
            if re.match(stubPattern, line):
                section.itemSpecs.append(None)
                continue
            # Items with quantity specifier
            m = re.match(droneCargoPattern, line)
            if m:
                try:
                    itemSpec = MultiItemSpec(m.group('typeName'))
                # Items which cannot be fetched are considered as stubs
                except EftImportError:
                    section.itemSpecs.append(None)
                else:
                    itemSpec.amount = int(m.group('amount'))
                    section.itemSpecs.append(itemSpec)
                continue
            # All other items
            m = re.match(modulePattern, line)
            if m:
                try:
                    itemSpec = RegularItemSpec(m.group('typeName'), chargeName=m.group('chargeName'))
                # Items which cannot be fetched are considered as stubs
                except EftImportError:
                    section.itemSpecs.append(None)
                else:
                    if m.group('offline'):
                        itemSpec.offline = True
                    if m.group('mutation'):
                        itemSpec.mutationIdx = int(m.group('mutation'))
                    section.itemSpecs.append(itemSpec)
                continue
        _clearTail(section.itemSpecs)
        sections.append(section)

    hasDroneBay = any(s.isDroneBay for s in sections)
    hasFighterBay = any(s.isFighterBay for s in sections)
    for section in sections:
        if section.isModuleRack:
            aFit.addModules(section.itemSpecs)
        elif section.isImplantRack:
            for itemSpec in section.itemSpecs:
                aFit.addImplant(itemSpec)
        elif section.isDroneBay:
            for itemSpec in section.itemSpecs:
                aFit.addDrone(itemSpec)
        elif section.isFighterBay:
            for itemSpec in section.itemSpecs:
                aFit.addFighter(itemSpec)
        elif section.isCargoHold:
            for itemSpec in section.itemSpecs:
                aFit.addCargo(itemSpec)
        # Mix between different kinds of item specs (can happen when some
        # blank lines are removed)
        else:
            for itemSpec in section.itemSpecs:
                if itemSpec is None:
                    continue
                if itemSpec.isModule:
                    aFit.addModule(itemSpec)
                elif itemSpec.isImplant:
                    aFit.addImplant(itemSpec)
                elif itemSpec.isDrone and not hasDroneBay:
                    aFit.addDrone(itemSpec)
                elif itemSpec.isFighter and not hasFighterBay:
                    aFit.addFighter(itemSpec)
                elif itemSpec.isCargo:
                    aFit.addCargo(itemSpec)

    # Subsystems first because they modify slot amount
    for m in aFit.subsystems:
        if m is None:
            dummy = Module.buildEmpty(aFit.getSlotByContainer(aFit.subsystems))
            dummy.owner = fit
            fit.modules.appendIgnoreEmpty(dummy)
        elif m.fits(fit):
            m.owner = fit
            fit.modules.appendIgnoreEmpty(m)
    svcFit.getInstance().recalc(fit)

    # Other stuff
    for modRack in (
        aFit.rigs,
        aFit.services,
        aFit.modulesHigh,
        aFit.modulesMed,
        aFit.modulesLow,
    ):
        for m in modRack:
            if m is None:
                dummy = Module.buildEmpty(aFit.getSlotByContainer(modRack))
                dummy.owner = fit
                fit.modules.appendIgnoreEmpty(dummy)
            elif m.fits(fit):
                m.owner = fit
                if not m.isValidState(m.state):
                    pyfalog.warning('service.port.eft.importEft: module {} cannot have state {}', m, m.state)
                fit.modules.appendIgnoreEmpty(m)
    for implant in aFit.implants:
        fit.implants.append(implant)
    for booster in aFit.boosters:
        fit.boosters.append(booster)
    for drone in aFit.drones.values():
        fit.drones.append(drone)
    for fighter in aFit.fighters:
        fit.fighters.append(fighter)
    for cargo in aFit.cargo.values():
        fit.cargo.append(cargo)

    return fit


def importEftCfg(shipname, contents, iportuser):
    """Handle import from EFT config store file"""

    # Check if we have such ship in database, bail if we don't
    sMkt = Market.getInstance()
    try:
        sMkt.getItem(shipname)
    except:
        return []  # empty list is expected

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
                processing_notify(
                    iportuser, IPortUser.PROCESS_IMPORT | IPortUser.ID_UPDATE,
                    "%s:\n%s" % (fitobj.ship.name, fitobj.name)
                )

        # Skip fit silently if we get an exception
        except Exception as e:
            pyfalog.error("Caught exception on fit.")
            pyfalog.error(e)
            pass

    return fits


def _importPrepareString(eftString):
    lines = eftString.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    while lines and not lines[0]:
        del lines[0]
    while lines and not lines[-1]:
        del lines[-1]
    return lines


def _importGetMutationData(lines):
    data = {}
    consumedIndices = set()
    for i in range(len(lines)):
        line = lines[i]
        m = re.match('^\[(?P<ref>\d+)\]', line)
        if m:
            ref = int(m.group('ref'))
            # Attempt to apply mutation is useless w/o mutaplasmid, so skip it
            # altogether if we have no info on it
            try:
                mutaName = lines[i + 1]
            except IndexError:
                continue
            else:
                consumedIndices.add(i)
                consumedIndices.add(i + 1)
            # Get custom attribute values
            mutaAttrs = {}
            try:
                mutaAttrsLine = lines[i + 2]
            except IndexError:
                pass
            else:
                consumedIndices.add(i + 2)
                pairs = [p.strip() for p in mutaAttrsLine.split(',')]
                for pair in pairs:
                    try:
                        attrName, value = pair.split(' ')
                    except ValueError:
                        continue
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        continue
                    attrInfo = getAttributeInfo(attrName.strip())
                    if attrInfo is None:
                        continue
                    mutaAttrs[attrInfo.ID] = value
            mutaItem = _fetchItem(mutaName)
            if mutaItem is None:
                continue
            data[ref] = (mutaItem, mutaAttrs)
            # If we got here, we have seen at least correct reference line and
            # mutaplasmid name line
            i += 2
            # Bonus points for seeing correct attrs line. Worst case we
            # will have to scan it once again
            if mutaAttrs:
                i += 1
    # Cleanup the lines from mutaplasmid info
    for i in sorted(consumedIndices, reverse=True):
        del lines[i]
    return data


def _importSectionIter(lines):
    section = Section()
    for line in lines:
        if not line:
            if section.lines:
                yield section
                section = Section()
        else:
            section.lines.append(line)
    if section.lines:
        yield section


def _importCreateFit(lines):
    """Create fit and set top-level entity (ship or citadel)."""
    fit = Fit()
    header = lines.pop(0)
    m = re.match('\[(?P<shipType>[\w\s]+),\s*(?P<fitName>.+)\]', header)
    if not m:
        pyfalog.warning('service.port.eft.importEft: corrupted fit header')
        raise EftImportError
    shipType = m.group('shipType').strip()
    fitName = m.group('fitName').strip()
    try:
        ship = _fetchItem(shipType)
        try:
            fit.ship = Ship(ship)
        except ValueError:
            fit.ship = Citadel(ship)
        fit.name = fitName
    except:
        pyfalog.warning('service.port.eft.importEft: exception caught when parsing header')
        raise EftImportError
    return fit


def _fetchItem(typeName, eagerCat=False):
    sMkt = Market.getInstance()
    eager = 'group.category' if eagerCat else None
    try:
        item = sMkt.getItem(typeName, eager=eager)
    except:
        pyfalog.warning('service.port.eft: unable to fetch item "{}"'.format(typeName))
        return None
    if sMkt.getPublicityByItem(item):
        return item
    else:
        return None


def _clearTail(lst):
    while lst and lst[-1] is None:
        del lst[-1]


class EftImportError(Exception):
    """Exception class emitted and consumed by EFT importer internally."""
    ...


class Section:

    def __init__(self):
        self.lines = []
        self.itemSpecs = []
        self.__itemDataCats = None

    @property
    def itemDataCats(self):
        if self.__itemDataCats is None:
            cats = set()
            for itemSpec in self.itemSpecs:
                if itemSpec is None:
                    continue
                cats.add(itemSpec.item.category.name)
            self.__itemDataCats = tuple(sorted(cats))
        return self.__itemDataCats

    @property
    def isModuleRack(self):
        return all(i is None or i.isModule for i in self.itemSpecs)

    @property
    def isImplantRack(self):
        return all(i is not None and i.isImplant for i in self.itemSpecs)

    @property
    def isDroneBay(self):
        return all(i is not None and i.isDrone for i in self.itemSpecs)

    @property
    def isFighterBay(self):
        return all(i is not None and i.isFighter for i in self.itemSpecs)

    @property
    def isCargoHold(self):
        return (
            all(i is not None and i.isCargo for i in self.itemSpecs) and
            not self.isDroneBay and not self.isFighterBay)


class BaseItemSpec:

    def __init__(self, typeName):
        item = _fetchItem(typeName, eagerCat=True)
        if item is None:
            raise EftImportError
        self.typeName = typeName
        self.item = item

    @property
    def isModule(self):
        return False

    @property
    def isImplant(self):
        return False

    @property
    def isDrone(self):
        return False

    @property
    def isFighter(self):
        return False

    @property
    def isCargo(self):
        return False


class RegularItemSpec(BaseItemSpec):

    def __init__(self, typeName, chargeName=None):
        super().__init__(typeName)
        self.charge = self.__fetchCharge(chargeName)
        self.offline = False
        self.mutationIdx = None

    def __fetchCharge(self, chargeName):
        if chargeName:
            charge = _fetchItem(chargeName, eagerCat=True)
            if not charge or charge.category.name != 'Charge':
                charge = None
        else:
            charge = None
        return charge

    @property
    def isModule(self):
        return self.item.category.name in MODULE_CATS

    @property
    def isImplant(self):
        return (
            self.item.category.name == 'Implant' and (
                'implantness' in self.item.attributes or
                'boosterness' in self.item.attributes))


class MultiItemSpec(BaseItemSpec):

    def __init__(self, typeName):
        super().__init__(typeName)
        self.amount = 0

    @property
    def isDrone(self):
        return self.item.category.name == 'Drone'

    @property
    def isFighter(self):
        return self.item.category.name == 'Fighter'

    @property
    def isCargo(self):
        return True


class AbstractFit:

    def __init__(self):
        # Modules
        self.modulesHigh = []
        self.modulesMed = []
        self.modulesLow = []
        self.rigs = []
        self.subsystems = []
        self.services = []
        # Non-modules
        self.implants = []
        self.boosters = []
        self.drones = {}  # Format: {item: Drone}
        self.fighters = []
        self.cargo = {}  # Format: {item: Cargo}
        # Other stuff
        self.mutations = {}  # Format: {reference: (mutaplamid item, {attr ID: attr value})}

    @property
    def __slotContainerMap(self):
        return {
            Slot.HIGH: self.modulesHigh,
            Slot.MED: self.modulesMed,
            Slot.LOW: self.modulesLow,
            Slot.RIG: self.rigs,
            Slot.SUBSYSTEM: self.subsystems,
            Slot.SERVICE: self.services}

    def getContainerBySlot(self, slotType):
        return self.__slotContainerMap.get(slotType)

    def getSlotByContainer(self, container):
        slotType = None
        for k, v in self.__slotContainerMap.items():
            if v is container:
                slotType = k
                break
        return slotType

    def addModules(self, itemSpecs):
        modules = []
        slotTypes = set()
        for itemSpec in itemSpecs:
            if itemSpec is None:
                modules.append(None)
                continue
            m = self.__makeModule(itemSpec)
            if m is None:
                modules.append(None)
                continue
            modules.append(m)
            slotTypes.add(m.slot)
        _clearTail(modules)
        # If all the modules have same slot type, put them to appropriate
        # container with stubs
        if len(slotTypes) == 1:
            slotType = tuple(slotTypes)[0]
            self.getContainerBySlot(slotType).extend(modules)
        # Otherwise, put just modules
        else:
            for m in modules:
                if m is None:
                    continue
                self.getContainerBySlot(m.slot).append(m)

    def addModule(self, itemSpec):
        if itemSpec is None:
            return
        m = self.__makeModule(itemSpec)
        if m is not None:
            self.getContainerBySlot(m.slot).append(m)

    def __makeModule(self, itemSpec):
        # Mutate item if needed
        m = None
        if itemSpec.mutationIdx in self.mutations:
            mutaItem, mutaAttrs = self.mutations[itemSpec.mutationIdx]
            mutaplasmid = getDynamicItem(mutaItem.ID)
            if mutaplasmid:
                try:
                    m = Module(mutaplasmid.resultingItem, itemSpec.item, mutaplasmid)
                except ValueError:
                    pass
                else:
                    for attrID, mutator in m.mutators.items():
                        if attrID in mutaAttrs:
                            mutator.value = mutaAttrs[attrID]
        # If we still don't have item (item is not mutated or we
        # failed to construct mutated item), try to make regular item
        if m is None:
            try:
                m = Module(itemSpec.item)
            except ValueError:
                return None

        if itemSpec.charge is not None and m.isValidCharge(itemSpec.charge):
            m.charge = itemSpec.charge
        if itemSpec.offline and m.isValidState(State.OFFLINE):
            m.state = State.OFFLINE
        elif m.isValidState(State.ACTIVE):
            m.state = State.ACTIVE
        return m

    def addImplant(self, itemSpec):
        if itemSpec is None:
            return
        if 'implantness' in itemSpec.item.attributes:
            self.implants.append(Implant(itemSpec.item))
        elif 'boosterness' in itemSpec.item.attributes:
            self.boosters.append(Booster(itemSpec.item))
        else:
            pyfalog.error('Failed to import implant: {}', itemSpec.typeName)

    def addDrone(self, itemSpec):
        if itemSpec is None:
            return
        if itemSpec.item not in self.drones:
            self.drones[itemSpec.item] = Drone(itemSpec.item)
        self.drones[itemSpec.item].amount += itemSpec.amount

    def addFighter(self, itemSpec):
        if itemSpec is None:
            return
        fighter = Fighter(itemSpec.item)
        fighter.amount = itemSpec.amount
        self.fighters.append(fighter)

    def addCargo(self, itemSpec):
        if itemSpec is None:
            return
        if itemSpec.item not in self.cargo:
            self.cargo[itemSpec.item] = Cargo(itemSpec.item)
        self.cargo[itemSpec.item].amount += itemSpec.amount
