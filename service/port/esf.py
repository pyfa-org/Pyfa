# =============================================================================
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


import esf_format
from esf_format import AttributeRecord, Entry, EsfFit, Kind, Location, MutaplasmidRecord, State, TypeRecord, sde
from logbook import Logger
from sqlalchemy import text

from eos.const import FittingModuleState, FittingSlot
from eos.db import get_gamedata_session
from eos.db.gamedata.queries import getItem, getMutaplasmid
from eos.gamedata import DynamicItemItem
from eos.saveddata.booster import Booster
from eos.saveddata.cargo import Cargo
from eos.saveddata.citadel import Citadel
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit
from eos.saveddata.implant import Implant
from eos.saveddata.module import Module
from eos.saveddata.ship import Ship
from service.fit import Fit as svcFit


pyfalog = Logger(__name__)

RACKS = {
    Location.HIGH: FittingSlot.HIGH,
    Location.MID: FittingSlot.MED,
    Location.LOW: FittingSlot.LOW,
    Location.RIG: FittingSlot.RIG,
    Location.SUB: FittingSlot.SUBSYSTEM,
    Location.SVC: FittingSlot.SERVICE,
}
SLOT_LOCATIONS = {slot: location for location, slot in RACKS.items()}
MAX_COUNT = 2 ** 32 - 1
MODULE_KINDS = (Kind.HIGH, Kind.MID, Kind.LOW, Kind.RIG, Kind.SUB, Kind.SVC)
SLOT_ORDER = (
    FittingSlot.SUBSYSTEM, FittingSlot.HIGH, FittingSlot.MED, FittingSlot.LOW, FittingSlot.RIG, FittingSlot.SERVICE)


class PyfaCatalog:
    """esf/1 catalog on top of pyfa's game data."""

    def __init__(self):
        session = get_gamedata_session()
        types = session.execute(text("SELECT typeID, typeName, published FROM invtypes")).all()
        attributes = session.execute(text("SELECT attributeID, attributeName, published FROM dgmattribs")).all()
        self._typeNames = sde.name_index(types, lambda r: r[0], lambda r: r[1], lambda r: bool(r[2]))
        self._attributeNames = sde.name_index(attributes, lambda r: r[0], lambda r: r[1], lambda r: bool(r[2]))
        self._attributes = {r[0]: AttributeRecord(id=r[0], name=r[1]) for r in attributes}
        self._types = {}

    def type(self, folded_name):
        typeID = self._typeNames.get(folded_name)
        return None if typeID is None else self.type_by_id(typeID)

    def type_by_id(self, type_id):
        if type_id not in self._types:
            self._types[type_id] = self._makeType(getItem(type_id, eager="group.category"))
        return self._types[type_id]

    def attribute(self, folded_name):
        attributeID = self._attributeNames.get(folded_name)
        return None if attributeID is None else self._attributes[attributeID]

    def attribute_by_id(self, attribute_id):
        return self._attributes.get(attribute_id)

    def modes(self, hull_id):
        try:
            ship = Ship(getItem(hull_id))
        except ValueError:
            return []
        return [self.type_by_id(item.ID) for item in ship.modeItems or ()]

    def mutaplasmids(self, type_id):
        baseItem = getItem(type_id)
        links = get_gamedata_session().query(DynamicItemItem).filter(DynamicItemItem.applicableTypeID == type_id).all()
        records = []
        for link in links:
            mutaplasmid = link.mutaplasmid
            rolls = []
            for attr in mutaplasmid.attributes:
                base = baseItem.attributes.get(attr.name)
                value = base.value if base is not None else (attr.info.defaultValue or 0.0)
                rolls.append((attr.ID, value))
            records.append(MutaplasmidRecord(type=self.type_by_id(mutaplasmid.ID), rolls=tuple(rolls)))
        return records

    @staticmethod
    def _makeType(item):
        if item is None:
            return None
        squadronSize = item.getAttribute("fighterSquadronMaxSize")
        return TypeRecord(
            id=item.ID,
            name=item.typeName,
            kind=sde.kind(item.group.categoryID, item.groupID, [e.ID for e in item.effects.values()]),
            active=item.isType("active"),
            capacity=item.getAttribute("capacity", 0.0),
            volume=item.getAttribute("volume", 0.0),
            squadron_size=None if squadronSize is None else int(squadronSize),
        )


_catalog = None


def getCatalog():
    global _catalog
    if _catalog is None:
        _catalog = PyfaCatalog()
    return _catalog


def importEsf(string):
    catalog = getCatalog()
    esfFits = esf_format.load(string, catalog)
    containers = {
        (f.hull, esf_format.fold(f.name)): f for f in esfFits
        if f.hull is not None and f.name is not None and catalog.type_by_id(f.hull).kind == Kind.CONTAINER}
    fits = []
    for esfFit in esfFits:
        fit = _importFit(esfFit, catalog, containers)
        if fit is not None:
            fits.append(fit)
    return fits


def _importFit(esfFit, catalog, containers):
    if esfFit.hull is None:
        pyfalog.warning("service.port.esf.importEsf: skipping fit {!r} without a ship", esfFit.name)
        return None
    hullItem = getItem(esfFit.hull)
    if catalog.type_by_id(esfFit.hull).kind == Kind.CONTAINER:
        return None
    fit = Fit()
    try:
        fit.ship = Ship(hullItem)
    except ValueError:
        try:
            fit.ship = Citadel(hullItem)
        except ValueError:
            pyfalog.warning("service.port.esf.importEsf: {} cannot be the ship of a fit", hullItem.typeName)
            return None
    fit.name = esfFit.name or hullItem.typeName
    if esfFit.mode is not None:
        fit.mode = fit.ship.validateModeItem(getItem(esfFit.mode), owner=fit)

    racks = {slot: [] for slot in SLOT_ORDER}
    drones = {}
    cargo = {}
    for entry in esfFit.entries:
        if entry.type is None:
            if entry.location in RACKS:
                racks[RACKS[entry.location]].append(None)
            continue
        record = catalog.type_by_id(entry.type)
        count = 1 if entry.count is None else entry.count
        stored = entry.location is not None and entry.location not in RACKS and entry.location != Location.TUBE
        if record.kind in MODULE_KINDS and not stored:
            for _ in range(count):
                module = _makeModule(entry, record)
                if module is not None:
                    racks[module.slot].append(module)
        elif record.kind == Kind.DRONE and entry.location in (None, Location.BAY):
            _addDrone(fit, drones, entry, count)
        elif record.kind == Kind.FIGHTER and entry.location in (None, Location.BAY, Location.TUBE):
            fighter = Fighter(getItem(entry.type))
            if entry.count is not None:
                fighter.amount = entry.count
            fighter.active = entry.location != Location.BAY
            fit.fighters.append(fighter)
        elif record.kind == Kind.IMPLANT and not stored:
            implant = Implant(getItem(entry.type))
            implant.active = entry.state != State.OFF
            fit.implants.append(implant)
        elif record.kind == Kind.BOOSTER and not stored:
            booster = Booster(getItem(entry.type))
            booster.active = entry.state != State.OFF
            fit.boosters.append(booster)
        else:
            _addCargo(fit, cargo, containers, entry, count)

    _fitRack(fit, racks[FittingSlot.SUBSYSTEM], FittingSlot.SUBSYSTEM)
    sFit = svcFit.getInstance()
    sFit.recalc(fit)
    sFit.fill(fit)
    for slot in SLOT_ORDER[1:]:
        _fitRack(fit, racks[slot], slot)
    return fit


def _addCargo(fit, cargo, containers, entry, count):
    if entry.type not in cargo:
        cargo[entry.type] = Cargo(getItem(entry.type))
        fit.cargo.append(cargo[entry.type])
    cargo[entry.type].amount += count
    if entry.fit_name is not None:
        container = containers.get((entry.type, esf_format.fold(entry.fit_name)))
        for content in container.entries if container is not None else ():
            _addCargo(fit, cargo, containers, content, 1 if content.count is None else content.count)


def _makeModule(entry, record):
    module = None
    if entry.mutaplasmid is not None:
        mutaplasmid = getMutaplasmid(entry.mutaplasmid)
        if mutaplasmid is not None:
            try:
                module = Module(mutaplasmid.resultingItem, getItem(entry.type), mutaplasmid)
            except ValueError:
                pass
            else:
                _applyMutations(module, entry)
    if module is None:
        try:
            module = Module(getItem(entry.type))
        except ValueError:
            pyfalog.warning("service.port.esf.importEsf: {} is not a module", record.name)
            return None
    if entry.charge is not None:
        charge = getItem(entry.charge)
        if module.isValidCharge(charge):
            module.charge = charge
    if entry.state == State.OFF:
        state = FittingModuleState.OFFLINE
    elif entry.state == State.ON:
        state = FittingModuleState.ONLINE
    elif entry.state == State.HEAT:
        state = FittingModuleState.OVERHEATED
    elif record.active:
        state = FittingModuleState.ACTIVE
    else:
        state = FittingModuleState.ONLINE
    module.state = module.getMaxState(state)
    return module


def _addDrone(fit, drones, entry, count):
    deployed = 0 if entry.location == Location.BAY else count
    if entry.mutaplasmid is None and entry.type in drones:
        drone = drones[entry.type]
        drone.amount += count
        drone.amountActive += deployed
        return
    drone = None
    if entry.mutaplasmid is not None:
        mutaplasmid = getMutaplasmid(entry.mutaplasmid)
        if mutaplasmid is not None:
            try:
                drone = Drone(mutaplasmid.resultingItem, getItem(entry.type), mutaplasmid)
            except ValueError:
                pass
            else:
                _applyMutations(drone, entry)
    if drone is None:
        drone = Drone(getItem(entry.type))
        drones[entry.type] = drone
    drone.amount = count
    drone.amountActive = deployed
    fit.drones.append(drone)


def _applyMutations(item, entry):
    for attrID, mutator in item.mutators.items():
        if attrID in entry.overrides:
            mutator.value = entry.overrides[attrID]


def _fitRack(fit, modules, slot):
    while modules and modules[-1] is None:
        modules.pop()
    for i, module in enumerate(modules):
        if module is None:
            module = Module.buildEmpty(slot)
        elif not module.fits(fit):
            continue
        module.owner = fit
        fit.modules.replaceRackPosition(i, module)


def exportEsf(fit, callback=None):
    catalog = getCatalog()
    esfFit = EsfFit(
        hull=fit.ship.item.ID,
        name=" ".join(fit.name.splitlines()) or None,
        mode=fit.mode.item.ID if fit.mode is not None else None,
    )
    entries = esfFit.entries

    for slot in SLOT_ORDER:
        rack = [m for m in fit.modules if m.slot == slot]
        while rack and rack[-1].isEmpty:
            rack.pop()
        for module in rack:
            if module.isEmpty:
                entries.append(Entry(None, location=SLOT_LOCATIONS[slot]))
                continue
            entry = _mutatedEntry(module)
            if module.charge is not None:
                entry.charge = module.charge.ID
            entry.state = _exportState(module, catalog.type_by_id(entry.type))
            entries.append(entry)

    for drone in fit.drones:
        stored = drone.amount - drone.amountActive
        if drone.amountActive > 0:
            entry = _mutatedEntry(drone)
            entry.count = _count(drone.amountActive)
            entries.append(entry)
        if stored > 0:
            entry = _mutatedEntry(drone)
            entry.count = _count(stored)
            entry.location = Location.BAY
            entries.append(entry)

    for fighter in fit.fighters:
        entries.append(Entry(
            fighter.item.ID,
            count=None if fighter.amount >= fighter.fighterSquadronMaxSize else fighter.amount,
            location=None if fighter.active else Location.BAY,
        ))

    for implant in fit.implants:
        entries.append(Entry(implant.item.ID, state=None if implant.active else State.OFF))
    for booster in fit.boosters:
        entries.append(Entry(booster.item.ID, state=None if booster.active else State.OFF))
    for cargo in fit.cargo:
        if cargo.amount >= 1:
            entries.append(Entry(cargo.item.ID, count=_count(min(cargo.amount, MAX_COUNT)), location=Location.CARGO))

    esfText = esf_format.save([esfFit], catalog)
    if callback:
        callback(esfText)
    else:
        return esfText


def _mutatedEntry(item):
    if not item.isMutated:
        return Entry(item.item.ID)
    return Entry(
        item.baseItem.ID,
        mutaplasmid=item.mutaplasmid.ID,
        overrides={attrID: mutator.value for attrID, mutator in item.mutators.items()},
    )


def _exportState(module, record):
    if module.state == FittingModuleState.OFFLINE:
        return State.OFF
    if module.state == FittingModuleState.OVERHEATED:
        return State.HEAT
    if module.state == FittingModuleState.ONLINE and record.active:
        return State.ON
    return None


def _count(amount):
    return None if amount == 1 else amount
