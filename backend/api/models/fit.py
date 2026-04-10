"""Pydantic request/response models for fits and their sub-resources."""

from typing import Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Module
# ---------------------------------------------------------------------------

class ModuleState(BaseModel):
    state: str  # offline | online | active | overload


class ModuleCharge(BaseModel):
    typeID: int


class ModuleAdd(BaseModel):
    typeID: int
    slot: str        # high | mid | low | rig | subsystem
    position: int


class ModuleOut(BaseModel):
    typeID: int
    typeName: str
    slot: str
    position: int
    state: str
    chargeTypeID: Optional[int] = None
    chargeTypeName: Optional[str] = None
    iconURL: Optional[str] = None


# ---------------------------------------------------------------------------
# Drones
# ---------------------------------------------------------------------------

class DroneAdd(BaseModel):
    typeID: int
    count: int = 1


class DroneActiveUpdate(BaseModel):
    count: int


class DroneOut(BaseModel):
    typeID: int
    typeName: str
    count: int
    activeCount: int
    iconURL: Optional[str] = None


# ---------------------------------------------------------------------------
# Implants / Boosters
# ---------------------------------------------------------------------------

class ImplantAdd(BaseModel):
    typeID: int


class ImplantOut(BaseModel):
    typeID: int
    typeName: str
    slot: int
    iconURL: Optional[str] = None


class BoosterAdd(BaseModel):
    typeID: int


class BoosterOut(BaseModel):
    typeID: int
    typeName: str
    slot: int
    iconURL: Optional[str] = None


# ---------------------------------------------------------------------------
# Fit (lite — for list views)
# ---------------------------------------------------------------------------

class FitCreate(BaseModel):
    shipTypeID: int
    name: str


class FitUpdate(BaseModel):
    name: Optional[str] = None
    notes: Optional[str] = None


class FitLite(BaseModel):
    fitID: int
    name: str
    shipTypeID: int
    shipName: str
    shipClass: Optional[str] = None
    characterName: Optional[str] = None
    notes: Optional[str] = None
    iconURL: Optional[str] = None


# ---------------------------------------------------------------------------
# Fit (full — for the editor screen)
# ---------------------------------------------------------------------------

class FitFull(FitLite):
    highSlots: list[Optional[ModuleOut]]
    midSlots: list[Optional[ModuleOut]]
    lowSlots: list[Optional[ModuleOut]]
    rigSlots: list[Optional[ModuleOut]]
    subsystemSlots: list[Optional[ModuleOut]]
    drones: list[DroneOut]
    implants: list[ImplantOut]
    boosters: list[BoosterOut]


# ---------------------------------------------------------------------------
# Import / Export
# ---------------------------------------------------------------------------

class EftImport(BaseModel):
    eftString: str


class EsiImport(BaseModel):
    esiFit: dict
