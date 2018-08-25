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
from eos.saveddata.citadel import Citadel
from eos.saveddata.module import Module, Slot, State
from eos.saveddata.ship import Ship
from gui.utils.numberFormatter import roundToPrec
from service.fit import Fit as svcFit
from service.market import Market


pyfalog = Logger(__name__)


def fetchItem(typeName, eagerCat=True):
    sMkt = Market.getInstance()
    eager = 'group.category' if eagerCat else None
    try:
        return sMkt.getItem(typeName, eager=eager)
    except:
        pyfalog.warning('EftPort: unable to fetch item "{}"'.format(typeName))
        return


class EftImportError(Exception):
    """Exception class emitted and consumed by EFT importer/exporter internally."""
    ...


class AmountMap(dict):

    def add(self, entity, amount):
        if entity not in self:
            self[entity] = 0
        self[entity] += amount


class AbstractFit:

    def __init__(self):
        self.modulesHigh = []
        self.modulesMed = []
        self.modulesLow = []
        self.rigs = []
        self.subsystems = []
        self.services = []
        self.drones = AmountMap()
        self.fighters = AmountMap()
        self.implants = set()
        self.boosters = set()
        self.cargo = AmountMap()

    # def addModule(self, m):
    #     modContMap = {
    #         Slot.HIGH: self.modulesHigh,
    #         Slot.MED: self.modulesMed,
    #         Slot.LOW: self.modulesLow,
    #         Slot.RIG: self.rigs,
    #         Slot.SUBSYSTEM: self.subsystems,
    #         Slot.SERVICE: self.services}


class Section:

    def __init__(self):
        self.lines = []
        self.itemData = []
        self.__itemDataCats = None

    @property
    def itemDataCats(self):
        if self.__itemDataCats is None:
            cats = set()
            for itemSpec in self.itemData:
                if itemSpec is None:
                    continue
                cats.add(itemSpec.item.category.name)
            self.__itemDataCats = tuple(sorted(cats))
        return self.__itemDataCats

    def cleanItemDataTail(self):
        while self.itemData and self.itemData[-1] is None:
            del self.itemData[-1]


class BaseItemSpec:

    def __init__(self, typeName):
        item = fetchItem(typeName, eagerCat=True)
        if item is None:
            raise EftImportError
        self.typeName = typeName
        self.item = item


class ItemSpec(BaseItemSpec):

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


class MultiItemSpec(BaseItemSpec):

    def __init__(self, typeName):
        super().__init__(typeName)
        self.amount = 0


class EftPort:

    SLOT_ORDER = [Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM, Slot.SERVICE]
    OFFLINE_SUFFIX = ' /OFFLINE'

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
        for slotType in cls.SLOT_ORDER:
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
                    modOfflineSuffix = cls.OFFLINE_SUFFIX if module.state == State.OFFLINE else ''
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
        modulePattern = '^(?P<typeName>[^,/]+)(, (?P<chargeName>[^,/]+))?(?P<offline>{})?( \[(?P<mutation>\d+)\])?$'.format(cls.OFFLINE_SUFFIX)
        droneCargoPattern = '^(?P<typeName>[^,/]+) x(?P<amount>\d+)$'

        dronebaySeen = False
        fightersSeen = False
        for section in cls.__importSectionIter(lines):
            for line in section.lines:
                # Stub line
                if re.match(stubPattern, line):
                    section.itemData.append(None)
                    continue
                # Items with quantity specifier
                m = re.match(droneCargoPattern, line)
                if m:
                    try:
                        itemSpec = MultiItemSpec(m.group('typeName'))
                    # Items which cannot be fetched are considered as stubs
                    except EftImportError:
                        section.itemData.append(None)
                    else:
                        itemSpec.amount = int(m.group('amount'))
                        section.itemData.append(itemSpec)
                # All other items
                m = re.match(modulePattern, line)
                if m:
                    try:
                        itemSpec = ItemSpec(m.group('typeName'), chargeName=m.group('chargeName'))
                    # Items which cannot be fetched are considered as stubs
                    except EftImportError:
                        section.itemData.append(None)
                    else:
                        if m.group('offline'):
                            itemSpec.offline = True
                        if m.group('mutation'):
                            itemSpec.mutationIdx = int(m.group('mutation'))
                        section.itemData.append(itemSpec)
            section.cleanItemDataTail()
            # Finally, start putting items into intermediate containers
            # All items in section have quantity specifier
            if all(isinstance(id, MultiItemSpec) for id in section.itemData):
                # Dronebay
                if len(section.itemDataCats) == 1 and section.itemDataCats[0] == 'Drone' and not dronebaySeen:
                    for entry in section.itemData:
                        aFit.drones.add(entry['typeName'], entry['amount'])
                    dronebaySeen = True
                # Fighters
                elif len(section.itemDataCats) == 1 and section.itemDataCats[0] == 'Fighter' and not fightersSeen:
                    for entry in section.itemData:
                        aFit.fighters.add(entry['typeName'], entry['amount'])
                    fightersSeen = True
                # Cargo
                else:
                    for entry in section.itemData:
                        aFit.cargo.add(entry['typeName'], entry['amount'])
            # All of items are normal or stubs
            elif all(isinstance(id, ItemSpec) or id is None for id in section.itemData):
                if len(section.itemDataCats) == 1:
                    if section.itemDataCats[0] in ('Module', 'Subsystem', 'Structure Module'):
                        slotTypes = set()
                        for entry in itemData:
                            if entry['type'] == 'stub':
                                continue
                            try:
                                m = Module(entry['item'])
                            except ValueError:
                                m = None
                            else:
                                slotTypes.add(m.slot)
                            entry['module'] = m
                        # If whole section uses container of the same type,
                        if len(slotTypes) == 1:
                            pass
                        else:
                            pass

                    else:
                        pass
                else:
                    pass

            # Mix between all types
            else:
                pass



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

            if not item.published:
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
