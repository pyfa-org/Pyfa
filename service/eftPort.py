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

from eos.db.gamedata.queries import getAttributeInfo
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


pyfalog = Logger(__name__)

MODULE_CATS = ('Module', 'Subsystem', 'Structure Module')
SLOT_ORDER = (Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM, Slot.SERVICE)
OFFLINE_SUFFIX = ' /OFFLINE'


def fetchItem(typeName, eagerCat=True):
    sMkt = Market.getInstance()
    eager = 'group.category' if eagerCat else None
    try:
        item = sMkt.getItem(typeName, eager=eager)
    except:
        pyfalog.warning('EftPort: unable to fetch item "{}"'.format(typeName))
        return None
    if sMkt.getPublicityByItem(item):
        return item
    else:
        return None


def clearTail(lst):
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
        item = fetchItem(typeName, eagerCat=True)
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
            charge = fetchItem(chargeName, eagerCat=True)
            if charge.category.name != 'Charge':
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

    @property
    def modContMap(self):
        return {
            Slot.HIGH: self.modulesHigh,
            Slot.MED: self.modulesMed,
            Slot.LOW: self.modulesLow,
            Slot.RIG: self.rigs,
            Slot.SUBSYSTEM: self.subsystems,
            Slot.SERVICE: self.services}

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
        clearTail(modules)
        modContMap = self.modContMap
        # If all the modules have same slot type, put them to appropriate
        # container with stubs
        if len(slotTypes) == 1:
            slotType = tuple(slotTypes)[0]
            modContMap[slotType].extend(modules)
        # Otherwise, put just modules
        else:
            for m in modules:
                if m is None:
                    continue
                modContMap[m.slot].append(m)

    def addModule(self, itemSpec):
        if itemSpec is None:
            return
        m = self.__makeModule(itemSpec)
        if m is not None:
            self.modContMap[m.slot].append(m)

    def __makeModule(self, itemSpec):
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


class EftPort:

    @classmethod
    def exportEft(cls, fit, mutations, implants):
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
                    if mutated and mutations:
                        mutants[mutantReference] = module
                        mutationSuffix = ' [{}]'.format(mutantReference)
                        mutantReference += 1
                    else:
                        mutationSuffix = ''
                    modOfflineSuffix = OFFLINE_SUFFIX if module.state == State.OFFLINE else ''
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
        if implants:
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
        if mutants and mutations:
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

    @classmethod
    def importEft(cls, eftString):
        lines = cls.__prepareImportString(eftString)
        try:
            fit = cls.__createFit(lines)
        except EftImportError:
            return

        aFit = AbstractFit()

        stubPattern = '^\[.+\]$'
        modulePattern = '^(?P<typeName>[^,/]+)(, (?P<chargeName>[^,/]+))?(?P<offline>{})?( \[(?P<mutation>\d+)\])?$'.format(OFFLINE_SUFFIX)
        droneCargoPattern = '^(?P<typeName>[^,/]+) x(?P<amount>\d+)$'

        sections = []
        for section in cls.__importSectionIter(lines):
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
            clearTail(section.itemSpecs)
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
        for subsystem in aFit.subsystems:
            if subsystem is None:
                continue
            if subsystem.fits(fit):
                subsystem.owner = fit
                fit.modules.append(subsystem)
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
                    continue
                if m.fits(fit):
                    m.owner = fit
                    if not m.isValidState(m.state):
                        pyfalog.warning('EftPort.importEft: module {} cannot have state {}', m, m.state)
                    fit.modules.append(m)
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

    @staticmethod
    def __prepareImportString(eftString):
        lines = eftString.splitlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        while lines and not lines[0]:
            del lines[0]
        while lines and not lines[-1]:
            del lines[-1]
        return lines

    @classmethod
    def __createFit(cls, lines):
        """Create fit and set top-level entity (ship or citadel)."""
        fit = Fit()
        header = lines.pop(0)
        m = re.match('\[(?P<shipType>[\w\s]+), (?P<fitName>.+)\]', header)
        if not m:
            pyfalog.warning('EftPort.importEft: corrupted fit header')
            raise EftImportError
        shipType = m.group('shipType').strip()
        fitName = m.group('fitName').strip()
        try:
            ship = fetchItem(shipType, eagerCat=False)
            try:
                fit.ship = Ship(ship)
            except ValueError:
                fit.ship = Citadel(ship)
            fit.name = fitName
        except:
            pyfalog.warning('EftPort.importEft: exception caught when parsing header')
            raise EftImportError
        return fit

    @staticmethod
    def __importSectionIter(lines):
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
