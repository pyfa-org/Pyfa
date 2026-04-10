"""Pydantic response models for fit stats (Section 6 of spec)."""

from typing import Optional
from pydantic import BaseModel


class ResistProfile(BaseModel):
    hp: float
    em: float
    therm: float
    kin: float
    exp: float


class EhpBreakdown(BaseModel):
    uniform: float
    em: float
    therm: float
    kin: float
    exp: float


class TankStats(BaseModel):
    shield: ResistProfile
    armor: ResistProfile
    hull: ResistProfile
    ehp: EhpBreakdown
    effectivehp: float


class DpsStats(BaseModel):
    turret: float
    missile: float
    drone: float
    total: float
    volley: float


class CapStats(BaseModel):
    stable: bool
    stableAt: Optional[float]
    timeToEmpty: Optional[float]
    capacity: float
    rechargeRate: float


class NavigationStats(BaseModel):
    maxVelocity: float
    agility: float
    alignTime: float
    warpSpeed: float
    signatureRadius: float


class SensorStrength(BaseModel):
    type: str
    value: float


class TargetingStats(BaseModel):
    maxTargetRange: float
    scanResolution: float
    maxLockedTargets: int
    sensorStrength: SensorStrength


class ResourceUsage(BaseModel):
    used: float
    total: float


class FittingResources(BaseModel):
    cpu: ResourceUsage
    powergrid: ResourceUsage
    calibration: ResourceUsage
    droneBandwidth: ResourceUsage
    droneBay: ResourceUsage


class PriceStats(BaseModel):
    hull: float
    fit: float
    total: float


class ValidationResult(BaseModel):
    valid: bool
    issues: list[str]


class FullStats(BaseModel):
    fitID: int
    shipName: str
    shipTypeID: int
    validation: ValidationResult
    tank: TankStats
    dps: DpsStats
    capacitor: CapStats
    navigation: NavigationStats
    targeting: TargetingStats
    fitting: FittingResources
    price: PriceStats
