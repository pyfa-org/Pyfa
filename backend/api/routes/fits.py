"""
Fit CRUD routes — /fits  and  /fits/{fit_id}/...

All EOS calls are wrapped in run_in_executor so they don't block uvicorn's
event loop.  EOS is synchronous/blocking by design; this is the correct
adapter pattern (see Section 15 of spec).
"""

import asyncio
from typing import Optional

import eos.db
from fastapi import APIRouter, HTTPException

from backend.api.models.fit import (
    BoosterAdd,
    BoosterOut,
    DroneActiveUpdate,
    DroneAdd,
    DroneOut,
    EftImport,
    EsiImport,
    FitCreate,
    FitFull,
    FitLite,
    FitUpdate,
    ImplantAdd,
    ImplantOut,
    ModuleAdd,
    ModuleCharge,
    ModuleOut,
    ModuleState,
)

router = APIRouter()

_ICON_BASE = "https://images.evetech.net/types/{typeID}/icon?size=64"


def _exe(fn, *args, **kwargs):
    """Run a blocking EOS call in the default thread executor."""
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, lambda: fn(*args, **kwargs))


def _module_state_str(state) -> str:
    from eos.const import FittingModuleState
    return {
        FittingModuleState.OFFLINE: "offline",
        FittingModuleState.ONLINE: "online",
        FittingModuleState.ACTIVE: "active",
        FittingModuleState.OVERLOAD: "overload",
    }.get(state, "online")


def _module_to_out(module, slot: str, position: int) -> ModuleOut:
    charge_id = None
    charge_name = None
    if module.charge:
        charge_id = module.charge.item.typeID
        charge_name = module.charge.item.name
    return ModuleOut(
        typeID=module.item.typeID,
        typeName=module.item.name,
        slot=slot,
        position=position,
        state=_module_state_str(module.state),
        chargeTypeID=charge_id,
        chargeTypeName=charge_name,
        iconURL=_ICON_BASE.format(typeID=module.item.typeID),
    )


def _fit_to_lite(fit) -> FitLite:
    return FitLite(
        fitID=fit.ID,
        name=fit.name,
        shipTypeID=fit.ship.item.typeID,
        shipName=fit.ship.item.name,
        shipClass=fit.ship.item.group.name if fit.ship.item.group else None,
        characterName=fit.character.name if fit.character else None,
        notes=fit.notes,
        iconURL=_ICON_BASE.format(typeID=fit.ship.item.typeID),
    )


def _fit_to_full(fit) -> FitFull:
    from eos.const import FittingSlot

    def slot_modules(slot_type, slot_label):
        count = fit.getSlotsFree(slot_type, True) + fit.getSlotsFree(slot_type, False)
        slots = [None] * count
        for mod in fit.modules:
            if mod.slot == slot_type:
                idx = fit.modules.index(mod)
                if idx < count:
                    slots[idx] = _module_to_out(mod, slot_label, idx)
        return slots

    drones = [
        DroneOut(
            typeID=d.item.typeID,
            typeName=d.item.name,
            count=d.amount,
            activeCount=d.amountActive,
            iconURL=_ICON_BASE.format(typeID=d.item.typeID),
        )
        for d in fit.drones
    ]

    implants = [
        ImplantOut(
            typeID=i.item.typeID,
            typeName=i.item.name,
            slot=i.slot,
            iconURL=_ICON_BASE.format(typeID=i.item.typeID),
        )
        for i in fit.implants
    ]

    boosters = [
        BoosterOut(
            typeID=b.item.typeID,
            typeName=b.item.name,
            slot=b.slot,
            iconURL=_ICON_BASE.format(typeID=b.item.typeID),
        )
        for b in fit.boosters
    ]

    lite = _fit_to_lite(fit)
    return FitFull(
        **lite.model_dump(),
        highSlots=slot_modules(FittingSlot.HIGH, "high"),
        midSlots=slot_modules(FittingSlot.MED, "mid"),
        lowSlots=slot_modules(FittingSlot.LOW, "low"),
        rigSlots=slot_modules(FittingSlot.RIG, "rig"),
        subsystemSlots=slot_modules(FittingSlot.SUBSYSTEM, "subsystem"),
        drones=drones,
        implants=implants,
        boosters=boosters,
    )


def _get_fit_or_404(fit_id: int):
    fit = eos.db.getFit(fit_id)
    if fit is None:
        raise HTTPException(status_code=404, detail=f"Fit {fit_id} not found")
    return fit


# ---------------------------------------------------------------------------
# Fit CRUD
# ---------------------------------------------------------------------------

@router.get("", response_model=list[FitLite])
async def list_fits():
    def _get():
        return [_fit_to_lite(f) for f in eos.db.getFitList()]
    return await _exe(_get)


@router.post("", response_model=FitLite, status_code=201)
async def create_fit(body: FitCreate):
    def _create():
        from service.fit import Fit as sFit
        ship = eos.db.getItem(body.shipTypeID)
        if ship is None:
            raise HTTPException(status_code=404, detail=f"Ship typeID {body.shipTypeID} not found")
        fit_id = sFit.getInstance().newFit(body.shipTypeID, body.name)
        return _fit_to_lite(eos.db.getFit(fit_id))
    return await _exe(_create)


@router.get("/{fit_id}", response_model=FitFull)
async def get_fit(fit_id: int):
    def _get():
        return _fit_to_full(_get_fit_or_404(fit_id))
    return await _exe(_get)


@router.put("/{fit_id}", response_model=FitLite)
async def update_fit(fit_id: int, body: FitUpdate):
    def _update():
        fit = _get_fit_or_404(fit_id)
        if body.name is not None:
            fit.name = body.name
        if body.notes is not None:
            fit.notes = body.notes
        eos.db.commit()
        return _fit_to_lite(fit)
    return await _exe(_update)


@router.delete("/{fit_id}", status_code=204)
async def delete_fit(fit_id: int):
    def _delete():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().deleteFit(fit_id)
    await _exe(_delete)


@router.post("/{fit_id}/duplicate", response_model=FitLite, status_code=201)
async def duplicate_fit(fit_id: int):
    def _dup():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        new_id = sFit.getInstance().copyFit(fit_id)
        return _fit_to_lite(eos.db.getFit(new_id))
    return await _exe(_dup)


# ---------------------------------------------------------------------------
# Modules
# ---------------------------------------------------------------------------

@router.post("/{fit_id}/modules", response_model=FitFull, status_code=201)
async def add_module(fit_id: int, body: ModuleAdd):
    def _add():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().addModule(fit_id, body.typeID)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_add)


@router.delete("/{fit_id}/modules/{position}", response_model=FitFull)
async def remove_module(fit_id: int, position: int):
    def _remove():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().removeModule(fit_id, position)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_remove)


@router.put("/{fit_id}/modules/{position}/state", response_model=FitFull)
async def set_module_state(fit_id: int, position: int, body: ModuleState):
    def _set():
        from service.fit import Fit as sFit
        from eos.const import FittingModuleState
        state_map = {
            "offline": FittingModuleState.OFFLINE,
            "online": FittingModuleState.ONLINE,
            "active": FittingModuleState.ACTIVE,
            "overload": FittingModuleState.OVERLOAD,
        }
        state = state_map.get(body.state)
        if state is None:
            raise HTTPException(status_code=422, detail=f"Unknown state '{body.state}'")
        _get_fit_or_404(fit_id)
        sFit.getInstance().changeModuleStates(fit_id, [position], state)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_set)


@router.put("/{fit_id}/modules/{position}/charge", response_model=FitFull)
async def set_module_charge(fit_id: int, position: int, body: ModuleCharge):
    def _set():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().setCharge(fit_id, position, body.typeID)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_set)


# ---------------------------------------------------------------------------
# Drones
# ---------------------------------------------------------------------------

@router.post("/{fit_id}/drones", response_model=FitFull, status_code=201)
async def add_drone(fit_id: int, body: DroneAdd):
    def _add():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().addDrone(fit_id, body.typeID, body.count)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_add)


@router.delete("/{fit_id}/drones/{type_id}", response_model=FitFull)
async def remove_drone(fit_id: int, type_id: int):
    def _remove():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().removeDrone(fit_id, type_id)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_remove)


@router.put("/{fit_id}/drones/{type_id}/active", response_model=FitFull)
async def set_drone_active(fit_id: int, type_id: int, body: DroneActiveUpdate):
    def _set():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().setDroneActive(fit_id, type_id, body.count)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_set)


# ---------------------------------------------------------------------------
# Implants & Boosters
# ---------------------------------------------------------------------------

@router.post("/{fit_id}/implants", response_model=FitFull, status_code=201)
async def add_implant(fit_id: int, body: ImplantAdd):
    def _add():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().addImplant(fit_id, body.typeID)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_add)


@router.delete("/{fit_id}/implants/{type_id}", response_model=FitFull)
async def remove_implant(fit_id: int, type_id: int):
    def _remove():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().removeImplant(fit_id, type_id)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_remove)


@router.post("/{fit_id}/boosters", response_model=FitFull, status_code=201)
async def add_booster(fit_id: int, body: BoosterAdd):
    def _add():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().addBooster(fit_id, body.typeID)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_add)


@router.delete("/{fit_id}/boosters/{type_id}", response_model=FitFull)
async def remove_booster(fit_id: int, type_id: int):
    def _remove():
        from service.fit import Fit as sFit
        _get_fit_or_404(fit_id)
        sFit.getInstance().removeBooster(fit_id, type_id)
        return _fit_to_full(eos.db.getFit(fit_id))
    return await _exe(_remove)


# ---------------------------------------------------------------------------
# Import / Export
# ---------------------------------------------------------------------------

@router.get("/{fit_id}/export/eft")
async def export_eft(fit_id: int):
    def _export():
        from service.port.port import Port
        _get_fit_or_404(fit_id)
        return Port.exportEft(eos.db.getFit(fit_id))
    eft_string = await _exe(_export)
    return {"eftString": eft_string}


@router.get("/{fit_id}/export/dna")
async def export_dna(fit_id: int):
    def _export():
        from service.port.port import Port
        _get_fit_or_404(fit_id)
        return Port.exportDna(eos.db.getFit(fit_id))
    dna_string = await _exe(_export)
    return {"dnaString": dna_string}


@router.post("/import/eft", response_model=list[FitLite], status_code=201)
async def import_eft(body: EftImport):
    def _import():
        from service.port.port import Port
        fits, _ = Port.importEft(body.eftString)
        for fit in fits:
            eos.db.save(fit)
        eos.db.commit()
        return [_fit_to_lite(f) for f in fits]
    return await _exe(_import)


@router.post("/import/esi", response_model=FitLite, status_code=201)
async def import_esi(body: EsiImport):
    def _import():
        from service.port.esi import ESIExport
        fit = ESIExport.importFit(body.esiFit)
        eos.db.save(fit)
        eos.db.commit()
        return _fit_to_lite(fit)
    return await _exe(_import)
